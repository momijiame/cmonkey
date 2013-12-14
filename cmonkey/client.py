#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

import hmac
import hashlib
import base64

import six
from six.moves.urllib import parse
# from urllib import parse
import requests


class AttributeInvokeMixin(object):

    def __getattr__(self, name):
        def handle(*args, **kwargs):
            return self.invoke(name, kwargs)
        return handle


@six.add_metaclass(ABCMeta)
class ClientBase(AttributeInvokeMixin):

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.session = requests.Session()

    def invoke(self, command, params):
        params['response'] = 'json'
        method, params, headers, data = self.produce(command, params)
        response = self.request(method, params, headers, data)
        return response.json()

    @abstractmethod
    def produce(self, command, params):
        return (None, None, None, None)

    def request(self, method=None, params=None, headers=None, data=None):
        params = params or {}
        headers = headers or {}
        data = data or {}
        return self.session.request(
            method or 'GET',
            self.endpoint,
            params=params,
            headers=headers,
            data=data,
        )


class CookieClient(ClientBase):

    def __init__(self, endpoint, username, password, digest=False):
        super(CookieClient, self).__init__(endpoint)
        self.username = username
        self.password = password
        self.digest = digest

    def produce(self, command, params):
        params['command'] = command
        session_key = self.login()
        params['sessionkey'] = session_key
        return 'GET', params, None, None

    def login(self):
        params = {
            'response': 'json',
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        password = self._md5(self.password) if self.digest else self.password
        data = {
            'command': 'login',
            'username': self.username,
            'password': password,
            'domain': '/',
        }
        r = self.request('POST', params, headers, data)
        r_json = r.json()
        data = r_json['loginresponse']
        return data['sessionkey']

    def _md5(self, s):
        m = hashlib.md5()
        m.update(s.encode())
        return m.hexdigest()


class SignatureBuilder(object):

    def __init__(self, apikey, secretkey):
        self.apikey = apikey
        self.secretkey = secretkey

    def build(self, params):
        if not 'apikey' in [k.lower() for k in params.keys()]:
            params['apikey'] = self.apikey
        # URL エンコードする
        quoted_params = dict([
            (k, parse.quote(v))
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

    def __init__(self, endpoint, apikey, secretkey):
        super(SignatureClient, self).__init__(endpoint)
        self.apikey = apikey
        self.secretkey = secretkey
        self.signature_builder = SignatureBuilder(apikey, secretkey)

    def produce(self, command, params):
        params['command'] = command
        signature = self.signature_builder.build(params)
        params['apikey'] = self.apikey
        params['signature'] = signature
        return 'GET', params, None, None
