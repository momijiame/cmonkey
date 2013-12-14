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

    option_t_help = 'Set authentication type (default: signature)'
    arg_parser.add_argument(
        '-t', '--authentication-type',
        type=str,
        required=False, default='signature',
        help=option_t_help,
    )

    option_a_help = 'Set API key (when using -t \'signature\')'
    environ_apikey = os.environ.get('CLOUDSTACK_API_APIKEY')
    arg_parser.add_argument(
        '-a', '--api-key',
        type=str,
        required=False, default=environ_apikey,
        help=option_a_help,
    )

    option_s_help = 'Set SECRET key (when using -t \'signature\')'
    environ_secretkey = os.environ.get('CLOUDSTACK_API_SECRETKEY')
    arg_parser.add_argument(
        '-s', '--secret-key',
        type=str,
        required=False, default=environ_secretkey,
        help=option_s_help,
    )

    option_u_help = 'Set username (when using -t \'cookie\')'
    environ_username = os.environ.get('CLOUDSTACK_API_USERNAME')
    arg_parser.add_argument(
        '-u', '--username',
        type=str,
        required=False, default=environ_username,
        help=option_u_help,
    )

    option_p_help = 'Set password (when using -t \'cookie\')'
    environ_password = os.environ.get('CLOUDSTACK_API_PASSWORD')
    arg_parser.add_argument(
        '-p', '--password',
        type=str,
        required=False, default=environ_password,
        help=option_p_help,
    )

    option_d_help = 'Use digested password (default: False)'
    arg_parser.add_argument(
        '-g', '--digested-password',
        action='store_true',
        required=False, default=False,
        help=option_d_help,
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
    _validate(args)

    return args


def _validate(args):
    # 認証タイプ別のバリデーション
    auth_types = {
        'signature': _validate_signature,
        'cookie': _validate_cookie,
    }
    auth_validate_function = auth_types.get(args.authentication_type)
    if not auth_validate_function:
        _invalid('-t/--authentication-type')
    auth_validate_function(args)


def _validate_signature(args):
    params = '-a/--api-key/os.environ["CLOUDSTACK_API_APIKEY"]'
    _require(args.api_key, params)
    params = '-s/--secret-key/os.environ["CLOUDSTACK_API_SECRETKEY"]'
    _require(args.secret_key, params)


def _validate_cookie(args):
    params = '-u/--username/os.environ["CLOUDSTACK_API_USERNAME"]'
    _require(args.username, params)
    params = '-p/--password/os.environ["CLOUDSTACK_API_PASSWORD"]'
    _require(args.password, params)


def _require(argument, arg_params):
    if not argument:
        reason = 'error: the following argument is required'
        msg = '%s: %s: %s' % (sys.argv[0], reason, arg_params)
        raise ValueError(msg)


def _invalid(arg_params):
    reason = 'error: the following argument is invalid'
    msg = '%s: %s: %s' % (sys.argv[0], reason, arg_params)
    raise ValueError(msg)


def main():
    try:
        _parse_args()
    except ValueError as e:
        print(e, file=sys.stderr)


if __name__ == '__main__':
    main()
