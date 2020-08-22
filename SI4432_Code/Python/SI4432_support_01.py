# -*- coding: utf-8 -*-
##from __future__ import unicode_literals   # program crashes !!!!


"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import hex
from builtins import chr
from builtins import range
from builtins import object
"""
from past.utils import old_div
_Version_Text = [
[ 1.0 , '01-08-2020', 'Stef Mientki',
'Test Conditions:', (),
"""
Python 3.7.8
  - timer removed
"""],


[ 0.1 , '31-10-2014', 'Stef Mientki',
'Test Conditions:', (),
"""
Initial Release
"""]
]

import __init__

import os
My_Path     = os.getcwd ()
print(My_Path)

from   General_Globals import Application
from   file_support    import File_Exists
from   inifile_support import inifile
from   dialog_support  import AskYesNo, Show_Message

import Base_GUI
#from   xlwings         import  Workbook, Range, Sheet
from   remote_support  import callLater, CallLater
from   serial_support   import *
from   datetime        import datetime as dt


#import PySide

import sys
"""
if 'PyQt4' in sys.modules:   ## this will force pyqtgraph to use PySide instead of PyQt4
  qt = sys.modules.pop( 'PyQt4')

  import pyqtgraph as pg
  sys.modules['PyQt4'] = qt
else:
  import pyqtgraph as pg

