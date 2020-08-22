from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from builtins import chr
from builtins import str
from builtins import range
from past.builtins import basestring
from past.utils import old_div
from builtins import object
import __init__
# ***********************************************************************
import sys
import  wx
import  wx.grid as gridlib
import  wx.lib.mixins.gridlabelrenderer as glr
#from PyLab_Works_Globals import *
from   language_support      import _
from   utility_support       import NoCase_List
from   dialog_support        import _Wrap_No_GUI
from   string_support        import _2U
import xlwt
import traceback
#import copy
# ***********************************************************************


__doc__ = """
# ***********************************************************************
# Creates a form that displays all the device properties
# and lets the user edit these properties
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 Stef Mientki
"""


## Set_Row_Color seems to interfere with Alter_Row_Color !!!!!!!

_Version_Text = [

[ 3.16 , '21-08-2012', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Dialog_RecordForm, Type Choice, Choices / ID_2_Choices / Choices_2_ID vermengeling
    het is nu voldoende om 1 van de onderstaande in te vullen:
      - Choices
      - ID_2_Choices
""" ],

[ 3.15 , '10-01-2012', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Dialog_RecordForm. added extra parameter "Help"
""" ],

[ 3.14 , '27-12-2011', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Field_Object.Type if it's a basesting, it's automatically converted to an int
""" ],

[ 3.13 , '9-12-2011', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Field_Object extended with properties ID_2_Choice and Choice_2_ID
- Get_Field_Objects now can handle the ablove extended Field_Object
""" ],

[ 3.12 , '3-11-2011', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Base_Grid.Fill_Data doesn't gives an error if Data is empty
""" ],

[ 3.11 , '12-05-2011', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Base_Grid.Set_region_Color added
- Base_Grid.Dont_Sort added
- Base_Grid.Align_All_Col didn't work
- Base_Grid.Set_All_ReadOnly was very slow with large grids
""" ],

[ 3.10 , '02-05-2011', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Sorting of columns didn't work, when special characters like trema's etc.
""" ],

[ 3.9 , '13-04-2011', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Base_Grid.Alter_Row_Color added
- Base_Grid.Set_Col_Widths, more relaxed input paramaters
""" ],

[ 3.8 , '11-01-2011', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Base_Grid.Append_Row, bug fixed
""" ],

[ 3.7 , '29-10-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Base_Grid.Set_All_ReadOnly    added
- Base_Grid.Append_Row          added
- Base_Grid.Append_Dict_Row     added
- Base_Grid.Get_Col_Value       added
- Base_Grid.Set_Col_Widths      added
- Base_Grid.Notify_Params_Changed modified
""" ],

[ 3.6 , '28-10-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Base_Grid.Align_All_Col   added
- Base_Grid.Get_Cell_Value  added
- Base_Grid.Set_Cell_Editor added
- Base_Grid.Set_All_Editor  added
- Base_Grid, can have a singleline or multiline string editor as default
- Base_Table_Grid now has a singleline editor
""" ],

[ 3.5 , '3-9-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Base_Simple_Grid added
- numRows, numCols changed case, might lead to problems in existing programs
""" ],

[ 3.4 , '2-7-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Fill_Properties_Data, now ignores the string 'None'
""" ],

[ 3.3 , '21-05-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- _On_Double_Click () method added
""" ],

[ 3.2 , '20-04-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Clear () method added
- RM-menu export didn't have a header
""" ],

[ 3.1 , '09-04-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Statistics gave bug if to little values
""" ],

[ 3.0 , '30-11-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Grid extended with BarGraph, this is not very well implemented,
  due to the unknown if the "CreateGrid" is already called.
  For the moment it only works if the creategrid is done automatically
  like in Fill_Data
""" ],


[ 2.9 , '23-11-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Bug in sorting (My_Key_String), if value was None
- Grid extended with statistics column and rows
""" ],

[ 2.8 , '03-11-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Align_Col now also aligns the col label
""" ],

[ 2.7 , '20-10-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- onCellSelected, also available when not table
""" ],

[ 2.6 , '20-09-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Load_TAB_File added
""" ],

[ 2.5 , '15-09-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Modify flag added
- Fill_Data, Fill_SQL added
- Double Click on column label is sort, added
""" ],


[ 2.4 , '12-08-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Base_Grid, extended with Save_Settings / Load_Settings
""" ],

[ 2.3 , '21-06-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Constant names MY_GRID_.._FIXED changed to MY_GRID_FIXED_..
- Data_Defs was not correctly interpreted
""" ],

[ 2.2 , '10-04-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Color type cells, didn't color upon init, bug fixed
""" ],


[ 2.1 , '27-07-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - New Base_Grid should be used as the base of all Grids
 - Added Get_Settings and Do_Settings,
   to save and reload the user settings in an config file
 - Setting Column Attributes improved to work around bug in wxPython
 - Added faciltity to define a set of attributes and
   to use them with new procedures for setting Cell, Row and Col Attributes
 - export Grid data to a tab-delimited file, through RM-menu
""")],

[ 2.0 , '10-12-2007', 'Stef Mientki',
'Test Conditions:', (),
_(0, '  - changed behavior of STAY ON TOP properties form')],

[ 1.0 , '14-07-2007', 'Stef Mientki',
'Test Conditions:', (),
_(0, ' - orginal release')]
]
# ***********************************************************************

Base_Grid_Double_Click = None

import  os

import  wx.lib.newevent

from dialog_support import AskFileForOpen, Ask_File_For_Save
from inifile_support import *
from menu_support import *
from file_support import Force_Dir

from date_time_support import Delphi_Date
from date_time_support import Kal
# ***********************************************************************


# ***********************************************************************
# We want to edit colors directly through a colordialog
# ***********************************************************************
#global MY_GRID_TYPE_COLOR, MY_GRID_PINS
MY_GRID_TYPE_COLOR     = 'color'
MY_GRID_TYPE_FILE      = 'file'
MY_GRID_PINS           = 'pins'

MY_GRID_FIXED_NONE     = 0    # No fixed columns or rows
MY_GRID_FIXED_ROW      = 1    # Only fixed Rows = TopRow
MY_GRID_FIXED_ROW_COL  = 2    # Both TopRow and LeftColumn fixed
MY_GRID_FIXED_COL_ROW  = 2    # idem for convenience
MY_GRID_FIXED_COL      = 3    # Only fixed Column = LeftColumn

MY_GRID_ROW_TYPED      = 11
MY_GRID_COL_TYPED      = 12


CT_STRING          = 0
CT_INT             = 1
CT_FLOAT           = 2
CT_DATETIME        = 3
CT_DateTime_String = 4
CT_DateTime_Delphi = 5
CT_DateTime_Access = 6
CT_Time_String     = 7
CT_Time_Delphi     = 8
CT_Time_Access     = 9
CT_TestOrganizer   = 10
CT_BOOL            = 11
CT_Multi_Line      = 12
CT_Email           = 13
CT_Choice          = 14

# For use in menus
CT_Names = []
CT_Names.append ( 'String'            )
CT_Names.append ( 'Integer'           )
CT_Names.append ( 'Float'             )
CT_Names.append ( 'DateTime'          )
CT_Names.append ( 'DateTime - String' )
CT_Names.append ( 'DateTime - Delphi' )
CT_Names.append ( 'DateTime - Access' )
CT_Names.append ( 'Time - String'     )
CT_Names.append ( 'Time - Delphi'     )
CT_Names.append ( 'Time - Access'     )
CT_Names.append ( 'TestOrganizer'     )
CT_Names.append ( 'Boolean'           )
CT_Names.append ( 'MultiLine'         )
CT_Names.append ( 'Email'             )
CT_Names.append ( 'Choice'            )

# For use in a execute statement :
CT_execs = """
S   = CT_STRING
I   = CT_INT
F   = CT_FLOAT
DT  = CT_DATETIME
DTS = CT_DateTime_String
DTD = CT_DateTime_Delphi
DTA = CT_DateTime_Access
"""


CT_S_INT           = 1000 + CT_INT
CT_S_FLOAT         = 1000 + CT_FLOAT

Test_Organizer_TestSoort = {}
Test_Organizer_TestSoort [1] = 'Vraag'
Test_Organizer_TestSoort [2] = 'Akto'
Test_Organizer_TestSoort [3] = 'Neuro'
Test_Organizer_TestSoort [13] = 'Rapport'

# ***********************************************************************


# ***********************************************************************
# Largely taken from the standard example
# ***********************************************************************
class CustomDataTable ( gridlib.PyGridTableBase ) :
  def __init__ ( self, data, data_types, data_defs ) :
    gridlib.PyGridTableBase.__init__ ( self )
    self.data       = data
    self.data_types = data_types
    self.data_defs  = data_defs

    self.CF = 0
    for data_def in self.data_defs :
      if data_def in [ MY_GRID_FIXED_COL, MY_GRID_FIXED_ROW_COL ] :
        self.CF = 1
        break

    self.RF = 0
    for data_def in self.data_defs :
      if data_def in [ MY_GRID_FIXED_ROW, MY_GRID_FIXED_ROW_COL ] :
        self.RF = 1
        break

  # ****************************************************************
  # excluding an possible fixed row !!
  # ****************************************************************
  def GetNumberRows ( self ) :
    return len ( self.data [ self.RF : ] )

  # ****************************************************************
  # excluding an possible fixed column !!
  # ****************************************************************
  def GetNumberCols ( self ) :
    return len ( self.data [0] [ self.CF : ] )

  # ****************************************************************
  # ****************************************************************
  def Correct_RC ( self, row, col ) :
    #print 'HJSOA',self.data_defs,row,col,
    for data_def in self.data_defs :
      if data_def in [ MY_GRID_FIXED_COL, MY_GRID_FIXED_ROW_COL ] :
        col += 1
        break
    for data_def in self.data_defs :
      if data_def in [ MY_GRID_FIXED_ROW, MY_GRID_FIXED_ROW_COL ] :
        row += 1
        break
    #print row,col
    return row, col

  # ****************************************************************
  # ****************************************************************
  def IsEmptyCell ( self, row, col ) :
    R, C = self.Correct_RC ( row, col )
    try:
      return not ( self.data [R] [C] )
    except IndexError:
      return True

  # ****************************************************************
  # ****************************************************************
  def GetValue ( self, row, col ) :
    R, C = self.Correct_RC ( row, col )
    try:
      #print 'TYPE',self.data_types[C],self.data [R] [C]
      Val = self.data [R] [C]
      if isinstance ( Val, basestring )  and \
         ( self.data_types [C] != gridlib.GRID_VALUE_STRING ) :
        #print 'OOOO',C,self.data_types[C], Val
        Val = Val.strip ()
        if Val != '' :
          if   self.data_types[C] == gridlib.GRID_VALUE_BOOL :
            Val = bool ( Val )
          elif self.data_types[C] == gridlib.GRID_VALUE_NUMBER :
            Val = int ( Val )
          elif self.data_types[C] == MY_GRID_TYPE_COLOR :
            Val = tuple ( Val )
          elif self.data_types[C] == gridlib.GRID_VALUE_FLOAT :
            Val = float ( Val )
          elif self.data_types[C] == gridlib.GRID_VALUE_CHOICE :
            Val = Val
          else :
            Val = Val
        else :
          if   self.data_types[C] == gridlib.GRID_VALUE_BOOL :
            Val = False
          elif self.data_types[C] == gridlib.GRID_VALUE_NUMBER :
            Val = 0
          elif self.data_types[C] == MY_GRID_TYPE_COLOR :
            Val = tuple ( wx.RED )
          elif self.data_types[C] == gridlib.GRID_VALUE_FLOAT :
            Val = 0
          elif self.data_types[C] == gridlib.GRID_VALUE_CHOICE :
            Val = 0
          else :
            Val = Val

      #print '----',C,self.data_types[C], Val
      return Val
    except IndexError:
      return ''

  # ****************************************************************
  # ****************************************************************
  def SetValue ( self, row, col, value ) :
    R, C = self.Correct_RC ( row, col )
    self.data [R] [C] = value

    # for some special cases, lets update the grid
    typ = self.GetRawTypeName ( row, col )
    if typ in [ MY_GRID_TYPE_COLOR ] :
      self.GetView().Update_Colors( row, col )


  """
  # ****************************************************************
  # never called with the starnge AppendRows in Grid !!
  # ****************************************************************
  def AppendRows ( self, numRows = 1, updateLabels = True ) : #*args, **kwargs):
    #print 'A',self.table.GetNumberRows (), self.GetNumberRows ()
    NC = self.GetNumberCols ()
    self.data.append ( NC * [''])
    return True
  """


  # ****************************************************************
  # Called when the grid needs to display labels
  # ****************************************************************
  def GetColLabelValue ( self, col ) :
    R, C = self.Correct_RC ( 0, col )
    return self.data [0] [C]

  # ****************************************************************
  # ****************************************************************
  def GetRowLabelValue ( self, row ) :
    R, C = self.Correct_RC ( row, 0 )
    return self.data [R] [0]

  # ****************************************************************
  # ****************************************************************
  def GetRawTypeName(self, row, col):
    for data_def in self.data_defs :
      if data_def == MY_GRID_ROW_TYPED :
        return self.data_types [row]
    else :
      return self.data_types [col]

  # ****************************************************************
  # ****************************************************************
  def GetTypeName(self, row, col):
    typ = self.GetRawTypeName ( row, col )
    if typ in [ MY_GRID_TYPE_COLOR,
                 MY_GRID_TYPE_FILE,
                 MY_GRID_PINS ] :
      return gridlib.GRID_VALUE_STRING
    else:
      return typ

  # ****************************************************************
  # ****************************************************************
  def CanGetValueAs ( self, row, col, typeName ) :
    for data_def in self.data_defs :
      if data_def == MY_GRID_ROW_TYPED :
        DataType = self.data_types [row].split(':')[0]
    else :
      DataType = self.data_types [col].split(':')[0]

    if typeName == DataType:
      return True
    else:
      return False

  # ****************************************************************
  # ****************************************************************
  def CanSetValueAs ( self, row, col, typeName ) :
    return self.CanGetValueAs ( row, col, typeName )
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class _Gridcell_Bargraph ( wx.grid.PyGridCellRenderer ) :
  """
Renderer for the graph bar.
This renderer is automatically called,
when the graph cell must be re-rendered.
  """
  def __init__ ( self, Max, Color, Color_Large = wx.RED ) :
    wx.grid.PyGridCellRenderer.__init__ ( self )
    self.Max         = Max
    self.Color       = Color
    self.Color_Large = Color_Large

  # ********************************************************
  def Draw ( self, grid, attr, dc, rect, row, col, IsSelected ) :
    """
Automatically called when the cell should be repainted.
    """
    dc.SetPen ( wx.TRANSPARENT_PEN )
    dc.SetBrush ( wx.Brush ( wx.WHITE, wx.SOLID ) )
    dc.DrawRectangle ( rect.x, rect.y, rect.width, rect.height )


    try:
      Value = int ( grid.GetCellValue ( row, col ) )
      Color = self.Color
      if Value >= self.Max :
        #Value = self.Max
        Color = self.Color_Large
      dc.SetBrush ( wx.Brush ( Color, wx.SOLID ) )
      #dx = int ( round ( Value * rect.width / self.Max ) )
      if Value > 100 :
        dx = rect.width
      else :
        dx = int ( round ( Value * rect.width / 100.0 ) )
      dc.DrawRectangle ( rect.x, rect.y, dx, rect.height )
    except :
      pass

  # ********************************************************
  def Clone ( self ) :
    """ Renderer needs this procedure """
    return Gridcell_Bargraph ()
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class _Gridcell_BarTwoColor ( wx.grid.PyGridCellRenderer ) :
  """
Renderer for the graph bar.
This renderer is automatically called,
when the graph cell must be re-rendered.
  """
  def __init__ ( self, Color, Color_Large = wx.RED ) :
    wx.grid.PyGridCellRenderer.__init__ ( self )
    self.Color       = Color
    self.Color_Large = Color_Large

  # ********************************************************
  def Draw ( self, grid, attr, dc, rect, row, col, IsSelected ) :
    """
Automatically called when the cell should be repainted.
    """
    dc.SetPen ( wx.TRANSPARENT_PEN )
    dc.SetBrush ( wx.Brush ( self.Color_Large, wx.SOLID ) )
    dc.DrawRectangle ( rect.x, rect.y, rect.width, rect.height )


    try:
      Value = int ( grid.GetCellValue ( row, col ) )
      Color = self.Color
      dc.SetBrush ( wx.Brush ( Color, wx.SOLID ) )
      #dx = int ( round ( Value * rect.width / self.Max ) )
      if Value > 100 :
        dx = rect.width
      else :
        dx = int ( round ( Value * rect.width / 100.0 ) )
      dc.DrawRectangle ( rect.x, rect.y, dx, rect.height )
    except :
      pass

  # ********************************************************
  def Clone ( self ) :
    """ Renderer needs this procedure """
    return Gridcell_Bargraph ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class _Gridcell_DayPlan ( wx.grid.PyGridCellRenderer ) :
  """
  This renderer is automatically called,
  when the graph cell must be re-rendered.
  """
  def __init__ ( self, Color, Max = 8 ) :
    wx.grid.PyGridCellRenderer.__init__ ( self )
    self.Color = Color
    self.Max   = Max

  # ********************************************************
  def Draw ( self, grid, attr, dc, rect, row, col, IsSelected ) :
    """
    Automatically called when the cell should be repainted.
    """
    #if grid.ToDay and (row,col) == grid.ToDay :
    #  dc.SetPen ( wx.Pen (wx.BLUE, 4 ))
    #else :
    dc.SetPen ( wx.TRANSPARENT_PEN )
    dc.SetBrush ( wx.Brush ( wx.WHITE, wx.SOLID ) )
    dc.DrawRectangle ( rect.x, rect.y, rect.width, rect.height )

    # If all cells are rendered, the font gets bold
    # so get the normal font here
    dc.SetFont ( grid.GetFont())

    dxt = 3
    try:
      CellValue = grid.GetCellValue ( row, col )
      Value = float ( CellValue )
      if Value > 0.5 :
        Color = self.Color
        if Value > self.Max :
          Value = self.Max
          Color = wx.RED
        dc.SetBrush ( wx.Brush ( Color, wx.SOLID ) )
        dx = int ( round ( Value * rect.width / self.Max ) )
        dc.DrawRectangle ( rect.x, rect.y, dx, rect.height )
        dc.DrawText ( '%.1f' % (Value), rect.x + dxt, rect.y )

    except :
      dc.DrawText ( CellValue, rect.x + dxt, rect.y )

    if grid.ToDay and ( row, col ) == grid.ToDay :
      dc.SetPen ( wx.Pen ( wx.RED, 4 ))
      dc.SetBrush (( wx.TRANSPARENT_BRUSH ))
      dc.DrawRectangle ( rect.x, rect.y, rect.width, rect.height )

    if ( row, col ) in grid.Day_Events :
      Color, Text = grid.Day_Events [ ( row, col ) ]
      dc.SetPen ( wx.Pen ( Color, 4 ))
      dc.SetBrush (( wx.TRANSPARENT_BRUSH ))
      dc.DrawRectangle ( rect.x, rect.y, rect.width, rect.height )
      if Text :
        dc.DrawText ( Text, rect.x + dxt, rect.y )



  # ********************************************************
  def Clone ( self ) :
    """ Renderer needs this procedure """
    return Gridcell_Bargraph ()
