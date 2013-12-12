#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import argparse


def _parse_args():
    description = 'Simple client script for Apache CloudStack'
    arg_parser = argparse.ArgumentParser(description=description)

    option_e_help = 'Set CloudStack API entry point'
    default_entry_point = 'http://localhost:8080/client/api'
    environ_entry_point = os.environ.get('CLOUDSTACK_API_ENTRYPOINT')
    arg_parser.add_argument(
        '-e', '--entry-point',
        type=str,
        required=False, default=(environ_entry_point or default_entry_point),
        help=option_e_help,
    )

    option_a_help = 'Set API key which can be taken from management WebUI'
    environ_apikey = os.environ.get('CLOUDSTACK_API_APIKEY')
    arg_parser.add_argument(
        '-a', '--api-key',
        type=str,
        required=False, default=environ_apikey,
        help=option_a_help,
    )

    option_s_help = 'Set SECRET key which can be taken from management WebUI'
    environ_secretkey = os.environ.get('CLOUDSTACK_API_SECRETKEY')
    arg_parser.add_argument(
        '-s', '--secret-key',
        type=str,
        required=False, default=environ_secretkey,
        help=option_s_help,
    )

    option_x_help = 'Use XML format (default: False, IOW: Use JSON format)'
    arg_parser.add_argument(
        '-x', '--xml-format',
        action='store_true',
        required=False, default=False,
        help=option_x_help,
    )

    option_c_help = 'Hide HTTP status code'
    arg_parser.add_argument(
        '-c', '--hide-status-code',
        action='store_true',
        required=False, default=False,
        help=option_c_help,
    )

    option_c_help = 'Hide HTTP headers'
    arg_parser.add_argument(
        '-d', '--hide-headers',
        action='store_true',
        required=False, default=False,
        help=option_c_help,
    )

    option_c_help = 'Hide HTTP response body'
    arg_parser.add_argument(
        '-b', '--hide-response-body',
        action='store_true',
        required=False, default=False,
        help=option_c_help,
    )

    parameters_help = 'key=value pairs (e.g. command=listHosts ...)'
    arg_parser.add_argument(
        'parameters',
        nargs='+',
        help=parameters_help,
    )

    args = arg_parser.parse_args()

    if not args.api_key:
        reason = 'error: the following arguments are required'
        params = '-a/--api-key/os.environ["CLOUDSTACK_API_APIKEY"]'
        msg = '%s: %s: %s' % (sys.argv[0], reason, params)
        print(msg, file=sys.stderr)
        sys.exit(2)

    if not args.secret_key:
        reason = 'error: the following arguments are required'
        params = '-s/--secret-key/os.environ["CLOUDSTACK_API_SECRETKEY"]'
        msg = '%s: %s: %s' % (sys.argv[0], reason, params)
        print(msg, file=sys.stderr)
        sys.exit(2)

    return args


def main():
    _parse_args()


if __name__ == '__main__':
    main()
