# -*- coding: utf-8 -*-

import nose

from cmonkey.auth import DummyAuthenticator
from cmonkey.client import CloudStackApiClient


class Test_CloudStackApiClient(object):

    def test_getattr(self):
        authenticator = DummyAuthenticator()
        CloudStackApiClient(authenticator)


if __name__ == "__main__":
    nose.main(argv=['nosetests', '-s', '-v'], defaultTest=__file__)