# ***********************************************************************


# *******************************************************
# *******************************************************
class MyColLabelRenderer ( glr.GridLabelRenderer ) :
  def __init__ ( self, bgcolor ) :
    self._bgcolor = bgcolor

  def Draw ( self, grid, dc, rect, col ) :
    dc.SetBrush ( wx.Brush ( self._bgcolor ))
    dc.SetPen ( wx.TRANSPARENT_PEN )
    dc.DrawRectangleRect ( rect )
    hAlign, vAlign = grid.GetColLabelAlignment()
    text = grid.GetColLabelValue ( col )
    self.DrawBorder ( grid, dc, rect )
    self.DrawText ( grid, dc, rect, text, hAlign, vAlign )
# ***********************************************************************


# ***********************************************************************
# This extends the gridlib.Grid with :
#   - standard RM-menu
# ***********************************************************************
class Base_Grid ( gridlib.Grid ) : ##, glr.GridWithLabelRenderersMixin ) :
  def __init__ ( self, parent, table = None, name = 'Base Grid',
                 editor = 'multiline' ) :
    gridlib.Grid.__init__ ( self, parent, -1 )
    ##glr.GridWithLabelRenderersMixin.__init__ ( self )

    if editor == 'multiline' :
      self.SetDefaultEditor ( wx.grid.GridCellAutoWrapStringEditor() )
    else :
      self.SetDefaultEditor ( wx.grid.GridCellTextEditor () )

    self.parent           = parent
    self.Set_Modal_Open   = None
    self.Last_Selected_Cell = None
    self.My_Name          = name
    self.Secret_Data      = False
    self.Extra_Statistics = False
    self.Editor_Active    = False
    self.Modified         = False
    self.Sort_Col         = None
    self.Col_Types        = []
    self.Row_Types        = []
    self.Export_Filename  = None
    self.Grid_Created     = False
    self.Notify_Params_Changed = None
    self.Dont_Sort             = False
    self.MY_Read_ONLY          = False
    self.Alt_Color             = None
    self.Active_Table          = None

    self.SetRowLabelSize ( 0 )
    self.SetColLabelSize ( 20 )
    self.SetColLabelAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )
    self.SetRowLabelAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )

    # If used with a table,
    # most calls will be done to the table instead of the grid
    # WATCH OUT: not all calls are identical
    if table :
      self.table  = table
    else :
      self.table = self

    ## TEST weggehaald van Fill_Data,
    ## teneinde Set_Col_Bargraph op ieder moment te kunnen geven
    ## GAAT NIET GOED bij TOA-OPNAMEN / SATISFACTION
    ##self.CreateGrid ( 1, 1, wx.grid.Grid.SelectCells )
    self.BarGraph_columns = []
    self.BarTwoColor_columns = []

    self.SetMargins ( 0, 0 )
    self.DefaultCellOverflow = False

    self.Random_Select = False
    self.Random_Select_Color = wx.Colour ( 100, 200, 100 )

    # *************************************************************
    # popup menus
    # *************************************************************
    pre = [ _(0, 'Export (tab delim)' ),
            _(0, 'Print (-Preview)'),
            'Export to Excel',
            'Open in Excel'
          ]
    self.Popup_Menu = My_Popup_Menu ( self.On_Popup_Item_Selected, None,
      pre = pre )
    self.Transparancy = 0
    self.Bind ( gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.On_Show_Popup )
    #self.Bind ( wx.EVT_CONTEXT_MENU, self.On_Show_Popup )
    # *************************************************************

    # ****************************************************************
    # EVENT BINDINGS
    # ****************************************************************
    #self.Bind ( gridlib.EVT_GRID_COL_SIZE,        self.OnColSize )
    self.Bind ( gridlib.EVT_GRID_EDITOR_SHOWN,    self.OnEditorShown )

    # EVT_GRID_EDITOR_HIDDEN is fired twice at the end of an edit session
    # while EVT_GRID_CELL_CHANGE is fired only once
    # print ( dir ( gridlib))
    if sys.version_info.major > 2 :
      self.Bind ( gridlib.EVT_GRID_CELL_CHANGED, self.OnEditorChange )
      #_On_Editor_Change )
    else :
      self.Bind ( gridlib.EVT_GRID_CELL_CHANGE, self.OnEditorChange )
      #_On_Editor_Change )
    self.Bind ( gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnLeftClick )

    self.Bind ( gridlib.EVT_GRID_CELL_LEFT_DCLICK , self._On_Double_Click )

    # CHANGED 22-10-2009
    ##if self.table != self :
    ##  self.Bind ( gridlib.EVT_GRID_SELECT_CELL,     self.onCellSelected )
    self.Bind ( gridlib.EVT_GRID_SELECT_CELL,     self.onCellSelected )

    self.Bind ( gridlib.EVT_GRID_EDITOR_CREATED,  self.onEditorCreated )

    self.Bind ( wx.EVT_KEY_DOWN, self._On_Key )

    # DoubleClick a column label = sort on this column
    self.Bind ( wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self._On_Col_DClick )

    # *************************************************************
    # Menu completions
    # *************************************************************
    Top_Window = wx.GetTopLevelParent ( self )
    if 'MenuBar' in dir ( Top_Window ) :
      if  'Bind_MenuItem' in dir ( Top_Window.MenuBar ) :
        MB = Top_Window.MenuBar.Bind_MenuItem
        MB ( 'File', 'Export'        , self._On_Export, self.GridWindow )
        MB ( 'File', 'Export-Launch' , self._On_Export_Launch, self.GridWindow )
    # *************************************************************

  # *******************************************************
  # ISNT POSSIBLE KAN NIET !!
  # *******************************************************
  '''
  def SetCellValue ( self, Row, Col, Value ) :
    """
Be sure the value to store in a cell is a string-type
    """
    if not ( isinstance ( Value, basestring )) :
      Value = str ( Value )
    print 'ZZZZZZZZZZZZZSSSSSSS', Row, Col, Value, type (Value)
    gridlib.Grid.SetCellValue ( self, Row, Col, Value )
  '''

  # *******************************************************
  # *******************************************************
  def Export_2_Excel ( self, Filename,
                       TabName = 'From DB',
                       Info_Row = None,
                       Info_Col = 0,
                       ColWidths = [] ) :

    wbk    = xlwt.Workbook()
    wsheet = wbk.add_sheet ( TabName )
    style  = xlwt.easyxf('pattern: pattern solid, fore_colour sky_blue;')
    style  = xlwt.easyxf('pattern: pattern solid, fore_colour white;')
    style_top = xlwt.easyxf('pattern: pattern solid, fore_colour orange;')
    #style  = xlwt.easyxf('pattern: pattern solid, fore_colour 42;')
    hstyle = xlwt.easyxf('pattern: pattern solid, fore_colour blue;font: colour white, bold True;')
    dstyle = xlwt.easyxf()


    algn1            = xlwt.Alignment()
    algn1.wrap       = 1
    algn1.horz       = xlwt.Alignment.HORZ_LEFT
    algn1.vert       = xlwt.Alignment.VERT_TOP
    style.alignment  = algn1
    hstyle.alignment = algn1
    dstyle.alignment = algn1


    """
    fnt = Font()
    fnt.name = 'Arial'
    fnt.colour_index = 4
    fnt.bold = True
    """

    borders = xlwt.Borders()
    w = 1
    borders.left = w
    borders.right = w
    borders.top = w
    borders.bottom = w
    style.borders = borders




    NRow = self.GetNumberRows ()
    NCol = self.GetNumberCols ()

    fixed_column = self.GetRowLabelSize () > 0

    # write column headers if available
    R_Off = 0
    C_Off = 0
    if fixed_column :
      C_Off = 1
    if self.GetColLabelSize () > 0 :
      for col in range ( NCol ) :
        wsheet.write ( R_Off, col+C_Off, self.GetColLabelValue ( col ), style_top )
      R_Off += 1

    # if extra info row
    if Info_Row :
      ##wsheet.write ( R_Off, 0, 'Toelichting', style )
      for col in range ( NCol ) :
        wsheet.write ( R_Off, col+C_Off, Info_Row [ col ], style )
      R_Off += 1


    # Write all data
    for row in range ( NRow ) :
      C_Off = 0
      if fixed_column :
        wsheet.write ( row+R_Off, 0, self.GetRowLabelValue ( row ), style)
        C_Off = 1
      for col in range ( NCol ) :
        Item = self.GetCellValue ( row, col  ).replace ( '\r', '').replace('\n',' | ')
        wsheet.write ( row+R_Off, col+C_Off, Item, style)

    wsheet.set_panes_frozen(True) # frozen headings instead of split panes
    if Info_Row :
      wsheet.set_horz_split_pos(2)
    else :
      wsheet.set_horz_split_pos(1) # in general, freeze after last heading row

    if Info_Col :
      wsheet.set_vert_split_pos( Info_Col )

    ##wsheet.set_remove_splits(True) # if user does unfreeze, don't leave a split there

    for col, W in enumerate ( ColWidths ) :
      wsheet.col(col).width = 200 * W

    try :
      wbk.save ( Filename )
    except :
      print ( 'Kan %s niet bewaren'% Filename )

  # *******************************************************
  # *******************************************************
  def Clear ( self ) :
    self.ClearGrid()
    self.Update ()

  #***************************************************
  #***************************************************
  def _On_Export_Launch ( self, event = None ):
    self._On_Export ( event )

    subprocess.Popen ( self.Export_Filename, shell = True )

  #***************************************************
  #***************************************************
  def _On_Export ( self, event = None ) :
    from date_time_support import Delphi_Date

    if not ( self.Export_Filename ) :
      self.Export_Filename = Change_FileExt ( Application.FileName, '.tab' )

    Force_Dir ( os.path.split ( self.Export_Filename )[0] )

    ##print 'GRID_EXPORT', self.Export_Filename
    # FOR EXCEL WE NEED LATIN-1 TRANSLATION
    import codecs
    #fh = codecs.open ( self.Export_Filename, 'w', 'latin-1' )
    fh = codecs.open ( self.Export_Filename, 'w', 'windows-1252' )

    NRow = self.GetNumberRows ()
    NCol = self.GetNumberCols ()

    fixed_column = self.GetRowLabelSize () > 0

    # write column headers if available
    if self.GetColLabelSize () > 0 :
      if fixed_column :
        line = '\t'
      else :
        line = ''
      for i in range ( NCol ) :
        line += self.GetColLabelValue ( i ) + '\t'
      line = line [ : -1 ] + '\n'
      fh.write ( line )

    # Write all data
    for row in range ( NRow ) :
      line = ''
      if fixed_column :
        line += self.GetRowLabelValue ( row ) + '\t'
      for col in range ( NCol ) :
        ##line += self.GetCellValue ( row, col  ) + '\t'
        ##line += self.GetCellValue ( row, col  ).replace('\n',' ') + '\t'
        line += self.GetCellValue ( row, col  ).replace ( '\r', '').replace('\n',' | ') + '\t'
      line = line [ : -1 ] + '\n'
      fh.write ( line )

    fh.close ()

  #***************************************************
  #***************************************************
  def _On_Col_DClick ( self, event ) :
    """
Double Click on column label = sort on this column.
If the selected column is the already sorted column,
the order is reversed.
"""
    if self.Dont_Sort :
      return
    new_col = event.GetCol ()
    #print 'GetCol',new_col, self.Sort_Col
    if new_col == self.Sort_Col :
      self.Sort_Reverse = not ( self.Sort_Reverse )
    else :
      self.Sort_Reverse = False
      self.Sort_Col = new_col
    self.Display_Data ( ) #new_col, self.Sort_Reverse )

  # *******************************************************
  # *******************************************************
  def Load_TAB_File ( self, Filename ) :
    """
    Loads a tab delimited file.
    """
    if not ( File_Exists ( Filename ) ) :
      self.ClearGrid()
      N = self.GetNumberCols ()
      if N > 0 : self.DeleteCols ( numCols = N )
      N = self.GetNumberRows ()
      if N > 0 : self.DeleteRows ( numRows = N )
      return

    fh = open ( Filename, 'r' )
    #import codecs
    #fh = codecs.open ( Filename, 'w', 'windows-1252' )
    #lines = fh.readlines ()
    lines = fh.read ().split ( chr(13) )
    fh.close ()
    Data = []
    for line in lines :
      #print line
      Data.append ( line.split ( '\t' ) )
    self.Fill_Data ( Data )

  # *******************************************************
  # *******************************************************
  def Fill_SQL ( self, Data, Sort_Col = None, Reverse = False, Col_Types = None ) :
    """
    For SQL we need some preprocessing
    there seems to be a bug in the SQLite library
    sometimes it gives back a string, sometimes a unicode
    so here we ensure that we've a unicode
    """
    # **************************************
    # if there's no data, clear the grid and return
    # **************************************
    if not(Data) or len ( Data ) == 0 :
      self.ClearGrid ()
      return

    # **************************************
    # be sure we've enough column types
    # **************************************
    if Col_Types :
      self.Col_Types = Col_Types
    NCol = len ( Data [0] )
    while len ( self.Col_Types ) < NCol :
      self.Col_Types.append ( CT_STRING )

    for R, Row in enumerate ( Data [ 1: ] ) :

      # Waar is dit voor nodig ?
      Data [R+1] = list ( Data [R+1] )

      for C, Col in enumerate ( Row ) :
        Value = Row [C]
        CT = self.Col_Types [C]
        if not ( Value is None ) :
          try :
            #if Value == 'None' :
            #  Value = None
            if Value == 'None' or Value == '<NULL>':
              Value = ''

            # Convert all DateTime types to float
            elif CT == CT_DateTime_String :
              Value = Delphi_Date ( Value )

            elif CT == CT_DateTime_Delphi :
              # Coming from SQL it might be a string
              # and it might contain a comma instead of a point !!
              if isinstance ( Value, basestring ) :
                try :
                  Value = int ( Value )
                except :
                  Value = float ( Value.replace ( ',', '.' ) )

            elif CT == CT_DateTime_Access :
              Value = Delphi_Date().from_Access ( Value )

            # Leave these types untouched
            elif type ( Value ) in [ int, float, str ]:
              pass

            # be sure to convert strings to unicode
            elif isinstance ( Value, str ) :
              #print type(Value),Value
              try :
                Value = str ( Value, 'utf8' )
              except :
                #print Row
                try :
                  Value = str ( Value )
                except :
                  pass
          except :
            Value = ''
        #else :
        #  print 'CT',C,CT,Value

        Data [R+1] [C] = Value

    self.Fill_Data ( Data, Sort_Col, Reverse, self.Col_Types )


  # *******************************************************
  # *******************************************************
  def Fill_Data ( self, Data, Sort_Col = None, Reverse = False, Col_Types = None ) :
    """
Fill the grid with Data.
Data is a list of rows, where each row is a list of values.
Data can be sorted (or reversed sorted) on a column.
The fields indicated with Date_Fields,
are assumed to contain a float, reprensenting the Delphi date.
These Delphi Dates will be translated in human readible date strings.
"""
    self.Active_Table = None
    self.Clear ()
    """
    try :
      if not ( Data ) :
        self.Clear ()
        return
    except :
      try :
        if not ( Data.any() ) :
          self.Clear ()
          return
      except :
        Data = [ [ 'All' ], [ str ( Data )] ]
"""

    self.Data              = Data
    self.Sort_Col          = Sort_Col
    self.Sort_Reverse      = Reverse

    # **************************************
    # be sure we've enough column types
    # **************************************
    if Col_Types :
      self.Col_Types = Col_Types
    NCol = len ( Data [0] )
    while len ( self.Col_Types ) < NCol :
      self.Col_Types.append ( CT_STRING )


    if Reverse :
      select_col = '   /\\'
    else :
      select_col = '   \\/'

    # **************************************
    # In case of extra statistics,
    # insert an extra string type column
    # **************************************
    if self.Extra_Statistics :
      NCol = len ( Data [0] )
      if len ( self.Col_Types ) < NCol + 1 :
        self.Col_Types.insert ( 0, CT_STRING )

      # extend Data with 1 column
      for i, Row in enumerate ( Data ) :
        Data [i] = [''] + Row

      Data [0][0] = 'Stats'

      # extend with Statistics Rows
      Row = NCol * ['']
      Data.insert ( 1, [ 'mean'   ] + Row )
      Data.insert ( 2, [ 'median' ] + Row )
      Data.insert ( 3, [ 'N'      ] + Row )
      Data.insert ( 4, [ 'SD'     ] + Row )

      if self.Sort_Col :
        self.Sort_Col += 1
      else :
        self.Sort_Col = 1

      # LETs do statisctics
      from numpy import mean, median, std
      N = len ( Data )
      for C, CT in enumerate ( self.Col_Types ) :
        if CT > 1000 :
          CT -= 1000
          A = []
          for i in range ( 5, N ) :
            Value = Data [i][C]
            if not ( Value in [ '', None ] ) :
              if isinstance ( Value, basestring ) :
                try :
                  Value = int ( Value )
                except :
                  try :
                    Value = float ( Value )
                  except :
                    Value = 0
              A.append ( Value )

          #print 'STATISICS', C, A, len(A),mean(A),median(A),std(A)
          Data [3][C] = len ( A )
          if len (A) > 4 :
            Data [1][C] = int ( round ( mean ( A ) ) )
            Data [2][C] = int ( round ( median ( A ) ) )
            Data [4][C] = int ( round ( std ( A ) ) )
        else :
          if ( C > 0 ) and \
             not ( CT in [ CT_DATETIME,
                           CT_DateTime_String,
                           CT_DateTime_Delphi,
                           CT_DateTime_Access,
                           CT_Time_String,
                           CT_Time_Delphi,
                           CT_Time_Access ] ) :
            Data[3][C] = N - 5
    # **************************************

    NRow = len ( Data ) - 1
    NCol = len ( Data [0] )
    if self.GetRowLabelSize () > 0 :
      NCol -= 1
    ##self.SetRowLabelSize ( 0 )
    ##self.SetColLabelSize ( 20 )
    ##self.SetColLabelAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )


    # **************************************
    # CreateGrid is only allowed once !!
    # **************************************
    ## ZEGT NIETS ?? print 'GWGWGW',self.GetGridWindow()
    if not self.Grid_Created :
      try :
        self.CreateGrid ( NRow, NCol)
        self.Grid_Created = True
        #self.Set_Col_BarGraph ( 5, 100, wx.Colour ( 0,255, 200 ) )

        # if the grid was created here,
        # we need to add the bargraph renderes
        for item in self.BarGraph_columns :
          attr = wx.grid.GridCellAttr ()
          attr.SetRenderer ( _Gridcell_Bargraph ( *item[1:] ))  ##[1], item[2] ) )
          self.SetColAttr ( item[0], attr )

        for item in self.BarTwoColor_columns :
          attr = wx.grid.GridCellAttr ()
          attr.SetRenderer ( _Gridcell_BarTwoColor ( *item[1:] ))
          self.SetColAttr ( item[0], attr )


      except :
        traceback.print_exc ()
        pass


    # **************************************
    # Set the right number of columns
    # **************************************
    NeedCol = len ( Data[0] )
    if self.GetRowLabelSize () > 0 :
      NeedCol -= 1
    NCol = self.GetNumberCols ()
    if NCol > NeedCol :
      self.DeleteCols ( numCols = NCol - NeedCol )
    elif NCol < NeedCol :
      self.AppendCols ( numCols = NeedCol - NCol )

    # **************************************
    # Remove all rows
    # **************************************
    N = self.GetNumberRows ()
    if N > 0 : self.DeleteRows ( numRows = N )

    # **************************************
    # Constants needed for some conversions
    # **************************************

    # **************************************
    # Display the data
    # **************************************
    self.Display_Data ()
  # ************************************************************


  # *******************************************************
  # *******************************************************
  def Fill_Properties_Data ( self, Data, Row_Types = None ) :
    """
Fill a property like grid with Data.
Data consists of 2 lists, the first one with the key value,
which will be placed in the fixed column.
The list in Data consists of the values and will be placed inthe second column.
By choosing this organization of the input data,
a 1-line result of a database query can be shown directly.
"""
    self.Data              = Data
    if Row_Types :
      self.Row_Types       = Row_Types

    # **************************************
    # be sure we've enough column types
    # **************************************
    NRow = len ( Data [0] )
    NCol = 1
    while len ( self.Row_Types ) < NRow :
      self.Row_Types.append ( None )


    # **************************************
    # CreateGrid is only allowed once !!
    # **************************************
    try :
      self.CreateGrid ( NRow, NCol)
      self.Grid_Created = True
    except :
      pass

    self.SetRowLabelSize ( 120 )
    self.SetColLabelSize ( 0 )
    self.SetRowLabelAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )
    self.SetColLabelValue ( 0, '' )

    # **************************************
    # Set the right number of columns
    # **************************************
    NC = self.GetNumberCols ()
    if NC > NCol :
      self.DeleteCols ( numCols = NC - NCol )
    elif NC < NCol :
      self.AppendCols ( numCols = NCol - NC )

    # **************************************
    # Remove all rows
    # **************************************
    N = self.GetNumberRows ()
    if N > NRow : self.DeleteRows ( numRows = ( N - NRow ) )
    else :
      Too_Short = NRow - self.GetNumberRows ()
      if Too_Short > 0 :
        self.AppendRows ( numRows = Too_Short )

    # **************************************
    # Constants needed for some conversions
    # **************************************
    dag_sec    = 60.0 * 60 * 24

    # **************************************
    # Display the data
    # **************************************
    self.SetDefaultColSize ( 200, True )
    for i, Field in enumerate ( Data[0] ) :
      self.SetRowLabelValue ( i, Field )

      if len ( Data ) > 1 :
        Value = Data[1][i]
        #print self.GetNumberRows(), self.GetNumberCols(),i,Value
        if ( Value is None ) or ( Value == 'None' ) :
          Value = ''
        else :
          Value = str ( Value )
      else :
        Value = ''
      self.SetCellValue ( i, 0, Value )

      N = len ( Value.splitlines() )
      if i> 2 : self.SetRowSize ( i, N*13+4 )

  # ************************************************************


  # ************************************************************
  # ************************************************************
  def Display_Data ( self, Sort_Col = None, Reverse = None ) :
    #print 'Display',Sort_Col, self.Sort_Col
    if Sort_Col != None :
      self.Sort_Col = Sort_Col
    if Reverse != None :
      self.Sort_Reverse = Reverse

    # **************************************
    # Set the column labels
    # **************************************
    #print 'SORTon', self.Sort_Col
    if self.Sort_Reverse :
      select_col = '   /\\'
    else :
      select_col = '   \\/'

    if self.GetRowLabelSize () > 0 :
      Col_Names = self.Data[0][1:]
    else :
      Col_Names = self.Data[0]

    for i, name in enumerate ( Col_Names ) :
      if not ( isinstance ( name, basestring )) :
        name = str ( name )
      if i == self.Sort_Col :
        self.SetColLabelValue ( i, name + select_col )
      else :
        self.SetColLabelValue ( i, name )

    # **************************************
    # Set the Row labels ( if necessary )
    # **************************************
    if self.GetRowLabelSize () > 0 :
      for i, Row in enumerate ( self.Data [1:] ) :
        if not ( Row[0] ) :
          self.SetRowLabelValue ( i, u'' )
        elif isinstance ( Row[0], str ) :
          self.SetRowLabelValue ( i, Row[0] )
        else :
          try :
            self.SetRowLabelValue ( i, Row[0].decode( 'utf-8' ))
          except :
            print('???????????????????????? >>',type(Row[0]))
            self.SetRowLabelValue ( i, Row[0] )

    # **************************************
    # procedured to sort the rows on one of the columns
    # **************************************
    def My_Key_Integer ( Item ) :
      try :
        return int ( Item [ self.Sort_Col ] )
      except :
        return None
    def My_Key_String ( Item ) :
      #Str_Item = str ( Item [ self.Sort_Col ] )
      Str_Item = str ( Item [ self.Sort_Col ] )
      # In case of value = None, return an empty string
      if not ( Str_Item ) :
        return ''
      return Str_Item.lower()
    def My_Key( Item ) :
      return Item [ self.Sort_Col ]

    # **************************************
    # Sort the data
    # **************************************
    if self.Sort_Col != None :
      if self.Extra_Statistics :
        N = 5
      else :
        N = 1
      if self.Col_Types [ self.Sort_Col ] == CT_STRING  :
        #print 'Basestring', type (self.Data [1][self.Sort_Col])
        ##Data = sorted ( self.Data [1:], key = My_Key_String, reverse = self.Sort_Reverse )
        Data = self.Data [1:N] + sorted ( self.Data [N:],
                 key = My_Key_String, reverse = self.Sort_Reverse )
      elif self.Col_Types [ self.Sort_Col ] == CT_INT  :
        #print 'Integer', type (self.Data [1][self.Sort_Col])
        ##Data = sorted ( self.Data [1:], key = My_Key_Integer, reverse = self.Sort_Reverse )
        Data = self.Data [1:N] + sorted ( self.Data [N:],
                 key = My_Key_Integer, reverse = self.Sort_Reverse )
      else :
        #print 'Other', type (self.Data [1][self.Sort_Col])
        ##Data = sorted ( self.Data [1:], key = My_Key, reverse = self.Sort_Reverse )
        Data = self.Data [1:N] + sorted ( self.Data [N:],
                 key = My_Key, reverse = self.Sort_Reverse )
    else :
      Data = self.Data [ 1 : ]

    """
    if self.Sort_Col != None :
      if isinstance ( self.Data [1][self.Sort_Col], basestring ) :
        print 'Basestring', type (self.Data [1][self.Sort_Col])
        Data = sorted ( self.Data [1:], key = My_Key_String, reverse = self.Sort_Reverse )
      else :
        print 'Other', type (self.Data [1][self.Sort_Col])
        Data = sorted ( self.Data [1:], key = My_Key, reverse = self.Sort_Reverse )
    else :
      Data = self.Data [ 1 : ]
    """

    # **************************************
    # Display the data
    # **************************************
    Too_Short = len ( Data ) - self.GetNumberRows ()
    if Too_Short > 0 :
      self.AppendRows ( numRows = Too_Short )
    for R, Row in enumerate ( Data ) :
      #if self.GetNumberself.AppendRows ( 1 )
      #if self.GetNumberRows ()

      if self.GetRowLabelSize () > 0 :
        Row_Data = Row [ 1: ]
      else :
        Row_Data = Row
      for C, Value in enumerate ( Row_Data ) :
        if Value != None :
          CT = self.Col_Types [C] % 1000
          #print type ( Value ), Value

          if CT in [ CT_DateTime_Access, CT_DateTime_Delphi, CT_DateTime_String ] :
            ##empty strings are not allowed in Delphi_Date
            if Value :
              Value = Delphi_Date ( Value ).to_String ()
            else :
              Value = ''

          elif CT in [ CT_Time_Access, CT_Time_Delphi, CT_Time_String ] :
            Value = Value.to_String_Time_Short ()


          elif CT == CT_TestOrganizer :
            if Value in Test_Organizer_TestSoort :
              Value = Test_Organizer_TestSoort [ Value ]

          elif isinstance ( Value, basestring ) :
            pass
            """
            elif isinstance ( Value, str ) :
              pass
            elif isinstance ( Value, unicode ) :
              Value = str ( Value )
            """

          else :
            Value = str ( Value )
        else :
          Value = ''

        try :
          self.SetCellValue ( R, C, Value )
          ##print R,C, Value
        except :
          print('>>>> Error Value =', Value)
          traceback.print_exc ()

    if self.Alt_Color:
      self.Alter_Row_Color ()

  # *******************************************************
  # *******************************************************
  def _On_Key ( self, event ) :
    #print '2222gsdufsdp',event.KeyCode, 'dir(event)', event.AltDown(), event.GetEventObject()
    Key = event.GetKeyCode ()
    #event.GetEventObject().WriteText('\n')

    if self.Random_Select and  ( Key == 32 ) :
      Row = self.GetGridCursorRow()
      Col = self.GetGridCursorCol()
      self.Toggle_Cell_Selected ( Row, Col )
    else :
      event.Skip ()

  # ********************************************************
  # ********************************************************
  def GetName ( self ) :
    return self.My_Name

  # *****************************************************************
  # *****************************************************************
  def On_Show_Popup ( self, event ) :
    self.Hit_Pos = event.GetPosition ()
    self.PopupMenu ( self.Popup_Menu, pos = self.Hit_Pos )

  # *****************************************************************
  # *****************************************************************
  def On_Popup_Item_Selected ( self, event ) :
    ID = event.Int
    if ID == 0 :
      if self.Export_Filename :
        pathname, filename = os.path.split ( self.Export_Filename )
      else :
        pathname = os.getcwd()
        filename = ''
      file = Ask_File_For_Save (
                DefaultLocation = pathname,
                DefaultFile     = filename,
                FileTypes       = '*.tab',
                                 Title = _(0, 'Save Table as TAB-delimited file' ))
      if file :
        self.Export_Filename = file
        self._On_Export ()

    elif ID == 1 :
      import wx.lib.printout as wp
      ptbl = wp.PrintGrid ( None, self)
      Table = ptbl.GetTable ()
      Table.SetLandscape()
      Table.SetPaperId(wx.PAPER_A4)
      ptbl.Preview()

    elif ID in ( 2, 3 ) :  # Export to Excel
      Filename = r'Temp.xls'
      while File_Exists ( Filename ) :
        Filename = os.path.splitext ( Filename)[0] + 'x.xls'
      self.Export_2_Excel ( Filename )
      if ID == 3 :
        subprocess.Popen ( [ Filename ], shell = True )

  # *****************************************************************
  # *****************************************************************
  def Get_Settings ( self ) :
    line = []
    for C in range ( self.table.GetNumberCols () ) :
      line.append ( self.GetColSize (C) )
    return line

  # *****************************************************************
  # *****************************************************************
  def Do_Settings ( self, line ) :
    if line :
      for C in range ( self.table.GetNumberCols () ) :
        self.SetColSize ( C, int ( line [C] ) )

  # ****************************************************************
  # v
  # ****************************************************************
  def Align_Col ( self, col,
                  align_hor = wx.ALIGN_LEFT,
                  align_ver = wx.ALIGN_CENTER ) :
    self.SetColLabelAlignment ( align_hor, align_ver )
    attr1 = gridlib.GridCellAttr()
    attr1.SetAlignment ( align_hor, align_ver )
    attr1.IncRef()       # Robin Dunn !!
    self.SetColAttr ( col, attr1 )

  # ****************************************************************
  # ****************************************************************
  def Align_All_Col ( self, align_hor = wx.ALIGN_LEFT,
                            align_ver = wx.ALIGN_CENTER ) :
    for C in range ( self.table.GetNumberCols () ) :
      self.Align_Col ( C, align_hor, align_ver )

  # ****************************************************************
  # v
  # ****************************************************************
  def Set_Cell_Editor ( self, Row, Col, Editor = wx.grid.GridCellTextEditor ) :
    self.SetCellEditor ( Row, Col, Editor () )
    """
    wx.grid.GridCellAutoWrapStringEditor()
    wx.grid.GridCellTextEditor ()
    wx.grid.GridCellBoolEditor ()  )
    wx.grid.GridCellChoiceEditor ( Field.Choices )  )
    wx.grid.GridCellAutoWrapStringEditor ()  )
    """

  # ****************************************************************
  # ****************************************************************
  def Get_Col_Widths ( self ) :
    Widths = []
    for Col in range ( self.table.GetNumberCols () ) :
      Widths.append ( self.GetColSize ( Col ) )
    return Widths

  # ****************************************************************
  # ****************************************************************
  ##def Set_Col_Widths ( self, Widths ) :
  def Set_Col_Widths ( self, *args ) :
    """
Sets the width of columns.
Width is a single integer or a list of integers.
This the specified number of columns is smaller than the available
number of columns, the remaining columns are set to the last value.
So if only 1 width is specified, all columns are set to that width.
If too many values are specified, they remaining are ignored.
Examples :
   Grid.Set_Col_Widths ( 100 )
   Grid.Set_Col_Widths ( ( 50, 150, 80 ) )
   Grid.Set_Col_Widths ( 50, 150, 80 )
    """

    """
    if isinstance ( Widths, int ) :
      Widths = [ Widths ]
    Widths = list ( Widths )
    """
    if len ( args ) == 1 :
      if Iterable ( args [0] ) :
        args = args [0]
    Widths = list ( args )

    N = self.table.GetNumberCols ()

    if len ( Widths ) == 0 :
      Widths.append ( 80 )

    while len ( Widths ) < N :
      Widths.append ( Widths [ -1 ] )

    for i in range ( N ) :
      self.SetColSize ( i, Widths [ i ] )

  # ****************************************************************
  # ****************************************************************
  def Set_All_Editor ( self, Editor = wx.grid.GridCellTextEditor ) :
    for Col in range ( self.table.GetNumberCols () ) :
      for Row in range ( self.table.GetNumberRows () ) :
        self.Set_Cell_Editor ( Row, Col, Editor )

  # ****************************************************************
  # ****************************************************************
  def Set_All_ReadOnly ( self ) :
    self.MY_Read_ONLY  = True
    ## The code below, makes the grid very slow
    #for Col in range ( self.table.GetNumberCols () ) :
    #  for Row in range ( self.table.GetNumberRows () ) :
    #    self.SetReadOnly ( Row, Col )

  # ****************************************************************
  # ****************************************************************
  def Delete_Row ( self, Row ) :
    self.DeleteRows ( Row )

  # ****************************************************************
  # ****************************************************************
  def Append_Row ( self, Col_Values ) :
    self.AppendRows ()
    Row = self.table.GetNumberRows () - 1
    for Col, Value in enumerate ( Col_Values ) :
      self.SetCellValue ( Row, Col, str ( Value )) #, 'windows-1252' ) )

  # ****************************************************************
  # ****************************************************************
  def Append_Dict_Row ( self, Row_Values ) :
    self.AppendRows ()
    Row = self.table.GetNumberRows () - 1
    NCol = self.table.GetNumberCols ()
    for Col in range ( NCol ) :
      Key = self.GetColLabelValue ( Col )
      Value = Row_Values [ Key ]
      if Value is None :
        Value = ''
      elif not ( isinstance ( Value, basestring )) :
        Value = str ( Value )
      self.SetCellValue ( Row, Col, Value )

  # ****************************************************************
  # ****************************************************************
  def AppendRows ( self, numRows = 1 ) :
    if self.table == self :
      gridlib.Grid.AppendRows ( self, numRows )
    else :
      # apparently in this construction table.AppendRows is NOT called
      # so we add the lines here
      NC = self.table.GetNumberCols ()
      for i in range ( numRows ) :
        self.table.data.append ( NC * [''] )
      self.ProcessTableMessage(wx.grid.GridTableMessage ( self.table,
        wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, numRows ) )

  # ****************************************************************
  # ****************************************************************
  def Get_Cell_Value ( self, Row, Col ) :
    if Row >= self.GetNumberRows () :
      return ''

    if self.table == self :
      GetValue = self.GetCellValue
    else :
      GetValue = self.table.GetValue
    return GetValue ( Row, Col )

  # ****************************************************************
  # ****************************************************************
  def Get_Col_Value ( self, Col ) :
    if Col >= self.GetNumberCols () :
      return self.GetNumberRows() * ['']

    ColValue = []
    if self.table == self :
      GetValue = self.GetCellValue
    else :
      GetValue = self.table.GetValue

    for i in range ( self.table.GetNumberRows () ) :
      ColValue.append ( GetValue ( i, Col ) )
    return NoCase_List ( ColValue )

  # ****************************************************************
  # ****************************************************************
  def GetRowValue ( self, Row ) :
    if Row >= self.GetNumberRows () :
      return self.GetNumberCols() * ['']

    RowValue = []
    if self.table == self :
      GetValue = self.GetCellValue
    else :
      GetValue = self.table.GetValue

    for i in range ( self.table.GetNumberCols () ) :
      RowValue.append ( GetValue ( Row, i ) )
    return RowValue

  # ****************************************************************
  # ****************************************************************
  def _On_Double_Click ( self, event ) :
    """
    By setting the variable Base_Grid_Double_Click of this module,
    to a callable function,
    this function will be called with CellValue, ColLabel, RowLabel
    """
    ##print 'DCLICK', Base_Grid_Double_Click, event.Row, event.Col, event.GetString()
    if Base_Grid_Double_Click :
      Row = event.Row
      Col = event.Col
      #if self.GetColLabelSize () > 0 :
      Col_Label = self.GetColLabelValue ( Col )
      Row_Label = self.GetRowLabelValue ( Row )
      ##print 'HYHTGTDFSG', Col_Label, Row_Label,self.GetCellValue ( Row, Col )
      Base_Grid_Double_Click ( self.GetCellValue ( Row, Col ),
                               Col_Label, Row_Label )
    else :
      event.Skip ()

  # ****************************************************************
  # ****************************************************************
  def OnLeftClick ( self, event ) :
    ##print 'Base_Grid ==> OnLeftClick'
    if self.table != self :
      if self.table.GetTypeName ( event.Row, event.Col ) == \
           gridlib.GRID_VALUE_BOOL :
        wx.CallLater ( 100, self.toggleCheckBox )
    event.Skip()

    if self.Random_Select :
      Row = event.GetRow ()
      Col = event.GetCol ()
      self.Toggle_Cell_Selected ( Row, Col )

  # *******************************************************
  # *******************************************************
  def Toggle_Cell_Selected ( self, Row, Col ) :
    """
    Special for random multiple cell selection,
    toggles the color of the clicked cell.
    """

    Value = self.GetCellValue ( Row, Col )
    if   Value == '__All__' :
      for Row in range ( 2, self.table.GetNumberRows () ) :
        Value = self.GetCellValue ( Row, Col )
        if Value :
          self.SetCellBackgroundColour ( Row, Col, self.Random_Select_Color )
        else :
          break
      self.ForceRefresh()

    elif Value == '__None__' :
      for Row in range ( 2, self.table.GetNumberRows () ) :
        Value = self.GetCellValue ( Row, Col )
        if Value :
          self.SetCellBackgroundColour ( Row, Col, wx.WHITE )
        else :
          break
      self.ForceRefresh()

    elif Value :
      Color = self.GetCellBackgroundColour ( Row, Col )
      if Color == self.Random_Select_Color :
        self.SetCellBackgroundColour ( Row, Col, wx.WHITE )
      else :
        self.SetCellBackgroundColour ( Row, Col, self.Random_Select_Color )
      self.ForceRefresh()

      Selected = []
      if self.Notify_Params_Changed :
        for Col in range ( self.table.GetNumberCols () ) :
          Fields = []
          for Row in range ( self.table.GetNumberRows () ) :
            Color = self.GetCellBackgroundColour ( Row, Col )
            if Color == self.Random_Select_Color :
              Value = self.GetCellValue ( Row, Col )
              if Value :
                Fields.append ( Value )
          if Fields :
            Table = self.GetColLabelValue ( Col )
            Selected.append ( ( Table, Fields ) )
        self.Notify_Params_Changed ( Selected )

  # ****************************************************************
  # ****************************************************************
  def onCheckBox ( self, event ) :
    self.afterCheckBox ( event.IsChecked () )

  # ****************************************************************
  # ****************************************************************
  def toggleCheckBox ( self ) :
    # this doesn't work always,
    # sometimes "cb" is not yet known !!
    try :
      self.cb.Value = not self.cb.Value
      self.afterCheckBox ( self.cb.Value )
    except :
      pass

  # ****************************************************************
  # ****************************************************************
  def afterCheckBox ( self, IsChecked ) :
    self.table.data [self.GridCursorRow + self.table.RF] \
                    [self.GridCursorCol + self.table.CF] = IsChecked
    self.OnEditorChange ( None )

  # ****************************************************************
  # ****************************************************************
  def onCellSelected ( self, event ) :
    #print 'Cell selected', event.Row, event.Col
    self.Last_Selected_Cell = event.Col, event.Row
    if self.table != self :
      if self.table.GetTypeName ( event.Row, event.Col ) in \
            [ gridlib.GRID_VALUE_BOOL, MY_GRID_TYPE_COLOR, MY_GRID_TYPE_FILE ] :
        wx.CallAfter ( self.EnableCellEditControl )
    event.Skip ()


  # ****************************************************************
  # called by table.SetValue, to change the active background color
  # ****************************************************************
  def Update_Colors ( self, R, C ) :
    RD = R + self.table.RF
    CD = C + self.table.CF
    if self.table.data [RD] [CD] :
      self.SetCellBackgroundColour ( R, C, self.table.data [RD] [CD] )
    else : # if empty string, leave it white
      self.SetCellBackgroundColour ( R, C, wx.WHITE )
    self.ForceRefresh()

  # ****************************************************************
  # Attribs = {
  #   'normal': [ font, textcolor, bgcolor ],
  #   3       : [ font, textcolor, bgcolor ],
  #   }
  # ****************************************************************
  def Define_Attribs ( self, Attribs ) :
    self.Attribs = Attribs
    for Attrib in Attribs :
      attr = gridlib.GridCellAttr()
      A = Attribs [ Attrib ]
      if A[0] :
        attr.SetFont ( A[0] )
      #else :
      #  attr.SetFont ( self.GetCellFont ( 0, 0 ) )
      if A[1] :
        attr.SetTextColour ( A[1] )
      if A[2] :
        attr.SetBackgroundColour ( A[2] )
      A.append ( attr )

  # ****************************************************************
  # ****************************************************************
  def Set_Cell_Attrib ( self, Col, Row, Attrib ) :
    try :
      A = self.Attribs [ Attrib ]
      if A[0] :
        self.SetCellFont ( Row, Col, A[0] )
      if A[1] :
        self.SetCellTextColour ( Row, Col, A[1] )
      if A[2] :
        self.SetCellBackgroundColour ( Row, Col, A[2] )
      self.ForceRefresh()
    except :
      pass

  # ****************************************************************
  # ****************************************************************
  def Set_Row_Attrib ( self, Row, Attrib ) :
    attr = self.Attribs [ Attrib ][-1]
    self.SetRowAttr ( Row, attr)
    self.ForceRefresh()

  # ****************************************************************
  # ****************************************************************
  def Set_Col_Attrib ( self, Col, Attrib ) :
    attr = self.Attribs [ Attrib ][-1]
    self.SetColAttr ( Col, attr)
    attr.IncRef()    # Robin Dunn !!
    self.ForceRefresh()

  # ****************************************************************
  # ****************************************************************
  ##def Set_Col_BarGraph ( self, Col, Max, Color ) :
  def Set_Col_BarGraph ( self, *args ) :
    """
    This should be changed, wether a grid is already ther or not
    at this moment we assume not creategrid is done yet,
    so we've to wait to create the renderers
    """
    ##self.BarGraph_columns.append ( ( Col, Max, Color ) )
    self.BarGraph_columns.append ( args )
    #attr = wx.grid.GridCellAttr ()
    #attr.SetRenderer ( _Gridcell_Bargraph ( Max, Color ) )
    #self.SetColAttr ( Col , attr )

  # ****************************************************************
  # ****************************************************************
  def Set_Col_BarTwoColor ( self, *args ) :
    self.BarTwoColor_columns.append ( args )

  # ****************************************************************
  # ****************************************************************
  def Set_Cell_Color ( self, Col, Row, Color ) :
    self.SetCellBackgroundColour ( Row, Col, Color )
    self.ForceRefresh()

  # ****************************************************************
  # ****************************************************************
  def Set_Col_Color ( self, Col, Color ) :
    # attribute objects let you keep a set of formatting values
    # in one spot, and reuse them if needed
    attr = gridlib.GridCellAttr()
    attr.SetFont ( self.GetCellFont ( 0, Col ) )
    #attr.SetTextColour ( wx.BLACK )
    attr.SetBackgroundColour ( Color )

    # you can set cell attributes for the whole row (or column)
    self.SetColAttr ( Col, attr )
    self.ForceRefresh()

  # ****************************************************************
  # ****************************************************************
  def Set_Row_Color ( self, Row, Color ) :
    # attribute objects let you keep a set of formatting values
    # in one spot, and reuse them if needed
    attr = gridlib.GridCellAttr()
    attr.SetFont ( self.GetCellFont ( Row, 0 ) )
    #attr.SetTextColour ( wx.BLACK )
    attr.SetBackgroundColour ( Color )

    # you can set cell attributes for the whole row (or column)
    self.SetRowAttr ( Row, attr)
    ##??attr.IncRef()    # Robin Dunn !!
    self.ForceRefresh()

  # ****************************************************************
  # ****************************************************************
  def Set_Region_Color ( self, R1, C1, R2, C2, Color ) :
    for R in range ( R1, R2+1 ) :
      for C in range ( C1, C2+1 ) :
        self.SetCellBackgroundColour ( R, C, Color )
    self.ForceRefresh()

  # ****************************************************************
  # ****************************************************************
  def Set_BG_Color_From_Parent ( self ) :
    # get rid of that ugly white background at places where there's no real grid
    self.SetDefaultCellBackgroundColour ( self.parent.GetBackgroundColour())

  # ****************************************************************
  # ****************************************************************
  def Alter_Row_Color ( self, Color = None ) :
    """
Call this once to set the alt row color.
Every fill will call this procedure, is Alt_Color is set
    """
    if Color :
      self.Alt_Color = Color

    # attribute objects let you keep a set of formatting values
    # in one spot, and reuse them if needed
    attr = gridlib.GridCellAttr()
    attr.SetFont ( self.GetCellFont ( 0, 0 ) )
    #attr.SetTextColour ( wx.BLACK )
    attr.SetBackgroundColour ( self.Alt_Color )

    for Row in range ( 1, self.GetNumberRows (), 2 ) :
      self.SetRowAttr ( Row, attr)
    self.ForceRefresh()

  # ****************************************************************
  # NOTE: OnEditorShown occurs before OnEditorCreated !!
  # ****************************************************************
  def onEditorCreated ( self, event) :
    '''
    def HandleShiftEnter ( event ) :
      print 'gsdufsdp',event.KeyCode, event.CtrlDown()
      if event.KeyCode == wx.WXK_RETURN and event.ShiftDown():
        event.GetEventObject().WriteText('\n')
      else:
        event.Skip()
      ctrlEH = event.GetControl().GetEventHandler()
      ctrlEH.Bind ( wx.EVT_KEY_DOWN, HandleShiftEnter)
    '''
    if self.MY_Read_ONLY :
      event.Veto()
      return

    self.Editor_Active = True
    if self.table == self :
      event.Skip ()
      return

    R = event.GetRow()
    C = event.GetCol()

    if self.table.GetRawTypeName ( R, C )  == gridlib.GRID_VALUE_BOOL :
      self.cb = event.Control
      self.cb.WindowStyle |= wx.WANTS_CHARS
      self.cb.Bind ( wx.EVT_KEY_DOWN, self._On_CB_KeyDown )
      self.cb.Bind ( wx.EVT_CHECKBOX, self.onCheckBox )

    elif self.table.GetRawTypeName ( R, C ) in \
           [ MY_GRID_TYPE_COLOR,  MY_GRID_TYPE_FILE ] :
      pass
    # proceed with normal event handle
    else:
      event.Skip()

  # ****************************************************************
  # NOTE: OnEditorShown occurs before OnEditorCreated !!
  # ****************************************************************
  def OnEditorShown(self, event):
    # so anyone can check if changes took place
    # on editor change doesn't happen,
    # until after the editor is stopped
    if self.MY_Read_ONLY :
      event.Veto()
      return

    self.Modified = True

    if self.table == self :
      event.Skip ()
      return

    R = event.GetRow()
    C = event.GetCol()
    RD = R + self.table.RF
    CD = C + self.table.CF

    if self.table.GetRawTypeName ( R, C )  == MY_GRID_TYPE_COLOR :
      # we manualy create a begin edit event
      #self.OnEditorCreated(event)

      # start the global color dialog
      # First block closing of the application
      #if self.Set_Modal_Open :
      #  self.Set_Modal_Open ( True )

      try:
        from dialog_support import Color_Dialog
        color = Color_Dialog ( self, self.table.data [RD] [CD] )
        # get the new color and store it
        self.table.data [RD] [CD] = color
        self.SetCellBackgroundColour ( R, C, self.table.data [RD] [CD] )
        self.ForceRefresh()

        # manualy generate an EditorChange event
        self.OnEditorChange(event)
        """
        colordlg = wx.ColourDialog ( self )
        colordlg.GetColourData().SetChooseFull(True)
        if self.Custom_Colors:
          cc = self.Custom_Colors
          for i in range ( len ( cc ) ):
            colordlg.GetColourData().SetCustomColour ( i, cc[i] )

        colordlg.GetColourData().SetColour ( self.table.data [RD] [CD] )
        if colordlg.ShowModal() == wx.ID_OK:
          # get the new color and store it
          self.table.data [RD] [CD] = colordlg.GetColourData().GetColour().Get()
          self.SetCellBackgroundColour ( R, C, self.table.data [RD] [CD] )
          self.ForceRefresh()

          # manualy generate an EditorChange event
          self.OnEditorChange(event)

        if self.Custom_Colors :
          cc = []
          for i in range ( 16 ):
            cc.append ( colordlg.GetColourData().GetCustomColour ( i ) )
          self.Custom_Colors = cc
        colordlg.Destroy()
        """
      finally:
        # unlock possibility to close the application
        #if self.Set_Modal_Open : self.Set_Modal_Open ( False )
        pass

      # prevent further actions for this event
      event.Veto()

    elif self.table.GetRawTypeName ( R, C )  == MY_GRID_TYPE_FILE :
      # start the global file dialog
      # First block closing of the application
      if self.Set_Modal_Open : self.Set_Modal_Open ( True )
      try:
        ##filepath, filename = path_split ( self.table.data [R] [1] )
        filepath, filename = path_split ( self.table.data [RD] [CD] )
      except:
        ##filepath = PG.Program_Directory
        filepath = os.getcwd ()
        filename = ''

      filename = AskFileForOpen ( filepath, filename,
                                  FileTypes = '*.dat', Title = 'Select File' )
      if filename:
        self.table.data [RD] [CD] = filename

        self.ForceRefresh()

        # manualy generate an EditorChange event
        self.OnEditorChange(event)

        # unlock possibility to close the application
        if self.Set_Modal_Open : self.Set_Modal_Open ( False )

      # prevent further actions for this event
      event.Veto()

    # proceed with normal event handle
    else:
      event.Skip()

  # ****************************************************************
  # Notify the parent/owner that some data properties have changed
  # ****************************************************************
  def OnEditorChange ( self, event ) :
    #if self.MY_Read_ONLY :
    #  event.Veto()
    #  return

    event.Skip()
    self.Editor_Active = False

    #print 'KKKLP', event.Row,event.Col #self.table, self, self.Notify_Params_Changed
    #print dir(event)
    #print event.ControlDown(), event.MetaDown(),event.CmdDown()

    Row = event.Row
    Col = event.Col
    if self.Notify_Params_Changed :
      if self.table == self :
        self.Notify_Params_Changed ( Row, Col, self.Get_Cell_Value ( Row, Col ) )
      else :
        self.Notify_Params_Changed ( Row, Col, self.GetTable().data )

  # ****************************************************************
  # Notify the parent/owner that some data properties have changed
  # ****************************************************************
  def Check_Editor_Active ( self ) :
    """
    If an editor is active, while the program is closing,
    the latest changes are not stored.
    So the parent can call this procedure to "store" the changes.
    """
    if self.Editor_Active :
      self.SaveEditControlValue ()


  # ****************************************************************
  # ****************************************************************
  def _On_CB_KeyDown ( self, event ) :
    if event.KeyCode == wx.WXK_UP :
      if self.GridCursorRow > 0:
        self.DisableCellEditControl ()
        self.MoveCursorUp ( False )
    elif event.KeyCode == wx.WXK_DOWN :
      if self.GridCursorRow < ( self.NumberRows - 1 ) :
        self.DisableCellEditControl ()
        self.MoveCursorDown ( False )
    elif event.KeyCode == wx.WXK_LEFT :
      if self.GridCursorCol > 0 :
        self.DisableCellEditControl ()
        self.MoveCursorLeft ( False )
    elif event.KeyCode == wx.WXK_RIGHT :
      if self.GridCursorCol < ( self.NumberCols - 1 ) :
        self.DisableCellEditControl ()
        self.MoveCursorRight ( False )
    else :
      event.Skip ()

  # testen bij meer colomns
  """
  def OnColSize ( self, event ) :
    #if event.GetRowOrCol() == 0 :
    self.ColSize0 ()
    event.Skip ()
  """

  # ****************************************************************
  # This is weird behavior of wxPython
  # if we don't leave room for a scrollbar,
  # the scrollbar will appear !!
  # Robin Dunn says: This is a problem with how the wx.ScrolledWindow is implemented.
  # Since it has fixed size scroll increments it always rounds the virtual size
  # up to an even multiple of the scroll increment,
  # so unless your virtual size is already an even multipl
  # you end up with needing a bit of extra unexpected space
  # in order to make the scrollbars be unnecessary.
  # ****************************************************************
  """
  def ColSize0 ( self ) :
    N = self.GetNumberCols () - 1
    if self.table.CF :
      w = self.GetRowLabelSize ()
    else :
      w = 0
    for col in range ( N ) :
      w += self.GetColSize ( col )
    self.SetColSize ( N, self.parent.GetSize()[0] - w - 20 )
  """

  # *************************************************************
  def Save_Settings ( self, ini = None, key = None, Data = True ) :
    #print 'SAVE GRID SETTINGS', ini, key
    # close cell editor, otherwise changes in progress will be lost
    self.Check_Editor_Active ()

    if not ( ini ) :
      return
    if not ( key ) :
      key = 'CS_'

    NR = self.GetNumberRows ()
    NC = self.GetNumberCols ()
    lijst = []
    lijst.append ( NR )
    lijst.append ( NC )
    lijst.append ( self.GetRowLabelSize () )
    lijst.append ( self.GetColLabelSize () )
    ini.Write ( key + 'RC', lijst)

    lijst = []
    colsize = []
    for i in range ( NC ) :
      lijst.append ( self.GetColLabelValue ( i ) )
      colsize.append ( self.GetColSize ( i ) )
    ini.Write ( key + 'Cols', lijst)
    ini.Write ( key + 'ColSize', colsize)

    lijst = []
    for i in range ( NR ) :
      lijst.append ( self.GetRowLabelValue ( i ) )
    ini.Write ( key + 'Rows', lijst)

    if Data and not ( self.Secret_Data ):
      lijst = []
      for C in range ( NC ) :
        for R in range ( NR ) :
          lijst.append ( self.GetCellValue ( R, C ) )
      ini.Write ( key + 'Cells', lijst)

  # *************************************************************
  def Load_Settings ( self, ini = None, key = None, Data = True ) :
    #print 'LOAD GRID SETTINGS', ini, key
    if not ( ini ) :
      return
    if not ( key ) :
      key = 'CS_'

    lijst = ini.Read ( key + 'RC', [] )
    if len ( lijst ) > 0 :
      NR = lijst.pop ( 0 )
    else :
      NR = self.GetNumberRows ()

    if len ( lijst ) > 0 :
      NC = lijst.pop ( 0 )
    else :
      NC = self.GetNumberCols ()

    # be sure we've enough rows and cols
    if NR > self.GetNumberRows () :
      self.AppendRows ( NR - self.GetNumberRows () )
    if NC > self.GetNumberCols () :
      self.AppendCols ( numCols = NC - self.GetNumberCols () )


    if len ( lijst ) > 0 :
      val = lijst.pop ( 0 )
      self.SetRowLabelSize ( val )
    if len ( lijst ) > 0 :
      val = lijst.pop ( 0 )
      self.SetColLabelSize ( val )

    lijst   = ini.Read ( key + 'Cols', [] )
    i = 0
    while len ( lijst ) > 0 :
      val = lijst.pop ( 0 )
      self.SetColLabelValue ( i, val )
      i += 1

    lijst = ini.Read ( key + 'ColSize', [] )
    i = 0
    while len ( lijst ) > 0 :
      val = lijst.pop ( 0 )
      self.SetColSize ( i, val )
      #print 'SET COL SIZE', i, val
      i += 1

    lijst = ini.Read ( key + 'Rows', [] )
    i = 0
    while len ( lijst ) > 0 :
      val = lijst.pop ( 0 )
      self.SetRowLabelValue ( i, val )
      i += 1

    if Data and not ( self.Secret_Data ):
      lijst = ini.Read ( key + 'Cells', [] )
      for C in range ( NC ) :
        for R in range ( NR ) :
          if len ( lijst ) > 0 :
            val = lijst.pop ( 0 )
            #print 'Gird load settings',R,C,val
            self.SetCellValue ( R, C, val )
          else :
            break

    self.ForceRefresh()
