# -*- coding: utf-8 -*-


""" 1-8-2020, SM
https://www.learnpyqt.com/blog/pyqt5-vs-pyside2/
https://machinekoder.com/pyqt-vs-qt-for-python-pyside2-pyside/
https://opensource.com/article/17/4/pyqt-versus-wxpython

- future imports weggehaald
- prevent generation of pyc files
- op meerder plaatsen hieronder wx.PySimpleApp () vervangen door wx.App ()


- =====  VPY3 = vervangen door py-3 versie vanuit support
++ Base_GUI.py VPY3
++ completer_support.py VPY3
++ date_time_support.py VPY3  calendar verwijderd ?
++ dialog_support.py VPY3
++ doc_support.py VPY3
++ file_support.py VPY3
++ General_Globals.py VPY3
++ grid_support.py VPY3
++ gui_support.py VPY3
++ gui_support_QT.py  <== terugcopy
++ help_support.py VPY3
++ html_support.py VPY3
++ inifile_support.py VPY3, line 250 list (...)
++ language_support.py VPY3
++ menu_support.py VPY3
++ picture_support.py VPY3
++ remote_support.py is gelijk, maar moet naar PySide2   <== terugcopy
++ Robbie_support.py VPY3
++ serial_support.py VPY3     <== terugcopy
++ SI4432_support.py VPY3     <== terugcopy
++ string_support.py VPY3
++ system_support.py VPY3,  line 211User under Fedora ??
++ tree_support.py VPY3
++ utility_support.py VPY3
++ wxp_widgets.py VPY3

pyqtgraph geeft problemen  
"""
_Version_Text = [
[ 1.0 , '01-08-2020', 'Stef Mientki',
'Test Conditions:', (),
"""
Python 3.7.8
"""],

[ 0.1 , '31-10-2014', 'Stef Mientki',
'Test Conditions:', (),
"""
Initial Release
"""]
]

import PySide2
import sys
sys.dont_write_bytecode = True  # prevent generation of PYC files

#form past.utils import old_div

import __init__
from   SI4432_support  import *

# *****************************************************************************
# search for the correct CommPort
# *****************************************************************************
ID_String = b'\xAA\xBB\xC1'
Filename = Base_GUI.Create_IniFileName ()
Get_CommPort (  ID_String, Filename )
sleep ( 5 )


