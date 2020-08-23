# -*- coding: utf-8 -*-

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
from   SI4432_support  import *

# *****************************************************************************
# search for the correct CommPort
# *****************************************************************************
ID_String = b'\xAA\xBB\xC2'
Filename = Base_GUI.Create_IniFileName ()
Get_CommPort (  ID_String, Filename )
sleep ( 5 )

# *****************************************************************************
class Stream_Viewer ( SI4432_Base ):
  def __init__ ( self, IniFile = None ):
    SI4432_Base.__init__ ( self )

    Title = 'ESP($$):   SI-4432 Interactive Viewer  (version %s)' % _Version_Text[0][0]

    GUI = """
self.Main_Window ,MainWindow  ,label = Title
  self.Splitter        ,X ,SplitterHor
    PanelVer
      self.Reg_Table         ,X,Table
      PanelHor
        self.RS232_Conn     ,Button  ,label='???' ,bind = self._On_Connect
        Button              ,label='Reset'        ,bind = self._On_Reset
        Button              ,label='All Regs'     ,bind = self._On_All_Regs
        self.Button_OK_Test ,Button ,label='OK ?' ,bind = self._On_OK_Test
        self.Button_Busy    ,Button ,label='Busy'
    self.NB              ,Notebook
      self.WebKit          ,X, Webkit  ,label = 'Registers'
      self.Memo_Code       ,TextCtrl   ,label = 'ESP code'
      self.WebKit2         ,Webkit     ,label = 'Help Page'
    """
    self.wxGUI = Create_GUI ( GUI , IniFile, Icon = 'vippi_bricks.png' )

    self.ID_String        = ID_String
    self.Help_File        = 'si4432_interactive_viewer.html'
    self.Registers_Header = [[ 'Address', '', 'Reset', 'Now','Diff', 'Reset','Now','Description' ]]
    self.Post_Init ()

    self.Set_Table ()
    Bind = self.Main_Window.Bind
    Bind ( 'F9', self._On_Execute_Code )
    self.Memo_Code.moveCursor ( QtGui.QTextCursor.End )

    self._On_PDF ()
    self._On_Help ()

  # *************************************************************
  # Send all GUI-settings to the ESP
  # *************************************************************
  def _On_Init ( self, event = None ) :
    self._On_Reset ()
    print ( "Register Viewer:  _On_Init")

  # *************************************************************
  # after a (soft) reset or request of all registers
  # *************************************************************
  def _Completion_0xF0 ( self ):
    Reset = self.Status == 0xF0
    self.Clear_Table ( Reset )
    for Address, Value in enumerate ( self.Register_Data [3:133] ) :
      self.Write_Table ( Address, Value, Reset )
    self.Set_Table ()

  # **********************************************************************
  def _On_Execute_Code ( self, event = None ) :
    self.Set_Busy ()

    Code = self.Memo_Code.GetStringSelection ()
    if not Code :
      Code = self.Memo_Code.GetValue ()
      Code = Code.splitlines ()
      while not Code[-1].strip() : Code = Code [:-1]
      New = []
      while Code[-1].strip() :
        New.insert ( 0, Code[-1] )
        Code = Code [:-1]
      Code = New
    else :
      Code = Code.splitlines ()

    # *********************************************************
    # Example Code
    ##   this->SI4432_Write ( 0x75, 0x53 ) ;   // Frequency Band Select
    ##   this->SI4432_Write ( 0x76, 0x62 ) ;   // Nominal Carrier Frequency
    # *********************************************************
    ToDo = False
    for Line_Org in Code :
      try :
        print ( "Line =", Line_Org )
        Line = Line_Org.strip()
        if not Line.startswith ( "//" ) :
        
          # *************************************
          # remove "this->" and whitespace again
          # *************************************
          if Line.startswith ("this" ) :
            x1 = Line.find ( "->" )
            Line = Line [ x1+2: ]
            Line = Line.strip ()
     
          # *************************************
          # remove function-name and brackects
          # *************************************
          if Line.startswith ( "SI4432_Write" ) :
            #print ( "Linez =", Line )
            x1 = Line.find ( '(' )
            Line = Line [ x1+1 : ]
            x1 = Line.find ( ')' )
            Line = Line [ : x1 ]
            Line = Line.strip()
    
          # *************************************
          # split on comma or space
          # *************************************
          if ',' in Line : Line = Line.split(',')
          else           : Line = Line.split(' ')
  
          # *************************************
          # Derive the Address and Value
          # *************************************
          Address = eval ( Line[0] )
          Value   = eval ( Line[1] )
  
          # *************************************
          # if all within the correct margins, send the code
          # *************************************
          if ( Address < 127 ) and ( Value < 256 ) :
            #print ( "Action", Address, Value  )
            self.Thread.ser.write ( b'\xFA' )
            self.Thread.ser.write ([ Address ])
            self.Thread.ser.write ([ Value ])
            ToDo = True
            My_Sleep ( 0.1 )
          
      except :
        traceback.print_exc ()
        print ( "Error in Line:", Line_Org )

    if not ( ToDo ) :
      self.Set_Busy ( False )

    # get all registers after a short delay
    sleep ( 0.2 )
    sleep ( 1 ) 
    #self.Status = 0xF1
    #self.Thread.ser.write ([ 0xF1 ])

    self._On_All_Regs ()     

# *****************************************************************************
# *****************************************************************************
if __name__ == '__main__':
  My_Main_Application ( Stream_Viewer )