# ***********************************************************************

# *********************************************
# *********************************************
class Field_Object ( object ) :
  def __init__ ( self, Org_Name, ReadOnly = False ) :
    self.Org_Name    = Org_Name
    self.Name        = Org_Name
    self.Value       = None
    self.Type        = CT_STRING
    self.Choices     = None
    self.ID_2_Choice = {}       # if choices are numbers, this is translation
    self.Choice_2_ID = {}       #                         reverse translation
    self.Validation  = ''
    self.Description = ''
    self.ReadOnly    = ReadOnly
    self.NotNull     = False

  def __repr__ ( self ) :
    import traceback
    try :
      Line = u''
      Line += 'Org_Name    = %s\n' % self.Org_Name
      Line += 'Name        = %s\n' % self.Name
      Line += 'Value       = %s\n' % _2U ( self.Value )
      Line += 'Type        = %s\n' % self.Type
      try :
        Line += 'Choices     = %s\n' % self.Choices
      except :
        Line += '\n' + traceback.format_exc ()

      if self.ID_2_Choice :
        for ID, Choice in list(self.ID_2_Choice.items ()) :
          Line += 'ID_2_Choices  = %s : %s\n' % ( ID, Choice )
      Line += 'Validation  = %s\n' % self.Validation
      Line += 'Description = %s\n' % self.Description
      Line += 'ReadOnly    = %s\n' % self.ReadOnly
      Line += 'NotNull     = %s\n' % self.NotNull
    except :
      ##print 'OOOOO',self.Org_Name, self.Value
      Line += '\n' + traceback.format_exc ()
    print('$$$$$$', type ( Line), self.Value, type(self.Value), '$$$$$$')
    return Line.encode ( 'Windows-1252')
