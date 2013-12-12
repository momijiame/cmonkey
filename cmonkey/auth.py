#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

import six
import hmac
import hashlib
import base64

from six.moves.urllib import parse


@six.add_metaclass(ABCMeta)
class Authenticator(object):

    @abstractmethod
    def authenticate(self):
        pass


class DummyAuthenticator(Authenticator):

    def authenticate(self):
        pass


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
        encoded_digest = base64.b64encode(digest)
        # URL エンコードする
        signature = parse.quote(encoded_digest)

        return signature
