#!/usr/bin/env python
# -*- coding: utf-8 -*-


class CloudStackApiClient(object):

    def __init__(self, authenticator):
        self.authenticator = authenticator