# *********************************************


# ***********************************************************************
# ***********************************************************************
class Field_Objects_Grid ( gridlib.Grid ) :
  def __init__ ( self, parent, name = 'Field Objects Grid' ) :
    gridlib.Grid.__init__ ( self, parent, -1 )

    self.parent           = parent
    self.My_Name          = name
    self.Grid_Created     = False
    self.Notify_Params_Changed = None

    self.table = self
    self.AutoSizeRows (True)

    self.SetMargins ( 0, 0 )
    ##?self.DefaultCellOverflow = False

    self.Bind ( wx.EVT_SIZE, self._On_Resize )

    if sys.version_info.major > 2 :
      self.Bind ( gridlib.EVT_GRID_CELL_CHANGED, self._On_Editor_Change )
    else :
      self.Bind ( gridlib.EVT_GRID_CELL_CHANGE, self._On_Editor_Change )

    self.Bind ( gridlib.EVT_GRID_EDITOR_SHOWN  , self._On_Editor_Shown )

    # To get multiline editor working, with a normal Enter !!
    #self.SetDefaultEditor ( wx.grid.GridCellAutoWrapStringEditor() )
    self.SetDefaultEditor ( wx.grid.GridCellTextEditor() )

    self.Bind ( wx.EVT_KEY_DOWN, self._On_Key_Down )

    self.SetRowLabelSize ( 190 )
    self.SetColLabelSize ( 24 )
    self.SetRowLabelAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )
    self.SetColLabelAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )

    self.Editor_Cell_Row = None
    self.Editor_Cell_Col = None

    self.Font_Normal = self.GetFont ()
    self.Font_Bold   = self.GetFont ()
    self.Font_Bold.SetWeight ( wx.BOLD )

  # *******************************************************
  # *******************************************************
  def _On_Resize ( self, event = None ) :
    #print 'Resizeggg'
    if event :
      event.Skip ()
    if self.GetNumberCols() > 1 :
      W = self.parent.GetClientSize()[0]
      w = self.GetRowLabelSize() + self.GetColSize(1)
      #print 'xczxcvzcxvzv',  W - w - 25
      ColSize = W - w - 25
      if ColSize <= 0:
          ColSize = 10
      self.SetColSize ( 0, ColSize )

  # *******************************************************
  # *******************************************************
  def _On_Key_Down ( self, event ) :
    # transform a normal Enter in a newline character
    if not ( self.Editor_Cell_Row ) :
      event.Skip ()
      return

    ##print 'FTAR',self.Editor_Cell_Row, self.Editor_Cell_Col,self.GetCellEditor ( self.Editor_Cell_Row, self.Editor_Cell_Col )
    if event.GetKeyCode() == wx.WXK_RETURN :
      Editor = self.GetCellEditor ( self.Editor_Cell_Row, self.Editor_Cell_Col )
      if isinstance ( Editor, wx.grid.GridCellAutoWrapStringEditor ) :
        event.EventObject.WriteText ( '\n' )
        #self.SetRowSize ( 3, 7*13+4 )
      else :
        Row = self.GetGridCursorRow() + 1
        if Row < self.GetNumberRows():
          self.SetGridCursor ( Row, 0)
          self.MakeCellVisible ( Row, 0)

    else :
      print('KKKK',event.GetKeyCode ())
      event.Skip ()

  # ****************************************************************
  # NOTE: OnEditorShown occurs before OnEditorCreated !!
  # ****************************************************************
  def _On_Editor_Shown ( self, event ) :
    self.Editor_Cell_Row = event.Row
    self.Editor_Cell_Col = event.Col

  # ****************************************************************
  # Notify the parent/owner that some data properties have changed
  # ****************************************************************
  def _On_Editor_Change ( self, event ) :
    self.Editor_Cell_Row = None
    self.Editor_Cell_Col = None

    #print 'KKKLP editor change', event.Row,event.Col #self.table, self, self.Notify_Params_Changed
    if self.Notify_Params_Changed :
      self.Notify_Params_Changed ( event.Row )

    if self.table == self :
      if event :
        event.Skip ()
      return


  # *******************************************************
  # *******************************************************
  def Get_Differences ( self, Field_Objects ) :
    Changes = self.Show_Differences ()
    for i in Changes :
      Value = self.GetCellValue ( i, 0 )

      try :
        if Value is None :
          Value = ''

        # *****  INTEGER  *******************************
        elif Field_Objects[i].Type == CT_INT :
          if Value.strip () :
            Field_Objects [i].Value = int ( Value )
          else :
            Field_Objects [i] = None

        # *****  FLOAT  *******************************
        elif Field_Objects[i].Type == CT_FLOAT :
          if Value.strip () :
            Field_Objects [i].Value = float ( Value )
          else :
            Field_Objects [i] = None

        # *****  Delphi DateTime  *****
        elif Field_Objects[i].Type == CT_DateTime_Delphi :
          Field_Objects [i].Value = Delphi_Date ( Value )

        # *****  Choices  *****
        elif Field_Objects[i].Type == CT_Choice :
          if Field_Objects [i].Choice_2_ID :
            Field_Objects [i].Value = Field_Objects [i].Choice_2_ID [ Value ]
          else :
            Field_Objects [i].Value = Value

        # *****  Else  *****
        else :
          Field_Objects [i].Value = Value

      except :
        pass

    return Changes


  # *******************************************************
  # *******************************************************
  def Show_Differences ( self ) :
    if self.GetNumberCols() > 1 :
      W = self.parent.GetClientSize()[0]
      w = old_div(( W - self.GetRowLabelSize() - 25 ), 2)
      self.SetColSize ( 0, w )
      self.SetColSize ( 1, w )

      Any_Diff = False
      Changes = []
      for i, Row in enumerate ( self.Data ) :
        Diff = False
        Value = Row.Value
        if Value is None :
          Value = ''

        # to see empty values, we need to highlight both

        # For special types we need special comparison
        if Row.Type == CT_DateTime_Delphi :
          if Value :
            Diff = Delphi_Date ( self.GetCellValue ( i, 0 ) ) != \
                   int ( float ( Row.Value ) )
            if Diff :
              Value = Delphi_Date ( Row.Value ).to_String ()
            else :
              Value = ''
          else :
            Diff = self.GetCellValue ( i, 0 ) != ''

        # *****  Choices  *****
        elif Row.Type == CT_Choice :
          ##if Value and  Row.Choice_2_ID :
          if Value and  Row.ID_2_Choice :
            ##GvV gewijzigd : int ( ) toegevoegd ivm foutmelding
            Value = str ( Row.ID_2_Choice [ int ( Value ) ] )
            Diff  = Value != self.GetCellValue ( i, 0 )
            ##print '???', Diff, type(Value), type(self.GetCellValue ( i, 0 ))
          else :
            Diff = self.GetCellValue ( i, 0 ) != u''
          if not ( Diff ) :
            Value = ''

        #elif self.GetCellValue ( i, 0 ) == str(Value) :
        #else :
        #  Diff = True
        else :
          Test = Value
          if not ( isinstance ( Value, basestring ) ) :
            Test = str ( Test )
          if self.GetCellValue ( i, 0 ) == Test :
            Value = ''
          else :
            Diff = True

        if Diff :
          Any_Diff = True
          Changes.append (i)
          self.SetCellFont ( i, 0, self.Font_Bold )
        else :
          self.SetCellFont ( i, 0, self.Font_Normal )

        #self.SetCellValue ( i, 1, str ( Value ))
        if not ( isinstance ( Value, basestring )) :
          Value = str ( Value )
        self.SetCellValue ( i, 1, Value )

      if Any_Diff :
        self.SetColLabelValue ( 1, 'Orginal')
      else :
        self.SetColLabelValue ( 1, '')
      self.ForceRefresh()
      return Changes

  # *******************************************************
  # *******************************************************
  def Do_Checks ( self ) :
    if self.GetNumberCols() > 1 :
      W = self.parent.GetClientSize()[0]
      w = old_div(( W - self.GetRowLabelSize() - 25 ), 2)
      self.SetColSize ( 0, w )
      self.SetColSize ( 1, w )

      Error = False
      for i, Row in enumerate ( self.Data ) :
        Result = True
        Value = Row.Validation
        x = self.GetCellValue ( i, 0 )
        ##print '+++',i,Value,Row.Type, x
        if Value :
          try :
            if Row.Type == CT_INT :
              x = int ( x )
            elif Row.Type == CT_FLOAT :
              x = float ( x )
            ##elif Row.Type == CT_DateTime_Delphi :
            ##  x = Delphi_Date ( x )
            Result = eval ( Value )
          except :
            Result = None
          print('Result:',Value, type(Value), Result)

        # *****  INTEGER  *******************************
        elif Row.Type == CT_INT :
          if x.strip() :
            try :
              x = int ( x )
            except :
              Result = None
              Value = 'Geheel getal vereist, bijv.  3 of 684 of -22'
            ##print 'Test INT', Result, Value

        elif Row.Type == CT_FLOAT :
          if x.strip() :
            try :
              x = float ( x )
            except :
              Result = None
              Value = 'Decimaal getal vereist, bijv.  3.7 of 684 of -22.77'
            ##print 'Test INT', Result, Value


        elif Row.Type == CT_DateTime_Delphi :
          if x :
            Result = Delphi_Date ( x )
            if not ( Result ) :
              Value = 'DD-MM-JJJJ,  geen geldige datum'

        elif Row.Type == CT_Email :
          if not ( x.strip () ) :
            Result = True
          else :
            from mail_support import Valid_Email_2
            Result = Valid_Email_2 ( x )
            Value = 'Geen geldig Email adres'

        ##if Result is None :
        if not ( Result ) :
          Error = True
          self.SetCellValue ( i, 1, str ( Value ) )
          self.SetCellFont ( i, 0, self.Font_Bold )
        else :
          self.SetCellValue ( i, 1, '')
          self.SetCellFont ( i, 0, self.Font_Normal )

      if Error :
        self.SetColLabelValue ( 1, 'Condition')
      else :
        self.SetColLabelValue ( 1, '')
      self.ForceRefresh ()

    # Do check
    return not ( Error )

  # *******************************************************
  # *******************************************************
  def Fill_Field_Data ( self, Field_Objects ) :
    """
Fill a property like grid with Data.
Data consists of 2 lists, the first one with the key value,
which will be placed in the fixed column.
The list in Data consists of the values and will be placed inthe second column.
By choosing this organization of the input data,
a 1-line result of a database query can be shown directly.
"""
    self.Data = copy.copy ( Field_Objects )

    # **************************************
    # be sure we've enough column types
    # **************************************
    NRow = len ( Field_Objects )
    NCol = 1

    # **************************************
    # CreateGrid is only allowed once !!
    # **************************************
    if not ( self.Grid_Created ) :
      ##P3:self.CreateGrid ( NRow, NCol+1, wx.grid.Grid.SelectCells )
      self.CreateGrid ( NRow, NCol+1 )
      self.Grid_Created = True

    Attr = gridlib.GridCellAttr()
    Attr.SetFont ( self.Font_Bold )
    Attr.SetReadOnly ( True )
    self.SetColAttr ( 1, Attr )
    Attr.IncRef ()

    self.SetColLabelValue ( 0, 'Value' )
    self.SetColLabelValue ( 1, '' )

    # **************************************
    # Display the data
    # **************************************
    self.SetDefaultColSize ( 50, True )
    for i, Field in enumerate ( Field_Objects ) :
      ##print '><><<><><Fill_Field_Data', i, Field.Name, Field.Type
      self.SetRowLabelValue ( i, Field.Name )
      self.SetCellFont ( i, 0, self.Font_Normal )

      if Field.Type == CT_Choice :
        if not Field.Choices :
          Field.Choices = []
          for ID, Choice in list(Field.ID_2_Choice.items()) :
            Field.Choices.append ( Choice )
          Field.Choices.sort ()

          if not Field.Choice_2_ID :
            for ID, Choice in list(Field.ID_2_Choice.items()) :
              Field.Choice_2_ID [ Choice ] = ID

        if not Field.ID_2_Choice :
          for ii, Choice in enumerate ( Field.Choices ) :
            Field.ID_2_Choice [ii] = Choice

        if not Field.Choice_2_ID :
          for ii, Choice in enumerate ( Field.Choices ) :
            Field.Choice_2_ID [ Choice ] = ii

      if Field.Value :
        Value = Field.Value
        if Field.Type and isinstance ( Field.Type, basestring ) :
          Field.Type = int ( Field.Type )

        if Field.Type == CT_DateTime_Delphi :
          Value = Delphi_Date ( Value ).to_String ()

        elif ( Field.Type == CT_Choice ) :
          """
          if not Field.ID_2_Choice :
            for ii, Choice in enumerate ( Field.Choices ) :
              Field.ID_2_Choice [ii] = Choice

          if not Field.Choice_2_ID :
            for ii, Choice in enumerate ( Field.Choices ) :
              Field.Choice_2_ID [ Choice ] = ii
          """

          try :
            ##GvV gewijzigd : int ( ) toegevoegd ivm foutmelding
            Value = Field.ID_2_Choice [ int ( Value ) ]
          except :
            import traceback
            print(traceback.format_exc ())
            print(Field.Name, Value, Field.ID_2_Choice)

        else :
          if not ( isinstance ( Value, basestring ) ) :
            Value = str ( Value )
      else :
        Value = ''

      """
      print '==========>> SetCelValue',Field.Name,
      try :
        print Field ##Field.Type,type(Value), Value
      except :
        print '???????'
      """

      self.SetCellValue ( i, 0, Value )
      self.SetCellValue ( i, 1, ''    )

      if Field.ReadOnly :
        self.SetCellBackgroundColour ( i, 0, wx.LIGHT_GREY )
        self.SetReadOnly ( i, 0 )
      else :
        self.SetCellBackgroundColour ( i, 0, wx.WHITE )
        self.SetReadOnly ( i, 0, False )

      N = 1
      if Field.Type == CT_BOOL :
        self.SetCellRenderer ( i, 0, wx.grid.GridCellBoolRenderer () )
        self.SetCellEditor   ( i, 0, wx.grid.GridCellBoolEditor ()  )
      elif Field.Type == CT_Choice :
        """
        if not Field.ID_2_Choice :
          for ii, Choice in enumerate ( Field.Choices ) :
            Field.ID_2_Choice [ii] = Choice

        if not Field.Choice_2_ID :
          for ii, Choice in enumerate ( Field.Choices ) :
            Field.Choice_2_ID [ Choice ] = ii
        """

        Keys = list(Field.Choice_2_ID.keys())
        Keys.sort()
        self.SetCellEditor ( i, 0, wx.grid.GridCellChoiceEditor ( Keys ))
        """
        if Field.ID_2_Choice :
          if not ( Field.Choice_2_ID ) :
            for K, V in Field.ID_2_Choice.iteritems() :
              Field.Choice_2_ID [ V ] = K

          Keys = Field.Choice_2_ID.keys()
          Keys.sort()
          self.SetCellEditor ( i, 0, wx.grid.GridCellChoiceEditor ( Keys ))
        else :
          self.SetCellEditor ( i, 0, wx.grid.GridCellChoiceEditor (
              Field.Choices )  )
        """

      elif Field.Type == CT_Multi_Line :
        self.SetCellRenderer ( i, 0, wx.grid.GridCellStringRenderer () )
        self.SetCellEditor   ( i, 0, wx.grid.GridCellAutoWrapStringEditor ()  )
        if Value :
          N = len ( Value.splitlines() )
          N = max ( N, 3)
        else :
          N = 3


      self.SetRowSize ( i, N*15+4 )
    self._On_Resize ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Field_Objects_Form ( wx.Dialog ) :
  def __init__ ( self, parent, title = 'title', Help = '' ) :

    Style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
    #Style ^= wx.CLOSE_BOX
    Style ^= wx.SYSTEM_MENU
    #wx.Dialog.__init__ ( self, None, title = title,
    wx.Dialog.__init__ ( self, parent, title = title,
                         size = ( 700, 500 ),         #( 600, 400 )
                         style = Style )
    if parent :
      Font = parent.GetFont ()
      self.SetFont ( Font )

    GUI = """
    P1            ,PanelVer  ,010
      NN_wx.StaticText,  label = Help
      self.Grid   ,Field_Objects_Grid
#      P2          ,PanelHor  ,00000000  ,wx.ALIGN_RIGHT
      P2          ,PanelHor  ,00000000
        B_Diff      ,wx.Button  ,label = "Difference"
        B_Check     ,wx.Button  ,label = "Check"
        B_Print     ,wx.Button  ,label = "Print"
        B_Cancel    ,wx.Button  ,wx.ID_OK,label = 'Ok'
        B_OK        ,wx.Button  ,wx.ID_CANCEL ,label = 'Cancel'
    """
    self.wxGUI = Create_wxGUI ( GUI )
    print("Start DIASDASDASD")
    ''' zou dit moeten geven
    P1_box.Add ( P2,0, wx.ALIGN_RIGHT )
    '''

    B_Diff  .Bind ( wx.EVT_BUTTON, self._On_Show_Difference )
    B_Check .Bind ( wx.EVT_BUTTON, self._On_Show_Check      )
    B_Print .Bind ( wx.EVT_BUTTON, self._On_Print           )
    #B_Print.Enable ( False )

  # ****************************************************************
  def Show_Modal ( self, Field_Objects = None ) :
    if Field_Objects :
      self.Grid.Fill_Field_Data ( Field_Objects )

    while True :
      Result = self.ShowModal ()
      if Result == wx.ID_CANCEL :
        return []
      if self.Grid.Do_Checks () :
        #Diff = self.Grid.Show_Differences ()
        #for i in Diff :
        #  Field_Objects[i].Value = self.Grid.Data[i].Value
        return self.Grid.Get_Differences ( Field_Objects )
      else :
        Show_Message ( """Controleer de vet gedrukte waarden,
deze voldoen niet aan de vereiste criteria""" )

  # ****************************************************************
  def _On_Show_Difference ( self, event = None ) :
    self.Grid.Show_Differences ()

  # ****************************************************************
  def _On_Show_Check ( self, event = None ) :
    self.Grid.Do_Checks ()

  # ****************************************************************
  def _On_Print ( self, event = None ) :
    #frame = wx.Frame(None, -1, "Dummy wx frame for testing printout.py")
    #frame.Show(True)
    import wx.lib.printout as wp
    ptbl = wp.PrintGrid ( None, self.Grid )
    #print dir(ptbl.GetTable())
    Table = ptbl.GetTable ()
    Table.SetLandscape()
    Table.SetPaperId(wx.PAPER_A4)

    """
    ['GetTable', 'Preview', 'Print', 'SetAttributes', '__doc__',
    '__init__', '__module__', 'grid', 'table', 'total_col', 'total_row']
    """
    #ptbl.SetLandscape()
    ptbl.Preview()
    ##app.MainLoop()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def Dialog_RecordForm ( Parent, Title, Field_Objects, Help = '' ) :
  Grid_RecordForm = Field_Objects_Form ( Parent, Title, Help )
  Changes = Grid_RecordForm.Show_Modal ( Field_Objects )
  Grid_RecordForm.Destroy ()
  return Changes