##import pyqtgraph.Qt
"""
import traceback

import numpy as np
##import matplotlib.pyplot as plt   ##<<<<<<<<<< PROBLEMS AFTER BOD


from   os.path import isfile
import serial
#import time
from   time import sleep,time,clock
import webbrowser
import sys
from   gui_support_QT   import *
from   PySide2.QtCore   import QThread, Signal, QTimer, QObject
from   PySide2.QtCore   import QUrl

import queue
from PySide2 import QtGui


KILO = 1000
MEGA = 1000000

# *****************************************************************************
# *****************************************************************************
Description = {}
Description [ 0x00 ] = 'Device Type Code 01000'
Description [ 0x01 ] = 'Version Code 00110'
Description [ 0x02 ] = 'Device Status'
Description [ 0x03 ] = 'Interrupt Status 1'
Description [ 0x04 ] = 'Interrupt Status 2'
Description [ 0x05 ] = 'Interrupt Enable 1'
Description [ 0x06 ] = 'Interrupt Enable 2'
Description [ 0x07 ] = 'Operating Mode and Function Control 1'
Description [ 0x08 ] = 'Operating Mode and Function Control 2'
Description [ 0x09 ] = '30 MHz Crystal Oscillator Load Capacitance'
Description [ 0x0A ] = 'Microcontroller Output Clock'
Description [ 0x0B ] = 'GPIO Configuration 0'
Description [ 0x0C ] = 'GPIO Configuration 1'
Description [ 0x0D ] = 'GPIO Configuration 2'
Description [ 0x0E ] = 'IO-Port Configuration'
Description [ 0x0F ] = 'ADC Configuration'

Description [ 0x10 ] = 'ADC Sensor Amplifier Offset'
Description [ 0x11 ] = 'ADC Value'
Description [ 0x12 ] = 'Temperature Sensor Calibration'
Description [ 0x13 ] = 'Temperature Value Offset'
Description [ 0x14 ] = 'Wake-Up Timer Period 1'
Description [ 0x15 ] = 'Wake-Up Timer Period 2'
Description [ 0x16 ] = 'Wake-Up Timer Period 3'
Description [ 0x17 ] = 'Wake-Up Timer Value 1'
Description [ 0x18 ] = 'Wake-Up Timer Value 2'
Description [ 0x19 ] = 'Low Duty Cycle Mode Duration'
Description [ 0x1A ] = 'Low Battery Detector Treshold'
Description [ 0x1B ] = 'Battery Voltage Level'
Description [ 0x1C ] = 'IF Filter Bandwidth'
Description [ 0x1D ] = 'AFC Loop Gearshift Override 00xx xxxx?'
Description [ 0x1E ] = 'AFC Timing Control'
Description [ 0x1F ] = 'Clock Recovery Gearshift Override'

Description [ 0x20 ] = 'Clock Recovery Oversampling Rate'
Description [ 0x21 ] = 'Clock Recovery Offset 2'
Description [ 0x22 ] = 'Clock Recovery Offset 1'
Description [ 0x23 ] = 'Clock Recovery Offset 0'
Description [ 0x24 ] = 'Clock Recovery Timing Loop Gain 1'
Description [ 0x25 ] = 'Clock Recovery Timing Loop Gain 0'
Description [ 0x26 ] = 'RSSI Received Signal Strength Indicator'
Description [ 0x27 ] = 'RSSI Treshold for Clear Channel Indicator'
Description [ 0x28 ] = 'Antenna Diversity 1'
Description [ 0x29 ] = 'Antenna Diversity 2'
Description [ 0x2A ] = 'AFC Limiter'
Description [ 0x2B ] = 'AFC Correction (MSBs)'
Description [ 0x2C ] = 'OOK Counter Value 1'
Description [ 0x2D ] = 'OOK Counter Value 2'
Description [ 0x2E ] = 'Slicer Peak Holder'
Description [ 0x2F ] = 'Reserved'

Description [ 0x30 ] = 'Data Access Control (Packet handling)'
Description [ 0x31 ] = 'EZMAC status (Packet handling)'
Description [ 0x32 ] = 'Header Control 1'
Description [ 0x33 ] = 'Header Control 2'
Description [ 0x34 ] = 'Preamble Length'
Description [ 0x35 ] = 'Preamble Detection Control'
Description [ 0x36 ] = 'Sync Word 3'
Description [ 0x37 ] = 'Sync Word 2'
Description [ 0x38 ] = 'Sync Word 1'
Description [ 0x39 ] = 'Sync Word 0'

Description [ 0x44 ] = 'Header Enable 2'
Description [ 0x45 ] = 'Header Enable 1'
Description [ 0x46 ] = 'Header Enable 0'

Description [ 0x58 ] = 'Reserved ???'

Description [ 0x69 ] = 'AGC Override 1 (if bit5=1: reads LNA Gain)'

Description [ 0x6D ] = 'TX Power'
Description [ 0x6E ] = 'TX Data Rate 1'
Description [ 0x6F ] = 'TX Data Rate 0'

Description [ 0x70 ] = 'Modulation Mode Control 1'
Description [ 0x71 ] = 'Modulation Mode Control 2'

Description [ 0x75 ] = 'Frequency Band Select'
Description [ 0x76 ] = 'Nominal Carrier Frequency'
Description [ 0x77 ] = 'Nominal Carrier Frequency'

# *****************************************************************************


# *****************************************************************************
# *****************************************************************************
def My_Bin ( Value ) :
  x = bin ( 256 + Value )
  return x[3:7] + '  ' + x[7:]
def My_Hex ( Value ) :
  x = hex ( 256 + Value )
  return x[:2] + x[3:5].upper()
# *****************************************************************************


# *****************************************************************************
# *****************************************************************************
def BCD ( Value ) :
  return 10 * (( Value & 0xF0 ) >> 4 ) + ( Value & 0x0F )
# *****************************************************************************


#global CommPort 
CommPort = ''
# *****************************************************************************
# search for the correct CommPort
# *****************************************************************************
def Get_CommPort ( ID_String, Filename ) :
  global CommPort
  IniFile = inifile ( Filename )
  IniFile.Section = 'CommPort'
  _CommPort = IniFile.Read ( 'CommName', default = None )

  Found     = False
  if _CommPort :
    Found = Test_CommPort ( _CommPort, ID_String )

  if not Found :
    CommPorts = Get_CommPorts()
    print ( CommPorts ) 
    for _CommPort in CommPorts :
      print ( _CommPort )
      if Test_CommPort ( _CommPort, ID_String ) :
        print ( "CommPort Found: " + CommPort )
        break
    else :
      Show_Message ( "Couldn't find a CommPort with a (correct programmed) PIC connected" )
      sys.exit ()

  IniFile.Write ( 'CommName', _CommPort )
  IniFile.Close ()

  #global CommPort
  CommPort = _CommPort
  ##return _CommPort
# *****************************************************************************


# *****************************************************************************
# sleep() + update of the GUI after the timeout
# especially usefull in long term processes
# *****************************************************************************
def My_Sleep ( Seconds ) :
  QtCore.QCoreApplication.instance ().processEvents ()
  sleep ( Seconds )
  QtCore.QCoreApplication.instance ().processEvents ()


# *****************************************************************************
# *****************************************************************************
class MyThread (QThread):
  received = Signal(object)

  # *************************************************
  def run(self):
    self.ser = None
    self.Timer = QTimer()
    self.Timer.timeout.connect(self.update)
    self.Timer.start(1)   # was 5
    self.exec_()

  # *************************************************
  def update(self, *args):
    if not self.ser :
      return

    #print ( 'KKKKKKKKKKKKK', self.ser )
    n = self.ser.inWaiting() #look if there is more to read
    if n:
      text = self.ser.read ( n )
      #print(text)
      self.received.emit ( text )

  # *************************************************
  def Start_Stop_Comm ( self, Start, ID_String = "" ) :  #*args ) :
    ##Start = args[0]   # True = start CommPort,  False = Stop CommPort
    if Start :
      ##CMD  =  args[1]
      ##print 'OOOOOOOOOOO', sys.CommPort
      self.ser = ser = serial.Serial ( CommPort, baudrate = 115200 )
      ser.timeout = 5

      # release the reset pin (normally DTR, but on 3V3 RTS)
      ser.setDTR ( True )
      ser.setRTS ( True )
      #sleep ( 0.5 )
      sleep ( 0.1 )
      ser.flushInput()
      ser.setDTR ( False )
      ser.setRTS ( False )


      sleep ( 1.5 )    # 0.5 seconds is too short, 1 seems to be enough

      while self.ser.inWaiting() :
        text = self.ser.read ( self.ser.inWaiting() )
        print ( "flush:", text )
        sleep ( 0.1 )

      #ser.write ( CMD.encode('windows-1252') )
      #ser.write ( CMD )
      ser.write ( ID_String )

    else  :
      Temp = self.ser
      self.ser = None
      if Temp :
        Temp.close()


# *****************************************************************************
class MySignals(QObject):
  dataReceived = Signal()
  Start_Signal = Signal ( object, object )


# *****************************************************************************
class SI4432_Base ( object ):
  def __init__ ( self, IniFile = None ):
    self.RS232_bmps = ( 'blink_3.ico', 'blink_7.ico' )
    self.Registers_Header = [[ 'Address', 'Reset', 'PIC', 'Excel','PIC','Excel','Diff','Description' ]]
    self.Auto_Connect = True
    self.Auto_Init    = True
    self.Status       = 70


  def Post_Init ( self ) :
    self.Set_Busy ()
    self.Main_Window.Bind ( 'closeEvent', self._On_Exit )

    Bind = self.Main_Window.Bind
    Bind ( 'F1', self._On_Help )

    Image = os.path.join ( My_Path, self.RS232_bmps [ 0 ] )
    Image = 'vippi_bricks.png'
    self.RS232_Conn.SetImage ( Image    )
    self.RS232_Conn.setText  ( CommPort )

    try :
      self.NB.SetSelection ( 1 )
    except :
      pass    # not all programs have a NB

    self.Register_Data = np.array ( [], 'uint8' )
    self.Register_Status = [ 0x02, 0x03, 0x04, 0x07, 0x26, 0x28, 0x29, 0x36 ]

    self.Registers = []
    ##self.Registers.append ( self.Registers_Header )
    for i in range ( 130 ) :
      if i in Description : Desc = Description [i]
      else                : Desc = ''
      self.Registers.append ( [ My_Hex(i), '', '', '', '', '', '', Desc ])
    self.Registers [127 ]=    [ 'AA'  , '', '', '', '', '', '', 'Controle' ]
    self.Registers [128 ]=    [ 'BB'  , '', '', '', '', '', '', 'Controle' ]
    self.Registers [129 ]=    [ 'DD'  , '', '', '', '', '', '', 'Controle' ]

    try :
      self.Reg_Table.Fill_Data ( self.Registers_Header + self.Registers )
    except :
      pass    ## not all programs have a Reg_Table

    # *********************************************
    # THREADING
    # *********************************************
    self.q = queue.Queue()
    self.text = b''
    self.Signals = MySignals()

    self.Processing = False
    self.dataReceived = self.Signals.dataReceived
    self.dataReceived.connect(self._Process)


    self.Thread = MyThread()
    self.Thread.received.connect(self._AddQueue)#self.Update_Image)

    self.Start_Signal = self.Signals.Start_Signal
    self.Start_Signal.connect ( self.Thread.Start_Stop_Comm )

    self.Thread.start()
    # *********************************************

    ##self.Timer = QTimer()
    ##self.Timer.timeout.connect ( self._On_Timer )
    if self.Auto_Connect :
      self.Set_Busy ()
      print('{{{{{{{{{{{{{{{{{{{{')
      self.Timer_Action = 'Connect'
      ###FF NIE self.Timer.start ( 100 )
      
    ## ipv Timer hier Connect aanroepen  
    self._On_Connect ()

  '''# *************************************************************
  def _On_Timer ( self, event = None ) :
    print ( ">>>>>>>>>>>>>>>>>>   HIER MAG IE NIE KOME <<<<<<<<<<<<<<  " )
    if self.Timer_Action == 'Connect' :
      print ( "Action Connect", self.Status )
      self.Timer.stop ()
      self._On_Connect ()

      if self.Auto_Init :
        self.Timer_Action = 'Init'
        self.Timer.start ( 1500 )

    elif self.Timer_Action == 'Init' :
      print ( "Connecting Done", self.Status )
      self.Timer.stop ()
      self._On_Init ()

      """
    elif self.Timer_Action == 'PDF' :
      self.NB.SetSelection ( 0 )
      self.Timer.stop ()
      self.WebKit.load ( self.URL )
    """
    else :
      self.Timer.stop ()

    if not self.Timer.isActive () :
      self.Timer_Action = ''
'''

  # **********************************************************************
  def _On_Connect ( self, event = None ) :
    if self.Thread.ser :
      Image = 0
    else :
      Image = 1

    try :
      Conn_Text = ['Connect', 'Disconnect']
      self.Button_Connect.setText ( Conn_Text [ Image ] )
    except :
      pass   # NB is not available in all programs

    Image = os.path.join ( My_Path, self.RS232_bmps [ Image ] )
    self.RS232_Conn.SetImage (Image )
    self.Set_Busy ()

    if self.Thread.ser :
      self.Start_Signal.emit ( False, None )
      self.Status = 0
    else :
      print ( ">>>> HIER start staus 0xFF" ) ;
      self.Status = 71
      self.Start_Signal.emit ( True, self.ID_String )

    self.Register_Data = np.array ( [], 'uint8' )

  # *************************************************************
  def _AddQueue ( self, Data ) :
    self.q.put ( Data )
    self.dataReceived.emit()

  # *************************************************************
  def _Process(self):
    if self.Processing:
      ##print 'kom ik hier wel eens?'
      return
    self.Processing = True

    try:
      while True:
        self.text += self.q.get(False)
    except queue.Empty:
      pass

    while self.text:
      N = len ( self.text )
      Data = self.text [ : N ]
      self.text = self.text [ N: ]
      self._Update_Plot ( Data )

    self.Processing = False

  # *************************************************************
  def _Update_Plot ( self, Data ) :
    Values = np.frombuffer ( Data, 'uint8' )
    self.Register_Data = np.hstack (( self.Register_Data, Values ))
    print ( '>>>> PPLOT ', self.Status, len(self.Register_Data), len(Values), Values) #, self.Register_Data )

    # *************************************************************
    if self.Status == 70 :   # KOMT NIET MEER VOOR
      if len ( self.Register_Data ) >= 360:
        print ( "Status 0, gaat naar 1" ) #, Values, self.Register_Data )
        self.Register_Data = np.array ( [], 'uint8' )
# wat doet emit true        
#        self.Start_Signal.emit ( True,self.ID_String )
#        self.Start_Signal.emit ( False, self.ID_String )
        self.Status = 71

    # *************************************************************
    # Check is ID_String is returned
    # *************************************************************
    elif self.Status == 71 :
      if len ( self.Register_Data ) >= 3:
        print ( Values[:3] )   # >>>> PPLOT  71 3 3 [170 187 194]
        print ( "Status 1, gaat naar 3" ) #, Values, self.Register_Data )
        self.Register_Data = np.array ( [], 'uint8' )
        self.Status = 73



    # *************************************************************
    # Wait for Register Dump surrounded by AABBCC  and AABBDD
    # 127 registers will be send + 6 surrounding bytes = 133
    # *************************************************************
    elif self.Status == 0xFF :
      ##print '0xFF found', len ( self.Register_Data )
      #if len ( self.Register_Data ) >= 136:
      if len ( self.Register_Data ) >= 360:

        self._Completion_0xFF ()
        #self._Set_OK_Version ()

        self._On_Init()

        self.Status = 0
        self.Register_Data = np.array ( [], 'uint8' )
        self.Set_Busy ( False )
        

    # *************************************************************
    # Wait for Register Dump + AABBCC (soft reset)
    # *************************************************************
    elif self.Status in [ 0xF0, 0xF1 ] :
      print ('0xF0/F1 found: soft reset', len ( self.Register_Data ))
      if len ( self.Register_Data ) >= 133:

        self._Completion_0xF0 ()
        self._Set_OK_Version ()

        if self.Status == 0xF0 :
          self._On_Init()

        self.Status = 0
        self.Set_Busy ( False )
        self.Register_Data = np.array ( [], 'uint8' )


    # *************************************************************
    # Wait for OK-test of the SI4432
    # *************************************************************
    elif self.Status == 0xF2 :
      print ( '0xF2 OK-Test', len (self.Register_Data) )
      if len ( self.Register_Data  ) >= 1 :

        self._Set_OK ( self.Register_Data[0] )

        self.Status = 0
        self.Set_Busy ( False )
        self.Register_Data = np.array ( [], 'uint8' )

    else :
      print ( 'print  krijg iets anders >>>>>>>>>>>>>>>>>>>>>>>>>>' )






  # *************************************************************
  def _On_Init ( self, event = None ) :
    pass

  # *************************************************************
  def _Completion_0xF0 ( self ):
    pass

  # *************************************************************
  def _Completion_0xF3 ( self ):
    pass

  # *************************************************************
  def _Completion_0xFF ( self ):
    pass

  # *************************************************************
  def _Set_OK ( self, OK ) :
    print ( "_Set_OK", OK )
    if OK == 0x44 : Text = 'OK yes'
    else          : Text = 'OK no'
    self.Button_OK_Test.setText ( Text )
    Image = os.path.join ( My_Path, self.RS232_bmps [ OK == 0x44 ] )
    self.Button_OK_Test.SetImage ( Image )

  # *************************************************************
  def _Set_OK_Version ( self ) :
    self._Set_OK ( self.Register_Data[-5] )

    Title =  self.Main_Window.windowTitle()
    if '$$' in Title :
      Version = self.Register_Data[-4]
      Title = Title.replace ( '$$', '%i' % Version )
      self.Main_Window.setWindowTitle ( Title )

  # *************************************************************
  def Set_Busy ( self, On = True ) :
    Image = os.path.join ( My_Path, self.RS232_bmps [ not On ] )
    self.Button_Busy.SetImage (Image )
    QtCore.QCoreApplication.instance ().processEvents ()


  # *************************************************************
  # Loads the tabel from the Grid into self.Registers
  # clears the hex and bin column (either PIC or Excel) and the diff column
  # writes the result back to the grid
  # *************************************************************
  def Clear_Table ( self, PIC = True ) :
    if PIC : Col = 2
    else   : Col = 3

    self.Registers = self.Reg_Table.Get_Data ()

    for i in range ( len ( self.Registers ) ) :
      self.Registers [i] [Col  ] = ''
      self.Registers [i] [Col+2] = ''
      self.Registers [i] [6    ] = ''
    self.Reg_Table.Fill_Data ( self.Registers_Header + self.Registers )
    QtCore.QCoreApplication.instance ().processEvents ()


  # *************************************************************
  # Loads the tabel from the Grid into self.Registers
  # *************************************************************
  def Get_Table ( self ) :
    self.Registers = self.Reg_Table.Get_Data ()

  # *************************************************************
  # Loads the tabel from the Grid into self.Registers
  # *************************************************************
  def Set_Table ( self ) :
    self.Reg_Table.Fill_Data ( self.Registers_Header + self.Registers )

    self.Reg_Table.setColumnWidth ( 0, 50 )
    self.Reg_Table.setColumnWidth ( 1, 5  )
    self.Reg_Table.setColumnWidth ( 2, 50 )
    self.Reg_Table.setColumnWidth ( 3, 50 )
    self.Reg_Table.setColumnWidth ( 4, 70 )
    self.Reg_Table.setColumnWidth ( 5, 70 )
    self.Reg_Table.setColumnWidth ( 6, 50 )
    self.Reg_Table.setColumnWidth ( 7, 400 )

    ##self.Register_Data = np.array ( [], 'uint8' )
    QtCore.QCoreApplication.instance ().processEvents ()

  # *************************************************************
  def Write_Table ( self, Address, Value, Reset = True ) :
    if Reset : Col = 2
    else     : Col = 3

    self.Registers [ Address ] [ Col   ] = My_Hex ( Value )
    self.Registers [ Address ] [ Col+2 ] = My_Bin ( Value )

    if  self.Registers [ Address ] [2] and self.Registers [ Address ] [3] and\
      ( self.Registers [ Address ] [2]  != self.Registers [ Address ] [3] ) :
      self.Registers [ Address ] [6] = '***'
    else :
      self.Registers [ Address ] [6] = ''

  # *************************************************************
  def _On_Reset ( self, event = None ) :
    self.Set_Busy ()
    self.Status = 0xF0
    self.Thread.ser.write ( b'\xFA\xF0' )

  # *************************************************************
  def _On_All_Regs ( self, event = None ) :
    self.Set_Busy ()
    self.Status = 0xF1
    self.Thread.ser.write ( b'\xFA\xF1' )

  # *************************************************************
  def _On_OK_Test ( self, event = None ) :
    self.Set_Busy ()
    self.Status = 0xF2
    self.Thread.ser.write ( b'\xFA\xF2' )

  # **********************************************************************
  def _Send_Freq ( self, Value ) :
    ##print 'Set Start Frequency', Value
    self.Thread.ser.write ( b'\xFA\xB0' )
    sleep ( 1 )

    Data  = old_div(Value, (256 * 256 * 256 ))
    Value = Value % ( 256 * 256 * 256 )
    self.Thread.ser.write ( [ Data ] )

    Data  = old_div(Value, ( 256 * 256 ))
    Value = Value % ( 256 * 256 )
    self.Thread.ser.write ( [ Data ] )

    sleep ( 0.5 )
    Data  = old_div(Value, 256)
    Value = Value % 256
    self.Thread.ser.write ( [ Data  ] )
    self.Thread.ser.write ( [ Value ] )

  # **********************************************************************
  def _Send_kHz_Stepsize ( self, Value ) :
    print('Set Frequency Step', Value)
    self.Thread.ser.write ( b'\xFA\xAF' )
    sleep ( 1 )
    self.Thread.ser.write ( [ Value ] )

  # **********************************************************************
  def _On_X90 ( self, event = None ) :
    #self.Thread.ser.write ( b'\xFA' )
    #self.Thread.ser.write ( [0x90] )
    
    self.Thread.ser.write ( b'\xFA' )
    self.Thread.ser.write ( b'\xB2' )
 
  # **********************************************************************
  def _On_X91 ( self, event = None ) :
    self.Thread.ser.write ( b'\xFA' )
    self.Thread.ser.write ( [0x91] )
  # **********************************************************************
  def _On_X92 ( self, event = None ) :
    self.Thread.ser.write ( b'\xFA' )
    self.Thread.ser.write ( [0x92] )
  # **********************************************************************
  def _On_X93 ( self, event = None ) :
    self.Thread.ser.write ( b'\xFA' )
    self.Thread.ser.write ( [0x93] )
  # **********************************************************************
  def _On_X94 ( self, event = None ) :
    self.Thread.ser.write ( b'\xFA' )
    self.Thread.ser.write ( [0x94] )

  # **********************************************************************
  def _On_PDF ( self, event = None ) :
    #Convert to html:  https://www.pdfonline.com/convert-pdf-to-html/
    URL = "file:///AN440_registers.html"
    URL = "AN440_registers.html"
    URL = "file://AN440_registers.html"
    URL = "file:///home/stef/CWin/D/Data_Python_25/UHF_Spectrum_Analyzer_Py3/AN440_registers.html"
    URL = "file://" + os.path.abspath("AN440_registers.html")
    print ( ">>>>>>>>>>>>???????????", URL )
    try :
      self.WebKit.load ( QUrl ( URL ))
      self.NB.SetSelection ( 0 )
    except :
      webbrowser.open ( URL )

  # **********************************************************************
  def _On_Help ( self, event = None ) :
    URL = 'http://mientki.ruhosting.nl/data_www/raspberry/doc/%s' % self.Help_File
    try :
      self.WebKit2.load ( QUrl ( URL ))
      self.NB.SetSelection ( 2 )
    except :
      webbrowser.open ( URL )

  # **********************************************************************
  def _On_Exit ( self, event = None ) :
    # to release the serial Comm port
    #if self.Thread.ser :
    #  self.Thread.ser.close()
    self.Start_Signal.emit ( False, None )
    My_Sleep ( 0.3 )
    self.Thread.quit()

# *****************************************************************************
# *****************************************************************************
if __name__ == '__main__':
  #Get_CommPort ( "CommPorts.cfg" )
  Get_CommPort (  b'\xAA\xBB\xC1', "CommPorts.cfg" )
