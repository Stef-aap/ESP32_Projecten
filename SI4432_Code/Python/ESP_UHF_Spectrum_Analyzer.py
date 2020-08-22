# -*- coding: utf-8 -*-

# *****************
# 11 juni 2020, calendar uitgeschakeld, import wx.calendar" geeft problemen onder Fedora Py27
# *****************

_Version_Text = [

[ 1.0 , '13-8-2020', 'Stef Mientki',
'Test Conditions:', (),
"""
Initial Release for Python 3 + PySide2
"""]
]

import sys
sys.dont_write_bytecode = True  # prevent generation of PYC files
from   SI4432_support  import *

# *****************************************************************************
# search for the correct CommPort
# *****************************************************************************
ID_String = b'\xAA\xBB\xC0'
Filename = Base_GUI.Create_IniFileName ()
Get_CommPort (  ID_String, Filename )
sleep ( 5 )

Sweep_Start_Freq = 200 * MEGA  ##200000000
# *****************************************************************************
class Spectrum_Analyzer ( SI4432_Base ):
  #
  def __init__ ( self, IniFile = None ):
    SI4432_Base.__init__ ( self )

    FSteps = '156 Hz,312 Hz,625 Hz,1250 Hz,2.5 kHz,5 kHz,10 kHz,20 kHz,50 kHz,100 kHz,200 kHz,500 kHz,1 MHz,2 MHz'.split(',')
    self.FSteps = [ 156, 312, 625, 1250, 2500, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000 ]

    FBW    = '2 kHz,5 kHz,10 kHz,20 kHz,50 kHz,100 kHz,200 kHz,500 kHz'.split(',')
    self.FBW = [ 2000, 5000, 10000, 20000, 50000, 100000, 200000,500000 ]

    Y_Range = '60 dB,80 dB,100 dB,120 dB'.split(',')
    self.Y_Range = [ 60, 80, 100, 120 ]

    self.Display_Mode = 'Last,Average,Max,Min,Smart'.split(',')
    self.NSamps = 'NSamp = 10,NSamp = 20,NSamp = 30,NSamp = 40,NSamp = 50'.split(',')

    Title = 'JAL:    UHF Spectrum Analyzer  (version %s)' % _Version_Text[0][0]

    GUI = """
  self.Main_Window ,MainWindow  ,label = Title
    self.Main_Window2 ,PanelVer    ,label= 'Test QT'
      self.Splitter    ,X,SplitterHor
        PanelVer

          PanelHor
            self.Radio_FStep  ,RadioBox  ,label='Step Frequency' ,choices = FSteps, majorDimension=1, bind=self._On_Radio_FStep, clicked=self._On_Radio_FStep
            PanelVer
              self.Radio_FBW    ,RadioBox  ,label='IF Bandwidth'   ,choices = FBW   , majorDimension=1, bind=self._On_Radio_FBW
              self.Radio_Y_Range,RadioBox  ,label='Display Range'  ,choices = Y_Range, bind=self._On_Radio_Y_Range
            PanelVer
              self.Radio_NSamp        ,RadioBox  ,label='NSamp' ,choices = self.NSamps, bind=self._On_Radio_NSamp
              self.Radio_Display_Mode ,RadioBox  ,label='Display Mode' ,choices = self.Display_Mode, bind=self._On_Radio_Display_Mode

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

          PanelHor
            Label                  ,label='Start    Freq [MHz]  '
            self.Edit_Freq_Start   ,LineEdit, bind = self._On_Edit_Start
          PanelHor
            Label                  ,label='End      Freq [MHz]  '
            self.Edit_Freq_End     ,LineEdit, bind = self._On_Edit_Start
          PanelHor
            Label                  ,label='Center Freq [MHz]  '
            self.Edit_Freq_Center  ,LineEdit, bind = self._On_Edit_Start

          self.Memo         ,TextCtrl

          PanelHor
            self.Button_Snapshot, Button  ,label= 'SnapShot'   ,bind = self._On_SnapShot
            self.Button_Freeze,   Button  ,label= 'Freeze'     ,bind = self._On_Freeze
            self.Button_Sweep,    Button  ,label= 'Full Sweep' ,bind = self._On_Full_Sweep
            self.Button_Search,   Button  ,label= 'Search'     ,bind = self._On_Search

        self.Plot_Splitter         ,X,SplitterVer
          self.Plot_Window_1         ,PanelVer
            self.Measure_Label_1       ,Label
          self.Plot_Window_2         ,PanelVer
            self.Measure_Label_2       ,Label
    """
    self.wxGUI = Create_GUI ( GUI , IniFile, Icon = 'vippi_bricks.png' )

    MB = self.Main_Window.menuBar()

    MB_File = MB.addMenu ( '&File' )
    MB_File.addAction ( 'Save Recording', self._On_Save_Recording )
    MB_File.addAction ( 'Load Recording', self._On_Load_Recording )

    #MB_Settings = MB.addMenu ( '&Settings' )
    #MB_Settings.addAction ( 'Settings', self._On_Settings )

    MB_Help = MB.addMenu('&Help')
    MB_Help.addAction ( 'Spectrum Analyzer (F1)', self._On_Help_Spectrum_Analyzer )
    MB_Help.addAction ( 'Dutch Frequencies (Shift_F1)', self._On_Help_Dutch_Frequencies )

    Bind = self.Main_Window.Bind
    Bind ( 'F1', self._On_Help_Spectrum_Analyzer )
    Bind ( 'shift+F1', self._On_Help_Dutch_Frequencies )

    self.Memo.clear()

    self.ID_String   = ID_String

    # some values we need for the serial processing
    self.NStep       = 256
    self.Freeze      = False
    self.Search      = False
    self.Search_Mean = 0
    self.Search_Time = perf_counter  #clock ()
    ##self.Search_Count = 0          ## <<<<<<<< TEMP

    self.Real_Signal_1 = []
    self.Real_Signal_2 = []
    self.X_Axis_2 = []

    self.Sweep_Full = 0
    self.Sweep_Region = None
    self.Weird_Hold_Region = False

    #self.Center_Freq = 433920
    self.Freq_Start  = 421120000
    self.Freq_Step   = 100000
    self.BW          = 10000
    self.NSamp       = 10
    self.X           = 5
    self.Mode        = 1

    # *************************************************
    # Define X-Axis in kHz
    # *************************************************
    self.X_Axis_1 = []
    for i in range ( self.NStep ) :
      self.X_Axis_1.append (( self.Freq_Start + i * self.Freq_Step ) / 1000000.0 )

    # *************************************************
    self.Plot_1 = pg.PlotWidget( )
    self.Plot_1.showGrid ( x=True, y=True, alpha = 0.7 )

    c = 20
    Axis_Color = ( c, c, c )
    self.Plot_1.getAxis ( 'bottom' ).setPen ( Axis_Color )
    self.Plot_1.getAxis ( 'left'   ).setPen ( Axis_Color )

    c = 220
    BG_Color = ( c, c, c )
    BG_Color = ( 212, 208, 200 )
    self.Plot_1.setBackground ( BG_Color )

    ##self._On_Radio_Y_Range ()
    ##self.Plot_1.setYRange ( 0.0, 170.0 )

    #cross hair
    self.vLine_1 = None
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

    self._On_Radio_Y_Range ()
    ##self.Plot_2.setYRange ( 0.0, 170.0 )

    # *************************************************

    # Add plots to the GUI
    self.Plot_Window_1.SBox.addWidget ( self.Plot_1 )
