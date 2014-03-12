#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import hmac
import hashlib
import base64
import collections
import sys
import time
from abc import ABCMeta, abstractmethod

import six
from six.moves.urllib import parse
from six.moves import range
import requests

LOG = logging.getLogger(__name__)


class AttributeInvokeMixin(object):

    def __getattr__(self, name):
        def handle(*args, **kwargs):
            return self.invoke(name, kwargs)
        return handle


class ApiResponse(collections.namedtuple('ApiResponse',
                                         [
                                             'status_code',
                                             'headers',
                                             'content_body'
                                         ]
                                         )):
    pass


class ApiRequest(collections.namedtuple('ApiRequest',
                                        [
                                            'method',
                                            'params',
                                            'headers',
                                            'data',
                                        ]
                                        )):
    pass


class RequestMixin(object):

    def __init__(self):
        self.session = requests.Session()

    def request(self, method=None, params=None, headers=None, data=None):
        params = params or {}
        headers = headers or {}
        data = data or {}
        return self.session.request(
            method or 'GET',
            self.entry_point,
            params=params,
            headers=headers,
            data=data,
        )


class RetryLimitExceededException(BaseException):

    def __init__(self, msg):
        super(RetryLimitExceededException, self).__init__(msg)


class AsyncBlockMixin(object):

    def __init__(self):
        super(AsyncBlockMixin, self).__init__()

    def block(self, response, retry=-1, interval=1):
        inner_body = next(iter(response.values()))
        job_id = inner_body.get('jobid')
        if not job_id:
            msg = 'JOB id not found (maybe synchronous request)'
            LOG.debug(msg)
            return
        retry = sys.maxsize if retry < 0 else retry
        for _i in range(retry):
            command = 'queryAsyncJobResult'
            params = {
                'response': 'json',
                'jobid': job_id,
            }
            api_req_params = self.produce(command, params)
            response = self.request(
                api_req_params.method,
                api_req_params.params,
                api_req_params.headers,
                api_req_params.data
            )
            content_body = response.json()
            inner_content_body = content_body['queryasyncjobresultresponse']
            job_status = inner_content_body['jobstatus']
            if job_status != 0:
                msg = 'JOB status changed: %s' % job_status
                LOG.debug(msg)
                return
            time.sleep(interval)
        raise RetryLimitExceededException('Retried %d times' % retry)


@six.add_metaclass(ABCMeta)
class ClientBase(AttributeInvokeMixin,
                 RequestMixin,
                 AsyncBlockMixin):

    def __init__(self, entry_point, async_block=True):
        super(ClientBase, self).__init__()
        self.entry_point = entry_point
        self.async_block = async_block

    def invoke(self, command, params):
        params['response'] = 'json'

        # HTTP リクエスト
        api_req_params = self.produce(command, params)
        response = self.request(
            api_req_params.method,
            api_req_params.params,
            api_req_params.headers,
            api_req_params.data,
        )

        # HTTP レスポンス
        status_code = response.status_code
        headers = dict(response.headers)
        content_body = response.json()

        if self.async_block:
            self.block(content_body)

        return ApiResponse(status_code, headers, content_body)

    @abstractmethod
    def produce(self, command, params):
        return None


class LoginFailedException(BaseException):

    def __init__(self, msg):
        super(LoginFailedException, self).__init__(msg)


class LoginMixin(object):

    def login(self, username, password, digest=False):
        params = {
            'response': 'json',
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        password = self._md5(password) if digest else password
        data = {
            'command': 'login',
            'username': username,
            'password': password,
            'domain': '/',
        }
        r = self.request('POST', params, headers, data)
        if r.status_code != 200:
            msg = '\'%s\' can not login' % username
            raise LoginFailedException(msg)
        r_json = r.json()
        data = r_json['loginresponse']
        return data['sessionkey']

    def _md5(self, s):
        m = hashlib.md5()
        m.update(s.encode())
        return m.hexdigest()


class CookieClient(ClientBase, LoginMixin):

    def __init__(self, entry_point, username, password,
                 digest=False, async_block=True):
        super(CookieClient, self).__init__(entry_point, async_block)
        self.username = username
        self.password = password
        self.digest = digest

    def produce(self, command, params):
        params['command'] = command
        session_key = self.login(self.username, self.password, self.digest)
        params['sessionkey'] = session_key
        return ApiRequest('GET', params, None, None)


class SignatureBuilder(object):

    def __init__(self, apikey, secretkey):
        self.apikey = apikey
        self.secretkey = secretkey

    def build(self, params):
        if not 'apikey' in [k.lower() for k in params.keys()]:
            params['apikey'] = self.apikey
        # URL エンコードする
        quoted_params = dict([
            (k, parse.quote(v, safe=''))
            for k, v in params.items()
        ])
        # lower case にする
        lower_pairs = [
            ('%s=%s' % (k, v)).lower()
            for k, v in quoted_params.items()
        ]
        # アルファベット順でソートする
        sorted_pairs = sorted(lower_pairs)
        query_string = '&'.join(sorted_pairs)
        # SHA1 のハッシュを計算する
        sha1hash = hmac.new(
            self.secretkey.encode(),
            query_string.encode(),
            hashlib.sha1,
        )
        digest = sha1hash.digest()
        # Base64 エンコードする
        signature = base64.b64encode(digest)

        return signature


class SignatureClient(ClientBase):

    def __init__(self, entry_point, apikey, secretkey, async_block=True):
        super(SignatureClient, self).__init__(entry_point, async_block)
        self.apikey = apikey
        self.secretkey = secretkey
        self.signature_builder = SignatureBuilder(apikey, secretkey)

    def produce(self, command, params):
        params['command'] = command
        signature = self.signature_builder.build(params)
        params['apikey'] = self.apikey
        params['signature'] = signature
        return ApiRequest('GET', params, None, None)


class IntegrationClient(ClientBase):

    def __init__(self, entry_point, async_block=True):
        super(IntegrationClient, self).__init__(entry_point, async_block)

    def produce(self, command, params):
        params['command'] = command
        return ApiRequest('GET', params, None, None)
