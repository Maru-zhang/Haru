#!/usr/bin/env python
# coding=utf-8

import sys

class Worker:

    def default_init(args):
        print(sys._getframe().f_code.co_name)

    def default_query(args):
        print(sys._getframe().f_code.co_name)

    def default_delete(args):
        print(sys._getframe().f_code.co_name)
    
    def default_update(args):
        print(sys._getframe().f_code.co_name)