#    self.Plot_Window_2.SBox.addWidget ( self.Plot_1 )
    self.Plot_Window_2.SBox.addWidget ( self.Plot_2 )

    self.Plot_1.scene().sigMouseMoved.connect ( self._On_Mouse_Hoover_1 )
    self.Plot_2.scene().sigMouseMoved.connect ( self._On_Mouse_Hoover_2 )

    # **********************************************
    # Get the settings from the GUI and set the SI4432 accordingly
    # **********************************************
    self.Post_Init ()


    # *********************************************
    # Visual settings may need serial communication
    # so be sure the threading is started
    # *********************************************
    My_Sleep ( 3 )

    if not  self.Radio_FBW.GetValue() :
      self.Radio_FBW.SetValue ( 5 )
    self._On_Radio_FBW ()
    My_Sleep ( 1 )

    if not  self.Radio_Display_Mode.GetValue() :
      self.Radio_Display_Mode.SetValue ( 1 )
    self._On_Radio_Display_Mode ()
    My_Sleep ( 1 )

    if not  self.Radio_NSamp.GetValue() :
      self.Radio_NSamp.SetValue ( 0 )
    self._On_Radio_NSamp ()
    My_Sleep ( 1 )

    if not  self.Radio_Y_Range.GetValue() :
      self.Radio_Y_Range.SetValue ( 0 )
    self._On_Radio_Y_Range ()
    My_Sleep ( 1 )

    i = self.Radio_FStep.GetValue()
    if not i : i = 9
    self.Radio_FStep.SetValue ( i )
    self.Freq_Step = self.FSteps [i]
    My_Sleep ( 1 )

    ##self._Send_Freq ( self.Freq_Start )
    self._Display_Settings ()
    self._On_Edit_Start ()

  # *************************************************************
  def _Completion_0x00 ( self, Data ):
    self.Data_Bytes += Data 
    if len ( self.Data_Bytes ) > 256+6 :
      # ***************************************
      # if no start sequence, keep last 3 bytes (might contain part of a start sequence)
      # ***************************************
      x1 = self.Data_Bytes.find ( b'\xAA\xBB\xCC' )
      if x1 < 0 :
        print ( self.Data_Bytes [ :-3] )
        self.Data_Bytes = self.Data_Bytes [-3:]
        return 

      # ***************************************
      # skip tail of the previous and wait till complete block
      # ***************************************
      self.Data_Bytes = self.Data_Bytes [ x1 : ]
      if len ( self.Data_Bytes ) < 256+6 : 
        return
       
      # ***************************************
      # now we have enough, so we should see 2 start sequences
      # ***************************************
      x1 = self.Data_Bytes.find ( b'\xAA\xBB\xCC', 3 )
      #print ( "Completion0, should give 259", x1 )
      
      # ***************************************
      # if block has correct length, plot the data
      # ***************************************
      New = False
      if x1 == 259 :
        self.Real_Signal_1 = np.frombuffer ( self.Data_Bytes[3:256+3], 'uint8' )
        New = True
        print ( "jopeie", len ( self.Data_Bytes ) )


        if not self.Freeze and self.Sweep_Full in [0,2] :
          self.vLine_1 = None
    
          ###self.Real_Signal_1 = np.frombuffer ( self.Data_Bytes[3:256+3], 'uint8' )
          self.Real_Signal_1 = self.Real_Signal_1 / 2.0
          if len ( self.Real_Signal_1 ) > 100 :
            self.Plot_1.plot( x=self.X_Axis_1,  y=self.Real_Signal_1, clear = True,
                            pen = pg.mkPen ( (0,0,255), width = 2 ) )
    
          self.Plot_1.setXRange ( self.X_Axis_1[0], self.X_Axis_1[-1], padding=0 )
          ##self.Plot_1.disableAutoRange()
          
          # ****************************
          # Search Mode
          # ****************************
          if self.Search :
            print ( "searching" ) 
            ##self.Search_Count += 1
            ##if self.Search_Count < 20 :
            if not self.Search_Mean :
              for Sample in self.Real_Signal_1 :
                self.Search_Mean += Sample
              self.Search_Mean = self.Search_Mean / len ( self.Real_Signal_1 )
              self.Search_Time = perf_counter()   #clock ()
            else :
              for Sample in self.Real_Signal_1 :
                if Sample > self.Search_Mean + 10 :
                  Now = perf_counter ()   #clock()
                  Delta = Now - self.Search_Time
                  self.Memo.append ( 'DeltaTime = %s' % Delta )
                  self.Search_Time = Now
        
                  ##self._On_SnapShot ()
                  self._On_SnapShot_Action()
                  break
    
        # ****************************
        # Full Sweep is building up
        # ****************************
        elif self.Sweep_Full == 1 :
          self.Sweep_Signal = np.append ( self.Sweep_Signal, self.Real_Signal_1 )
    
          if self.Sweep_SubBand < 3 :
            self.Sweep_SubBand += 1
    
            self.Freq_Start = Sweep_Start_Freq +\
                              self.Sweep_Band * 100 * MEGA +\
                              250 * self.Sweep_SubBand * self.Freq_Step
            self._Send_Freq ( self.Freq_Start )

            # ************************************************
            # Hier moet iets mee, hoe voorkom je oude data !!
            # ************************************************
            x1 = len ( self.Data_Bytes ) - 6
            My_Sleep ( 1 )
            #WEG??self.text = b''
              
    
          else :
            if self.Sweep_Band < 6 : ##6 :
              self.Sweep_Band       += 1
              self.Sweep_SubBand     = 0
    
              self.Freq_Start = Sweep_Start_Freq +\
                                self.Sweep_Band * 100 * MEGA
              self._Send_Freq ( self.Freq_Start )

              # ************************************************
              # Hier moet iets mee, hoe voorkom je oude data !!
              # ************************************************
              x1 = len ( self.Data_Bytes ) - 6
              My_Sleep ( 2 )
              ###WEG?self.text = b''
    
            else :
              # *************************************
              # Here we've the full scan
              # *************************************
              self.Sweep_Signal = self.Sweep_Signal / 2.0
              self.X_Axis_Sweep = []
              for i in range ( len ( self.Sweep_Signal )) :
                self.X_Axis_Sweep.append (( 250 * MEGA + i * self.Freq_Step ) / 1E6 )
              self.Plot_1.plot( x=self.X_Axis_Sweep,  y=self.Sweep_Signal, clear = True,
                                pen = pg.mkPen ( (0,0,255), width = 2) )
    
              if not self.vLine_1 :
                self.vLine_1 = pg.InfiniteLine ( angle=90, movable=False, pen = pg.mkPen((255,0,0)))
                self.hLine_1 = pg.InfiniteLine ( angle=0,  movable=False, pen = pg.mkPen((255,0,0)))
                self.Plot_1.addItem ( self.vLine_1, ignoreBounds=True)
                self.Plot_1.addItem ( self.hLine_1, ignoreBounds=True)
    
              self.X_Axis_1 = self.X_Axis_Sweep
              self.Real_Signal_1 = self.Sweep_Signal
    
              ##self._On_SnapShot ()
              self._On_SnapShot_Action ()
    
              self.Sweep_Full = 2
    
              # ******************************
              # selection in bottom plot will be shown in upper plot
              # ******************************
              ##if not self.Sweep_Region :
              self.Sweep_Region = pg.LinearRegionItem()
              self.Sweep_Region.setZValue(10)
              # Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
              # item when doing auto-range calculations.
              self.Plot_2.addItem ( self.Sweep_Region, ignoreBounds = True )
              self.Sweep_Region.sigRegionChanged.connect ( self._Region_Shifted )
              ##else :
              ##  self.Sweep_Region.show()
    
              self.Sweep_Region.setRegion ( [ 300, 350 ] )
              # ******************************
    
              # *********************************************************
              # shift of the upper plot will adapt the selection in bottom plot
              # *********************************************************
              self.Plot_1.sigRangeChanged.connect ( self._Shift_Region )
              ##self.Plot_1.setAutoVisible(y=True) helpt niet
              # *********************************************************
          
      #else :
      #  print ( self.Data_Bytes [ :x1] )
        
      # ***************************************
      # FINALLY remove the block (either just handled or ignored)
      # ***************************************
      self.Data_Bytes = self.Data_Bytes [ x1: ]
      
  # *************************************************************
  def _On_Full_Sweep ( self, event = None ) :
    # ask for extra confirmation
    if self.Sweep_Full == 0 :
      Question = 'Are you sure you want to perform a full scan ?'
    else :
      Question = 'Are you sure you want to go back to the Normal Mode ?'
    Result = AskYesNo ( Question, Title = 'Switch Global Mode' )
    if not Result :
      return

    # Going into Full Sweep Mode
    if self.Sweep_Full == 0 :
      # change Button functions
      self.Button_Snapshot.setText ( 'Refresh' )
      self.Button_Freeze.setText ( 'Life' )
      self.Button_Sweep.setText ( 'Normal' )
      #self.Button_Zoom.setText ()

    # Going back to Normal Mode
    else :
      self.Button_Snapshot.setText ( 'SnapShot' )
      self.Button_Freeze.setText ( 'Freeze' )
      self.Button_Sweep.setText ( 'Full Sweep' )
      self.Sweep_Region.hide ()

    if self.Sweep_Full == 0 :
      print ('FULL SWEEP')
      self.Freeze = True

      self.Sweep_Band       = 0
      self.Sweep_SubBand    = 2

      self.Freq_Step  = 100 * KILO ##100000
      self.Freq_Start = 250 * MEGA ##250000000
      self._Send_Freq ( self.Freq_Start )

      self.Sweep_Signal = np.asarray ( [] )
      My_Sleep ( 5 )
      ###WEG? self.text = b''

      self.Sweep_Full = 1
      self._Enable_Controls ()

    else :
      # goto Normal Mode
      self.Sweep_Full = 0
      self.Freeze     = 0
      self._Enable_Controls ()
      self._On_Edit_Start ()


  # *************************************************************
  def _On_SnapShot ( self, event = None ) :
    if self.Search and self.Search_Mean :
      # some special actions to recover from Search Mode
      self.Search      = False
      self.Button_Snapshot.setText ( 'SnapShot' )
      self.Button_Search.setText ( 'Search' )
      self.Button_Sweep.setDisabled ( False )
    self._On_SnapShot_Action ()

  # *************************************************************
  def _On_SnapShot_Action ( self, event = None ) :
    if self.Sweep_Full == 2 :
      if not self.Freeze :
        self.Freeze = True
      self._On_Freeze ()
      return

    self.X_Axis_2 = self.X_Axis_1
    self.Real_Signal_2 = self.Real_Signal_1
    if self.Sweep_Full == 0 and not self.Search : width = 2
    else                                        : width = 1
    if self.Search : Clear = False
    else           : Clear = True
    self.Plot_2.plot( x=self.X_Axis_2,  y=self.Real_Signal_2, clear = Clear,
                     pen = pg.mkPen ( (0,0,255), width = width ))
    self.Plot_2.setXRange ( self.X_Axis_2[0], self.X_Axis_2[-1], padding=0 )

    #cross hair
    if not self.Search :
      self.vLine_2 = pg.InfiniteLine ( angle=90, movable=False, pen = pg.mkPen((255,0,0)))
      self.hLine_2 = pg.InfiniteLine ( angle=0,  movable=False, pen = pg.mkPen((255,0,0)))
      self.Plot_2.addItem ( self.vLine_2, ignoreBounds=True )
      self.Plot_2.addItem ( self.hLine_2, ignoreBounds=True )


  # *************************************************************
  def _On_Freeze ( self, event = None ) :
    self.Freeze = not self.Freeze

    if self.Freeze :
      self.Button_Freeze.setText ( '   Life   ' )

      """
      # some special actions to recover from Search Mode
      self.Search      = False
      self.Button_Search.setText ( 'Search' )
      self.Button_Snapshot.setDisabled ( False )
      self.Button_Sweep.   setDisabled ( False )
      """

    else :
      self.Button_Freeze.setText ( 'Freeze' )


    if self.Freeze and not self.vLine_1 :
      self.vLine_1 = pg.InfiniteLine ( angle=90, movable=False, pen = pg.mkPen((255,0,0)))
      self.hLine_1 = pg.InfiniteLine ( angle=0,  movable=False, pen = pg.mkPen((255,0,0)))
      self.Plot_1.addItem ( self.vLine_1, ignoreBounds=True)
      self.Plot_1.addItem ( self.hLine_1, ignoreBounds=True)

    if not self.Freeze and self.Sweep_Full > 0 :
      minX, maxX = self.Sweep_Region.getRegion()
      print ('Band:', minX, maxX )
      self.Edit_Freq_Start.setText ( '%s' % ( minX ))
      self.Edit_Freq_End.setText (  '%s' % ( maxX ))
      self.Edit_Freq_Center.setText ( '' )
      self.Freeze = False
      self._On_Edit_Start ()

    if self.Freeze and self.Sweep_Full == 2 :
      #self.X_Axis_1 = self.X_Axis_Sweep
      #self.Real_Signal_1 = self.Sweep_Signal
      self.Plot_1.plot( x=self.X_Axis_Sweep,  y=self.Sweep_Signal, clear = True,
                        pen = pg.mkPen ( (0,0,255), width = 2 ) )
      self._Region_Shifted()

  # *************************************************************
  def _On_Search ( self ) :
    if not ( self.Search ) :
      # clear Plot_2
      self.X_Axis_2 = self.X_Axis_1
      self.Real_Signal_2 = self.Real_Signal_1
      self.Plot_2.plot( x=self.X_Axis_2,  y=self.Real_Signal_2, clear = True,
                       pen = pg.mkPen ( (0,0,255), width = 1 ))
      self.Plot_2.setXRange ( self.X_Axis_2[0], self.X_Axis_2[-1], padding=0 )
      ##self._On_SnapShot_Action ()

      self.Button_Search.setText ( '  .....  ' )
      self.Button_Snapshot.setText ( 'Normal' )
      ##self.Button_Snapshot.setDisabled ( True )
      self.Button_Sweep.setDisabled ( True )

    self.Search      = True
    self.Search_Mean = 0

  # **********************************************************************
  def _Display_Settings ( self ) :
    #if self.Sweep_Full > 0 :
    #  return

    # Define X-Axis in kHz
    self.X_Axis_1 =[]
    for i in range ( self.NStep ) :
      self.X_Axis_1.append (( self.Freq_Start + i * self.Freq_Step ) / 1000000.0 )

    self.Memo.clear()
    self.Memo.append ( 'Start    Frequency = %s MHz' % ( self.Freq_Start / 1E6) )
    self.Memo.append ( 'Center Frequency = %s MHz'   % ( self.Freq_Start / 1E6 + self.NStep * self.Freq_Step / 2E6 ))
    self.Memo.append ( 'End      Frequency = %s MHz' % ( self.Freq_Start / 1E6 + self.NStep * self.Freq_Step / 1E6 ))

  # **********************************************************************
  def _Send_Freq ( self, Value ) :
    SI4432_Base._Send_Freq ( self, Value )

    # Send the Frequency Step
    sleep ( 1 )
    FStep = self.FSteps.index ( self.Freq_Step )
    self.Thread.ser.write ( b'\xFA\xAF')
    self.Thread.ser.write ( [ FStep ] )

    self.Radio_FStep.Radio[FStep].setChecked(True)

    # Define X-Axis in kHz
    if not self.Freeze :
      self.X_Axis_1 = []
      for i in range ( self.NStep ) :
        self.X_Axis_1.append (( self.Freq_Start + i * self.Freq_Step ) / 1E6 )

    """
    print 'XXX Start Freq [MHz] = %s,  Step = %s [kHz],   End Freq = %s [MHz]' % (
      self.Freq_Start / 1E6, self.Freq_Step / 1E3,
      ( self.Freq_Start + 256 * self.Freq_Step ) / 1E6 )
    """

    self._Display_Settings ()

  # **********************************************************************
  def _Enable_Controls ( self ) :
    if self.Sweep_Full == 0 :
      Disable = self.Edit_Freq_Center.GetValue() == '' and\
                self.Edit_Freq_Start. GetValue() != '' and\
                self.Edit_Freq_End.   GetValue() != ''

      self.Radio_FStep.setDisabled ( Disable )

      Disable = False
      self.Edit_Freq_Start. setDisabled ( Disable )
      self.Edit_Freq_End.   setDisabled ( Disable )
      self.Edit_Freq_Center.setDisabled ( Disable )

    else :
      Disable = True
      self.Radio_FStep.     setDisabled ( Disable )
      self.Edit_Freq_Start. setDisabled ( Disable )
      self.Edit_Freq_End.   setDisabled ( Disable )
      self.Edit_Freq_Center.setDisabled ( Disable )

    QtCore.QCoreApplication.instance().processEvents ()

  # **********************************************************************
  def _On_Edit_Start ( self, event = None ) :
    print ( '<<<<< On Edit' )
    F_Start  = self.Edit_Freq_Start.GetValue ()
    F_End    = self.Edit_Freq_End.GetValue ()
    F_Center = self.Edit_Freq_Center.GetValue ()

    try :
      #*************************************
      # If a center frequency is specified we use that
      #*************************************
      if F_Center :
        Value = int ( float ( F_Center ) * 1000000 )
        self.Freq_Start = Value - ( self.NStep / 2 ) * self.Freq_Step

      #*************************************
      # Else If Start en End Frequencies are definied
      #*************************************
      elif F_End and F_Start :
        F_Start = int ( float ( F_Start ) * 1000000 )
        F_End   = int ( float ( F_End   ) * 1000000 )
        if F_End > F_Start :
          FStep = int ( round ( 1.0 * ( F_End - F_Start ) / self.NStep ))
          # Find the nearest step frequency larger or equal
          for i in range ( len ( self.FSteps )) :
            if self.FSteps [i] >= FStep :
              if i > 0 :
                if ( FStep - self.FSteps [i-1] ) < ( self.FSteps[i] - FStep ) :
                  i -= 1
              break
          else :
            return
          self.Freq_Step = self.FSteps [i]
          self.Freq_Start = F_Start

      #*************************************
      # Else If only a start Frequency is definied
      #*************************************
      elif F_Start :
        self.Freq_Start = int ( float ( F_Start ) * 1000000 )

      self.Freeze = False
      self.Freq_Start = int ( self.Freq_Start )
      self._Send_Freq ( self.Freq_Start )
    except :
      traceback.print_exc ()
      print ( '???', F_Start, F_End, F_Center ) #() )

    self._Enable_Controls()
    self._Display_Settings ()

  # **********************************************************************
  def _On_Radio_FStep ( self, event = None ) :
    i = self.Radio_FStep.GetValue()
    self.Freq_Step = self.FSteps [i]
    self._On_Edit_Start ()

  # **********************************************************************
  def _On_Radio_FBW ( self, event = None ) :
    i = self.Radio_FBW.GetValue()
    self.Thread.ser.write ( b'\xFA' )
    self.Thread.ser.write ( [i+0x10] )
    self._Display_Settings ()

  # **********************************************************************
  def _On_Radio_Display_Mode ( self, event = None ) :
    i = self.Radio_Display_Mode.GetValue()
    self.Thread.ser.write ( b'\xFA' )
    self.Thread.ser.write ( [i+0x80] )
    self._Display_Settings ()
    print ( "Set Mode =", i )

  # **********************************************************************
  def _On_Radio_Y_Range ( self, event = None ) :
    i = self.Radio_Y_Range.GetValue()
    if not i is None :
      self.YRange = self.Y_Range [i]
      self.Plot_1.setYRange ( 0.0, self.YRange )
      self.Plot_2.setYRange ( 0.0, self.YRange )

  # **********************************************************************
  def _On_Radio_NSamp ( self, event = None ) :
    i = self.Radio_NSamp.GetValue()
    self.Thread.ser.write ( b'\xFA' )
    self.Thread.ser.write ( [i+0x20] )
    self._Display_Settings ()
    print ( "Set NSample =", i )

  # **********************************************************************
  def _On_Mouse_Hoover_1 ( self, evt):
    if not self.Freeze or self.Sweep_Full == 1 :
      return
    if self.Plot_1.sceneBoundingRect().contains ( evt ) :
      mousePoint = self.Plot_1.plotItem.vb.mapSceneToView ( evt )
      ##index = int(mousePoint.x())
      x = mousePoint.x()
      for i, X in enumerate ( self.X_Axis_1 ) :
        if X >= x :
          break
      else :
        return

      try :    # i might not be valid
        self.Measure_Label_1.setText (
          """<center>
             <span style='font-size: 12pt; color: red'>  y=%0.1f,
             <span style='color: black'>                 Freq=%0.6f,</span>
             <span style='color: blue'>                  Signal=%0.1f</span>
             </center>""" % (
             mousePoint.y(), mousePoint.x(), self.Real_Signal_1[i]))
      except :
        pass
      self.vLine_1.setPos ( mousePoint.x() )
      self.hLine_1.setPos ( mousePoint.y() )

  # **********************************************************************
  def _On_Mouse_Hoover_2 ( self, evt):
    if self.Search :
      return

    if self.X_Axis_2 and self.Plot_2.sceneBoundingRect().contains ( evt ) :
      mousePoint = self.Plot_2.plotItem.vb.mapSceneToView ( evt )
      x = mousePoint.x()
      for i, X in enumerate ( self.X_Axis_2 ) :
        if X >= x :
          break
      else :
        return

      try :  # i might not be valid
        self.Measure_Label_2.setText (
        """<center>
           <span style='font-size: 12pt; color: red'>  y=%0.1f,
           <span style='color: black'>                 Freq=%0.6f,</span>
           <span style='color: blue'>                Signal=%0.1f</span>
           </center>""" % (
           mousePoint.y(), mousePoint.x(), self.Real_Signal_2[i]))
      except :
        pass

      self.vLine_2.setPos ( mousePoint.x() )
      self.hLine_2.setPos ( mousePoint.y() )

  # *************************************************************
  # Selection in lower plot will be shown in upper plot
  # *************************************************************
  def _Region_Shifted ( self ) :
    if self.Sweep_Full == 2  and self.Freeze :
      self.Sweep_Region.setZValue ( 10 )
      minX, maxX = self.Sweep_Region.getRegion()

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

    if self.Sweep_Full == 2 and self.Freeze :
      # the first time viewRange is a PySide.QtCore.QRect
      try :
        Region = viewRange[0]
        self.Sweep_Region.setRegion ( Region )
      except :
        pass

  # **********************************************************************
  def _On_Save_Recording ( self, event = None ) :
    pass

  # **********************************************************************
  def _On_Load_Recording ( self, event = None ) :
    pass

  # **********************************************************************
  def _On_Help_Spectrum_Analyzer ( self, event = None ) :
    url = 'http://mientki.ruhosting.nl/data_www/raspberry/doc/spectrum_analyzer.html'
    webbrowser.open ( url )

  # **********************************************************************
  def _On_Help_Dutch_Frequencies ( self, event = None ) :
    url = 'http://mientki.ruhosting.nl/data_www/raspberry/doc/Frequenties%20Nederland%20totaal.pdf'
    webbrowser.open ( url )


# *****************************************************************************
# *****************************************************************************
if __name__ == '__main__':
  My_Main_Application ( Spectrum_Analyzer )

