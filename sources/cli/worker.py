#!/usr/bin/env python
# coding=utf-8

from sources.cli.haru import logger

class Worker(object):

    def run(self):
        
        if self.init not None:
            logger.debug("init action ...")
