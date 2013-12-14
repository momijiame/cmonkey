# -*- coding: utf-8 -*-

import sys

import nose
from nose.tools.trivial import eq_

from cmonkey.cmd.cmonkey import _parse_args
from nose.tools.nontrivial import raises

try:
    import mock
except ImportError:
    from unittest import mock


class Test_Main(object):

    def test_parse_default(self):
        sys.argv = ['cmonkey', '-a', 'foo', '-s', 'bar', 'command=listUsers']
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
        eq_(args.hide_response_body, False)
        eq_(args.parameters, ['command=listUsers'])

    @raises(ValueError)
    def test_parse_error_required_a(self):
        sys.argv = ['cmonkey', '-s', 'bar', 'command=listUsers']
        _parse_args()

    @raises(ValueError)
    def test_parse_error_required_s(self):
        sys.argv = ['cmonkey', '-a', 'foo', 'command=listUsers']
        _parse_args()

    @raises(ValueError)
    def test_parse_error_invalid_t(self):
        sys.argv = ['cmonkey', '-t', 'foo', 'command=listUsers']
        _parse_args()

if __name__ == "__main__":
    nose.main(argv=['nosetests', '-s', '-v'], defaultTest=__file__)
