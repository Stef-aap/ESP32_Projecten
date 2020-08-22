# -*- coding: utf-8 -*-
##from __future__ import unicode_literals   # program crashes !!!!

_Version_Text = [
[ 0.1 , '24-11-2014', 'Stef Mientki',
'Test Conditions:', (),
"""
Initial Release
"""]
]

import __init__
from   SI4432_support  import *

# *****************************************************************************
# search for the correct CommPort
# *****************************************************************************
Filename = Base_GUI.Create_IniFileName ()
Get_CommPort ( Filename )


# *****************************************************************************
class WS3000 ( SI4432_Base ):
  #
  def __init__ ( self, IniFile = None ):
    SI4432_Base.__init__ ( self )

    Title = 'JAL:    WS-3000 Weather Station  (version %s)' % _Version_Text[0][0]

    GUI = """
  self.Main_Window ,MainWindow  ,label = Title
    self.Main_Window2 ,PanelVer    ,label= 'Test QT'
      self.Splitter    ,X,SplitterHor
        PanelVer

          self.Label_ID     ,Label
          self.Memo         ,TextCtrl

          PanelHor
            Button  ,label= '0x90'     ,bind = self._On_X90
            Button  ,label= '0x91'     ,bind = self._On_X91
            Button  ,label= '0x92'     ,bind = self._On_X92
            Button  ,label= '0x93'     ,bind = self._On_X93
            Button  ,label= '0x94'     ,bind = self._On_X94

          PanelHor
            self.RS232_Conn      ,Button  ,label='???'   ,bind = self._On_Connect
            Button                        ,label='Reset' ,bind = self._On_Reset
            self.Button_OK_Test  ,Button  ,label='OK ?'  ,bind = self._On_OK_Test
            self.Button_Busy     ,Button  ,label='Busy'

        self.Plot_Splitter         ,X,SplitterVer
          self.Plot_Window_1         ,PanelVer
            self.Measure_Label_1       ,Label
          self.Plot_Window_2         ,PanelVer
            self.Measure_Label_2       ,Label
    """
    self.wxGUI = Create_GUI ( GUI , IniFile, Icon = 'vippi_bricks.png' )
    self.Memo.moveCursor ( QtGui.QTextCursor.End )

    self.Help_File      = 'si4432_ws3000_hack.html'
    self.Program_Number = 0xF7

    self.Memo.clear()
    #self.Memo.append ( 'StartTime = %s' % time() )
    self.Memo.append ( dt.now().strftime ( 'start: %d-%m-%Y   %H:%M') )

    self.Data          = ''
    self.Signal_Temperature = []
    self.Signal_Humidity    = []
    self.Signal_WindSpeed   = []
    self.Signal_RainFall    = []
    self.Signal_N_Total     = []
    self.Signal_N_Good      = []
    self.Signal_N_Wrong     = []
    self.Signal_RSSI        = []

    self.Last_Time          = 0
    self.X_Axis             = []

    # *************************************************
    self.Plot_1 = pg.PlotWidget()
    self.Plot_1.showGrid ( x=True, y=True, alpha = 0.7 )

    c = 20
    Axis_Color = ( c, c, c )
    self.Plot_1.getAxis ( 'bottom' ).setPen ( Axis_Color )
    self.Plot_1.getAxis ( 'left'   ).setPen ( Axis_Color )

    c = 220
    BG_Color = ( c, c, c )
    BG_Color = ( 212, 208, 200 )
    self.Plot_1.setBackground ( BG_Color )

    #cross hair
    self.vLine_1 = pg.InfiniteLine ( angle=90, movable=False, pen = pg.mkPen((255,0,0)))
    self.hLine_1 = pg.InfiniteLine ( angle=0,  movable=False, pen = pg.mkPen((255,0,0)))
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

    #cross hair
    self.vLine_2 = pg.InfiniteLine ( angle=90, movable=False, pen = pg.mkPen((255,0,0)))
    self.hLine_2 = pg.InfiniteLine ( angle=0,  movable=False, pen = pg.mkPen((255,0,0)))
    # *************************************************

    # Add plots to the GUI
    self.Plot_Window_1.SBox.addWidget ( self.Plot_1 )
    self.Plot_Window_2.SBox.addWidget ( self.Plot_2 )

    self.Plot_1.scene().sigMouseMoved.connect ( self._On_Mouse_Hoover_1 )
    self.Plot_2.scene().sigMouseMoved.connect ( self._On_Mouse_Hoover_2 )

    # **********************************************
    # Get the settings from the GUI and set the SI4432 accordingly
    # **********************************************
    self.Post_Init ()

  # *************************************************************
  def _Update_Plot ( self, Data ) :
    self.Data += Data

    if self.State_Receive == 0 :
      # after reset, wait till register dump has finished
      if len ( self.Data ) < 134 :
        return
      self.Data = self.Data [ 134: ]
      self.State_Receive = 1

    if self.State_Receive > 0 :
      # skip Data until start sequence
      x0 = self.Data.find ( '\xCC\xBB\xAA' )
      if x0 < 0 :
        self.Data = ''
      elif x0 > 0 :
        self.Data = self.Data [ x0: ]

      # ************************************************
      # process all complete samplesets (each 14 bytes)
      # ************************************************
      while len ( self.Data ) >= 14 :
        New_Moment = True
        Nu = time ()
        if Nu - self.Last_Time > 1000 :
          self.Last_Time = Nu
        elif Nu - self.Last_Time < 40 :
          New_Moment = False
        self.Last_Time = Nu

        if New_Moment :
          # redraw the plots
          self.X_Axis = range ( len ( self.Signal_RSSI ) )
          self.Plot_1.plot( x=self.X_Axis,  y=self.Signal_Temperature, clear=True,
                            pen = pg.mkPen ( (255,0,0), width = 2 ) )
          self.Plot_1.plot( x=self.X_Axis,  y=self.Signal_Humidity, clear=False,
                            pen = pg.mkPen ( (0,0,255), width = 2 ) )
          self.Plot_1.plot( x=self.X_Axis,  y=self.Signal_WindSpeed, clear=False,
                            pen = pg.mkPen ( (0,0x80,0), width = 2 ) )
          self.Plot_1.plot( x=self.X_Axis,  y=self.Signal_RainFall, clear=False,
                            pen = pg.mkPen ( (0x99,0x32,0xCC), width = 2 ) )

          self.Plot_2.plot( x=self.X_Axis,  y=self.Signal_N_Good, clear=True,
                            pen = pg.mkPen ( (0,0x80,0), width = 2 ) )
          self.Plot_2.plot( x=self.X_Axis,  y=self.Signal_N_Wrong, clear=False,
                            pen = pg.mkPen ( (255,0,0), width = 2 ) )
          self.Plot_2.plot( x=self.X_Axis,  y=self.Signal_RSSI, clear=False,
                            pen = pg.mkPen ( (0,0,255), width = 2 ) )

          self.Plot_1.addItem ( self.vLine_1, ignoreBounds=True)
          self.Plot_1.addItem ( self.hLine_1, ignoreBounds=True)
          self.Plot_1.enableAutoRange()

          self.Plot_2.addItem ( self.vLine_2, ignoreBounds=True)
          self.Plot_2.addItem ( self.hLine_2, ignoreBounds=True)
          self.Plot_2.enableAutoRange()

          self.Signal_Humidity   .append ( 0 )
          self.Signal_N_Good     .append ( 0 )
          self.Signal_N_Total    .append ( 0 )
          self.Signal_N_Wrong    .append ( 0 )
          self.Signal_RainFall   .append ( 0 )
          self.Signal_RSSI       .append ( 0 )
          self.Signal_Temperature.append ( 0 )
          self.Signal_WindSpeed  .append ( 0 )

        Index = len ( self.Signal_N_Total ) - 1

        Values = np.frombuffer ( self.Data[3:14], 'uint8' )
        self.Data = self.Data [ 14: ]

        # check CRC
        self.Signal_N_Total [ Index ] += 1
        CRC_OK = Values [ 8 ] == Values [ 9 ]

        if CRC_OK :
          if self.Signal_N_Good [Index ] < 8 :
            self.Signal_N_Good [ Index ] += 1
        else :
          self.Signal_N_Wrong [ Index ] += 1

        print '------',
        for i in range ( 11 ) :
          print hex (Values[i]),
        print

        # Sensor Information
        if ( Values[0] & 0xF0 ) == 0x50 :
          # as long as no data filled, fill it now
          if CRC_OK and self.Signal_RSSI [ Index ] == 0 :
            ID = 16 * ( Values[0] & 0x0F ) + ( Values[1] & 0xF0) /16
            ##print 'ID = ', hex (ID)
            self.Label_ID.SetValue ( 'ID = %s' % hex ( ID ))
            self.Signal_RSSI        [ Index ] = Values[10]/20.0
            self.Signal_Temperature [ Index ] = 25.6 * ( Values[1] & 0x0F ) + Values[2]/10.0
            self.Signal_Humidity    [ Index ] = Values[3]/10.0
            self.Signal_WindSpeed   [ Index ] = 1.22 * Values[4]
            self.Signal_RainFall    [ Index ] = \
              0.3 * ( ( 256 * ( Values[6] & 0x0F ) + Values[7] ) - 0x30C )

        # Time Information
        elif CRC_OK and ( Values[0] & 0xF0 ) == 0x60 :
          print 'XXXX',
          for i in range ( 11 ) :
            print hex (Values[i]),
          print
          # as long as no data filled, fill it now
          #if CRC_OK and self.Signal_RSSI [ Index ] == 0 :
          Hour   = BCD ( Values[2] & 0x3F )
          Minute = BCD ( Values[3]        )
          Second = BCD ( Values[4]        )
          Year   = BCD ( Values[5]        ) + 2000
          Month  = BCD ( Values[6] & 0x1F )
          Day    = BCD ( Values[7]        )
          TimeStamp = dt ( Year, Month, Day, Hour, Minute, Second )
          ##dt.now().strftime ( '%d-%m-%Y')
          self.Memo.append ( dt.now().strftime ( '%d-%m-%Y   %H:%M') )
        else :
          print 'zzzzzXXXX',
          for i in range ( 11 ) :
            print hex (Values[i]),
          print


  # **********************************************************************
  def _On_Mouse_Hoover_1 ( self, evt):
    if self.Plot_1.sceneBoundingRect().contains ( evt ) :
      mousePoint = self.Plot_1.plotItem.vb.mapSceneToView ( evt )
      x = mousePoint.x()
      for i, X in enumerate ( self.X_Axis ) :
        if X >= x :
          break
      else :
        return

      self.Measure_Label_1.setText (
        """<center><b>
           <span style='font-size: 12pt; color: black'>  x=%i,
           <span style='color: red'>                     Temp=%0.1f Celcius, </span>
           <span style='color: blue'>                    Humidity=%i %%, </span>
           <span style='color: green'>                   Wind=%i m/s, </span>
           <span style='color: #9932CC'>                 Rain=%i mm</span>
           </b></center>""" % (
          mousePoint.x(),
          self.Signal_Temperature [i],
          10*self.Signal_Humidity [i],
          self.Signal_WindSpeed   [i],
          self.Signal_RainFall    [i] ))

      self.vLine_1.setPos ( mousePoint.x() )
      self.hLine_1.setPos ( mousePoint.y() )

  # **********************************************************************
  def _On_Mouse_Hoover_2 ( self, evt):
    if self.X_Axis and self.Plot_2.sceneBoundingRect().contains ( evt ) :
      mousePoint = self.Plot_2.plotItem.vb.mapSceneToView ( evt )
      x = mousePoint.x()
      for i, X in enumerate ( self.X_Axis ) :
        if X >= x :
          break
      else :
        return

      self.Measure_Label_2.setText (
        """<center><b>
           <span style='font-size: 12pt; color: black'>  x=%i,
           <span style='color: green'>                   NGood=%i, </span>
           <span style='color: red'>                     NWrong=%i, </span>
           <span style='color: blue'>                    RSSI=%i</span>
           </bold></center>""" % (
           mousePoint.x(),
           self.Signal_N_Good    [i],
           self.Signal_N_Wrong   [i],
           10 * self.Signal_RSSI [i] ))

      self.vLine_2.setPos ( mousePoint.x() )
      self.hLine_2.setPos ( mousePoint.y() )

# *****************************************************************************
# *****************************************************************************
if __name__ == '__main__':
  My_Main_Application ( WS3000 )
  sys.exit()

