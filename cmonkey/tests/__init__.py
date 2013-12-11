# -*- coding: utf-8 -*-

import sys

import nose
from nose.tools.trivial import eq_

from cmonkey import _parse_args

try:
    import mock
except ImportError:
    from unittest import mock


class Test_Main(object):

    def test_parse_default(self):
        sys.argv = ['cmonkey', 'command=listUsers']
        args = _parse_args()
        eq_(args.entry_point, 'http://localhost:8080/client/api')
        eq_(args.api_key, None)  # XXX
        eq_(args.secret_key, None)  # XXX
        eq_(args.xml_format, False)
        eq_(args.show_status_code, False)
        eq_(args.show_headers, False)
        eq_(args.show_response_body, False)
        eq_(args.parameters, ['command=listUsers'])


if __name__ == "__main__":
    nose.main(argv=['nosetests', '-s', '-v'], defaultTest=__file__)
