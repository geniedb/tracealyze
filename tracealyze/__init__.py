#/usr/bin/env python
'''
Created on 14 Jun 2012

@author: david
'''

from message_pb2 import RawMsg, _RAWMSG_MESSAGETYPE
from google.protobuf import text_format

class EntryGroup(object):
    def __init__(self, entries):
        self.entries = entries
    
    def earliest(self):
        return min(self.entries, key=lambda x: x.time)    
        
    def latest(self):
        return max(self.entries, key=lambda x: x.time)
    
    def duration(self):
        return self.latest().time - self.earliest().time

class Log(EntryGroup):
    def __init__(self, source):
        self.entries = [x for x in source]
    
    def groupByOts(self):
        groups = {}
        queued = []
        for item in self.entries:
            if item.msg.table.find('$') is -1 and item.socket != "SUB":
                if not item.msg.HasField('originatingTs'):
                    queued.append(item)
                    continue
                if item.msg.originatingTs in groups:
                    groups[item.msg.originatingTs].entries.append(item)
                else:
                    queued.append(item)
                    groups[item.msg.originatingTs] = EntryGroup(queued)
                    queued = []
                    groups[item.msg.originatingTs].originatingTs = item.msg.originatingTs
        return groups.values()
       
    def __iter__(self):
        return self.entries.__iter__()

class LogSource(object):
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
        if len(group.strip()) is not 0:
            yield LogEntry(group)
        raise   StopIteration()

class LogEntry(object):
    def __init__(self, logstr=None):
        '''
        Constructor
        '''
        self.logstr = logstr
        if logstr.startswith("# time: "):
            (self.time,sep,logstr) = logstr.partition("\n")
            self.time = float(self.time[8:])
        (self.dirn,sep,logstr) = logstr.partition("\t")
        (self.socket, sep, logstr) = logstr.partition("\t")
        self.msg = RawMsg()
        text_format.Merge(logstr,self.msg)
    
    def __repr__(self):
        return "<log entry type '{type}', socket '{socket}'>".format(type=self.type, socket=self.socket)
    
    def __str__(self):
        return self.logstr
    
    @property
    def type(self):
        return _RAWMSG_MESSAGETYPE.values_by_number[self.msg.type].name
    
    @type.setter
    def type(self, value):
        self.msg.type = int(value)   