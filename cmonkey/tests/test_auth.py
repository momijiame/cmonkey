# -*- coding: utf-8 -*-

import nose
from nose.tools.trivial import eq_

from cmonkey.auth import SignatureBuilder


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


if __name__ == "__main__":
    nose.main(argv=['nosetests', '-s', '-v'], defaultTest=__file__)
