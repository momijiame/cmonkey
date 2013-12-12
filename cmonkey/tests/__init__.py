# -*- coding: utf-8 -*-

import sys

import nose
from nose.tools.trivial import eq_

from cmonkey import _parse_args, SignatureBuilder

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
        eq_(signature, 'QEq3xbEHhBmSfFw4RwVzkWyQYWc%3D')


class Test_Main(object):

    def test_parse_default(self):
        sys.argv = ['cmonkey', '-a', 'foo', '-s', 'bar', 'command=listUsers']
        args = _parse_args()
        eq_(args.entry_point, 'http://localhost:8080/client/api')
        eq_(args.api_key, 'foo')
        eq_(args.secret_key, 'bar')
        eq_(args.xml_format, False)
        eq_(args.hide_status_code, False)
        eq_(args.hide_headers, False)
        eq_(args.hide_response_body, False)
        eq_(args.parameters, ['command=listUsers'])

    def test_parse_error_required_a(self):
        sys.argv = ['cmonkey', '-s', 'bar', 'command=listUsers']
        sys.exit = mock.Mock()
        _parse_args()
        calls = [
            mock.call(2)
        ]
        sys.exit.assert_has_calls(calls)

    def test_parse_error_required_s(self):
        sys.argv = ['cmonkey', '-a', 'foo', 'command=listUsers']
        sys.exit = mock.Mock()
        _parse_args()
        calls = [
            mock.call(2)
        ]
        sys.exit.assert_has_calls(calls)

if __name__ == "__main__":
    nose.main(argv=['nosetests', '-s', '-v'], defaultTest=__file__)
