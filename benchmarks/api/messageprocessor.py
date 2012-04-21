# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# Copyright (C) 2011
# Yang Lu
# http://www.cs.brown.edu/~yanglu/
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# -----------------------------------------------------------------------
import execnet
import logging
from message import *

LOG = logging.getLogger(__name__)

class MessageProcessor:
    ''' Message Processor'''
    def __init__(self, channel):
        self._channel = channel
        self._worker = None
        self._config = None
        
    def createWorker(self):
        '''Worker factory method'''
        benchmark = self._config['benchmark']
        fullName= benchmark.title()+"Worker"
        moduleName = 'benchmarks.%s.%s' % (benchmark.lower(), fullName.lower())
        moduleHandle = __import__(moduleName, globals(), locals(), [fullName])
        klass = getattr(moduleHandle, fullName)
        return klass()
        
    def processMessage(self):
        '''Main loop'''
        for item in self._channel:
            msg = getMessage(item)
            LOG.info("Incoming Message: %s" % getMessageName(msg.header))
            if msg.header == MSG_CMD_INIT :
                self._config = msg.data
                self._worker = self.createWorker()
                self._worker.initialize(self._config, self._channel, msg)
            elif msg.header == MSG_CMD_LOAD :
                self._worker.startLoading(self._config, self._channel, msg)
            elif msg.header == MSG_CMD_EXECUTE :
                self._worker.startExecution(self._config, self._channel, msg)
            elif msg.header == MSG_CMD_STOP :
                pass
            elif msg.header == MSG_EMPTY :
                pass
            else:
                LOG.warn("Unexpected message type")
                return
    ## DEF

if __name__ == '__channelexec__':
    mp = MsgProcessor(channel)
    mp.processMessage()