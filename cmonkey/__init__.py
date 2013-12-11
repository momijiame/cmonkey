#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os


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
    # TODO: check

    option_s_help = 'Set SECRET key which can be taken from management WebUI'
    environ_secretkey = os.environ.get('CLOUDSTACK_API_SECRETKEY')
    arg_parser.add_argument(
        '-s', '--secret-key',
        type=str,
        required=False, default=environ_secretkey,
        help=option_s_help,
    )
    # TODO: check

    option_x_help = 'Use XML format (default: False, IOW: Use JSON format)'
    arg_parser.add_argument(
        '-x', '--xml-format',
        action='store_true',
        required=False, default=False,
        help=option_x_help,
    )

    option_c_help = 'Show HTTP status code'
    arg_parser.add_argument(
        '-c', '--show-status-code',
        action='store_true',
        required=False, default=False,
        help=option_c_help,
    )

    option_c_help = 'Show HTTP headers'
    arg_parser.add_argument(
        '-d', '--show-headers',
        action='store_true',
        required=False, default=False,
        help=option_c_help,
    )

    option_c_help = 'Show HTTP response body'
    arg_parser.add_argument(
        '-b', '--show-response-body',
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
    return args


def main():
    _parse_args()


if __name__ == '__main__':
    main()
