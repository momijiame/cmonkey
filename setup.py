#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def _load_requires_from_file(filepath):
    return [pkg_name.rstrip('\r\n') for pkg_name in open(filepath).readlines()]


def _install_requires():
    requires = _load_requires_from_file('requirements.txt')
    return requires


def _test_requires():
    test_requires = _load_requires_from_file('test-requirements.txt')
    return test_requires


def _packages():
    return find_packages(
        exclude=[
            '*.tests',
            '*.tests.*',
            'tests.*',
            'tests'
        ],
    )


if __name__ == '__main__':
    setup(
        name='cmonkey',
        version='0.0.1',
        description='Simple client script for Apache CloudStack',
        author='momijiame',
        author_email='amedama.ginmokusei@gmail.com',
        url='https://github.com/momijiame/cmonkey',
        packages=_packages(),
        install_requires=_install_requires(),
        tests_require=_test_requires(),
        test_suite='nose.collector',
        entry_points="""
        [console_scripts]
        cmonkey = cmonkey:main
        """,
    )
