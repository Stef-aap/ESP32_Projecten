# -*- coding: utf-8 -*-
##from __future__ import unicode_literals   # program crashes !!!!


_Version_Text = [
[ 1.0 , '16-08-2020', 'Stef Mientki',
'Test Conditions:', (),
"""
Refactored for use with the ESP32 or ES8266
"""],

[ 0.1 , '16-10-2014', 'Stef Mientki',
'Test Conditions:', (),
"""
Initial Release
"""]
]

import PySide2
import sys
sys.dont_write_bytecode = True  # prevent generation of PYC files

import __init__
from   SI4432_support  import *

# *****************************************************************************
# search for the correct CommPort
# *****************************************************************************
ID_String  = b'\xAA\xBB\xC3'   # QIA Receiver
ID_String2 = b'\xAA\xBB\xC4'   # SI4432 Receiver
Filename = Base_GUI.Create_IniFileName ()
Get_CommPort (  ID_String, Filename )
sleep ( 5 )

# *****************************************************************************
class Stream_Viewer ( SI4432_Base ):
  def __init__ ( self, IniFile = None ):
    SI4432_Base.__init__ ( self )

    self.Trigger_Levels       = [ 'High', 'Medium', 'Low', 'KAKU', 'PT2262-Sync', 'Free Run' ]
    self.Trigger_Level_Values = [  0.05,   0.1,      0.2,   -2,     -1,            -20       ]

    Title = 'ESP:    Logic Stream Viewer  (version %s)' % _Version_Text[0][0]

    GUI = """
  self.Main_Window ,MainWindow  ,label = Title
    self.Main_Window2 ,PanelVer    ,label= 'Test QT'
      self.Splitter    ,X,SplitterHor
        PanelVer

          PanelHor
            PanelVer
              self.Radio_Trigger_Level      ,RadioBox  ,label='Trigger Level'  ,choices = self.Trigger_Levels, bind=self._On_Radio_Trigger
              self.QIA_Chip                 ,CheckBox  ,label='use QIA Receiver'
            
#            PanelVer
#              PanelHor
#                Label                     ,label='1C'
#                self.Edit_1C              ,LineEdit, bind = self._On_Edit_Regs
            
          PanelHor
            Label                         ,label='                  Pre Decode   '
            self.Edit_Pre_Decode          ,LineEdit, bind = self._On_Edit_Pre_Decode

          PanelHor
            Label                         ,label='PT2262 Low width [us]   '
            self.Edit_Trig_Sync_Width     ,LineEdit, bind = self._On_Edit_Pre_Decode

          PanelHor
            Label                         ,label='      Packet Length [us]   '
            self.Edit_Trig_Packet_Length  ,LineEdit, bind = self._On_Edit_Pre_Decode

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

          self.Memo         ,TextCtrl

          PanelHor
            self.Button_Snapshot, Button  ,label= 'SnapShot'   ,bind = self._On_SnapShot
            self.Button_Freeze,   Button  ,label= 'Freeze'     ,bind = self._On_Freeze

        self.Plot_Splitter         ,X,SplitterVer
          self.Plot_Window_1         ,PanelVer
            self.Measure_Label_1       ,Label
          self.Splitter_Plot2      ,X,SplitterHor
            self.Memo_Measure          ,TextCtrl

            self.NB              ,Notebook
              self.Plot_Window_2         ,PanelVer  , label = 'SnapShot'
                self.Measure_Label_2       ,Label
              self.Plot_Window_3         ,PanelVer  , label = 'Trigger'

    """
    self.wxGUI = Create_GUI ( GUI , IniFile, Icon = 'vippi_bricks.png' )
    ##self.Main_Window.Bind ( 'closeEvent', self._On_Exit )

    print ( "Use QIA Receiver", self.QIA_Chip.GetValue() )
    global ID_String
    if not self.QIA_Chip.GetValue() :
      ID_String = ID_String2

    self.ID_String    = ID_String  
    self.Help_File    = 'stream_viewer.html'

    MB = self.Main_Window.menuBar()

    MB_Help = MB.addMenu('&Help')
    MB_Help.addAction ( 'Stream Viewer (F1)', self._On_Help )

    Bind = self.Main_Window.Bind
    Bind ( 'F1', self._On_Help )
    Bind ( 'F2', self._On_Select_Trigger )

    self.Memo.clear()
    self.Memo_Measure.clear ()

    # some values we need for the serial processing
    self.Freeze         = False
    self.Freeze_Request = False

    self.N_Trace        = 10

    self.Real_Signal_1     = np.zeros(0,'uint8')
    self.Real_Signal_Total = []
    self.Raw_Signals       = []
    self.Trigger_Indexes   = []
    for i in range ( self.N_Trace ) :
      self.Real_Signal_Total.append ( self.Real_Signal_1 )
      self.Raw_Signals.append ( [] )
      self.Trigger_Indexes.append ( [] )

    self.Packet_Length     = 3200
    self.Packet_SyncWidth  = 115
    self.Trigger_Signal    = None

    self.Real_Signal_2     = []
    self.X_Axis_2          = []

    self.Weird_Hold_Region = False

    self.Channel     = 0

    # *************************************************
    # Define X-Axis in kHz
    # *************************************************
    self.Nx    = 10000
    self.NSamp = 15000
    self.X_Axis_1 = range ( 0, 10*self.Nx, 10 )

    # *************************************************
    class MyPlot ( pg.PlotWidget ) :
      doubleClicked = Signal()
      def mouseDoubleClickEvent ( self, event ) :
        # Calling the orginal must be done first, to prevent error messages !!
        pg.PlotWidget.mouseDoubleClickEvent(self, event)
        self.doubleClicked.emit()
        ##self.CallBack ()

      ##def Set_CallBack ( self, CallBack ) :
      ##  self.CallBack = CallBack
    # *************************************************

    #self.Plot_1 = pg.PlotWidget( )
    self.Plot_1 = MyPlot()

    # Both methods work
    self.Plot_1.doubleClicked.connect ( self._On_Select_Trigger )
    ##self.Plot_1.Set_CallBack ( self._On_Select_Trigger )

    self.Plot_1.showGrid ( x=True, y=True, alpha = 0.7 )

    c = 20
    Axis_Color = ( c, c, c )
    self.Plot_1.getAxis ( 'bottom' ).setPen ( Axis_Color )
    self.Plot_1.getAxis ( 'left'   ).setPen ( Axis_Color )

    c = 220
    BG_Color = ( c, c, c )
    BG_Color = ( 212, 208, 200 )
    self.Plot_1.setBackground ( BG_Color )

    self.Plot_1.setXRange ( self.X_Axis_1[0], self.X_Axis_1[-1], padding=0 )

    #cross hair
    ##self.vLine_1 = None
    self.vLine_1 = pg.InfiniteLine ( angle=90, movable=False, pen = pg.mkPen((255,0,0)))
    self.hLine_1 = pg.InfiniteLine ( angle=0,  movable=False, pen = pg.mkPen((255,0,0)))

    self.Region_1 = pg.LinearRegionItem()
    self.Region_1.setZValue(10)
    self.Region_1.sigRegionChanged.connect ( self._Region_Shifted_1 )
    self.Region_1.setRegion ( [ 10000, 20000 ] )
    # *************************************************

    # *************************************************
    self.Plot_2 = pg.PlotWidget()
    self.Plot_2.showGrid ( x=True, y=True, alpha = 0.7 )

    c = 20
    Axis_Color = ( c, c, c )
    self.Plot_2.getAxis ( 'bottom' ).setPen ( Axis_Color )
    self.Plot_2.getAxis ( 'left'   ).setPen ( Axis_Color )

    c = 220
    BG_Color = ( c, c, c )
    BG_Color = ( 212, 208, 200 )
    self.Plot_2.setBackground ( BG_Color )

    self.Region_2 = pg.LinearRegionItem()
    self.Region_2.setZValue(10)
    self.Region_2.sigRegionChanged.connect ( self._Region_Shifted )
    self.Region_2.setRegion ( [ 10000, 30000 ] )
    # *************************************************


    # *************************************************
    self.Plot_3 = pg.PlotWidget()
    self.Plot_3.showGrid ( x=True, y=True, alpha = 0.7 )

    c = 20
    Axis_Color = ( c, c, c )
    self.Plot_3.getAxis ( 'bottom' ).setPen ( Axis_Color )
    self.Plot_3.getAxis ( 'left'   ).setPen ( Axis_Color )

    c = 220
    BG_Color = ( c, c, c )
    BG_Color = ( 212, 208, 200 )
    self.Plot_3.setBackground ( BG_Color )
    # *************************************************

    # Add plots to the GUI
    self.Plot_Window_1.SBox.addWidget ( self.Plot_1 )
