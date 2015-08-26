#!/bin/env python
# coding: utf8
#
# To fetch old values for deleted keys in AOF log
#
# @file:    aof_fetch
# @author:  chosen0ne(louzhenlin86@126.com)
# @date:    2014/10/13 16:05:35

from optparse import OptionParser

from command import CommandParser
from utils import (fetch_cmd_patterns, match_and_filter_cmds, format_cmd_buf,
                   write_array)


def main():
    opts = cmd_opt_parse()

    multi_cmd_patterns, key_patterns = fetch_cmd_patterns(opts.pattern,
                                                          opts.pattern_file,
                                                          opts.pattern_sep)

    ofname = opts.output if opts.output else opts.input + '.fetch'
    of = open(ofname, 'w')
    readable_fname = opts.readable if opts.readable else \
        opts.input + '.fetch_readable'
    readable_f = open(readable_fname, 'w')
    filtered_fname = opts.filtered if opts.filtered else \
        opts.input + '.filtered'
    filtered_f = open(filtered_fname, 'w')
    filtered_rfname = opts.input + '.filtered_readable'
    filtered_rf = open(filtered_rfname, 'w')

    # fetch all commands on the specified keys
    matched_cmds = []
    with open(opts.input) as f:
        cmd_parser = CommandParser(f)

        # iterate each command in AOF
        for cmds, raw_buf in cmd_parser:
            key = cmds[1]

            for key_pattern in key_patterns:
                if not key_pattern.match(key):
                    continue

                matched_cmds.append((cmds, raw_buf))

    # filter specified commands
    for cmds, raw_buf in matched_cmds:
        old_part_num = len(cmds)
        matched, skip = match_and_filter_cmds(cmds, multi_cmd_patterns,
                                              filtered_f, filtered_rf)
        if matched:
            output_f = filtered_f
            output_readable_f = filtered_rf
        else:
            output_f = of
            output_readable_f = readable_f

        if not skip:
            if old_part_num != len(cmds):
                raw_buf = format_cmd_buf(cmds)

            write_array(raw_buf, output_f)
            output_readable_f.write(' '.join(cmds) + '\n')

    of.close()
    readable_f.close()
    filtered_f.close()


def cmd_opt_parse():
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input',
                      help='input AOF log file')
    parser.add_option('-o', '--output', dest='output',
                      help='output AOF log file')
    parser.add_option('-f', '--filtered', dest='filtered',
                      help='file to store filtered commands')
    parser.add_option('-r', '--readable', dest='readable',
                      help='file to store commands filtered in a readable '
                      'format')
    parser.add_option('-p', '--pattern', dest='pattern',
                      help='pattern to match cmd, eg: "CMD,KEY,SUBKEY"')
    parser.add_option('-m', '--pattern_file', dest='pattern_file',
                      help='multiple pattern in file, each pattern in a line')
    parser.add_option('-s', '--pattern_sep', dest='pattern_sep', default=',',
                      help='separator in pattern')

    options, args = parser.parse_args()
    # check options
    if not options.input:
        parser.error('options -i requires an argument')

    if not options.pattern and not options.pattern_file:
        parser.error('options -p or -m can not be empty at the same time')

    return options


if __name__ == '__main__':
    main()
