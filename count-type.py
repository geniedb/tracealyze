#!/usr/bin/env python
'''
Created on 14 Jun 2012

@author: david
'''

import sys
from argparse import ArgumentParser, FileType, REMAINDER
from LogEntry import Log, LogEntry 

class defdict(dict):
    def __missing__(self, key):
        return 0

if __name__ == '__main__':
    parser = ArgumentParser(description='Count different types of message.')
    parser.add_argument('files', metavar='FILE', type=Log, nargs=REMAINDER, help='Trace file', default=[sys.stdin])
    params = parser.parse_args()
    
    seen = defdict()
    
    for log in params.files:
        for logentry in log:
            if logentry.socket != "SUB":
                seen[logentry.type] += 1
    
    for (k,v) in seen.iteritems():
        print "{count:8} {type}".format(count=v, type=k)