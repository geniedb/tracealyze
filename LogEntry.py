#/usr/bin/env python
'''
Created on 14 Jun 2012

@author: david
'''

from message_pb2 import RawMsg, _RAWMSG_MESSAGETYPE
from google.protobuf import text_format

class Log(object):
    def __init__(self, filename):
        self.file = open(filename)
        
    def __iter__(self):
        group = str()
        for line in self.file:
            if len(line.strip()) is 0:
                yield LogEntry(group)
                group = str()
            else:
                group = group + line
        yield LogEntry(group)
        raise   StopIteration()

class LogEntry(object):
    def __init__(self, logstr=None):
        '''
        Constructor
        '''
        (self.dirn,sep,rest) = logstr.partition("\t")
        (self.socket, sep, msg) = rest.partition("\t")
        self.msg = RawMsg()
        text_format.Merge(msg,self.msg)
        
    @property
    def type(self):
        return _RAWMSG_MESSAGETYPE.values_by_number[self.msg.type].name
    
    @type.setter
    def type(self, value):
        self.msg.type = int(value)   