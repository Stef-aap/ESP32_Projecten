#from __future__ import division
#from __future__ import print_function
#from future import standard_library
#standard_library.install_aliases()
#from builtins import str
#from past.utils import old_div
#from builtins import object
#-------------------------------------------------------------------------------
# Name:        Remote Python Support
# Purpose:     Some usefull tools for execnet (remote python)
#
# Author:      Robbert Mientki
#
# Created:     17-12-2010
# Copyright:   (c) Robbert 2010
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

TempVarUnique = 1


def GetProxyObjectTemp():
  global TempVarUnique
  TempVar = 'ProxyObjectTempVar'+str(TempVarUnique)
  TempVarUnique += 1
  return TempVar



class ProxyObject(object):
  def __init__(self,Name):
    #print '_Proxyinit'
    # retreive some basic parameters of the object
    self.____Name = Name
  def __call__(self,*args,**kwargs):
    if self.____Name.endswith('__nonzero__'):
      ex = """
try:
  main_channel.send(bool({ObjectName}))
except:
  main_channel.send('')
  import traceback
  traceback.print_exc ()
  """.strip().format(ObjectName = self.____Name[:-len('__nonzero__')-1])
      ProxyObjectChannel.send(ex)
      return ProxyObjectChannelReceive()
    if self.____Name.endswith('__unicode__'):
      ex = """
try:
  main_channel.send(unicode({ObjectName}))
except:
  main_channel.send('')
  import traceback
  traceback.print_exc ()
print unicode({ObjectName})
  """.strip().format(ObjectName = self.____Name[:-len('__unicode__')-1])
      ProxyObjectChannel.send(ex)
      return ProxyObjectChannelReceive()
    if self.____Name.endswith('__len__'):
      ex = """
try:
  main_channel.send(len({ObjectName}))
except:
  main_channel.send('')
  import traceback
  traceback.print_exc ()
print unicode({ObjectName})
  """.strip().format(ObjectName = self.____Name[:-len('__len__')-1])
      ProxyObjectChannel.send(ex)
      return ProxyObjectChannelReceive()
    if self.____Name.endswith('__eq__'):
      if isinstance(args[0],ProxyObject):
        arg = args[0].____Name
      else:
        arg = repr(args[0])

      ex = """
try:
  main_channel.send({ObjectName}=={arg})
except:
  main_channel.send('')
  import traceback
  traceback.print_exc ()
  """.strip().format(ObjectName = self.____Name[:-len('__eq__')-1], arg = arg)
      ProxyObjectChannel.send(ex)
      return ProxyObjectChannelReceive()

    TempVar = GetProxyObjectTemp()
    line = TempVar +' = ' + self.____Name + '('
    for arg in args:
      if isinstance(arg,ProxyObject):
        line += arg.____Name + ', '
      else:
        line += repr(arg) + ', '
    for key,value in list(kwargs.items()):
      if isinstance(value,ProxyObject):
        line += key + '=' + value.____Name + ', '
      else:
        line += key + '=' + repr(arg) + ', '
    line += ')'
    ProxyObjectChannel.send(line)
    if self.____Name.endswith('__str__') or self.____Name.endswith('__repr__') :
      ex="""
try:
  main_channel.send({TempVar})
except:
  main_channel.send('')
  import traceback
  traceback.print_exc ()
""".strip().format(TempVar = TempVar)
      ProxyObjectChannel.send(ex)
      return ProxyObjectChannelReceive()  ## Not so dangerous
      #ProxyObjectChannel.send('main_channel.send('+TempVar+')')
      #return ProxyObjectChannelReceive() ## Dangerous
    return ProxyObject(TempVar)

  def __repr__(self): return self.__getattr__('__repr__')()
  def __str__(self) : return self.__getattr__('__str__')()
  def __unicode__(self) : return self.__getattr__('__unicode__')()
  def __bool__(self) : return self.__getattr__('__nonzero__')()
  def __eq__(self,*args,**kwargs) : return self.__getattr__('__eq__')(*args,**kwargs)
  def __len__(self,*args,**kwargs) : return self.__getattr__('__len__')(*args,**kwargs)

  def __iter__(self):
    TempVar = GetProxyObjectTemp()
    ex = """
try:
  {TempVar} = iter({ObjectName})
  main_channel.send('Ok')
except:
  main_channel.send('')
  import traceback
  traceback.print_exc ()
""".strip().format(TempVar = TempVar, ObjectName = self.____Name)
    ProxyObjectChannel.send(ex)
    result = ProxyObjectChannelReceive()
    if not result: return None

    class a(object):
      def __init__(self,Name):
        self.Name = Name

      def __iter__(self):
        return self
      def __next__(self):
        TempVar = GetProxyObjectTemp()

        ex = """
try:
  {TempVar} = {Iter}.next()
  main_channel.send('Ok')
except:
  main_channel.send('')
  import traceback
  traceback.print_exc ()
""".strip().format(TempVar = TempVar, Iter = self.Name)
        ProxyObjectChannel.send(ex)
        result = ProxyObjectChannelReceive()
        if result:
          return ProxyObject(TempVar)
        else:
          from exceptions import StopIteration
          raise StopIteration


    return a(TempVar)



  def __getattr__(self,Name):
    #print '>>',Name
    if Name.startswith('_ProxyObject____'):
      #print 'HEY'
      return object.__getattr__(self,Name)
    return ProxyObject(self.____Name + '.' + Name)

  def __setattr__(self,Name,Value):
    #print '<<',Name
    if Name.startswith('_ProxyObject____'):
      #print 'hey2'
      object.__setattr__(self,Name,Value)
      return
    TempVar = GetProxyObjectTemp()
    line = self.____Name + '.'+ Name + ' = '
    if isinstance(Value,ProxyObject):
      line += Value.____Name
    else:
      line += repr(Value)
    ProxyObjectChannel.send(line)
    return ProxyObject(TempVar)


  def __setitem__(self,key,Value):
    #TempVar = GetProxyObjectTemp()
    line = self.____Name + '['
    if isinstance(key,ProxyObject):
      line += key.____Name
    else:
      line += repr(key)
    line += '] = '
    if isinstance(Value,ProxyObject):
      line += Value.____Name
    else:
      line += repr(Value)
    ProxyObjectChannel.send(line)
    #return ProxyObject(TempVar)