#    self.Plot_Window_2.SBox.addWidget ( self.Plot_1 )
    self.Plot_Window_2.SBox.addWidget ( self.Plot_2 )
    self.Plot_Window_3.SBox.addWidget ( self.Plot_3 )

    self.Plot_1.scene().sigMouseMoved.connect ( self._On_Mouse_Hoover_1 )


    IniFile = self.wxGUI.IniFile
    IniFile.Section = 'Trigger'

    IniFile = self.wxGUI.IniFile
    IniFile.Section = 'Trigger'

    self.Pulse_Treshold    = IniFile.Read ( 'Pulse_Treshold' )
    self.Pulse_Ignore_Low  = IniFile.Read ( 'Pulse_Ignore_Low' )
    self.Pulse_Ignore_High = IniFile.Read ( 'Pulse_Ignore_High' )
    self.TLow              = IniFile.Read ( 'TLow' )
    self.THigh             = IniFile.Read ( 'THigh' )

    self.Trigger_Template  = IniFile.Read ( 'Trigger_Template', default = None )
    if not self.Trigger_Template is None :
      self.Trigger_Template  = np.array ( self.Trigger_Template )
    self.Trigger_Sum       = IniFile.Read ( 'Trigger_Sum' )

    self._On_Edit_Pre_Decode ()

    i = self.Radio_Trigger_Level.GetValue()
    if i is None :
      self.Radio_Trigger_Level.SetValue(4)
      self._On_Radio_Trigger ()


    ##if not self.Trigger_Template is None :
    self._Write_Trigger_Template ()

    # **********************************************
    # Get the settings from the GUI and set the SI4432 accordingly
    # **********************************************
    self.Post_Init ()

  
  # *************************************************************
  def _Completion_0x00 ( self, Data ):
    #self.Data_Bytes += Data 
    #print ( ">>>>>", len (Data) )
    if self.Freeze : return
    
    
    
    self.Data_Bytes += Data 
    if len ( self.Data_Bytes ) >  40 :   ## WAS 40, is erg traag TESTEN
      i = self.Radio_Trigger_Level.GetValue()
      Free_Run = self.Trigger_Level_Values[i] < -10

      Times = np.frombuffer ( self.Data_Bytes, 'uint8' )
      self.Data_Bytes = b""

      # *****************************************************
      # Test if first byte has bit-0 set (startbit of a High-Low Sequence)
      # otherwise skip until a startbyte is found
      # (in the PIC version , the second byte had bit-0 set)
      # *****************************************************
      while (( Times[0] & 1 ) == 0 ) and ( len ( Times ) > 2 ) :
        Times = Times [1:]

      Periods = len ( Times ) // 4
      ##print 'REC', Free_Run, N
      for i in range ( Periods ) :
        M = 64 * ( Times[4*i  ] & 0xFE)  + Times[4*i+1] // 2
        N = 64 *   Times[4*i+2]          + Times[4*i+3] // 2

        Ones  = 2*self.Channel + np.ones  ( M, 'uint8')
        Zeros = 2*self.Channel + np.zeros ( N, 'uint8')
        self.Real_Signal_1 = np.hstack ( ( self.Real_Signal_1, 0.5*Ones, 0.5*Zeros ) )
        #print ( len ( self.Real_Signal_1))

        #if i == 0 :
        #  print ( M, N, Times[:4] )

        # The Raw signal, but bytes transfered to words
        # The first element and all other even elements are ones
        self.Raw_Signals [ self.Channel ].append ( M )
        self.Raw_Signals [ self.Channel ].append ( N )
        ##print ' >>>',Zeros[:3],Ones[:3],self.Real_Signal_1[:3]

        # **************************************************
        # if more than NSamp we should have found a trigger
        # **************************************************
        if not Free_Run and len ( self.Real_Signal_1 ) > self.NSamp :

          # Search for trigger signal
          self.Real_Signal_Total [ self.Channel ] = self.Real_Signal_1
          self._Get_Trigger_Index ( self.Channel, Only_First=True )

          self.Channel += 1
          self.Channel %= self.N_Trace

          if not self.Freeze_Request :
            self.Raw_Signals [ self.Channel ] = []   ##<<<<<<<<<<!!!!!!!

          #print ('TRIIGGGER')
          break

        # **************************************************
        # if free running
        # **************************************************
        elif Free_Run and len ( self.Real_Signal_1 ) > self.Nx :
          self.Real_Signal_Total [ self.Channel ] = self.Real_Signal_1
          self.Channel += 1
          self.Channel %= self.N_Trace
          if not self.Freeze_Request :
            self.Raw_Signals [ self.Channel ] = []   ##<<<<<<<<<<!!!!!!!
          break

      if (Free_Run and len ( self.Real_Signal_1 ) > self.Nx ) or\
         len ( self.Real_Signal_1 ) > self.NSamp :
        for i, Signal in enumerate ( self.Real_Signal_Total ) :
          X = range ( 0, 10*len(Signal), 10 )
          self.Plot_1.plot( x=X, y=Signal, clear = (i==0),
                     pen = pg.mkPen ( (0,0,255), width = 1 ))
        self.Real_Signal_1 = np.zeros(0,'uint8')
        if self.Freeze_Request :
          self._Do_Freeze ()

      else :
        #self.Plot_1.plot( x=self.X_Axis_1,  y=self.Real_Signal_1, clear = True,
        X = range ( 0, 10*len(self.Real_Signal_1), 10 )
        self.Plot_1.plot( x=X, y=self.Real_Signal_1, clear = False,
                          pen = pg.mkPen ( (0,0,255), width = 1 ) )

      ##self.Plot_1.setXRange ( self.X_Axis_1[0], self.X_Axis_1[-1], padding=0 )
      self.Plot_1.setYRange ( 0, 10 )
      ##self.Plot_1.disableAutoRange()
    
  # *************************************************************
  # Finds first or all trigger moments (depending on Only_First)
  # as index(es) of the start of the trigger
  # If Plot=True also draws the found signals
  # *************************************************************
  def _Get_Trigger_Index ( self, Channel, Only_First=False, Plot=False ) :
    i = self.Radio_Trigger_Level.GetValue()
    Trigger_Level = self.Trigger_Level_Values [i]
    #print ( "TriggerLevel", Trigger_Level )

    # PT2262 syncbit triggering
    if   Trigger_Level == -1 :
      self._Get_Trigger_PT2262 ( Channel, Only_First=Only_First, Plot=Plot )

    # KAKU stopbit triggering
    elif   Trigger_Level == -2 :
      self._Get_Trigger_KAKU ( Channel, Only_First=Only_First, Plot=Plot )

    # if normal trigger
    elif Trigger_Level > 0 :
      self._Get_Trigger_Normal ( Trigger_Level, Channel, Only_First=Only_First, Plot=Plot )

    # otherwise, in freeze mode use the lowest trigger level
    else :
      # if Frozen, and free run, still find triggers with the lowest trigger level
      if self.Freeze :
        Trigger_Level = self.Trigger_Level_Values [ 2 ]
        self._Get_Trigger_Normal ( Trigger_Level, Channel, Only_First=Only_First, Plot=Plot )

  # *************************************************************
  # *************************************************************
  def _Get_Trigger_KAKU ( self, Channel, Only_First=False, Plot=False ) :
    if self.Trigger_Template is None :
       return
    Signal = np.array ( self.Raw_Signals [ Channel ] )

    # Signal_Cumsum contains the startmoment of each edge of the signal
    Signal_Cumsum = np.cumsum ( Signal )

    # *****************************************
    #          25  = small pulse
    #          125 = large pulse
    Stop_Low = 200   # long low of the stopbit
    # *****************************************

    # *****************************************
    # Find all low periods (odd index)
    # with a long enough period to be a stop-bit
    # *****************************************
    Stop_Index = np.where ( Signal > Stop_Low )
    ##print 'KKKK', Stop_Index,type(Stop_Index),

    # *****************************************
    # np.where delivers a tuple, so first convert to np.array
    # then create a mask
    # and apply the mask to the found values
    # *****************************************
    Stop_Index = np.array ( Stop_Index )
    mask = ( Stop_Index % 2) == 1
    Stop_Index = np.extract ( mask, Stop_Index )
    ##print 'KKKK', Stop_Index,

    # *****************************************
    # we have 32 final-bits
    # each final-bit consists of 4 periods High-Low-High-Low
    # so we need at least 32*4=128 periods
    # *****************************************
    NLevels = 128
    Indexes = []
    x1 = 0
    for x2 in Stop_Index :
      if x2 - 2 - x1 >= NLevels :
        Indexes.append (( x2-NLevels-2, x2-2 ))
      x1 = x2
    ##print 'KKKK', Indexes

    for Index in Indexes :
      x1 = Signal_Cumsum [ Index[0] ]
      x2 = Signal_Cumsum [ Index[1] ]

      # ***************************************************************
      # during life syncing, we are not allowed to look at the previous
      # because we don't know if it's full period
      # ***************************************************************
      if Only_First :
        self.Real_Signal_Total [ Channel ] = self.Real_Signal_1 [x1:]

        # also Raw_Signals must be corrected
        Cumsum = np.cumsum ( np.array ( self.Raw_Signals [ Channel ] ))
        for i in range ( len ( Cumsum )) :
          if Cumsum [i] >= x1 :
            break
        self.Raw_Signals [ Channel ] = [Cumsum[i]-x1] + self.Raw_Signals [ Channel ] [i+1:]

        ##print 'MMMMM', x1,i
        return x1
      # ***************************************************************

      if Plot :
        print ( '===', Channel, x2-x1, x1, x2 )
        ##self.Trigger_Indexes [ Channel ].append ( Start_Index + Trigger_Start  )
        X = range ( 10*x1, 10*x2, 10 )
        self.Plot_1.plot( x=X,
          y = self.Real_Signal_Total [ Channel ][x1:x2],
          clear=False, pen = pg.mkPen ( (255,0,0), width = 1 ))
        QtCore.QCoreApplication.instance ().processEvents ()


    self.Trigger_Indexes [ Channel ] = Indexes
    ##return Indexes

  # *************************************************************
  # *************************************************************
  def _Get_Trigger_PT2262 ( self, Channel, Only_First=False, Plot=False ) :
    print ( "Trigger PT2262", self.Trigger_Template )
    if self.Trigger_Template is None :
       return
    Signal       = np.array ( self.Raw_Signals [ Channel ] )

    #if ( not self.Freeze and len (self.Real_Signal_1 ) < self.Packet_Length ) or \
    #   ( self.Freeze and len ( Signal ) <= len ( self.Trigger_Template ) ) :
    if len ( Signal ) <= len ( self.Trigger_Template ) :
      return
    #if len (self.Real_Signal_1) < self.Packet_Length/10 :
    #  return

    # Signal_Cumsum contains the startmoment of each edge of the signal
    Signal_Cumsum = np.cumsum ( Signal )

    # eigenlijk wil ik hier alleen de odd elements "0"
    Start_Index = np.where ( Signal_Cumsum > self.Packet_Length/10 )
    if Start_Index[0][0] % 2 > 0 : Start_Index = Start_Index[0][0] + 1
    else                         : Start_Index = Start_Index[0][0]

    Signal         = Signal [ Start_Index : ]   ##<<<<<<<<<<<<<<<<<<
    Trigger_Starts = np.where ( Signal > self.Packet_SyncWidth )[0]

    x2_prev = 0
    Indexes = []
    self.Trigger_Indexes [ Channel ] = [0]
    for Trigger_Start in Trigger_Starts :
      x2 = int ( Signal_Cumsum [ Start_Index + Trigger_Start - 1 ] )
      x1 = int ( x2 - self.Packet_Length )
      if x1 < x2_prev :
        continue
      x2_prev = x2

      # ***************************************************************
      # during life syncing, we are not allowed to look at the previous
      # because we don't know if it's full period
      # ***************************************************************
      if Only_First :
        self.Real_Signal_Total [ Channel ] = self.Real_Signal_1 [x1:]

        # also Raw_Signals must be corrected
        Cumsum = np.cumsum ( np.array ( self.Raw_Signals [ Channel ] ))
        for i in range ( len ( Cumsum )) :
          if Cumsum [i] >= x1 :
            break
        self.Raw_Signals [ Channel ] = [Cumsum[i]-x1] + self.Raw_Signals [ Channel ] [i+1:]

        return x1
      # ***************************************************************

      ##Indexes.append ( i )

      if Plot :
        ##print '===', Channel, x2-x1, x1, x2
        self.Trigger_Indexes [ Channel ].append ( Start_Index + Trigger_Start  )
        X = range ( 10*x1, 10*x2, 10 )
        self.Plot_1.plot( x=X,
          y = self.Real_Signal_Total [ Channel ][x1:x2],
          clear=False, pen = pg.mkPen ( (255,0,0), width = 1 ))
        QtCore.QCoreApplication.instance ().processEvents ()

    return Indexes


  # *************************************************************
  # *************************************************************
  def _Get_Trigger_Normal ( self, Trigger_Level, Channel, Only_First=False, Plot=False ) :
    #print ( 'Trigger Normal', self.Trigger_Template )
    if self.Trigger_Template is None :
      return

    Signal_Start = self.Real_Signal_Total [ Channel ][0]
    Signal       = np.array ( self.Raw_Signals [ Channel ] )
    if len ( Signal ) <= len ( self.Trigger_Template ) :
      return

    Result = []
    N = len ( Signal )
    M = len ( self.Trigger_Template )
    for i in range ( 0, N-M, 2 ) :
      Result.append ( sum ( abs ( self.Trigger_Template - Signal [ i:i+M])))
    Result = np.array ( Result )

    Max = max ( Result )
    Min = min ( Result )
    Treshold = Min + Trigger_Level * ( Max - Min )

    # Signal_Cumsum contains the startmoment of each edge of the signal
    Signal_Cumsum = np.cumsum ( Signal )

    mins = argrelextrema ( Result , np.less )[0]
    # first element will not be found, because it's not surrounded by larger value
    if Result[0] < Treshold :
      mins = np.hstack ( ([0], mins ))
    """
    print 'RRRR', Result [:50]
    print Treshold
    print self.Trigger_Template[:50]
    print Signal[:50]
    print mins[:40]
    """

    x2_prev = 0
    Indexes = []
    for i in mins :
      if Result[i] < Treshold :
        x1 = Signal_Cumsum [2*i]
        if x1 < x2_prev :
          continue

        # during life syncing, we are not allowed to look at the previous
        # becaus we don't know if it's full period
        if Only_First :
          self.Real_Signal_Total [ Channel ] = self.Real_Signal_1 [x1:]

          # also Raw_Signals must be corrected
          Cumsum = np.cumsum ( np.array ( self.Raw_Signals [ Channel ] ))
          for i in range ( len ( Cumsum )) :
            if Cumsum [i] >= x1 :
              break
          self.Raw_Signals [ Channel ] = self.Raw_Signals [ Channel ] [i:]
          return x1

        # During replay we have to look at the previous period
        # because cumsum misses the starting 0-position
        if i > 0 : x1 = Signal_Cumsum [2*(i-1)]
        else     : x1 = 0

        x2 = x1 + self.Trigger_Sum
        x2_prev = x2
        if x2 > len ( self.Real_Signal_Total [ Channel ] ) :
           x2 = len ( self.Real_Signal_Total [ Channel ] )

        Indexes.append ( i )

        if Plot :
          X = range ( 10*x1, 10*x2, 10 )
          self.Plot_1.plot( x=X,
            y = self.Real_Signal_Total [ Channel ][x1:x2],
            clear=False, pen = pg.mkPen ( (255,0,0), width = 1 ))
          QtCore.QCoreApplication.instance ().processEvents ()

    return Indexes

  # *************************************************************
  # *************************************************************
  def _Decode ( self, Times, Channel = -1, Separator='' ) :
    #if Times is None or len ( Times ) == 0 :
    #  return "", ""
    if Times is None :
      return "", ""
    
    i = self.Radio_Trigger_Level.GetValue()
    Trigger_Level = self.Trigger_Level_Values [i]

    # PT2262 syncbit triggering
    if   Trigger_Level == -1 :
      return self._Decode_PT2262 ( Times, Channel, Separator )

    elif Trigger_Level == -2 :
      return self._Decode_KAKU ( Times, Channel, Separator )

    # if normal trigger
    elif Trigger_Level > 0 :
      return self._Decode_Normal ( Times, Channel, Separator )

    # otherwise, in freeze mode use the lowest trigger level
    else :
      # if Frozen, and free run, still find triggers with the lowest trigger level
      if self.Freeze :
        return self._Decode_Normal ( Times, Channel, Separator )

    return '', ''

  # *************************************************************
  # *************************************************************
  def _Decode_KAKU ( self, Times, Channel = -1, Separator='' ) :
    # *****************************************
    #          25  = small pulse
    #          125 = large pulse
    Stop_Low = 200   # long low of the stopbit
    # *****************************************

    Line = ''
    New  = []
    for i,T in enumerate ( Times ) :
      pass

    Indexes = self.Trigger_Indexes [ Channel ]
    if Indexes :
      Indexes = Indexes[0]
      print ( Channel, Indexes, len(Times),Times )
      Signal = Times [ Indexes[0] : Indexes[1] ]
      for i in range ( len ( Signal) / 2 ) :
        Low  = Signal [1]
        High = Signal [0]
        Signal = Signal [2:]
        if Low > 2 * High : Line += '1'
        else              : Line += '0'
      print ( 'LINE:', Channel, Line )

    # next decode step
    if len ( Line ) > 60 :
      while len (Line) < 64 :
        Line = '0' + Line
      if len ( Line ) > 64 :
        Line = Line [ len(Line)-64 : ]
      Value = 0
      for i in range ( 32 ) :
        First  = Line [0]
        Second = Line [1]
        if   Line[:2] == '01' : Value = ( Value << 1 ) | 0
        elif Line[:2] == '10' : Value = ( Value << 1 ) | 1
        else                              : break
        Line   = Line [2:]
      else :
        Unit  = Value & 0x0F
        if ( Value & 0x10 ) >> 4 : On    = 'On'
        else                     : On    = 'Off'
        if ( Value & 0x20 ) >> 5 : Group = 'Gr'
        else                     : Group = 'NGr'
        #Address = Value >> 6
        Address = Value & 0xFFFFFFCF
        New_Line = 'A=0x%s_%s_%s_%s    U=0x%s    %s    %s' % (
          hex(Address)[2:4].upper(),
          hex(Address)[4:6].upper(),
          hex(Address)[6:8].upper(),
          hex(Address)[8:10].upper(),
          hex(Unit)[2:].upper(),
          On, Group )
        return Line, New_Line ##( hex ( Value )).upper()
    return '', ''

  # *************************************************************
  # *************************************************************
  def _Decode_PT2262 ( self, Times, Channel = -1, Separator='' ) :
    TLow  = self.TLow
    THigh = self.THigh

    Line = ''
    New  = []
    for i,T in enumerate ( Times ) :
      if   T < self.Pulse_Ignore_Low  : Line += '-' ; New.append ( T     )
      elif T < self.Pulse_Treshold    : Line += '0' ; New.append ( TLow  )
      elif T < self.Pulse_Ignore_High : Line += '1' ; New.append ( THigh )
      else                            : Line += '+' ; New.append ( T     )
      if i%4 == 3 :
        Line += Separator

    ##print Line

    # The trigger is the sync bit at the end of each transmitted package
    # so we need to track the signal in reversed order to correctly decode
    Indexes = self.Trigger_Indexes [ Channel ]
    Indexes.reverse ()
    HexLine = ''

    # start with the last found trigger moment (while Indexes is reversed)
    for ii, I2 in enumerate ( Indexes[:-1] ) :

      # I2 is the index of the long period of the sync bit is
      # So we to go one step back and step over the positive puls of the sync bit
      I2 -= 1

      # The previous trigger puls is one step further, because of the reversed Indexes
      I1 = Indexes [ii+1]

      # Now loop backwards through the signal and
      # place each decoded digit in front of the others
      for i in range ( I2, I1, -4 ) :
        Block = New [ i-4 : i ]
        if   Block == [ TLow, THigh, TLow, THigh ] : HexLine = '0' + HexLine
        elif Block == [ THigh, TLow, THigh, TLow ] : HexLine = '1' + HexLine
        elif Block == [ TLow, THigh, THigh, TLow ] : HexLine = 'F' + HexLine
        else                                       : HexLine = '?' + HexLine
        HexLine = 4*Separator + HexLine

      HexLine = '   ' + HexLine
    return Line, HexLine


  # *************************************************************
  # *************************************************************
  def _Decode_Normal ( self, Times, Channel = -1, Separator='' ) :
    TLow  = self.TLow
    THigh = self.THigh

    Line = ''
    New  = []
    for i,T in enumerate ( Times ) :
      if   T < self.Pulse_Ignore_Low  : Line += '?' ; New.append ( T     )
      elif T < self.Pulse_Treshold    : Line += '0' ; New.append ( TLow  )
      elif T < self.Pulse_Ignore_High : Line += '1' ; New.append ( THigh )
      else                            : Line += '-' ; New.append ( T     )
      if i%4 == 3 :
        Line += Separator

    New = self.Pre_Decode + New
    N = len ( New ) // 4
    HexLine = ''

    for i in range ( N ) :
      Block = New [ 4*i : 4*i+4 ]
      if   Block == [ TLow, THigh, TLow, THigh ] : HexLine += '0'
      elif Block == [ THigh, TLow, THigh, TLow ] : HexLine += '1'
      elif Block == [ TLow, THigh, THigh, TLow ] : HexLine += 'F'
      else                                       : HexLine += '?'
      HexLine += 4*Separator

    # Resync, werkt niet goed
    """
    if Channel >= 0 :
      Sync = self._Get_Trigger_Index ( Channel )
      print ( 'SYNCSSS', Sync,N,New )
      HexLine += ' || '
      for ii in range ( len ( Sync ) ):
        x1 = Sync [ii]
        if ii <> len ( Sync )-1 :  x2 = Sync [ii+1]
        else                    :  x2 = len ( New )
        N = 1 + ( x2-x1)/4
        print '>>>',x1,x2,N
        if ii > 0 : x1 += len ( self.Pre_Decode )
        HexLine += ' % '
        for i in range ( N ) :
          Block = New [ x1+4*i : x1+4*i+4 ]
          if   Block == [ TLow, THigh, TLow, THigh ] : HexLine += '0'
          elif Block == [ THigh, TLow, THigh, TLow ] : HexLine += '1'
          elif Block == [ TLow, THigh, THigh, TLow ] : HexLine += 'F'
          else                                       : HexLine += '?'
    #"""

    return Line, HexLine

  # **********************************************************************
  def _On_Radio_Trigger ( self, event = None ) :
    i = self.Radio_Trigger_Level.GetValue()
    Trigger_Level = self.Trigger_Level_Values [i]
    if Trigger_Level < 0 :
      return

    Result = self.Trigger_Signal
    if not Result :
      return
    self.Plot_3.plot( y = Result, clear = True,
                      pen = pg.mkPen ( (0,0,255), width = 2 ))

    Max = max ( Result )
    Min = min ( Result )
    Treshold = Min + Trigger_Level * ( Max - Min )

    self.Plot_3.plot( x = [ 0, len(Result) ],
                      y = [ Treshold, Treshold ],
                      clear = False,
                      pen = pg.mkPen ( (255,0,0), width = 1 ))
    self.Plot_3.enableAutoRange()

  # *************************************************************
  # *************************************************************
  # *************************************************************
  def _On_TTT ( self, event = None ) :
    print  ( 'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT', event )
    self._On_Select_Trigger ( event )
    ##return False

  def _On_Select_Trigger ( self, event = None ) :
    i = self.Radio_Trigger_Level.GetValue()
    Trigger_Level = self.Trigger_Level_Values [i]
    if ( Trigger_Level < 0 ) and ( Trigger_Level > -10 ) :
      return
    elif Trigger_Level == -20 :
      i = 0
      self.Radio_Trigger_Level.SetValue(i)
      Trigger_Level = self.Trigger_Level_Values [i]
      QtCore.QCoreApplication.instance ().processEvents ()

    Channel = int ( self.crosshair_y ) ## / 2 )
    print ( 'Trigger on Channel', Channel, i, )

    try :
      Signal = np.array ( self.Raw_Signals [ Channel ] )
      
      #print ( "Region", self.Region_minX. self.Region_maxX, self.Region_minX//10 )

      Trigger = self.Real_Signal_Total [ Channel ] [ int(self.Region_minX/10) : int(self.Region_maxX/10) ]
      Trigger_Start = self.Real_Signal_Total [ Channel ] [ int(self.Region_minX/10) ] - Channel

      Times = []
      Value = Trigger[0]
      T     = 0
      for Trig in Trigger :
        if Trig == Value :
          T += 1
        else :
          # store the raw T value and reset the parameters
          Times.append ( T )
          T = 1
          Value = Trig

      # *****************************************************
      # ignore the first time because it will not be complete
      # the last sample is not yet stored (ignored for the same reason)
      # *****************************************************
      Trigger = np.array ( Times [1:] )

      # *****************************************************
      # if the first sample of the signal was a "1",
      # then the first Trig sample will reflect a "0"-signal (because first Trig is removed)
      # so we've to remove another one to be sure the Trigger starts with a "1"-signal
      # *****************************************************
      if Trigger_Start :
        Trigger = Trigger [1:]
      self.Trigger_Template = Trigger

      Result = []
      N = len ( Signal )
      M = len ( Trigger )
      for i in range ( 0, N-M, 2 ) :
        Result.append ( sum ( abs ( Trigger - Signal [ i:i+M])))

      self.Trigger_Sum = sum ( Trigger )

      # *****************************************************
      # let's do it for all signals and show the triggers in a plot
      # redraw all the plots
      # restore region and crosshair
      # *****************************************************
      Plot = self.Plot_1
      for Channel in range ( self.N_Trace ) :
        X = range ( 0, 10*len(self.Real_Signal_Total [ Channel ]), 10 )
        Plot.plot( x=X , y = self.Real_Signal_Total [ Channel ], clear = Channel==0,
                   pen = pg.mkPen ( (0,0,255), width = 1 ))
        QtCore.QCoreApplication.instance ().processEvents ()

      self.Plot_1.addItem ( self.Region_1, ignoreBounds = True )

      self.Plot_1.addItem ( self.vLine_1, ignoreBounds=True)
      self.Plot_1.addItem ( self.hLine_1, ignoreBounds=True)

      # *****************************************************
      # highlight the trigger moments
      # *****************************************************
      for Channel in range ( self.N_Trace ) :
        self._Get_Trigger_Index ( Channel, Plot=True )
      self.Memo_Measure.append ('')

      # *****************************************************
      #"""
      self.Trigger_Signal = Result
      self.Plot_3.plot( y = Result, clear = True,
                        pen = pg.mkPen ( (0,0,255), width = 2 ))

      Max = max ( Result )
      Min = min ( Result )
      Treshold = Min + Trigger_Level * ( Max - Min )

      self.Plot_3.plot( x = [ 0, len(Result) ],
                        y = [ Treshold, Treshold ],
                        clear = False,
                        pen = pg.mkPen ( (255,0,0), width = 1 ))
      self.Plot_3.enableAutoRange()
      #"""
      # *****************************************************
    except :
      traceback.print_exc ()

    # *****************************************************
    # now we can do some statistics to find the short and long time periods
    # first stack all the Raw signals together
    # *****************************************************
    Raw_Total = np.array([])
    for Raw in self.Raw_Signals :
      Raw_Total = np.hstack ( ( Raw_Total, Raw ))

    # *****************************************************
    # remove outliers (very small and very large values)
    # sort the data and remove 10% on the left and right
    # *****************************************************
    N = len ( Raw_Total )
    #N /= 10
    N = N // 10
    Raw_Total.sort ()
    Raw_Total = Raw_Total [ N : - N ]
    ##print '****', Raw_Total

    # *****************************************************
    # Because the distribution of both time low and time high
    # have very sharp peaks, the problem will lie in the region inbetween
    # As the signal can well have a not uniform distribution of low and high times
    # Mean is much better than Median
    # *****************************************************
    Mean   = np.mean ( Raw_Total )
    ##print 'med/mean', Mean

    Low  = Raw_Total [ np.where ( Raw_Total < Mean ) ]
    High = Raw_Total [ np.where ( Raw_Total > Mean ) ]
    ##print 'Low', Low
    ##print 'High', High

    Left  = np.percentile ( Low, 0.95 )
    Right = np.percentile ( High, 0.05 )
    ##print 'Lowborder', Left,type(Left)
    ##print 'Highborder', Right,type(Right)

    self.Pulse_Treshold = int ( 0.5 * ( Left + Right ))
    ##print 'Treshold', self.Pulse_Treshold

    # *****************************************************
    # Now split the Raw_Total again on base of the treshold
    # *****************************************************
    Low  = Raw_Total [ np.where ( Raw_Total < self.Pulse_Treshold ) ]
    High = Raw_Total [ np.where ( Raw_Total > self.Pulse_Treshold ) ]

    # *****************************************************
    # *****************************************************
    self.Pulse_Ignore_Low  = np.percentile ( Low, 0.05 )
    self.Pulse_Ignore_High = np.percentile ( High, 0.95 )
    ##print 'Ignore Lowborder', self.Pulse_Ignore_Low
    ##print 'Ignore Highborder', self.Pulse_Ignore_High

    # *****************************************************
    # because we have to deal with fysical signals and not with statistics
    # we have to check if these borders are wide enough
    # so determine the Mean and we should allow for at least 20% deviation
    # *****************************************************
    Left  = np.mean ( Low )
    Right = np.mean ( High )
    if 0.8 * Left < self.Pulse_Ignore_Low :
      self.Pulse_Ignore_Low = int (0.8 * Left )
    if 1.2 * Right > self.Pulse_Ignore_High :
      self.Pulse_Ignore_High = int (1.2 * Right )
    ##print 'Ignore Lowborder', self.Pulse_Ignore_Low
    ##print 'Ignore Highborder', self.Pulse_Ignore_High

    # *****************************************************
    # again determine Mean (after remove ignored tails)
    # and that will be the final TLow and THigh
    # *****************************************************
    TLow = np.mean
    Low = Low [ np.where ( Low > self.Pulse_Ignore_Low )]
    self.TLow = int ( round ( np.mean ( Low )))

    High = High [ np.where ( High < self.Pulse_Ignore_High )]
    self.THigh = int ( round ( np.mean ( High )))
    ##print 'TLow/THigh:', self.TLow, self.THigh

    # *****************************************************
    print ('Times:  TLow_Ignore = %s,   TLow = %s,   Treshold = %s,   THigh = %s,   THigh_Ignore = %s' % (
      self.Pulse_Ignore_Low, self.TLow, self.Pulse_Treshold, self.THigh, self.Pulse_Ignore_High ))

    self._Write_Trigger_Template ()


  # *************************************************************
  def _On_SnapShot ( self, event = None ) :
    self._On_SnapShot_Action ()

  # *************************************************************
  def _On_SnapShot_Action ( self, event = None ) :
    self.X_Axis_2 = self.X_Axis_1

    ##self.Plot_2.removeItem ( self.Region_2 )
    #########self.Plot_2.sigRangeChanged.disconnect ( self._Shift_Region )

    Clear = False
    width = 1
    for i, Signal in enumerate ( self.Real_Signal_Total ) :
      X = range ( 0, 10*len(Signal), 10 )
      self.Plot_2.plot( x=X, y=Signal, clear = (i==0),
    #self.Plot_2.plot( y=self.Real_Signal_2, clear = Clear,
                     pen = pg.mkPen ( (0,0,255), width = width ))

    self.Plot_2.setXRange ( self.X_Axis_2[0], self.X_Axis_2[-1], padding=0 )
    self.Plot_2.setYRange ( 0, 10 )

    print (dir (self.Plot_2.sigRangeChanged))
    self.Plot_2.addItem ( self.Region_2, ignoreBounds = True )

    # ******************************

    # *********************************************************
    # shift of the upper plot will adapt the selection in bottom plot
    # *********************************************************
    ##########self.Plot_1.sigRangeChanged.connect ( self._Shift_Region )
    ##self.Plot_1.setAutoVisible(y=True) helpt niet
    # *********************************************************


  # *************************************************************
  def _On_Freeze ( self, event = None ) :

    if self.Freeze :
      self.Raw_Signals [ self.Channel ] = []   ##<<<<<<<<<<!!!!!!!
      self.Freeze = not self.Freeze
      self.Button_Freeze.setText ( 'Freeze' )
      self.Plot_1.setXRange ( self.X_Axis_1[0], self.X_Axis_1[-1], padding=0 )
      self.Plot_2.removeItem ( self.Region_2 )

    else :
      self.Freeze_Request = True
      self.Button_Freeze.setText ( 'Freezing' )

  # *************************************************************
  def _Do_Freeze ( self, event = None ) :
    self.Freeze         = True
    self.Freeze_Request = False

    self.Button_Freeze.setText ( '   Life   ' )

    print ('Trig-TEMPLATE', self.Trigger_Template)

    if self.Trigger_Template is None :
      """
      for i, Signal in enumerate ( self.Real_Signal_Total ) :
        ##X = range ( 0, len(Signal), 10 )
        X = range ( 0, len(Signal) )
        self.Plot_1.plot( x=X, y=Signal, clear = (i==0),
           pen = pg.mkPen ( (0,0,255), width = 1 ))
      """
      pass
    else :
      self._Write_Trigger_Template ()

      for Channel in range ( self.N_Trace ) :
        self._Get_Trigger_Index ( Channel, Plot=True )

      for Channel in range ( len (self.Raw_Signals)-1, -1, -1 ):
        Line, HexLine = self._Decode ( self.Raw_Signals [ Channel ], Channel )
        self.Memo_Measure.append ('DECODED %s : %s' % ( Channel, HexLine ))
      self.Memo_Measure.append ('')
      self.Memo_Measure.moveCursor ( QtGui.QTextCursor.End )

    self.Plot_1.addItem ( self.Region_1, ignoreBounds = True )

    self.Plot_1.addItem ( self.vLine_1, ignoreBounds=True)
    self.Plot_1.addItem ( self.hLine_1, ignoreBounds=True)

  # **********************************************************************
  def _Write_Trigger_Template ( self ) : ## self, event = None ) :
    i = self.Radio_Trigger_Level.GetValue()
    #'''  FFWEG
    Trigger_Level = self.Trigger_Level_Values [i]

    # PT2262-Sync
    if Trigger_Level == -1 :
      self.Memo_Measure.append ( 'PT 2262 Syncbit Trigger' )
      self.Memo_Measure.append ( '   Negative Long Sync = %s [us]' % (10*self.Packet_SyncWidth) )
      self.Memo_Measure.append ( '            Packet Length = %s [us]' % (10*self.Packet_Length))
      self.Memo_Measure.append ( '' )

    # Normal trigger
    elif Trigger_Level > 0 :
      print (self.Trigger_Template, self._Decode)
      Line, HexLine = self._Decode ( self.Trigger_Template, Separator='_' )

      Pre_Line = ''
      for x in self.Pre_Decode :
        if x == self.TLow : Pre_Line += '0'
        else              : Pre_Line += '1'
      N = len ( Pre_Line )
      Line = N*'_' + Line [N:]

      self.Memo_Measure.append ( '        Pre-Decode : %s' % Pre_Line    )
      self.Memo_Measure.append ( 'Trigger-Template : %s' % Line    )
      self.Memo_Measure.append ( '     HEX decoded : %s' % HexLine )
      self.Memo_Measure.append ( '' )
    #'''

  # **********************************************************************
  def _On_Edit_Regs ( self, event = None ) :
    Value_1C = self.Edit_1C.GetValue ()
    print ( "VALUE_1C =", Value_1C )
    print ( "VALUE_1C =", eval( "0x" + Value_1C ) ) 
    
  # **********************************************************************
  def _On_Edit_Pre_Decode ( self, event = None ) :
    Pre_Decode = self.Edit_Pre_Decode.GetValue ()
    self.Pre_Decode = []
    for x in Pre_Decode :
      if x in '0Ss' : self.Pre_Decode.append ( self.TLow  )
      if x in '1Ll' : self.Pre_Decode.append ( self.THigh )

    Value = self.Edit_Trig_Sync_Width.GetValue ()
    try :
      self.Packet_SyncWidth = int ( Value ) / 10
    except :
      self.Edit_Trig_Sync_Width.SetValue ( '%i' % (10* self.Packet_SyncWidth ))
      #traceback.print_exc()
      pass

    Value = self.Edit_Trig_Packet_Length.GetValue ()
    try :
      self.Packet_Length = int ( Value ) / 10
    except :
      self.Edit_Trig_Packet_Length.SetValue ( '%i' % (10* self.Packet_Length ))

      #traceback.print_exc()
      pass


    # If frozen, redisplay the trigger and signals decoding
    if self.Freeze :
