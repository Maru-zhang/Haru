#!/usr/bin/env python
# coding=utf-8

import sys
import jenkins

from sources.cli.haru import Haru

if __name__ == '__main__':
    argv = sys.argv[1:]
    haru = Haru(argv)