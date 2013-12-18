#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import json
import collections
import argparse

from cmonkey import (
    SignatureClient,
    CookieClient,
    IntegrationClient
)


def _request(args):
    call_parameters = collections.deque(args.parameters)
    api_command = call_parameters.popleft()
    api_args = _analyze_parameters(call_parameters)
    # クライアントを取得する
    client = _get_client(args)
    # API を実行する
    api_method = getattr(client, api_command)
    status_code, headers, content_body = api_method(**api_args)
    # レスポンスを表示する
    response = {}
    if not args.hide_status_code:
        response['status-code'] = status_code
    if not args.hide_headers:
        response['headers'] = headers
    if not args.hide_content_body:
        response['content-body'] = content_body
    indent = 4 if args.pretty_print else None
    print(json.dumps(response, indent=indent))


def _analyze_parameters(call_parameters):
    api_args = {}
    for call_param in call_parameters:
        pair = call_param.split('=')
        if len(pair) != 2:
            _invalid_parameter(pair[0])
        key, value = pair
        api_args[key] = value
    return api_args


def _get_client(args):
    clients = {
        'signature': (
            SignatureClient,
            [
                args.entry_point,
                args.api_key,
                args.secret_key,
            ],
        ),
        'cookie': (
            CookieClient,
            [
                args.entry_point,
                args.username,
                args.password,
                args.digested_password,
            ],
        ),
        'integration': (
            IntegrationClient,
            [
                args.entry_point,
            ],
        ),
    }
    client_cls, init_args = clients[args.authentication_type]
    return client_cls(*init_args)


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

    option_c_help = 'Hide HTTP status code (default: False)'
    arg_parser.add_argument(
        '-c', '--hide-status-code',
        action='store_true',
        required=False, default=False,
        help=option_c_help,
    )

    option_d_help = 'Hide HTTP headers (default: False)'
    arg_parser.add_argument(
        '-d', '--hide-headers',
        action='store_true',
        required=False, default=False,
        help=option_d_help,
    )

    option_b_help = 'Hide HTTP content body (default: False)'
    arg_parser.add_argument(
        '-b', '--hide-content-body',
        action='store_true',
        required=False, default=False,
        help=option_b_help,
    )

    option_r_help = 'Pretty print'
    arg_parser.add_argument(
        '-i', '--pretty-print',
        action='store_true',
        required=False, default=False,
        help=option_r_help,
    )

    parameters_help = 'command and key=value pairs'
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
        'signature': _validate_params_signature,
        'cookie': _validate_params_cookie,
        'integration': _validate_params_integration,
    }
    auth_validate_function = auth_types.get(args.authentication_type)
    if not auth_validate_function:
        _invalid_argument('-t/--authentication-type')
    auth_validate_function(args)


def _validate_params_signature(args):
    params = '-a/--api-key/os.environ["CLOUDSTACK_API_APIKEY"]'
    _require_argument(args.api_key, params)
    params = '-s/--secret-key/os.environ["CLOUDSTACK_API_SECRETKEY"]'
    _require_argument(args.secret_key, params)


def _validate_params_cookie(args):
    params = '-u/--username/os.environ["CLOUDSTACK_API_USERNAME"]'
    _require_argument(args.username, params)
    params = '-p/--password/os.environ["CLOUDSTACK_API_PASSWORD"]'
    _require_argument(args.password, params)


def _validate_params_integration(args):
    pass


def _require_argument(argument, arg_params):
    if not argument:
        reason = 'error: the following argument is required'
        msg = '%s: %s: %s' % (sys.argv[0], reason, arg_params)
        raise ValueError(msg)


def _invalid_argument(arg_params):
    reason = 'error: the following argument is invalid'
    _invalid(arg_params, reason)


def _invalid_parameter(param_key):
    reason = 'error: the following parameter is invalid'
    _invalid(param_key, reason)


def _invalid(entry, reason):
    msg = '%s: %s: %s' % (sys.argv[0], reason, entry)
    raise ValueError(msg)


def main():
    try:
        args = _parse_args()
        _request(args)
    except BaseException as e:
        print('Error: %s' % e, file=sys.stderr)

if __name__ == '__main__':
    main()
