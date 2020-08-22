# -*- coding: utf-8 -*-
##from __future__ import unicode_literals   # program crashes !!!!


_Version_Text = [
[ 0.2 , '...2014', 'Stef Mientki','Test Conditions:', (),
"""
- On startup, the reset value of the PIC is read
"""],

[ 0.1 , '16-10-2014', 'Stef Mientki','Test Conditions:', (),
"""
Initial Release
"""]
]

import __init__

import os
My_Path     = os.getcwd ()
print (My_Path)

from   General_Globals import Application
from   file_support    import File_Exists
from   inifile_support import inifile
from   dialog_support  import AskYesNo, Show_Message
import Base_GUI
from   xlwings         import  Workbook, Range, Sheet
from   remote_support  import callLater, CallLater
from   copy            import copy

KILO = 1000
MEGA = 1000000


Programs = """
(F0) SI4432_Spectrum_Analyzer
(F1) SI4432_Stream_Viewer
(F2) SI4432 after Init from Excel
(F3) SI4432 after Reset
(F5) SI4432_OOK_Transmit
(F5) SI4432_Interactive_Viewer
(F6) SI4432_UHF Generator
(F7) SI4432 WS3000 Receiver
"""
Programs = Programs.splitlines ()[1:]


# *****************************************************************************
# *****************************************************************************
Registers_OOK_Rx = {}
Registers_OOK_Rx [ 0x06 ] = 'B82'
Registers_OOK_Rx [ 0x07 ] = 'B83'
Registers_OOK_Rx [ 0x0B ] = 'B84'
Registers_OOK_Rx [ 0x0C ] = 'B85'
Registers_OOK_Rx [ 0x0D ] = 'B86'

Registers_OOK_Rx [ 0x1C ] = 'L68'
Registers_OOK_Rx [ 0x1D ] = 'L59'
Registers_OOK_Rx [ 0x1F ] = 'L78'

Registers_OOK_Rx [ 0x20 ] = 'L69'
Registers_OOK_Rx [ 0x21 ] = 'L70'
Registers_OOK_Rx [ 0x22 ] = 'L71'
Registers_OOK_Rx [ 0x23 ] = 'L72'
Registers_OOK_Rx [ 0x24 ] = 'L73'
Registers_OOK_Rx [ 0x25 ] = 'L74'
#Registers_OOK_Rx [ 0x2C ] = 'L75'
#Registers_OOK_Rx [ 0x2D ] = 'L76'
Registers_OOK_Rx [ 0x2E ] = 'L77'

#Registers_OOK_Rx [ 0x58 ] = ''
Registers_OOK_Rx [ 0x69 ] = 'L79'
#Registers_OOK_Rx [ 0x6E ] = 'L34'
#Registers_OOK_Rx [ 0x6F ] = 'L35'

Registers_OOK_Rx [ 0x70 ] = 'L36'
Registers_OOK_Rx [ 0x71 ] = 'L44'
Registers_OOK_Rx [ 0x75 ] = 'L24'
Registers_OOK_Rx [ 0x76 ] = 'L25'
Registers_OOK_Rx [ 0x77 ] = 'L26'


# *****************************************************************************
Registers_OOK_Tx = copy ( Registers_OOK_Rx )

Registers_OOK_Tx [ 0x06 ] = 'B93'
Registers_OOK_Tx [ 0x07 ] = 'B94'
Registers_OOK_Tx [ 0x0B ] = 'B95'
Registers_OOK_Tx [ 0x0C ] = 'B96'
Registers_OOK_Tx [ 0x0D ] = 'B97'

Registers_OOK_Tx [ 0x2A ] = 'E92'
Registers_OOK_Tx [ 0x2C ] = 'E93'
Registers_OOK_Tx [ 0x2D ] = 'E94'
Registers_OOK_Tx [ 0x2E ] = 'E95'

