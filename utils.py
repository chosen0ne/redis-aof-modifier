#!/bin/env python
# coding: utf8
#
#
# @file:    utils
# @author:  chosen0ne(louzhenlin86@126.com)
# @date:    2014/10/14 11:45:31

import re

TWO_BASE_PART = 2
THREE_BASE_PART = 3


def fetch_cmd_patterns(pattern, pattern_file, pattern_sep):
    multi_cmd_patterns = []
    key_patterns = []
    if pattern:
        patterns = _fetch_one_pattern(pattern, pattern_sep)
        key_patterns.append(patterns[1])
        multi_cmd_patterns.append(patterns)

    if pattern_file:
        with open(pattern_file) as f:
            for line in f:
                patterns = _fetch_one_pattern(line[:-1], pattern_sep)
                key_patterns.append(patterns[1])
                multi_cmd_patterns.append(patterns)

    return multi_cmd_patterns, key_patterns


def match_and_filter_cmds(cmd_parts, multi_cmd_patterns, filtered_file=None,
                          readable_file=None):
    '''
        @return (is_matched, need_skip)
            is_matched: cmd matches the pattern or not
            need_skip: cmd isn't integrated, no need to output
    '''
    for cmd_pattern in multi_cmd_patterns:
        # match cmd
        if not cmd_pattern[0].match(cmd_parts[0]):
            continue

        rm_info = []
        # COMMAND,KEY
        if _is_two_part_cmd(cmd_parts[0]):
            # process command with multi keys format
            for i in range(1, len(cmd_parts)):
                if cmd_pattern[1].match(cmd_parts[i]):
                    rm_info.append((i, TWO_BASE_PART))

            valid_part_num = 2

        # COMMAND,KEY,SUBKEY
        else:
            # match key
            if not cmd_pattern[1].match(cmd_parts[1]):
                continue

            if len(cmd_pattern) == 2:
                return True, False

            # check subkey
            for i in range(2, len(cmd_parts)):
                if cmd_pattern[2].match(cmd_parts[i]):
                    rm_info.append((i, THREE_BASE_PART))

            valid_part_num = 3

        _rm_matched_cmd(rm_info, cmd_parts, filtered_file, readable_file)

        if len(cmd_parts) < valid_part_num:
            return True, True

    return False, False


def write_array(array, f):
    for ele in array:
        f.write(ele)


def format_cmd_buf(cmd_parts):
    cmd_buf = []
    part_num = len(cmd_parts)
    cmd_buf.append('*%d\r\n' % part_num)
    for part in cmd_parts:
        cmd_buf.append('$%d\r\n' % len(part))
        cmd_buf.append('%s\r\n' % part)

    return cmd_buf


def _rm_matched_cmd(rm_info, cmd_parts, filtered_file, readable_file):
    for idx, part_type in rm_info:
        if part_type == TWO_BASE_PART:
            cmd = (cmd_parts[0], cmd_parts[idx])
            cmd_format = '%s %s\n'
        else:
            cmd = (cmd_parts[0], cmd_parts[1], cmd_parts[idx])
            cmd_format = '%s %s %s\n'

        if filtered_file:
            write_array(format_cmd_buf(cmd), filtered_file)

        if readable_file:
            readable_file.write(cmd_format % cmd)

        del cmd_parts[idx]


def _fetch_one_pattern(pattern_strs, sep):
    pattern_strs = pattern_strs.split(sep)
    cmd_patterns = []
    for s in pattern_strs:
        cmd_patterns.append(re.compile(s, re.I))

    return cmd_patterns


def _is_cmd_key_match(cmd_parts, cmd_pattern, key_pattern):
    return cmd_pattern.match(cmd_parts[0]) and key_pattern.match(cmd_parts[1])


def _is_two_part_cmd(cmd):
    prefix = cmd[0].upper()
    if prefix == 'H':
        return False
    elif prefix == 'S':
        return False
    elif prefix == 'Z':
        return False

    return True
