#!/bin/env python
# coding: utf8
#
# Redo Aof log
#
# @file:    aof_redo
# @author:  chosen0ne(louzhenlin86@126.com)
# @date:    2014/10/21 16:22:55

from optparse import OptionParser

import redis
from command import CommandParser


def main():
    opts = cmd_opt_parse()

    conn = redis.StrictRedis(opts.host, opts.port)

    with open(opts.input) as f:
        parser = CommandParser(f)

        for cmd_detail, _ in parser:
            cmd = cmd_detail[0].lower()
            if cmd == 'del':
                cmd = 'delete'

            func = getattr(conn, cmd)

            # redo command
            func(*cmd_detail[1:])


def cmd_opt_parse():
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input',
                      help='input AOF log file')
    parser.add_option('-H', '--host', dest='host', default='localhost',
                      help='redis host to redo')
    parser.add_option('-p', '--port', dest='port', default=6379,
                      help='redis port to redo')

    options, _ = parser.parse_args()

    if not options.input:
        parser.error('options -i requires an argument')

    return options


if __name__ == '__main__':
    main()
