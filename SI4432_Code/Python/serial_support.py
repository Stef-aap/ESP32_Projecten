from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import hex
#!/usr/bin/env python
import __init__


_Version_Text = [

[ 0.2 , '6-8-2020', 'Stef Mientki',
'Test Conditions:', (),"""
Test_CommPort gewijzigd, send ID_String en verwacht dezelfde terug
"""],

[ 0.1 , '6-10-2014', 'Stef Mientki',
'Test Conditions:', (),"""

# from: serial.tools.list_ports

"""]
]

from   time   import sleep
import serial


# ***********************************************************************
# chose an implementation, depending on os
#~ if sys.platform == 'cli':
#~ else:
# ***********************************************************************
import os
# chose an implementation, depending on os
if os.name == 'nt': #sys.platform == 'win32':
    from serial.tools.list_ports_windows import *
elif os.name == 'posix':
    from serial.tools.list_ports_posix import *
#~ elif os.name == 'java':
else:
    raise ImportError("Sorry: no implementation for your platform ('%s') available" % (os.name,))


# ***********************************************************************
# ***********************************************************************
def Get_CommPorts () :
  iterator = sorted(comports())
  Result = []
  for port, desc, hwid in iterator:
    Result.append ( port )
  return Result


# ***********************************************************************
# ***********************************************************************
def Test_CommPort ( Port, ID_String, Command = "" ) :
  ser = None
  try :
    ser = serial.Serial ( Port, baudrate = 115200 )
    #print("CCCCConnnected Port" + Port + "   CMD=" + Command )
    ser.timeout = 5
    ser.flushInput()

    # release the reset pin (normally DTR, but on 3V3 RTS)
    ser.setDTR ( False )
    ser.setRTS ( False )

    if Command :
      ser.write ( Command )

    N        = 0
    NSeconds = 0
    NSec_Max = 20
    print('polling ', end=' ')
    while N < 300 and NSeconds < NSec_Max:
      print('.', end=' ')
      n = ser.inWaiting() #look if there is more to read
      if n:
        N += n
        text = ser.read ( n )
        #print ( '>>>>', n, text )
        #print ( type(ID_String), ID_String )
        if ID_String in text :
          print('Found Comm-Port:', Port)
          ser.close ()
          return True
        else :
          ser.write ( ID_String )   # <<<<< extra
          N = 0 
          #print ( "ReTry ID_String") 
        
      sleep (0.5)
      NSeconds += 1

    if NSeconds >= NSec_Max :
      print('NOT Found Comm-Port:', Port)
      ser.close ()

  except :
    traceback.print_exc ()
    print ( "Failed to connect CommPort=" + Port + "   CMD=" + Command )
    if ser :
      ser.close ()


# *****************************************************************************
from gui_support_QT import *
import queue
from PySide2.QtCore import QThread, Signal, QTimer, QObject
CommPort = "COM6"
# *****************************************************************************
class Serial_Receive_Thread (QThread):
  received = Signal(object)

  # *************************************************
  def run(self):
    self.ser = ser = serial.Serial ( CommPort, baudrate = 115200 )

    # release the reset pin (normally DTR, but on 3V3 RTS)
    """
    ser.setDTR ( True )
    ser.setRTS ( True )
    sleep ( 0.1 )
    ser.flushOutput()
    ser.setDTR ( False )
    ser.setRTS ( False )
    """

    sleep(1)
    n = self.ser.inWaiting() #look if there is more to read
    print('XCXCXC', n, repr(self.ser.read ( n )))

    ser.flushInput()
    ser.timeout = 5

    self.Timer = QTimer()
    self.Timer.timeout.connect(self.update)
    self.Timer.start(1)   # was 5
    print('SENNNNNNN')
    self.exec_()

  # *************************************************
  def update(self, *args):
    n = self.ser.inWaiting() #look if there is more to read
    print('update', n, end=' ')
    if n:
      print('update', n, end=' ')
      text = self.ser.read ( n )
      ##print repr(text)
      self.received.emit ( text )

# *****************************************************************************
class MySignals(QObject):
  dataReceived = Signal()

# *****************************************************************************
class Serial_Thread_Class ( QObject ) :
  def __init__ ( self ) :

    # *********************************************
    # THREADING
    # *********************************************
    self.q = queue.Queue()
    self.text = ''
    self.Signals = MySignals()

    self.Processing = False
    self.dataReceived = self.Signals.dataReceived
    self.dataReceived.connect(self._Process)

    self.Thread = Serial_Receive_Thread()
    self.Thread.received.connect(self._AddQueue)#self.Update_Image)
    self.Thread.start()
    print('started')
   # *********************************************

  # *************************************************************
  def _AddQueue ( self, Data ) :
    print('data', data)
    self.q.put ( Data )
    self.dataReceived.emit()

  # *************************************************************
  def _Process(self):
    if self.Processing:
      print('kom ik hier wel eens?')
      return
    self.Processing = True

    try:
      while True:
        self.text += self.q.get(False)
        print('::', self.Text)
    except queue.Empty:
      pass

    self.Processing = False

# ***********************************************************************
if __name__ == '__main__':
  """
  CommPorts = Get_CommPorts()

  ID_String = '\xAA\xBB\xCC'
  for Port in CommPorts [-1:] :
    print Port, Test_CommPort ( Port, ID_String )
  #"""



  """
  if True :
    ser = serial.Serial ( 'COM6', baudrate = 115200 )
    ser.timeout = 2

    ser.setRTS ( True )
    ser.setRTS ( False )

    sleep ( 2 )
    ser.flushInput ()

    ser.write ( 'AT\r\n' )
    sleep ( .2 )
    n = ser.inWaiting ()
    print '111', n
    print '222', ser.read ( n )
    ser.close ()

  else :
    Serial_Thread = Serial_Thread_Class ()
    sleep(5)
    Serial_Thread.Thread.ser.write ( r'AT\r\n' )
    print 'write'
    ##print dir ( Serial_Thread )
    sleep (5)
    n = Serial_Thread.Thread.ser.inWaiting() #look if there is more to read
    print 'update', n, Serial_Thread.Thread.ser.read ( n )
"""

  if True :
    ser = serial.Serial ( 'COM3', baudrate = 115200 )
    ser.timeout = 2

    ser.setRTS ( True )
    ser.setRTS ( False )

    sleep ( 2 )
    ser.flushInput ()

    ser.write ( '\xA2' )
    sleep ( 2 )
    n = ser.inWaiting ()
    print('111', n)
    Line = ser.read ( n )
    for kar in Line :
      print(hex ( ord ( kar ) ), end=' ')
    ser.close ()

