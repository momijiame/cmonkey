#!/usr/bin/env python
# -*- coding: utf-8 -*-


class CloudStackApiClient(object):

    def __init__(self, authenticator):
        self.authenticator = authenticator

    def __getattr__(self, name):
        def handle(*args, **kwargs):
            return self._request(name, kwargs)
        return handle

    def _request(self, command, params):
        pass
