# -*- coding: utf-8 -*-

import sys

import nose
from nose.tools.trivial import eq_, ok_
from nose.tools.nontrivial import raises

from cmonkey.cmd import _parse_args, _request, _get_client
from cmonkey import SignatureClient, CookieClient, IntegrationClient


class Test_Main(object):

    def test_parse_default_signature(self):
        sys.argv = [
            'cmonkey',
            '-a', 'foo',
            '-s', 'bar',
            'listUsers',
        ]
        args = _parse_args()
        eq_(args.entry_point, 'http://localhost:8080/client/api')
        eq_(args.authentication_type, 'signature')
        eq_(args.api_key, 'foo')
        eq_(args.secret_key, 'bar')
        eq_(args.username, None)
        eq_(args.password, None)
        eq_(args.digested_password, False)
        eq_(args.hide_status_code, False)
        eq_(args.hide_headers, False)
        eq_(args.hide_content_body, False)
        eq_(args.pretty_print, False)
        eq_(args.no_block_asynchronous, True)
        eq_(args.parameters, ['listUsers'])

    def test_parse_default_cookie(self):
        sys.argv = [
            'cmonkey',
            '-t', 'cookie',
            '-u', 'foo',
            '-p', 'bar',
            'listUsers',
        ]
        args = _parse_args()
        eq_(args.entry_point, 'http://localhost:8080/client/api')
        eq_(args.authentication_type, 'cookie')
        eq_(args.api_key, None)
        eq_(args.secret_key, None)
        eq_(args.username, 'foo')
        eq_(args.password, 'bar')
        eq_(args.digested_password, False)
        eq_(args.hide_status_code, False)
        eq_(args.hide_headers, False)
        eq_(args.hide_content_body, False)
        eq_(args.pretty_print, False)
        eq_(args.parameters, ['listUsers'])

    @raises(ValueError)
    def test_parse_error_required_a(self):
        sys.argv = [
            'cmonkey',
            '-s', 'bar',
            'listUsers',
        ]
        _parse_args()

    @raises(ValueError)
    def test_parse_error_required_s(self):
        sys.argv = [
            'cmonkey',
            '-a', 'foo',
            'listUsers',
        ]
        _parse_args()

    @raises(ValueError)
    def test_parse_error_invalid_t(self):
        sys.argv = [
            'cmonkey',
            '-t', 'foo',
            'listUsers',
        ]
        _parse_args()

    @raises(ValueError)
    def test_parse_error_required_u(self):
        sys.argv = [
            'cmonkey',
            '-t', 'cookie',
            '-p', 'bar',
            'listUsers',
        ]
        _parse_args()

    @raises(ValueError)
    def test_parse_error_required_p(self):
        sys.argv = [
            'cmonkey',
            '-t', 'cookie',
            '-u', 'foo',
            'listUsers',
        ]
        _parse_args()

    @raises(ValueError)
    def test_exec_error_invalid_param(self):
        sys.argv = [
            'cmonkey',
            '-t', 'cookie',
            '-u', 'foo',
            '-p', 'bar',
            'listUsers',
            'a',
        ]
        args = _parse_args()
        _request(args)

    def test_get_client_default(self):
        sys.argv = [
            'cmonkey',
            '-a', 'foo',
            '-s', 'bar',
            'listUsers',
        ]
        args = _parse_args()
        client = _get_client(args)
        ok_(isinstance(client, SignatureClient))

    def test_get_client_signature(self):
        sys.argv = [
            'cmonkey',
            '-t', 'signature',
            '-a', 'foo',
            '-s', 'bar',
            'listUsers',
        ]
        args = _parse_args()
        client = _get_client(args)
        ok_(isinstance(client, SignatureClient))

    def test_get_client_cookie(self):
        sys.argv = [
            'cmonkey',
            '-t', 'cookie',
            '-u', 'foo',
            '-p', 'bar',
            'listUsers',
        ]
        args = _parse_args()
        client = _get_client(args)
        ok_(isinstance(client, CookieClient))

    def test_get_client_integration(self):
        sys.argv = [
            'cmonkey',
            '-t', 'integration',
            'listUsers',
        ]
        args = _parse_args()
        client = _get_client(args)
        ok_(isinstance(client, IntegrationClient))


if __name__ == "__main__":
    nose.main(argv=['nosetests', '-s', '-v'], defaultTest=__file__)
