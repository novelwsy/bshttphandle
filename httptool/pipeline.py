#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class PipeLine(object):
    def __init__(self, moduleName, ignoreSessions=[]):
        self.moduleName = moduleName
        self.sessionModule = __import__(moduleName)
        self.sessionNames = None
        self.breakonerror = True
        if hasattr(self.sessionModule, '__breakonerror__'):
            self.breakonerror = getattr(self.sessionModule, '__breakonerror__')
        if hasattr(self.sessionModule, '__pipeline__'):
            self.sessionNames = getattr(self.sessionModule, '__pipeline__')
        else:
            self.sessionNames = []
            for name in dir(self.sessionModule):
                if not name.startswith('_'):
                    self.sessionNames.append(name)
        self.sessions = {}
        for name in self.sessionNames:
            self.sessions[name] = getattr(self.sessionModule, name)

    def run(self, startSession=None):
        from ColorConsole import dcc
        dcc.setColor(dcc.blue)
        print('start module [%s] tests.' % self.moduleName)
        dcc.setColor(dcc.reset)
        retval = True
        start = 0
        if startSession != None:
            start = self.sessionNames.index(startSession)
        # print(self.sessionNames)
        for sessionId in range(start, len(self.sessionNames)):
            name = self.sessionNames[sessionId]
            func = self.sessions[name]
            try:
                ret = func()
                # 如果返回Goto语句
                if isinstance(ret, Goto):
                    if ret.breakCurrent:
                        dcc.setColor(dcc.yellow)
                        print('module %s break.' % self.moduleName)
                        dcc.setColor(dcc.reset)
                    dcc.setColor(dcc.yellow)
                    print("goto %s -> %s" % (ret.pipeline, ret.startSession))
                    nextPipeline = self
                    if ret.pipeline != None:
                        nextPipeline = PipeLine(ret.pipeline)
                    nextPipeline.run(ret.startSession)
                    if ret.breakCurrent:
                        return False
                # 返回多个值
                if isinstance(ret, tuple):
                    retval = ret[0]
                else:
                    retval = ret
                if retval == None:
                    retval = True
                if retval == False:
                    dcc.setColor(dcc.red)
                    print('  Session %s failed' % name)
                    if self.breakonerror:
                        print('    PipeLine quit.')
                        break
                    dcc.setColor(dcc.reset)
                else:
                    dcc.setColor(dcc.green)
                    print('  session %s success' % name)
                    dcc.setColor(dcc.reset)
            except Exception, e:
                retval = False
                dcc.setColor(dcc.red)
                print('  Session %s failed.' % name)
                dcc.setColor(dcc.reset)
                dcc.setColor(dcc.yellow)
                print(e)
                dcc.setColor(dcc.reset)
                if self.breakonerror:
                    print('    PipeLine quit.')
                    break
        dcc.setColor(dcc.blue)
        print('finish module %s tests.' % self.moduleName)
        dcc.setColor(dcc.reset)
        return retval


class Goto(object):
    def __init__(self, sessionName, pipeline=None, breakCurrent=True):
        self.startSession = sessionName
        self.pipeline = pipeline
        self.breakCurrent = breakCurrent