## _CallbackEventHandler: Copied from IEP, License?, Source?
try:
  from queue import Queue, Empty
except:
  from queue import Queue, Empty
#import PySide2.QtCore as QtCore
from   PySide2.QtCore   import QThread, Signal, QTimer, QObject, QEvent
import PySide2.QtGui  as QtGui

#class _CallbackEventHandler(QtCore.QObject):
class _CallbackEventHandler(QObject):
    """ Helper class to provide the callLater function.
    """

    def __init__(self):
        #QtCore.QObject.__init__(self)
        QObject.__init__(self)
        self.queue = Queue()
        self.Lock = False

    def customEvent(self, event):
      #if self.Lock==False:  ## Should be atomic
      #  self.Lock = True
        while True:
            ##print '1'
            try:
                callback, args = self.queue.get_nowait()
            except Empty:
                break
            try:
                #print 'callback'
                callback(*args)
                #print 'callbackend'
            except Exception as why:
                print('callback failed: {0}:\n{1}'.format(callback, why))

       # self.Lock = False

    def postEventWithCallback(self, callback, *args):
        self.queue.put((callback, args))
        #QtGui.qApp.postEvent(self, QtCore.QEvent(QtCore.QEvent.User))
        QtGui.qApp.postEvent(self, QEvent(QEvent.User))

def callLater(callback, *args):
    """ callLater(callback, *args)
    Post a callback to be called in the main thread.
    """
    _callbackEventHandler.postEventWithCallback(callback, *args)

# Create callback event handler instance and insert function in IEP namespace
_callbackEventHandler = _CallbackEventHandler()



def CallLater(delay, callback, *args):
  from time import sleep
  sleep(old_div(delay, 1000.0))
  callLater(callback,*args)