# ***********************************************************************


# ***********************************************************************
# the improved handling of boolean editing, is taken from Frank Millman
#   http://wiki.wxpython.org/Change_wxGrid_CheckBox_with_one_click
# ***********************************************************************
class Year_Grid ( Base_Grid ):
  def __init__ ( self, parent, name = 'Year Grid' ) :


    Base_Grid.__init__ ( self, parent, name = name )
    # WERKT NIET self.SetForegroundColour  (  wx.RED )

    self.Bind ( gridlib.EVT_GRID_CELL_LEFT_CLICK, self._OnLeftClick )

    self.ToDay      = None
    self.Day_Events = {}
    self._On_Left_Click_Completion = None

  # ****************************************************************
  # ****************************************************************
  def _OnLeftClick ( self, event ) :
    Row = event.GetRow ()
    Col = event.GetCol ()
    print('Click', Col, Row)
    if self._On_Left_Click_Completion :
      self._On_Left_Click_Completion ( Row, Col )
    event.Skip ()

  # ****************************************************************
  # ****************************************************************
  def Set_Col_DayPlan ( self, Col, Color = wx.GREEN, Max = 8 ) :
    """
    """
    attr = wx.grid.GridCellAttr ()
    attr.SetRenderer ( _Gridcell_DayPlan ( Color, Max ) )
    self.SetColAttr ( Col , attr )

  # ****************************************************************
  # ****************************************************************
  def Set_ToDay ( self, Week, Day ) :
    self.ToDay = ( Week, Day )