# *****************************************************************************
class Stream_Viewer ( SI4432_Base ):
  def __init__ ( self, IniFile = None ):
    SI4432_Base.__init__ ( self )

    Title = 'ESP($$): UHF Generator (version %s)' % _Version_Text[0][0]

    Powers = '20 dBm,17 dBm,14 dBm,11 dBm,8 dBm,5 dBm,2 dBm,-1 dBm'.split(',')
    Modes  = 'off,fixed,sweep 2 sec,sweep 10 sec,0.5 Hz OOK,5 Hz OOK,FSK 434-100,FSK 868,KAKU(hangs)'.split(',')

    GUI = """
self.Main_Window ,MainWindow  ,label = Title
  PanelVer
    PanelHor
      self.Radio_Mode  ,RadioBox  ,label='Mode'  ,choices=Modes,  bind=self._On_Radio_Mode
      self.Radio_Power ,RadioBox  ,label='Power' ,choices=Powers, bind=self._On_Radio_Power
    PanelHor
      Label                  ,label='Start    Freq [MHz]  '
      self.Edit_Freq_Start   ,LineEdit, bind = self._On_Edit_Start
    PanelHor
      Label                  ,label='End      Freq [MHz]  '
      self.Edit_Freq_End     ,LineEdit, bind = self._On_Edit_Start
    PanelHor
      self.RS232_Conn      ,Button  ,label='???'   ,bind = self._On_Connect
      Button                        ,label='Reset' ,bind = self._On_Reset
      self.Button_OK_Test  ,Button  ,label='OK ?'  ,bind = self._On_OK_Test
      self.Button_Busy     ,Button  ,label='Busy'
    PanelHor
      Button  ,label= '0x90'     ,bind = self._On_X90
      Button  ,label= '0x91'     ,bind = self._On_X91
      Button  ,label= '0x92'     ,bind = self._On_X92
      Button  ,label= '0x93'     ,bind = self._On_X93
      Button  ,label= '0x94'     ,bind = self._On_X94
    self.Memo_Code        ,TextCtrl
    """
    self.wxGUI = Create_GUI ( GUI , IniFile, Icon = 'vippi_bricks.png' )
    self.Memo_Code.moveCursor ( QtGui.QTextCursor.End )

    self.ID_String      = ID_String
    self.Help_File      = 'si4432_uhf_generator.html'
    self.Mode           = self.Radio_Mode.GetValue()
    self.Mode_Old       = -1
    self.Freq_Start_Old = -1
    self.StepSize_Old   = -1

    # **********************************************
    # Be sure we've valid values in case the Config file doesn't exists
    # **********************************************
    Power = self.Radio_Power.GetValue()
    if Power is None :
      self.Radio_Power.SetValue ( 7 )
    self.Mode = self.Radio_Mode.GetValue()
    if self.Mode is None :
      self.Mode = 1
      self.Radio_Mode.SetValue ( self.Mode )

    self.Freq_Start = self.Edit_Freq_Start.GetValue ()
    if not self.Freq_Start :
      self.Edit_Freq_Start.SetValue ( '434.0' )
    self.Freq_Start = int ( float ( self.Edit_Freq_Start.GetValue ()) * MEGA )
    
    self.Freq_End = self.Edit_Freq_End.GetValue ()
    if not self.Freq_End :
      self.Edit_Freq_End.SetValue ( '440.0' )
    self.Freq_End = int ( float ( self.Edit_Freq_End.GetValue ()) * MEGA )
    
    print ( "Power  = ", self.Radio_Power.GetValue() )
    print ( "Mode   = ", self.Mode )
    print ( "Freq   = ", self.Edit_Freq_Start.GetValue() )

    # **********************************************
    # Get the settings from the GUI and set the SI4432 accordingly
    # **********************************************
    self.Post_Init ()

  # *************************************************************
  # Send all GUI-settings to the ESP
  # *************************************************************
  def _On_Init ( self, event = None ) :
    self._On_Edit_Start ()
    self._On_Radio_Power ()
    self._Do_Settings ()
    print ( "UHF_Generator:  _On_Init")

  # *************************************************************
  # set parameters, so initially and after a reset
  # all settings will be send to the ESP
  # *************************************************************
  def _On_Reset ( self, event = None ) :
    self.Mode           = self.Radio_Mode.GetValue()
    self.Mode_Old       = -1
    self.Freq_Start_Old = -1
    self.StepSize_Old   = -1
    SI4432_Base._On_Reset ( self )

  # *************************************************************
  # Turn Generator Off (but leave buttons untouched)
  # *************************************************************
  def _On_Close ( self, event = None ) :
    #self.Radio_Mode.SetValue ( 0 )  # willen we niet
    #self._On_Radio_Mode()
    self.Thread.ser.write ( b'\xFA\xB1' )
    My_Sleep ( 0.1 )
    SI4432_Base._On_Close ( self )

  # **********************************************************************
  def _Do_Settings ( self ) :
    if self.Mode != self.Mode_Old :
      if self.Freq_Start_Old != self.Freq_Start :
        self._Send_Freq ( self.Freq_Start )
        self.Freq_Start_Old = self.Freq_Start

      # **********************************************
      # calculate and send stepsize (in 10 kHz units) if necessarry
      # **********************************************
      if self.Mode in [2,3] :
        #StepSize = int (old_div(( self.Freq_End - self.Freq_Start ),2560000))
        StepSize = int ( ( self.Freq_End - self.Freq_Start ) / 2560000 )

        if   StepSize < 1   : StepSize = 1      # minimu = 10 kHz
        elif StepSize > 200 : StepSize = 200    # maxmim = 2 MHz

        if StepSize != self.StepSize_Old :
          self._Send_kHz_Stepsize ( StepSize )
          self.StepSize_Old = StepSize

        # **********************************************
        # Warning message if 480 MHz border is crossed
        # **********************************************
        if self.Freq_Start < 480 * MEGA and\
           self.Freq_Start + 256 * StepSize * 10000 > 480 * MEGA :
          self.Memo_Code.append ( 'WARNING: sweep crosses 480 MHz')
          self.Memo_Code.moveCursor ( QtGui.QTextCursor.End )

      # **********************************************
      # send Mode command
      # **********************************************
      print ( "Do Settings, Set Mode = ", self.Mode )
      self.Thread.ser.write ( b'\xFA' )
      self.Thread.ser.write ( [ 0xB1 + self.Mode ] )
      self.Mode_Old = self.Mode
      My_Sleep ( 0.1 )

  # **********************************************************************
  def _On_Radio_Power ( self, event = None ) :
    Power = self.Radio_Power.GetValue()
    Power = 0x80 + ( 7 - Power )
    self.Thread.ser.write ( b'\xFA')
    self.Thread.ser.write ( [ Power ] )
    print ( "Set Power = %i" % Power )

  # **********************************************************************
  def _On_Radio_Mode ( self, event = None ) :
    self.Mode = self.Radio_Mode.GetValue()
    self._Do_Settings ()

  # **********************************************************************
  def _On_Edit_Start ( self, event = None ) :
    Freq_Start  = self.Edit_Freq_Start.GetValue ()
    Freq_End    = self.Edit_Freq_End.GetValue ()
    try :
      # **********************************************
      # try to interpretate the Start and End frequency
      # **********************************************
      self.Freq_Start = int ( float ( Freq_Start ) * MEGA )
      try :
        self.Freq_End   = int ( float ( Freq_End   ) * MEGA )
      except :
        self.Freq_End = self.Freq_Start

      # **********************************************
      # if negative sweep, change End Frequency
      # **********************************************
      if self.Freq_End <= self.Freq_Start :
        self.Freq_End = self.Freq_Start + 100*MEGA
        #self.Edit_Freq_End.SetValue ( '%.6f' % ( old_div(self.Freq_End, MEGA) ))
        self.Edit_Freq_End.SetValue ( '%.6f' % ( self.Freq_End / MEGA ))
        self.Freq_End   = int ( float ( self.Freq_End   ) * MEGA )

      self.Mode_Old = -1
      self._Do_Settings ()
    except :
      traceback.print_exc ()
      print('_On_Edit_Start ERROR:', Freq_Start, Freq_End)

# *****************************************************************************
# *****************************************************************************
if __name__ == '__main__':
  My_Main_Application ( Stream_Viewer )
