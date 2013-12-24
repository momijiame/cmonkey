# -*- coding: utf-8 -*-

import hashlib

import nose
from nose.tools.trivial import eq_

from cmonkey import (
    CookieClient,
    SignatureClient,
    SignatureBuilder,
    IntegrationClient,
    ApiResponse,
    ApiRequest
)

try:
    import mock
except ImportError:
    from unittest import mock


class Test_SignatureBuilder(object):

    APIKEY = 'B1glHBDDvXwKz4XkLXhd_Hk5-Fp8RZfukbE4shWk2p9nRjPvtMLTtNtawtD1H-a4kh06P0U5eRBELVOl6OAThg'
    SECRETKEY = 'VpznCS2q7t9-Sd8QJJwW_VLm_IX1g3ua9fMasSyD8jD5XBXso3heVG6_3PUcQi5lVWZXXYKoJwcWukv0V7DvCQ'

    def test_build(self):
        params = {
            'command': 'listUsers',
            'keyword': 'ad',
        }
        builder = SignatureBuilder(self.APIKEY, self.SECRETKEY)
        signature = builder.build(params)
        eq_(signature, b'QEq3xbEHhBmSfFw4RwVzkWyQYWc=')

    def test_contains_slash(self):
        params = {
            'command': 'createZone',
            'dns1': '203.0.113.1',
            'internaldns1': '198.51.100.1',
            'name': 'sample-zone',
            'networktype': 'Advanced',
            'guestcidraddress': '192.0.2.0/24',
        }
        builder = SignatureBuilder(self.APIKEY, self.SECRETKEY)
        signature = builder.build(params)
        eq_(signature, b'4+XLXpBJuqKH/BVg2WNYRcPFjTY=')


class Test_CookieClient(object):

    def test_request(self):
        endpoint = 'http://localhost:8080/client/api'
        username = 'admin'
        password = 'password'
        client = CookieClient(endpoint, username, password)
        # モックアウト
        sessionkey = 'hogehoge'
        client.login = mock.MagicMock(return_value=sessionkey)
        response = mock.Mock()
        response.status_code = 200
        response.headers = {}
        response.json = lambda: {}
        client.request = mock.Mock(return_value=response)
        # 実行
        params = {
            'account': 'admin',
            'response': 'json',
        }
        client.listUsers(**params)
        # 検証
        calls = [
            mock.call(username, password, False)
        ]
        client.login.assert_has_calls(calls)
        params['command'] = 'listUsers'
        params['sessionkey'] = sessionkey
        calls = [
            mock.call(ApiRequest('GET', params, None, None))
        ]
        client.request.assert_has_calls(calls)

    def test_login_digest(self):
        self._test_login(digest=True)

    def test_login_no_digest(self):
        self._test_login(digest=False)

    def _test_login(self, digest):
        endpoint = 'http://localhost:8080/client/api'
        username = 'admin'
        password = 'password'
        client = CookieClient(endpoint, username, password, digest=digest)
        # モックアウト
        response_mock = mock.Mock()
        response_mock.status_code = 200
        response_mock.json = lambda: {
            'loginresponse': {
                'sessionkey': 'hoge',
            },
        }
        client.request = mock.MagicMock(return_value=response_mock)
        # 実行
        client.login(username, password, digest)
        # 検証
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
        calls = [
            mock.call('POST', params, headers, data)
        ]
        client.request.assert_has_calls(calls)

    def _md5(self, s):
        m = hashlib.md5()
        m.update(s.encode())
        return m.hexdigest()


class Test_IntegrationClient(object):

    def test_request(self):
        endpoint = 'http://localhost:8080/client/api'
        client = IntegrationClient(endpoint)
        # モックアウト
        response = mock.Mock()
        response.status_code = 200
        response.headers = {}
        response.json = lambda: {}
        client.request = mock.Mock(return_value=response)
        # 実行
        params = {
            'account': 'admin',
            'response': 'json',
        }
        response = client.listUsers(**params)
        # 検証
        eq_(type(response), ApiResponse)
        params['command'] = 'listUsers'
        calls = [
            mock.call(ApiRequest('GET', params, None, None))
        ]
        client.request.assert_has_calls(calls)


class Test_SignatureClient(object):

    APIKEY = 'p-dZvP8oknG8RwRuHM_k-pTCqni9wY-_n3mdroNn4Bo9u_hG9FXO39gcjmWWCwClSJgP47-fU3JBh8yCs_Do1A'
    SECRETKEY = 'HzlToLKEgOenK11URMpy-3arN5ZJ0JqRC-We9FDhcEbKtMIBE71kebVeYCWeLNA7SIZVDpM_yUSM6vtjU7K3MQ'
    SIGNATURE = b'jhoz5uOKJp8707r9MeMJjCOVLqM='

    def test_request(self):
        endpoint = 'http://localhost:8080/client/api'
        client = SignatureClient(endpoint, self.APIKEY, self.SECRETKEY)
        # モックアウト
        response = mock.Mock()
        response.status_code = 200
        response.headers = {}
        response.json = lambda: {}
        client.request = mock.Mock(return_value=response)
        # 実行
        params = {
            'account': 'admin',
            'response': 'json',
        }
        client.listUsers(**params)
        # 検証
        params['command'] = 'listUsers'
        params['apikey'] = self.APIKEY
        params['signature'] = self.SIGNATURE
        calls = [
            mock.call(ApiRequest('GET', params, None, None))
        ]
        client.request.assert_has_calls(calls)


if __name__ == "__main__":
    nose.main(argv=['nosetests', '-s', '-v'], defaultTest=__file__)