##      self._Write_Trigger_Template ()
      self._Do_Freeze ()

  # **********************************************************************
  def _On_Mouse_Hoover_1 ( self, evt):
    if not self.Freeze :
      return
    if self.Plot_1.sceneBoundingRect().contains ( evt ) :
      mousePoint = self.Plot_1.plotItem.vb.mapSceneToView ( evt )

      self.crosshair_x = mousePoint.x()
      self.crosshair_y = mousePoint.y()

      minX, maxX = self.Region_1.getRegion()
      Delta      = mousePoint.x() - minX

      self.Measure_Label_1.setText (
        """<center>
           <span style='font-size: 12pt; color: red'>  Channel = %s,
           <span style='color: black'>                 Region = %s [us],</span>
           <span style='color: blue'>                  Crosshair = %s [us]</span>
           <span style='color: red'>                   Frequency = %.3f [kHz]</span>
           </center>""" % (
           int(mousePoint.y()),
           int ( maxX-minX ),
           int(Delta),
           1000.0 / Delta
            ))

      self.vLine_1.setPos ( int(mousePoint.x()) )
      self.hLine_1.setPos ( int(mousePoint.y()) )

  # *************************************************************
  # Selection in upper plot determines trigger signal
  # *************************************************************
  def _Region_Shifted_1 ( self ) :
    if self.Freeze :
      self.Region_minX, self.Region_maxX = self.Region_1.getRegion()

  # *************************************************************
  # Selection in lower plot will be shown in upper plot
  # *************************************************************
  def _Region_Shifted ( self ) :
    if self.Freeze :
      self.Region_2.setZValue ( 10 )
      minX, maxX = self.Region_2.getRegion()

      # extra trick to get resizing of the  region working
      self.Weird_Hold_Region = True
      self.Plot_1.setXRange ( minX+1, maxX+1, padding=0 )
      self.Plot_1.setXRange ( minX, maxX, padding=0 )

  # *************************************************************
  # Shifting of upper plot will move the region in lower plot
  # *************************************************************
  def _Shift_Region ( self, window, viewRange ) :
    # extra trick to get resizing of the  region working
    if self.Weird_Hold_Region :
      self.Weird_Hold_Region = False
      return

    if self.Freeze :
      # the first time viewRange is a PySide.QtCore.QRect
      try :
        Region = viewRange[0]
        self.Region_2.setRegion ( Region )
      except :
        pass


  # **********************************************************************
  """
  def _On_Close ( self, event = None ) :

    IniFile = self.wxGUI.IniFile
    IniFile.Section = 'Trigger'
    IniFile.Write ( 'Pulse_Treshold', self.Pulse_Treshold )
    IniFile.Write ( 'Pulse_Ignore_Low', self.Pulse_Ignore_Low )
    IniFile.Write ( 'Pulse_Ignore_High', self.Pulse_Ignore_High )
    IniFile.Write ( 'TLow', self.TLow )
    IniFile.Write ( 'THigh', self.THigh )

    IniFile.Write ( 'E', self.Trigger_Template )

    # type <type 'numpy.int32'> is written as a string
    IniFile.Write ( 'Trigger_Sum', int ( self.Trigger_Sum ) )

    SI4432_Base._On_Close ( self )
"""

# *****************************************************************************
# *****************************************************************************
if __name__ == '__main__':
  My_Main_Application ( Stream_Viewer )

