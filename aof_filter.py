#!/bin/env python
# coding: utf8
#
# Filter specified commands on a key in AOF log
#
# @file:    aof_modifier
# @author:  chosen0ne(louzhenlin86@126.com)
# @date:    2014/10/13 11:12:33

from optparse import OptionParser

from command import CommandParser
from utils import (fetch_cmd_patterns, match_and_filter_cmds, write_array,
                   format_cmd_buf)


def main():
    opts = cmd_opt_parse()

    multi_cmd_patterns, _ = fetch_cmd_patterns(opts.pattern,
                                               opts.pattern_file,
                                               opts.pattern_sep)

    ofname = opts.output if opts.output else opts.input + '.new'
    of = open(ofname, 'w')
    filtered_fname = opts.filtered if opts.filtered else \
        opts.input + '.filtered'
    filtered_f = open(filtered_fname, 'w')
    readable_fname = opts.readable if opts.readable else \
        opts.input + '.filtered_readable'
    readable_f = open(readable_fname, 'w')

    with open(opts.input) as f:
        cmd_parser = CommandParser(f)

        for cmds, raw_buf in cmd_parser:
            old_part_num = len(cmds)
            matched, skip = match_and_filter_cmds(cmds, multi_cmd_patterns,
                                                  filtered_f, readable_f)
            if matched:
                output_file = filtered_f
                if not skip:
                    readable_f.write(' '.join(cmds) + '\n')
            else:
                output_file = of

            if not skip:
                if old_part_num != len(cmds):
                    raw_buf = format_cmd_buf(cmds)

                write_array(raw_buf, output_file)

    of.close()
    filtered_f.close()
    readable_f.close()


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