Registers_OOK_Tx [ 0x30 ] = 'E97'
Registers_OOK_Tx [ 0x32 ] = 'E98'
Registers_OOK_Tx [ 0x33 ] = 'E99'
Registers_OOK_Tx [ 0x34 ] = 'E100'
Registers_OOK_Tx [ 0x35 ] = 'E101'
Registers_OOK_Tx [ 0x36 ] = 'E102'
Registers_OOK_Tx [ 0x37 ] = 'E103'
Registers_OOK_Tx [ 0x38 ] = 'E104'
Registers_OOK_Tx [ 0x39 ] = 'E105'

Registers_OOK_Tx [ 0x6E ] = 'E122'
Registers_OOK_Tx [ 0x6F ] = 'E123'

Registers_OOK_Tx [ 0x72 ] = 'E127'

# *****************************************************************************
"""
Registers_FSK_Rx = copy ( Registers_OOK_Rx )

Registers_FSK_Rx [ 0x06 ] = 'B102'
Registers_FSK_Rx [ 0x07 ] = 'B103'
Registers_FSK_Rx [ 0x0B ] = 'B104'
Registers_FSK_Rx [ 0x0C ] = 'B105'
Registers_FSK_Rx [ 0x0D ] = 'B106'
"""


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
# search for the correct CommPort
# *****************************************************************************
from   serial_support   import *
Filename = Base_GUI.Create_IniFileName ()
IniFile = inifile ( Filename )
IniFile.Section = 'CommPort'
CommPort = IniFile.Read ( 'CommName', default = None )

ID_String = '\xAA\xBB\xCC'
Found     = False
if CommPort :
  Found = Test_CommPort ( CommPort, ID_String )

if not Found :
  CommPorts = Get_CommPorts()
  for CommPort in CommPorts :
    if Test_CommPort ( CommPort, ID_String ) :
      break
  else :
    Show_Message ( "Couldn't find a CommPort with a (correct programmed) PIC connected" )
    exit ()

IniFile.Write ( 'CommName', CommPort )
IniFile.Close ()
# *****************************************************************************


import PySide

import sys
if 'PyQt4' in sys.modules:   ## this will force pyqtgraph to use PySide instead of PyQt4
  qt = sys.modules.pop( 'PyQt4')

  import pyqtgraph as pg
  sys.modules['PyQt4'] = qt
else:
  import pyqtgraph as pg

import traceback
import pyqtgraph.Qt
##print pyqtgraph.Qt.USE_PYSIDE

import numpy as np
import matplotlib.pyplot as plt   ##<<<<<<<<<< PROBLEMS AFTER BOD


from   os.path import isfile
import serial
#import time
from   time import sleep,time,clock
import webbrowser
import sys
from   gui_support_QT import *
from   PySide.QtCore import QThread, Signal, QTimer, QObject
from   PySide.QtCore      import QUrl


# *****************************************************************************
# sleep() + update of the GUI after the timeout
# especially usefull in long term processes
# *****************************************************************************
def My_Sleep ( Seconds ) :
  QtCore.QCoreApplication.instance ().processEvents ()
  sleep ( Seconds )
  QtCore.QCoreApplication.instance ().processEvents ()


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

    n = self.ser.inWaiting() #look if there is more to read
    if n:
      text = self.ser.read ( n )
      self.received.emit ( text )

  # *************************************************
  def Start_Stop_Comm ( self, *args ) :
    Start = args[0]
    if Start :
      CMD  =  args[1]
      self.ser = ser = serial.Serial ( CommPort, baudrate = 115200 )
      ser.timeout = 5

      # release the reset pin (normally DTR, but on 3V3 RTS)
      ser.setDTR ( True )
      ser.setRTS ( True )
      sleep ( 0.5 )
      ser.flushInput()
      ser.setDTR ( False )
      ser.setRTS ( False )

      sleep ( 1.5 )    # 0.5 seconds is too short, 1 seems to be enough

      print ( 'CMD', repr(CMD) )
      ser.write ( CMD )

    else  :
      Temp = self.ser
      self.ser = None
      Temp.close()


# *****************************************************************************
class MySignals(QObject):
  dataReceived = Signal()
  Start_Signal = Signal(object,object)


import Queue
from PySide import QtGui

