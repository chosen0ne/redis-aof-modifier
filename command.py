#!/bin/env python
# coding: utf8
#
# use to parse command
#
# @file:    command
# @author:  chosen0ne(louzhenlin86@126.com)
# @date:    2014/10/13 11:51:44

import logging

ENDLINE = '\r\n'

logger = logging.getLogger('root')
logger.setLevel(logging.INFO)


class CommandParser(object):

    def __init__(self, f):
        self._f = f
        self._lineno = 0
        self._cmd_buf = None

    def __iter__(self):
        while True:
            cmd = self._parse()
            if len(cmd) == 0:
                break

            yield cmd

    def _parse(self):
        '''
            to get command
        '''
        cmd = []
        self._cmd_buf = []

        # part count: *3
        part_num_line = self._readline()
        if len(part_num_line) == 0:
            return cmd

        try:
            part_num = self._parse_num(part_num_line, prefix='*')
        except:
            logging.exception('failed to parse part num')
            return cmd

        # iterate each part
        for i in range(part_num):
            cmd.append(self._parse_str())

        return cmd, self._cmd_buf

    def _parse_str(self):
        size_part_line = self._readline()
        try:
            str_len = self._parse_num(size_part_line, prefix='$')
        except:
            logging.exception('failed to parse size for string, line',
                              size_part_line)

        str_part_line = self._readline()
        if str_len != len(str_part_line) - 2:
            logging.error('string len not matched, expected: %d, read: %d, '
                          'str: [%s]', str_len, len(str_part_line) - 2,
                          str_part_line)
        return str_part_line[:-2]

    def _parse_num(self, line, prefix='*'):
        # *2\n
        if len(line) < 3:
            logging.error('line is too short, lineno: %d, line: [%s], '
                          'line len: %d', self._lineno, line, len(line))
            raise Exception('line is too short')

        if line[0] != prefix or line[-2:] != ENDLINE:
            logging.error('invalid format, line number: %d, line: [%s]',
                          self._lineno, line)
            raise Exception('invalid format, line number')

        num_str = line[1:-2]
        if not num_str.isdigit():
            logging.error('part count need a number, lineno: %d, line: [%s]',
                          self._lineno, line)
            raise Exception('invalid number string')

        return int(num_str)

    def _readline(self):
        self._lineno += 1
        line = self._f.readline()
        self._cmd_buf.append(line)

        return line


if __name__ == '__main__':
    with open('aof.log') as f:
        parser = CommandParser(f)
        for cmd, buf in parser:
            print cmd
            print buf
