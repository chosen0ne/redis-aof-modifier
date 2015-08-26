#!/bin/env python
# coding: utf8
#
#
# @file:    assert_result
# @author:  chosen0ne(louzhenlin86@126.com)
# @date:    2014/10/21 15:58:33

import redis

src = redis.StrictRedis('localhost', 6379)
dist = redis.StrictRedis('localhost', 16379)


def main():
    src_keys = src.keys()
    dist_keys = dist.keys()

    src_key_set = set(src_keys)
    dist_key_set = set(dist_keys)

    more = dist_key_set - src_key_set
    less = src_key_set - dist_key_set
    if more:
        print '+dist:', more
    if less:
        print '+src:', less


if __name__ == '__main__':
    main()