# ***********************************************************************


# ***********************************************************************
# the improved handling of boolean editing, is taken from Frank Millman
#   http://wiki.wxpython.org/Change_wxGrid_CheckBox_with_one_click
# ***********************************************************************
class Base_Table_Grid ( Base_Grid ):
  def __init__ ( self, parent,
                 data, data_types, data_defs,
                 ##custom_colors = None,
                 ##Set_Modal_Open = None,
                 name = 'Table Grid',
                 Notify_Params_Changed = None ) :

    self.table                 = CustomDataTable ( data, data_types, data_defs )
    #gridlib.Grid.__init__(self, parent, -1)
    Base_Grid.__init__ ( self, parent, self.table, name = name, editor = 'singleline' )

    ##self.Custom_Colors         = custom_colors
    ##self.Set_Modal_Open        = Set_Modal_Open
    self.Notify_Params_Changed = Notify_Params_Changed

    # attach table (ownership = True to auto destroy)
    self.SetTable ( self.table, True )

    for data_def in data_defs :
      if data_def in [ MY_GRID_FIXED_COL, MY_GRID_FIXED_ROW_COL ]:
        self.SetRowLabelSize ( 40 )
        break
    else :
      self.SetRowLabelSize ( 0 )

    for data_def in data_defs :
      if data_def in [ MY_GRID_FIXED_ROW, MY_GRID_FIXED_ROW_COL ]:
        self.SetColLabelSize ( 16 )
        break
    else :
      self.SetColLabelSize ( 0 )

    self.SetRowLabelAlignment (wx.ALIGN_LEFT, wx.ALIGN_CENTER )
    self.SetColLabelAlignment (wx.ALIGN_RIGHT, wx.ALIGN_CENTER )

    #self.AutoSizeRows (True)
    #self.DeleteRows ()
    #self.ClearGrid ()

    # due to a bug / limitation in wxPython
    # numbers are always aligned right
    # so therefor we align everyhting right
    attr1 = gridlib.GridCellAttr()
    attr1.SetAlignment ( wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
    #attr1.SetAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTER_VERTICAL)
    #attr1.SetAlignment ( wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
    for col in range ( self.GetNumberCols () ) :
      self.SetColAttr ( col, attr1 )
      attr1.IncRef()    # Robin Dunn !!

      for row in range ( self.GetNumberRows () ) :
        typ = self.table.GetRawTypeName ( row, col )
        if typ in [ MY_GRID_TYPE_COLOR ] :
          self.table.GetView().Update_Colors( row, col )
# ***********************************************************************


# ***********************************************************************
# the improved handling of boolean editing, is taken from Frank Millman
#   http://wiki.wxpython.org/Change_wxGrid_CheckBox_with_one_click
# ***********************************************************************
class Base_Simple_Grid ( gridlib.Grid ) : #Base_Grid ):
  """
Simple grid with multiline editor
can be used with a fixed Row and a fixed Column
Extensively used in RadQuest !!
  """
  def __init__ ( self, parent, name = 'Table Grid' ) :
    self.My_Name = name
    gridlib.Grid.__init__ ( self, parent, -1 )
    self.Grid_Created = False

    self.SetColLabelSize ( 16 )
    self.SetRowLabelSize ( 40 )

    # To get multiline editor working, with a normal Enter !!
    # Also On_Key must be fetched
    self.SetDefaultEditor ( wx.grid.GridCellAutoWrapStringEditor() )
    self.SetDefaultRenderer ( wx.grid.GridCellStringRenderer () )
    self.Bind ( wx.EVT_KEY_DOWN, self._On_Key )
    self.Clear ()

  # *******************************************************
  # *******************************************************
  def Clear ( self, NCols = None, NRows = None ):
    # Create the grid once
    if not ( self.Grid_Created ) :
      self.Grid_Created = True
      if NRows and NCols :
        self.CreateGrid ( NRows, NCols)
      else :
        self.CreateGrid ( 5, 5 )

    # Correct number of Columns and Rows
    self._Correct_NCol ( NCols )
    self._Correct_NRow ( NRows )

    if NRows and NCols :
      for Row in range ( NRows ) :
        for Col in range ( NCols ) :
          self.SetCellValue ( Row, Col, '' )

  # *******************************************************
  # *******************************************************
  def _Correct_NCol ( self, NCols ) :
    if NCols :
      NCol = self.GetNumberCols ()
      if NCol > NCols :
        self.DeleteCols ( numCols = NCol - NCols )
      elif NCol < NCols :
        self.AppendCols ( numCols = NCols - NCol )

  # *******************************************************
  # *******************************************************
  def _Correct_NRow ( self, NRows ) :
    if NRows :
      NRow = self.GetNumberRows ()
      if NRow > NRows :
        self.DeleteRows ( numRows = NRow - NRows )
      elif NRow < NRows :
        self.AppendRows ( numRows = NRows - NRow )

  # *******************************************************
  # *******************************************************
  def Set_Col_Labels ( self, Labels ) :
    NLabel = len ( Labels )
    if NLabel > self.GetNumberCols () :
      self._Correct_NCol ( NLabel )
    for i, Label in enumerate ( Labels ) :
      if not isinstance ( Label, basestring ) :
        Label = str ( Label )
      self.SetColLabelValue ( i, Label )

  # *******************************************************
  # *******************************************************
  def Set_Row_Labels ( self, Labels ) :
    NLabel = len ( Labels )
    if NLabel > self.GetNumberRows () :
      self._Correct_NRow ( NLabel )
    for i, Label in enumerate ( Labels ) :
      if not isinstance ( Label, basestring ) :
        Label = str ( Label )
      self.SetRowLabelValue ( i, Label )

  # *******************************************************
  # *******************************************************
  def Align_Hor ( self, Align = wx.ALIGN_CENTRE ) :
    # Sets the alignment of Labels and Cells
    self.SetRowLabelAlignment    ( Align, wx.ALIGN_CENTRE )
    self.SetColLabelAlignment    ( Align, wx.ALIGN_CENTRE )
    self.SetDefaultCellAlignment ( Align, wx.ALIGN_TOP    )

  # ********************************************************
  # ********************************************************
  def GetName ( self ) :
    # Special for notebooks and other components,
    # which use this name to show to the user
    return self.My_Name

  # *******************************************************
  # *******************************************************
  def _On_Key ( self, event ) :
    Key = event.GetKeyCode ()
    if Key == wx.WXK_RETURN :
      event.EventObject.WriteText ( '\n' )
    else :
      event.Skip ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class tProperties_Form ( wx.Frame ) :
  def __init__ ( self, parent, device,
                 data, data_types, data_defs,
                 title, Pos = (50,50) ):
    self.device = device
    self.data   = data

    # the initial height/width of the form is derived from
    # the number of elements corrected for fixed row/col
    N = len ( data )
    for data_def in data_defs :
      if data_def in [ MY_GRID_FIXED_ROW, MY_GRID_FIXED_ROW_COL ]:
        N += 1
        break
    h = 55 + 17 * N

    N = len ( data [0] )
    for data_def in data_defs :
      if data_def in [ MY_GRID_FIXED_COL, MY_GRID_FIXED_ROW_COL ]:
        N += 1
        break
    w = 40 + 40 * N


    FormStyle = wx.DEFAULT_FRAME_STYLE | \
                wx.TINY_CAPTION_HORIZ
                #wx.STAY_ON_TOP
    if parent:
      FormStyle = FormStyle | wx.FRAME_FLOAT_ON_PARENT    # needs a parent

    wx.Frame.__init__(
        self, parent, -1, title,
        size = ( w, h ),
        pos = Pos,
        style = FormStyle
        )


    GUI = """
    P1            ,PanelVer  ,10
      self.Grid   ,Base_Table_Grid ,data, data_types, data_defs
      P2          ,PanelHor  ,00
        self.B_Save    ,wx.Button,  label = 'Save'
        Button_2    ,wx.Button,  label = "Test2", pos = (100,0)
    """
    self.wxGUI = Create_wxGUI ( GUI, Ini_File_String = 'self.Ini_File' )


    self.B_Save.Bind ( wx.EVT_BUTTON, self._On_Save )


    self.Grid.Set_Cell_Attrib (0,0,'normal')

    # Binding to the panel instead of the form works better
    #panel.Bind ( wx.EVT_SIZE, self.OnResize )

    # Timer to test dynamic updating of grid
    self.Timer = wx.Timer ( self )
    # the third parameter is essential to allow other timers
    self.Bind ( wx.EVT_TIMER, self.OnTimer, self.Timer )
    #self.Timer.Start ( 2000 )


  def OnTimer ( self, event ) :
    #print self.data [1] [1]
    self.data [1] [1] += 1
    self.Device_Refresh_Properties ( self.data )

  # *********************************************************
  # *********************************************************
  def _On_Save ( self ) :
    """ SHOULD BE OVERRIDEN BY THE PARENT"""
    pass


  # *********************************************************
  # called by the device's container, if properties like position changes
  # in this case the table information will be updated
  # *********************************************************
  def Device_Refresh_Properties (self, data ):
    for R in range ( len(data)):
      try:    self.Grid.GetTable().SetValue ( R, 1, data[R][1] )
      except: pass
    self.Grid.Refresh()

  def Set_Modal_Open ( self, modal_open = True ):
    print('Set_Modal_Open', modal_open)

  def Notify_Params_Changed ( self, data ) :
    print('Notify_Params_Changed')

  """
  def OnResize ( self, event ) :
    event.Skip ()
    self.grid.ColSize0 ()
  """
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Test_Form ( wx.Frame ) :
  def __init__ ( self, ini = None ) :
    wx.Frame.__init__( self, None )

    GUI = """
    self.NB              ,wx.Notebook   ,style = wx.BK_LEFT
      self.Grid          ,Base_Grid        ,name = 'File'
    """
    self.wxGUI = PG.Create_wxGUI ( GUI, my_parent = 'self' )

    #gridlib.Grid.AppendCols()
    #gridlib.Grid.InsertCols()

    self.Grid.CreateGrid ( 10, 5 )
    self.Grid.SetCellValue ( 2, 1, 'aap' )

    # *******************************************************
    # *******************************************************
    self.Grid.SetLabelBackgroundColour ( wx.RED )
    columns = [ 'field' ]
    #self.Grid.SetColLabelValue ( 0, 'beer')
    #self.Grid.CreateGrid ( 0, len ( columns ), gridlib.Grid.SelectRows )
    #self.Grid.SetSelectionMode ( gridlib.Grid.SelectCells )
    ##self.Grid.CreateGrid ( 1, 1, gridlib.Grid.SelectCells )

    for i, name in enumerate ( columns ) :
      self.Grid.SetColLabelValue ( i, name )

    self.Grid.SetRowLabelSize ( 0 )
    self.Grid.SetColLabelAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )
    self.Grid.SetColLabelSize ( 20 )

    #self.Grid.SetDefaultRowSize ( 8, True )  ##DONT USE !!
    MH = 8
    #self.Grid.SetRowMinimalAcceptableHeight ( MH )
    #self.Grid.SetDefaultRowSize ( MH, True )
    self.Grid.EnableEditing ( False )
    ##self.Grid.SetCellHighlightPenWidth ( 0 )
    self.Grid.DisableDragRowSize ( )

    self.Grid.Random_Select = True
    self.Grid.Random_Select_Color = wx.Colour ( 200, 100, 100 )

    # Enable Column moving
    import  wx.lib.gridmovers   as  gridmovers
    gridmovers.GridColMover ( self.Grid )
    self.Grid.Bind ( gridmovers.EVT_GRID_COL_MOVE, self._On_Col_Move, self.Grid )

  # *******************************************************
  # *******************************************************
  def _On_Col_Move ( self, event ) :
    Col = event.GetMoveColumn ()    # Column being moved
    To  = event.GetBeforeColumn ()  # Before which column to insert
    print('Col moved', Col, 'to', To)

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
#class Test_Year_Grid ( wx.Frame ) :
#  def __init__ ( self, ini = None ) :
#    wx.Frame.__init__( self, None )
class Test_Year_Grid ( My_Frame_Class ) :
  def __init__ ( self, ini = None ) :
    print('ZXZXZX',ini)
    My_Frame_Class.__init__( self, ini )

    self.State_DagNr = False
    self.Button_Texts = ( 'DagNr', 'Uren' )

    GUI = """
    self.NB              ,wx.Notebook   ,style = wx.BK_LEFT
      NN_PanelHor  ,011
        self.P1  ,PanelVer  ,01
#        NN_PanelVer  ,01
          NN_PanelHor   ,10
            NN_wx.StaticText   ,label = '  woensdag 14 april 2010'
            self.B_DagNr        ,wx.Button  ,label = 'Date'   ,size=(40,18)
          self.Grid          ,Year_Grid        ,name = 'File'
        NN_PanelVer  ,00
          Spacer   ,30
          NN_PanelHor  ,00
            Spacer  ,30
            self.Grid_Day    ,Base_Grid
    """
    self.wxGUI = PG.Create_wxGUI ( GUI, self.Ini_File, my_parent = 'self' )
    print(self.wxGUI.code)

    #gridlib.Grid.AppendCols()
    #gridlib.Grid.InsertCols()

    self.Grid.CreateGrid ( 25, 6 ) #, gridlib.Grid.SelectCells )
    NRow = self.Grid.GetNumberRows ()
    NCol = self.Grid.GetNumberCols ()

    W      = 25
    Wmaand = 45
    self.Grid.SetMinSize ( ( 58 + 5 * W + Wmaand, 300 ) )

    # *******************************************************
    # *******************************************************
    #self.Grid.SetLabelBackgroundColour ( wx.RED )

    Columns = 'Maand,Ma,Di,Wo,Do,Vr'
    Columns = Columns.split ( ',' )
    for i, Dag in enumerate ( Columns ) :
      self.Grid.SetColLabelValue ( i, Dag )

    self.Grid.SetColSize ( 0, Wmaand )
    for Col in range ( 1, 6 ) :
      self.Grid.SetColSize ( Col, W )
      #if COl <> 4 :
      self.Grid.Set_Col_DayPlan ( Col )
      #Set_Col_!DayPlan ( self, Col, Color, Max = 8 ) :

    self.StartWeek = 12
    for i in range ( NRow ) :
      self.Grid.SetRowLabelValue ( i, str ( self.StartWeek + i ) )

    ThisWeek =  15
    ThisDay  =  2
    self.Grid.Set_ToDay ( ThisWeek - self.StartWeek, ThisDay )

    self.Grid.SetRowLabelSize ( 30 )
    self.Grid.SetColLabelSize ( 20 )
    #self.Grid.SetColLabelAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )
    #self.Grid.SetColLabelAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )

    self.Grid.EnableEditing ( False )
    self.Grid.DisableDragRowSize ( )

    self.Grid.Random_Select = True
    self.Grid.Random_Select_Color = wx.Colour ( 200, 100, 100 )

    Free = []
    Free.append ( [ 0,2,6,0,0 ] )
    Free.append ( [ 0,2,4,0,0 ] )
    Free.append ( [ 0,4,0,0,0 ] )
    Free.append ( [ 0,7,0.7,6,0 ] )
    for Row, RowData in enumerate ( Free ) :
      for Col, CellData in enumerate ( RowData ) :
        self.Grid.SetCellValue (
          Row + ThisWeek - self.StartWeek, Col+1, str ( CellData ) )

    import random
    for Row in range ( 7, NRow ) :
      for Col in range ( 1, 6 ) :
        self.Grid.SetCellValue ( Row, Col, str ( random.uniform ( -2, 8 )))

    for Row in range ( NRow ) :
      self.Grid.SetCellValue ( Row, 5, '  -' ) #'Out' )

    Week = 22
    for i in range ( 1, 6 ) :
      self.Grid.SetCellValue ( Week   - self.StartWeek, i, 'vak' )
      self.Grid.SetCellValue ( Week+1 - self.StartWeek, i, 'vak' )
      self.Grid.SetCellValue ( Week+2 - self.StartWeek, i, 'vak' )

    Day  = 1
    Week = 12
    self.Grid.Day_Events [ ( Week-self.StartWeek, Day ) ] = wx.BLUE, 'VM'
    Day  = 4
    Week = 14
    self.Grid.Day_Events [ ( Week-self.StartWeek, Day ) ] = wx.CYAN, 'B2'

    self.Grid._On_Left_Click_Completion = self._On_Day_Select


    # ********************************
    self.Grid_Day.CreateGrid ( 20, 4 )
    NRow = self.Grid_Day.GetNumberRows ()
    NCol = self.Grid_Day.GetNumberCols ()

    WK = 20
    W  = 200
    self.Grid_Day.SetRowLabelSize ( 50 )
    self.Grid_Day.SetColLabelAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )
    self.Grid_Day.SetColLabelSize ( 20 )
    self.Grid_Day.SetColSize ( 0, WK )
    self.Grid_Day.SetColSize ( 1, WK )
    self.Grid_Day.SetColSize ( 2, WK )
    self.Grid_Day.SetColSize ( 3, W )
    self.Grid_Day.SetMinSize ( ( 60 + 3* WK + W , (NRow+1) * 17 +8 ) )

    self.Grid_Day.SetColLabelValue ( 0, 'K1' )
    self.Grid_Day.SetColLabelValue ( 1, 'K2' )
    self.Grid_Day.SetColLabelValue ( 2, 'K3' )

    import time
    DT = Delphi_Date ()
    DT = round ( DT ) + old_div(8.0, 24)
    HalfHour = old_div(0.5, 24)
    for Row in range ( NRow ) :
      self.Grid_Day.SetRowLabelValue ( Row, DT.to_String_Time_Short )
      DT += HalfHour

    #self.Grid_Day._On_Left_Click_Completion = self._On_Time_Select
    #self.Grid_Day.Bind ( gridlib.EVT_GRID_CELL_LEFT_CLICK, self._On_Time_Select )
    self.Grid_Day.Bind ( gridlib.EVT_GRID_CELL_RIGHT_CLICK, self._On_Time_Select )

    self.B_DagNr.Bind ( wx.EVT_BUTTON, self._On_Button )

  # *******************************************************
  # *******************************************************
  def _On_Button ( self, event ) :
    if self.State_DagNr :
      Date = Kal ()
      Data = Date.Get_Days_of_Week_Range ( 4, 5 )
      for Row, RowData in enumerate ( Data ) :
        for Col, CellData in enumerate ( RowData ) :
          self.Grid.SetCellValue ( Row, Col, str( CellData ) )
    else :
      pass
    self.B_DagNr.SetLabel ( self.Button_Texts [ self.State_DagNr ] )
    self.State_DagNr = not ( self.State_DagNr )

  # *******************************************************
  # *******************************************************
  def _On_Time_Select ( self, event ) :
    # werkt niet print 'TTTT', self.Grid_Day.GetSelectedCells ()

    self.RM_Col = event.GetCol ()
    self.RM_Row = event.GetRow ()

    pre = []

    if self.RM_Col in range (3) :
      pre.append ( 'Screening'       )
      pre.append ( 'NaMeting-1'      )
      pre.append ( 'NaMeting-2'      )
      pre.append ( 'FollowUp-1'      )
      pre.append ( 'FollowUp-2'      )
    else :
      pre.append ( 'Intake'          )
      pre.append ( 'Behandeling 5'   )
      pre.append ( 'Laatste Gesprek' )
      pre.append ( 'Exit Gesprek'    )

    #self.Popup_Menu = My_Popup_Menu_Robbie ( self, None, func=None, pre=pre)
    self.Popup_Menu = My_Popup_Menu ( self._On_Popup_Select, None, pre=pre )
    #self.Popup_Menu.SetEnabled ( 1, False )

    self.PopupMenu ( self.Popup_Menu )

  # *******************************************************
  # *******************************************************
  def _On_Popup_Select ( self, event ) :
    index = event.GetInt ()
    Value = self.Popup_Menu.items [ index ].GetText ()
    if self.RM_Col in range (3) :
      self.Grid_Day.SetCellValue ( self.RM_Row, self.RM_Col, 'X' )
      self.Grid_Day.SetCellValue ( self.RM_Row+1, self.RM_Col, 'X' )
    else :
      self.Grid_Day.SetCellValue ( self.RM_Row, self.RM_Col, Value )

  # *******************************************************
  # *******************************************************
  def _On_Day_Select ( self, Row, Col ) :
    print('=======', Row, Col)
    self.Grid_Day.SetColLabelValue ( 3, 'woensdag 14 april 2010' )

# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class Test_MultiLine_Grid ( wx.Frame ) :
  def __init__ ( self, ini = None ) :
    wx.Frame.__init__( self, None )

    GUI = """
    self.Grid          ,Base_Simple_Grid    ,name = 'File'
    """
    Create_wxGUI ( GUI )

    #self.Grid.CreateGrid   ( 10, 5 )
    self.Grid.Align_Hor ()
    self.Grid.Clear ( 4, 10 )
    self.Grid.Set_Col_Labels ( ['aap', 'beer'])
    self.Grid.Set_Row_Labels ( ['Raap', 'Rbeer'])
    #self.Grid.Align_Hor ()

    self.Grid.SetCellValue ( 2, 1, 'aap\nbeer' )
    self.Grid.SetRowSize   ( 2, 80 )

    self.Grid.SetRowLabelSize ( 50 )
    #self.Grid.SetColLabelAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )
    self.Grid.SetColLabelSize ( 20 )
# ***********************************************************************


# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 5 )

  # ****************************************************************
  # ****************************************************************
  if Test ( 1 ) :
    app = wx.App ()
    data_collection = 2

    # ***********   *****************************************************
    # Fixed first Row,
    # Typed defined by Columns
    # ****************************************************************
    if data_collection == 1 :
      data_values = [
        [ 'Name',     'Enabled',  'X0',  'Gain',  'Color',  'LineType', 'FileName' ],
        [ 'Signal 1',  True,      30,    0.2,     wx.RED,   'Solid',    'D:/test.dat'],
        [ 'Signal 2',  False,     50,    0.25344, wx.BLUE,  'Dash-Dot', ''],
        [ 'Signal 3',  True,      70,    2,       wx.GREEN, 'Solid',    ''] ]
      data_types = [
        gridlib.GRID_VALUE_STRING,
        gridlib.GRID_VALUE_BOOL,
        gridlib.GRID_VALUE_NUMBER,
        gridlib.GRID_VALUE_FLOAT + ':6,2',
        MY_GRID_TYPE_COLOR,
        gridlib.GRID_VALUE_CHOICE + ':Solid,Das-Dot,Dash,Dot',
        MY_GRID_TYPE_FILE ]
      data_defs = ( MY_GRID_FIXED_ROW, MY_GRID_COL_TYPED )

    # ****************************************************************
    # Fixed first Row & first Column,
    # Typed defined by ROW
    # ****************************************************************
    elif data_collection == 2 :
      data_values = [
        [ 'xxx',      'Value'   ],
        [ 'Size',      30       ],
        [ 'Float',     23.45674 ],
        [ 'Color',     wx.RED   ],
        [ 'File',      ''       ],
        [ 'Bool',      True     ],
        [ 'Choice',    'all'    ] ]
      data_types = [
        gridlib.GRID_VALUE_NUMBER,
        gridlib.GRID_VALUE_FLOAT + ':6,2',
        MY_GRID_TYPE_COLOR,
        MY_GRID_TYPE_FILE,
        gridlib.GRID_VALUE_BOOL,
        gridlib.GRID_VALUE_CHOICE + ':JAL,Delphi,Python,other']
      data_defs = ( MY_GRID_ROW_TYPED, MY_GRID_FIXED_ROW_COL )

    # ****************************************************************
    # ****************************************************************
    elif data_collection == 3 :
      data_values = [
        [ 'xxx',      'Value'   ],
        [ 'Size',     'string'  ],
        [ 'Color',     wx.RED   ],
        [ 'Color',     wx.GREEN   ],
        [ 'Color',     wx.RED   ],
        [ 'Color',     wx.RED   ],
        [ 'Color',     wx.RED   ],
        [ 'Choice',    ('string',)    ] ]
      data_types = [
        gridlib.GRID_VALUE_STRING,
        MY_GRID_TYPE_COLOR,
        MY_GRID_TYPE_COLOR,
        MY_GRID_TYPE_COLOR,
        MY_GRID_TYPE_COLOR,
        MY_GRID_TYPE_COLOR,
        gridlib.GRID_VALUE_STRING]
      data_defs = ( MY_GRID_ROW_TYPED, MY_GRID_FIXED_ROW_COL )

    # ****************************************************************
    # ****************************************************************
    elif data_collection == 4 :
      data_values = [
        [ 'xxx',      'Value', 'other'   ],
        [ 'Size',     'string'  , 'other'],
        [ 'Color',     wx.RED, wx.GREEN   ],
        [ 'Color',     wx.GREEN,wx.BLUE   ],
        [ 'Color',     wx.RED ,wx.RED  ],
        [ 'Color',     wx.RED ,wx.RED  ],
        [ 'Color',     wx.RED, wx.RED   ],
        [ 'Choice',    ('string',), 'aap'    ] ]
      data_types = [
        gridlib.GRID_VALUE_STRING,
        MY_GRID_TYPE_COLOR,
        MY_GRID_TYPE_COLOR,
        MY_GRID_TYPE_COLOR,
        MY_GRID_TYPE_COLOR,
        MY_GRID_TYPE_COLOR,
        gridlib.GRID_VALUE_STRING]
      data_defs = ( MY_GRID_ROW_TYPED, MY_GRID_FIXED_ROW_COL )

    ini = inifile ( os.path.join ( os.getcwd (), 'grid_support_test.cfg' ) )
    frame = tProperties_Form ( None, None,
                               data_values, data_types, data_defs,
                               "Properties LEDa", Pos = ( 20, 20 ) )
    frame.Show ()
    app.MainLoop ()

  # ****************************************************************
  # ****************************************************************
  if Test ( 3 ) :
    My_Main_Application ( Test_Form )

  # ****************************************************************
  # ****************************************************************
  if Test ( 4 ) :
    My_Main_Application ( Test_Year_Grid )

  # ****************************************************************
  # ****************************************************************
  if Test ( 5 ) :
    My_Main_Application ( Test_MultiLine_Grid )

  # ****************************************************************
  # Test of Dialog_RecordForm : edit Field_Objects
  # ****************************************************************
  if Test ( 6 ) :
    Field_Objects = []

    New = Field_Object ( 'Urgentie' )
    New.Type = CT_Choice
    """
    New.ID_2_Choice [ 6 ] = 'aap'
    New.ID_2_Choice [ 9 ] = 'beer'
    New.ID_2_Choice [ 3 ] = 'donky'
    New.ID_2_Choice [ 2 ] = 'coala'
    New.Value = 9
    """
    New.Choices = 'aap,beer,cola,dony,eend,fazant'.split(',')
    New.Value   = 2
    Field_Objects.append ( New )

    New = Field_Object ( 'Indicatie' )
    New.Value = 'aap'
    Field_Objects.append ( New )

    Changes = Dialog_RecordForm ( None, 'Title', Field_Objects )
    print(Changes)
    for Change in Changes :
      X = Field_Objects [ Change ]
      print('%s  =  %s' % ( X.Name, X.Value ))

# ***********************************************************************
pd_Module ( __file__ )