# *****************************************************************************
class Stream_Viewer ():
  def __init__ ( self, IniFile = None ):

    Title = 'JAL:   SI-4432 Register Viewer  (version %s)' % _Version_Text[0][0]

    self.Modulations = 'OOK-Rx,OOK-Tx,FSK-Rx,FSK-Tx,GFSK-Rx,GFSK-Tx'.split(',')

    GUI = """
  self.Main_Window ,MainWindow  ,label = Title
    self.Splitter        ,X ,SplitterHor
      PanelVer
        Radio_Program        ,RadioBox  ,label='Project (Read SI4432)'  ,choices = Programs, bind=self._On_Radio_Program
        PanelHor
          Button  ,label= '0x90'     ,bind = self._On_X90
          Button  ,label= '0x91'     ,bind = self._On_X91
          Button  ,label= '0x92'     ,bind = self._On_X92
          Button  ,label= '0x93'     ,bind = self._On_X93
          Button  ,label= '0x94'     ,bind = self._On_X94
        PanelHor
          self.RS232_Conn    ,Button  ,label = '???'
          Button                 ,label= 'PDF-File'      ,bind = self._On_PDF
          Button                 ,label= 'Help-File'     ,bind = self._On_Help
          Button                 ,label= 'Clear'         ,bind = self._On_Clear
          Button                 ,label= 'Save'          ,bind = self._On_Save
        self.Radio_Modulation  ,RadioBox,label='Modulation'   ,choices = self.Modulations, bind=self._On_Radio_Modulation
        TextCtrl
      self.Splitter2       ,SplitterHor
        self.Reg_Table       ,Table
        self.NB              ,Notebook
          self.WebKit          ,X, Webkit  ,label = 'Registers'
          self.Memo_Code       ,TextCtrl   ,label = 'JAL code'
          self.WebKit2         ,Webkit     ,label = 'Help Page'

    """
    self.wxGUI = Create_GUI ( GUI , IniFile, Icon = 'vippi_bricks.png' )
    ##self.Main_Window.Bind ( 'closeEvent', self._On_Exit )
    self.Memo_Code.moveCursor ( QtGui.QTextCursor.End )
    self.RS232_Conn.setText ( CommPort )

    # for some unknown reason the PDF view will only start after a second time
    # so here's the first time
    self._On_PDF ()

    self.RS232_bmps = ( 'blink_3.ico', 'blink_7.ico' )
    Image = os.path.join ( My_Path, self.RS232_bmps [ 0 ] )
    self.RS232_Conn.SetImage (Image )

    print ( dir(self.wxGUI.GUI) )
    self.Radio_Program =  self.wxGUI.p_locals [ 'Radio_Program' ]
    print (' piep')

    self.Register_Data = np.array ( [], 'uint8' )

    self.Registers = []
    self.Registers_Header = [[ 'Address', 'Reset', 'PIC', 'Excel','PIC','Excel','Diff','Description' ]]
    ##self.Registers.append ( self.Registers_Header )
    for i in range ( 131 ) :
      if i in Description : Desc = Description [i]
      else                : Desc = ''
      self.Registers.append ( [ My_Hex(i), '', '', '', '', '', '', Desc ])
    self.Registers [128 ]=    [ 'AA'  , '', '', '', '', '', '', 'Controle' ]
    self.Registers [129 ]=    [ 'BB'  , '', '', '', '', '', '', 'Controle' ]
    self.Registers [130 ]=    [ 'CC'  , '', '', '', '', '', '', 'Controle' ]

    self.Reg_Table.Fill_Data ( self.Registers_Header + self.Registers )
    ##for Col in range ( 5 ) :
    ##  self.Reg_Table.setColumnWidth ( Col, 40 )


    # *********************************************
    # THREADING
    # *********************************************
    self.q = Queue.Queue()
    self.text = ''
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

    # *********************************************
    # Start getting the reset values
    # *********************************************
    self.Reset_Registers = True
    self.Radio_Program.SetValue ( 3 )
    self._On_Radio_Program ()

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
    except Queue.Empty:
      pass

    while self.text:
      #if len(self.text) <= 40:
      #  break

      N = len ( self.text )
      Data = self.text [ : N ]
      self.text = self.text [ N: ]
      self._Update_Plot ( Data )

    self.Processing = False

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
    self.Reg_Table.setColumnWidth ( 1, 50 )
    self.Reg_Table.setColumnWidth ( 2, 50 )
    self.Reg_Table.setColumnWidth ( 3, 50 )
    self.Reg_Table.setColumnWidth ( 4, 70 )
    self.Reg_Table.setColumnWidth ( 5, 70 )
    self.Reg_Table.setColumnWidth ( 6, 50 )
    self.Reg_Table.setColumnWidth ( 7, 400 )

    QtCore.QCoreApplication.instance ().processEvents ()

  # *************************************************************
  def Write_Table ( self, Address, Value, PIC = True ) :
    if PIC : Col = 2
    else   : Col = 3

    self.Registers [ Address ] [ Col   ] = My_Hex ( Value )
    self.Registers [ Address ] [ Col+2 ] = My_Bin ( Value )

    if  self.Registers [ Address ] [2] and self.Registers [ Address ] [3] and\
      ( self.Registers [ Address ] [2]  != self.Registers [ Address ] [3] ) :
      self.Registers [ Address ] [6] = '***'
    else :
      self.Registers [ Address ] [6] = ''


  # *************************************************************
  def _Update_Plot ( self, Data ) :
    ##print '<<<', Data
    Values = np.frombuffer ( Data, 'uint8' )
    self.Register_Data = np.hstack (( self.Register_Data, Values ))

    ##print '>>>',len (self.Register_Data)
    if len ( self.Register_Data ) >= 134:
      self.Start_Signal.emit ( False, None )

      Image = os.path.join ( My_Path, self.RS232_bmps [ 0 ] )
      self.RS232_Conn.SetImage (Image )

      ID_String = '\xAA\xBB\xCC'
      print ( len (self.Register_Data) )

      if not self.Reset_Registers :
        self.Clear_Table ( PIC = True )
        for Address, Value in enumerate ( self.Register_Data[3:134] ) :
          self.Write_Table ( Address, Value, PIC = True )
      else :
        for Address, Value in enumerate ( self.Register_Data[3:134] ) :
          self.Registers [ Address ] [ 1 ] = My_Hex ( Value )

      self.Set_Table ()
      self.Register_Data = np.array ( [], 'uint8' )

  # **********************************************************************
  def _On_Radio_Program ( self, event = None ) :
    Radio = self.Radio_Program.GetValue()
    print ( 'Transmit :', repr('\xFB') + repr(chr ( 0xF0 + Radio )) )
    self.Start_Signal.emit ( True, '\xFB'+ chr ( 0xF0 + Radio ) )

    Image = os.path.join ( My_Path, self.RS232_bmps [ 1 ] )
    self.RS232_Conn.SetImage (Image )
    QtCore.QCoreApplication.instance ().processEvents ()

    self.Reset_Registers = Radio == 3
    print ( 'self Reset', self.Reset_Registers )

    if not self.Reset_Registers :
      x = self.Reg_Table.Get_Data ()
      for i in range ( len ( x ) ) :
        x[i][2] = ''
        x[i][4] = ''
        x[i][6] = ''
      self.Registers = [ self.Registers[0] ] + x
      self.Reg_Table.Fill_Data ( self.Registers )

  # **********************************************************************
  def _On_X90 ( self, event = None ) :
    self.Thread.ser.write ( '\xFA' )
    self.Thread.ser.write ( [0x90] )

  # **********************************************************************
  def _On_X91 ( self, event = None ) :
    self.Thread.ser.write ( '\xFA' )
    self.Thread.ser.write ( [0x91] )
  # **********************************************************************
  def _On_X92 ( self, event = None ) :
    self.Thread.ser.write ( '\xFA' )
    self.Thread.ser.write ( [0x92] )
  # **********************************************************************
  def _On_X93 ( self, event = None ) :
    self.Thread.ser.write ( '\xFA' )
    self.Thread.ser.write ( [0x93] )
  # **********************************************************************
  def _On_X94 ( self, event = None ) :
    self.Thread.ser.write ( '\xFA' )
    self.Thread.ser.write ( [0x94] )

  # **********************************************************************
  def _On_Radio_Modulation ( self, event = None ) :
    Radio = self.Radio_Program.GetValue()
    if not Radio is None :
      Filename = Programs [ Radio ].split (')')[1].strip() + '.xlsx'
      Filename = os.path.join ( My_Path, Filename )
    if Radio is None or not File_Exists ( Filename ) :
      Filename = 'hacked_Si443x Register Settings_RevB1-v5.xlsx'
      Filename = os.path.join ( My_Path, Filename )
    wb = Workbook ( Filename )
    Sheet('Modem Registers Calculations').activate()
    self.Get_Table ()

    self.Memo_Code.append ( 'procedure SI4432_Init_from_Excel () is' )
    Value = Range ( 'A9' ).value
    self.Memo_Code.append ( '  -- Modulation Type     : %s' % Value )
    Value = Range ( 'C14' ).value
    self.Memo_Code.append ( '  -- Frequency Deviation : %s [kHz]' % Value )
    Value = Range ( 'C9' ).value
    self.Memo_Code.append ( '  -- Manchester          : %s' % Value )
    Value = Range ( 'J9' ).value
    self.Memo_Code.append ( '  -- Carrier Frequency   : %s [MHz]' % Value )
    Value = Range ( 'L9' ).value
    self.Memo_Code.append ( '  -- Data Rate           : %s [kb/s]' % Value )
    Value = Range ( 'E14' ).value
    self.Memo_Code.append ( '  -- Receiver Bandwidth  : %s [kHz]' % Value )
    self.Memo_Code.append ( '' )

    Radio = self.Radio_Modulation.GetValue()
    Modulation = 'Registers_' + self.Modulations [ Radio ].replace ( '-', '_' )
    try :
      Relevant_Registers = eval ( Modulation )

      self.Memo_Code.append ( '  SI4432_Reset ()' )
      self.Memo_Code.append ( '' )

      ##for Address, Loc in Relevant_Registers.iteritems() :
      Addresses = Relevant_Registers.keys ()
      Addresses.sort ()
      for Address in Addresses :
        Loc = Relevant_Registers [ Address ]
        try :
          #Address = int ( '0x' + Address )
          Value = Range ( Loc ).value

          if self.Registers [ Address ][1][2:] == Value : Line = '  ;'
          else                                          : Line = '  '

          if isinstance ( Value, basestring ) :
            Value = eval ( '0x' + Value )
          else :
            Value = '%s' % int ( Value )
            Value = eval ( '0x' + Value )
          ##print Loc, Value, type(Value)

          self.Write_Table ( Address, Value, PIC = False )
          if Address in Description : Desc = Description [ Address ]
          else                      : Desc = ''
          self.Memo_Code.append ( Line + 'SI4432_Write ( %s, %s )    -- %s' % (
            My_Hex(Address), My_Hex(Value), Desc ))
        except:
          if not Value == 'N/A' :
            traceback.print_exc()
            print ( 'Excel problem OOK registers', Address, Value, Loc, Range ( Loc ).value )

      self.Memo_Code.append ( 'end procedure' )
      self.Memo_Code.append ( '' )
      self.Memo_Code.moveCursor ( QtGui.QTextCursor.End )

    except :

      Value = Range ( 'A14' ).value
      self.Memo_Code.append ( '  -- AFC                : %s' % Value )
      Value = Range ( 'B14' ).value
      self.Memo_Code.append ( '  -- Rb Error           : %s' % Value )

      Value = Range ( 'G80' ).value
      print ( 'UUUUUU', Value )
      if Value == 'FIFO MODE' :
        self.Memo_Code.append ( '' )
        self.Memo_Code.append ( '  -- ******  FIFO MODE  *****************' )
        for index in range ( 82, 122 ) :
          Value = Range ( 'G%s' % index ).value
          if Value != 0 :
            Line = Value +', '
            try :
              Line += Range ( 'H%s' % index ).value
            except :
              Line += str ( Range ( 'H%s' % index ).value )
            Value = str ( Range ( 'I%s' % index ).value )
            if Value!= '0' :
              Line += ', ' + Value
            self.Memo_Code.append ( '  -- ' + Line )

      else :
        self.Memo_Code.append ( '' )
        self.Memo_Code.append ( '  -- ******  PH + FIFO MODE  *****************' )
        for index in range ( 82, 141 ) :
          Value = Range ( 'J%s' % index ).value
          if Value != 0 :
            Line = Value +', '
            try :
              Line += Range ( 'K%s' % index ).value
            except :
              Line += str ( Range ( 'H%s' % index ).value )
            Value = str ( Range ( 'L%s' % index ).value )
            if Value != '0' :
              Line += ', ' + Value
            self.Memo_Code.append ( '  -- ' + Line )

      self.Memo_Code.append ( '' )
      self.Memo_Code.append ( '  SI4432_Reset ()' )
      self.Memo_Code.append ( '' )

      for index in range ( 82, 132 ) :
        try :
          Value = Range ( 'D%s' % index ).value
          if isinstance ( Value, basestring ) :
            Value = eval ( '0x' + Value )
          else :
            Value = '%s' % int ( Value )
            Value = eval ( '0x' + Value )
          if Value != 0 :
            Address = Value
            Value = Range ( 'E%s' % index ).value

            if self.Registers [ Address ][1][2:] == Value : Line = '  ;'
            else                                          : Line = '  '

            if isinstance ( Value, basestring ) :
              if Value == 'N/A' :
                continue
              Value = eval ( '0x' + Value )
            else :
              Value = '%s' % int ( Value )
              Value = eval ( '0x' + Value )

            self.Write_Table ( Address, Value, PIC = False )
            if Address in Description : Desc = Description [ Address ]
            else                      : Desc = ''

            print ( '<><>',self.Registers[Address], Value )
            self.Memo_Code.append ( Line + 'SI4432_Write ( %s, %s )    -- %s' % (
              My_Hex(Address), My_Hex(Value), Desc ))
        except:
          traceback.print_exc()
          print ( 'Excel problem', index, Range ( 'D%s' % index ).value, Range ( 'E%s' % index ).value )

      self.Memo_Code.append ( 'end procedure' )
      self.Memo_Code.append ( '' )
      self.Memo_Code.moveCursor ( QtGui.QTextCursor.End )
      ## ?? self.Clear_Table ( PIC = False )

    self.Set_Table()
    self.NB.SetSelection ( 1 )

  # **********************************************************************
  def _On_Clear ( self, event = None ) :
    self.Memo_Code.clear ()

  # **********************************************************************
  def _On_Save ( self, event = None ) :
    Filename = os.path.join ( My_Path, 'Registers.csv' )
    fh = open ( Filename, 'wb' )
    for Row in self.Registers_Header + self.Registers :
      Line = ''
      for Item in Row[:-1] :
        Line += str(Item) + ','
      Line += '"' + Row[-1] + '",'
      fh.write ( Line + '\r\n' )
    ##fh.write ( self.Memo_Code.GetValue () )
    fh.close ()

    Filename = os.path.join ( My_Path, 'Registers.JAL' )
    fh = open ( Filename, 'wb' )
    fh.write ( self.Memo_Code.GetValue () )
    fh.close ()

  # **********************************************************************
  def _On_PDF ( self, event = None ) :
    Filename = 'AN440_registers.pdf'
    Filename = os.path.join ( My_Path, Filename )
    URL = QUrl.fromUserInput(Filename)
    self.WebKit.load ( URL )
    self.NB.SetSelection ( 0 )

  # **********************************************************************
  def _On_Help ( self, event = None ) :
    URL = 'http://mientki.ruhosting.nl/data_www/raspberry/doc/si4432_register_viewer.html'
    self.WebKit2.load ( QUrl ( URL ))
    self.NB.SetSelection ( 2 )


# *****************************************************************************
# *****************************************************************************
if __name__ == '__main__':
  My_Main_Application ( Stream_Viewer )
