"""
from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import range
from builtins import object
"""
import __init__
# THIS MODULE MAY NOT USE _(,
# because the use of Create_wxGUI
# needs to search for the parent frame of gui_support

__doc__ = """
doc_string translated ?
"""
import sys
sys.gui_support_version = 'WX'
from language_support import  Language_Current, Set_Language, Flag_Object
from language_support import _
import traceback

_Version_Text = [

[ 2.13 ,  '24-04-2015', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- SetSplitter CallLater, added a resize at 1000 msec
"""],

[ 2.12 , '24-01-2011', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- My_Frame_Class, automatically tries to call Save_Settings
- My_Frame_Class, extended with subclaFwxss
"""],

[ 2.11 , '27-10-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Save_Settings, executed line by line and error reporting added
"""],

[ 2.10 , '02-10-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- My_Frame_Class extended with **kwargs
- My_Main_Application extended with **kwargs that will be passed to the form
"""],

[ 2.9 , '23-09-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- When error in Create_wxGUI, generated code is only printed untill the error line
"""],

[ 2.8 , '28-08-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- GUI restore settings wrapped in try / except
  this prevents errors in dynamical generated views
"""],

[ 2.7 , '20-06-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- tried to add alignment for panels Panels_Align, didn't succeed
  see comment in grid_support.Field_Objects_Form
"""],

[ 2.6 , '17-04-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- ScrollVer, ScrollHor panels added
"""],

[ 2.5 , '22-03-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- wx.Choice auto save restore added
- Nameless classes NN_ added ( e.g. NN_PanelHor, NN_StaticText, ... )
- My_Frame_Class, added method Set_Extra_Title
"""],

[ 2.4 , '17-01-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- CallLater, time increasesd from 100 tot 300 msec
"""],

[ 2.3 , '01-12-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Spacer class added ( can be used without a name !!)
"""],

[ 2.2 , '26-11-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- GUI_ListBox   added as class,   including save/restore
- GUI_ListBox2 started, because normal Listbox can't highlight items
- Restore_Settings and Load_Settings added
"""],

[ 2.1 , '24-10-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Create_wxGUI, extended with StackUp paramater, so you can use intermediate
  classes of the form and still execute in the higher frame
"""],


[ 2.0 , '22-10-2009', 'Robbert Mientki',
'Test Conditions:', (2,),
"""
- if a component has a GetValue and SetValue it's automatically included
  in the Save / Restore facility
- wxGUI_String class added, which is especially handy
  when you need to build a GUI string dynamically.
- components are allowed to declared as an iterable type, like :
    Button[3]       ,wx.Button
    self.Button[3]  ,wx.Button
- __repr__ added to wxGUI
"""],

[ 1.16 , '20-10-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- MultiSplitterHor, MultiSplitterVer added as classes, including save/restore
- GUI_CheckListBox                   added as class,   including save/restore
"""],

[ 1.15 , '11-09-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- _Save_Restore, now uses %% also in GetValue
- _Save_Restore for Combobox was not correct
"""],

[ 1.14 , '14-06-2009', 'Stef Mientki',
'Test Conditions:', (3,),
"""
- Default inifile, now also works from My_Path
"""],

[ 1.13 , '28-05-2009', 'Stef Mientki',
'Test Conditions:', (3,),
"""
- Base_STC, added to auto save / reload
"""],

[ 1.12 , '10-04-2009', 'Stef Mientki',
'Test Conditions:', (3,),
"""
- Last BoxSizer ( on the top component ) is only added,
  if this top component is of type wx.Window or wx.Sizer
- better localization of Icon
"""],

[ 1.11 , '20-01-2009', 'Stef Mientki',
'Test Conditions:', (3,),
"""
 - added: MultiSplitterHor = MultiSplitterWindow
 - added: MultiSplitterVer
"""],

[ 1.10 , '18-11-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
 - bug if Ini_File_String was None in Create_wxGUI
"""],

[ 1.9 , '11-11-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
 - My_Main_Application, didn't iniated the form correctly (ini)
"""],

[ 1.8 , '08-11-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
 - My_Main_Application, you can add a Splash screen added
"""],

[ 1.7 , '01-11-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
 - My_HtmlWindow added (CSS translated html pages + wxp-widgets)
"""],

[ 1.6 , '25-10-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
 - Filename and linenumber added to error message
"""],

[ 1.5 , '24-10-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
 - Errors in GUI-string were suppressed (and not shown),
   now they are made visible,
   while the program still tries to continue
 - PreView_wxGUI added
"""],

[ 1.4 , '22-10-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
 - Implicit Import of types in list _Special_Types
"""],

[ 1.3 , '21-10-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
 - Create_wxGUI changed to a class, to simplify interactions
 - Create_wxGUI now restores config settings automatically
"""],

[ 1.2 , '13-10-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
 - In Notebook creation, removed the imageId, gave problems under Ubuntu
 - changed name of GUI_NoteBook to GUI_Notebook
 - my_MiniFrame removed (it's better to maintain just one: My_Frame_Class)
"""],

[ 1.1 , '27-08-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
 - GUI_NoteBook added
"""],

[ 1.0 , '14-07-2007', 'Stef Mientki',
'Test Conditions:', (),
' - orginal release']
]


# ***********************************************************************
_ToDo = """
 - if component placed on a Notebook is not a wx.Window,
   automatically insert a wx.Panel in between
 - better error message: remove the first 2 lines (non-info),
   and add filename of the calling file
 - PreView-wxGUI in AUI-panes
"""
# ***********************************************************************


# !!! import wx before any support library !!!
# otherwise the IDE won't do auto-suggest
import wx
import wx.html as  html

import  wx.lib.buttons  as  buttons
BmpBut = buttons.GenBitmapButton


from inifile_support import *
from wx.lib.splitter import MultiSplitterWindow

#import wx.lib.pdfviewer as iepdf
#from  wx.lib.pdfviewer import pdfViewer

##from Scintilla_support import Base_STC


########### Extra
#from tree_support import Custom_TreeCtrl_Base
#import wx.lib.iewin as iewin
#from grid_support import Base_Grid
########### Extra



# ***********************************************************************
# ***********************************************************************
class Spacer ( wx.StaticText ) :
  """
  Defines a Horizontal or Vertical Spacer.
  It can be used without a name in wxGUI builder.
  """
  def __init__ ( self, parent, space = 10 ) :
    wx.StaticText.__init__ ( self, parent, size = ( space, space ) )
# ***********************************************************************
class HorSpacer ( wx.StaticText ) :
  """
  Defines a Horizontal Spacer.
  It can be used without a name in wxGUI builder.
  """
  def __init__ ( self, parent, space = 10 ) :
    wx.StaticText.__init__ ( self, parent, size = ( space, 1 ) )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class StaticText ( wx.StaticText ) :
  """ Special for NN_ type """
  def __init__ ( self, *args, **kwargs ) :
    wx.StaticText.__init__ ( self, *args, **kwargs )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Panel ( wx.Panel ) :
  """ Special for NN_ type """
  def __init__ ( self, *args, **kwargs ) :
    wx.Panel.__init__ ( self, *args, **kwargs )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class _MultiSplitter ( MultiSplitterWindow ) :
  def __init__ ( self, *args, **kwargs ) :
    MultiSplitterWindow.__init__ ( self, *args, **kwargs )

  def GetValue ( self ) :
    Result = []
    for i in range ( len ( self._windows ) ) :
      Result.append ( self.GetSashPosition ( i ) )
    return Result

  def SetValue ( self, Value ) :
    N = min ( len ( Value ), len ( self._windows ) )
    for i in range ( N ) :
      print ( '_MultiSplitter', i, Value[i] )
      self.SetSashPosition ( i, Value [i] )

class MultiSplitterHor ( _MultiSplitter ) :
  def __init__ ( self, *args, **kwargs ) :
    _MultiSplitter.__init__ ( self, *args, **kwargs )

class MultiSplitterVer ( _MultiSplitter ) :
  def __init__ ( self, *args, **kwargs ) :
    _MultiSplitter.__init__ ( self, *args, **kwargs )
    self.SetOrientation ( wx.VERTICAL )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
#"""
class GUI_ListBox2 ( wx.ListCtrl ) :
  """
  ToDo
  meant to create a "working" simple listbox,
  which can highlight items
  """
  def __init__ ( self, *args, **kwargs ) :
    wx.ListCtrl.__init__ ( self, *args, **kwargs )

  def Set ( self, Choices ) :
    self.InsertColumn ( 0, 'aap' )
    #self.Append ( Choices )
    for i, Choice in enumerate ( Choices ) :
      self.Append ( ( Choice, ) )

  def SetItemForegroundColour ( self, indx, Color ) :
    #dc.SetFont  ( wx.SystemSettings_GetFont ( wx.SYS_DEFAULT_GUI_FONT ) )
    item = self.GetItem ( indx )
    #font = self.GetItemFont ( item )
    #_boldFont = wx.Font(font.GetPointSize(), font.GetFamily(),
    #                         self._normalFont.GetStyle(), wx.BOLD, self._normalFont.GetUnderlined(),
    #                         self._normalFont.GetFaceName(), self._normalFont.GetEncoding())
    #
    font = wx.Font ( 10, wx.SWISS, wx.NORMAL, wx.BOLD )
    self.SetItemFont ( item, font)
    item.SetTextColour ( Color )

  def GetValue ( self ) :
    return self.GetSelection ()

  def SetValue ( self, Value ) :
    if ( Value < 0 ) or ( Value >= self.GetItemCount () ):
      return
    self.SetSelection ( Value )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class GUI_ListBox ( wx.ListBox ) :
  def __init__ ( self, *args, **kwargs ) :
    wx.ListBox.__init__ ( self, *args, **kwargs )

  def GetValue ( self ) :
    return self.GetSelection ()

  def SetValue ( self, Value ) :
    if ( Value < 0 ) or ( Value >= self.GetCount () ):
      return
    self.SetSelection ( Value )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class GUI_CheckListBox ( wx.CheckListBox ) :
  def __init__ ( self, *args, **kwargs ) :
    wx.CheckListBox.__init__ ( self, *args, **kwargs )

  def GetValue ( self ) :
    Result = []
    for Index in range ( self.GetCount () ) :
      if self.IsChecked ( Index ) :
        Result.append ( Index )
    return Result

  def SetValue ( self, Values ) :
    for Index in Values :
      self.Check ( Index )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class GUI_ComboBox ( wx.ComboBox ) :
  """
  Additional features:
    - Get_Selected_Index
  """
  def __init__ ( self, *args, **kwargs ) :
    wx.ComboBox.__init__ ( self, *args, **kwargs )

  def Get_Selected_Index ( self ) :
    Indx = self.GetSelection ()
    if Indx >= 0 :
      return Indx

    Value = self.GetValue ().lower()
    Choices = self.GetStrings ()
    for Indx, Choice in enumerate ( Choices ) :
      if Choice.lower() == Value :
        return Indx
    return -1
# ***********************************************************************


# ***********************************************************************
# Platform independant browser
#   - Windows the embedded IE browser (activeX) is used
#   - Linux webkit should work well,
#       but we couldn't get it to work,
#       so we used the external browser instead.
#   - Mac, webkit should work well,
#       but we can't test it
#       so we used the external browser instead.
# ***********************************************************************
#if Platform_Windows :
try:
    import wx.lib.iewin as iewin
    class Platform_Web_Browser ( iewin.IEHtmlWindow ) :
      pass
except:
  try:
      #import wx.lib.iewin as iewin
      import wx.lib.iewin_old as iewin
      class Platform_Web_Browser ( iewin.IEHtmlWindow ) :
        pass
  except:

    #else :
      """
      from wx.webview import WebView
      class Platform_Web_Browser ( WebView ) :
        def __init__ ( self, *args, **kwargs ) :
          WebView.__init__ ( self, *args, **kwargs )
          self.LoadUrl = self.LoadURL
      """
      class Platform_Web_Browser ( wx.StaticText ) :
        def __init__ ( self, *args, **kwargs ) :
          wx.StaticText.__init__ ( self, *args, **kwargs )
          self.SetLabel ( '\n\nSorry there\'s no WebKit support for this Operating System')
          font = wx.Font ( 18, wx.SWISS, wx.NORMAL, wx.NORMAL )
          self.SetFont ( font )
        def LoadUrl ( self, *args, **kwargs ) :
          import webbrowser
          print('wb',args)
          webbrowser.open ( args[0] )
        def Stop ( self ) :
          pass
# ***********************************************************************

# ***********************************************************************
# Platform independant PDF Viewer
# ***********************************************************************
if Platform_Windows :
  try:
    from   wx.lib.pdfwin   import PDFWindow
    class Platform_PDF_Viewer ( PDFWindow ) :
      pass
  except:

      class Platform_PDF_Viewer ( wx.StaticText ) :
        def __init__ ( self, *args, **kwargs ) :
          wx.StaticText.__init__ ( self, *args, **kwargs )
          self.SetLabel ( '\n\nSorry there\'s no PDF support for this Operating System (Error While Loading)')
          font = wx.Font ( 18, wx.SWISS, wx.NORMAL, wx.NORMAL )
          self.SetFont ( font )
        def LoadFile ( self, *args, **kwargs ) :
          pass
else :
  class Platform_PDF_Viewer ( wx.StaticText ) :
    def __init__ ( self, *args, **kwargs ) :
      wx.StaticText.__init__ ( self, *args, **kwargs )
      self.SetLabel ( '\n\nSorry there\'s no PDF support for this Operating System')
      font = wx.Font ( 18, wx.SWISS, wx.NORMAL, wx.NORMAL )
      self.SetFont ( font )
    def LoadFile ( self, *args, **kwargs ) :
      pass
# ***********************************************************************


# ***********************************************************************
# Platform independant PDF Viewer
# ***********************************************************************
if Platform_Windows :
  class Platform_Html_Editor ( wx.Panel ) :
    def __init__ ( self, *args, **kwargs ) :
      wx.Panel.__init__ ( self, *args, **kwargs )
      #              self.Dock_Punthoofd   ,wx.Panel        ,name = 'Python'
      #              self.Dock_Punthoofd   ,Platform_Web_Editor   ,name = 'Python'
      #print 'ARGHH',args,kwargs
      self.Dock           = args[0]
      self.Ini_Section    = 'Py2Delphi'
      self.PyRichView     = None
      Path = os.path.split ( __file__ )[0]
      self.RichView_Path  = Nice_Path ( Path, '..', 'Delphi_RichView' )
      self.Transport_File = Nice_Path ( self.RichView_Path, 'PyRichView_py.cfg' )
      #self.RichView_Path  = r'D:\Data_Python_25\TO_Aggregatie'
      #self.Transport_File = os.path.join ( self.RichView_Path, 'PyRichView_py.cfg' )

    # ***************************************************
    # ***************************************************
    def Load_File ( self, Filename ) :
      Filename = str ( Nice_Path ( Filename ) )
      if not ( self.PyRichView ) :
        from   test_dock_delphi   import   Launch_And_Attach_Application
        #Application = [ os.path.join ( self.RichView_Path,'PyRichView.exe' ) ]
        Application = Nice_Path ( self.RichView_Path, 'PyRichView.exe' )
        Application_Form_Class = 'Tform_RVE_Python'
        Params = [ Filename ]
        App = Launch_And_Attach_Application ( self, self, Application,
                                        None, Application_Form_Class, Params,
                                        self._Msg_CallBack )
        self.PyRichView = App
        #self.Dock.Layout()
        self.Dock.SendSizeEvent ()

      else :
        from   test_dock_delphi   import  WM_Py_Open
        Ini = inifile ( self.Transport_File, Force_Strings = True )
        Ini.Section = self.Ini_Section
        Ini.Write ( 'Open', Filename )
        Ini.Close ()
        self.PyRichView.Send_Message ( WM_Py_Open )

    # ***************************************************
    # ***************************************************
    def Set_BasePath ( self, Path ) :
      if self.PyRichView :
        Path = str ( Nice_Path ( Path ) )
        from   test_dock_delphi   import  WM_Py_SetBasePath
        Ini = inifile ( self.Transport_File, Force_Strings = True )
        Ini.Section = self.Ini_Section
        Ini.Write ( 'BasePath', Path )
        Ini.Close ()
        self.PyRichView.Send_Message ( WM_Py_SetBasePath )

    # ***************************************************
    # ***************************************************
    def _Msg_CallBack ( self, hWnd, msg, wParam, lParam ) :
      pass #print 'MMMMMSSG', hWnd, msg, wParam, lParam

    # ***************************************************
    # ***************************************************
    def Close ( self ) :
      if self.PyRichView :
        self.PyRichView.Close ()
        self.PyRichView = None
else :
  class Platform_Html_Editor ( wx.StaticText ) :
    def __init__ ( self, *args, **kwargs ) :
      wx.StaticText.__init__ ( self, *args, **kwargs )
      self.SetLabel ( '\n\nSorry there\'s no Html-Editor for this Operating System')
      font = wx.Font ( 18, wx.SWISS, wx.NORMAL, wx.NORMAL )
      self.SetFont ( font )
    def Load_File ( self, Filename ) :
      pass
    def Close ( self ) :
      pass
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class Main_Application ( wx.App ) :
  pass
# ***********************************************************************


class MyApp ( wx.App ) :
  def FilterEvent ( self, evt ) :
    if not ( type ( evt ) in [ wx.UpdateUIEvent,
                               wx.IdleEvent,
                               wx.PaintEvent,
                               wx.EraseEvent,
                               wx.NcPaintEvent,
                               #wx.SizeEvent,
                               wx.MoveEvent,
                               wx.SetCursorEvent,
                               wx.MouseEvent,
                               wx.ActivateEvent,
                               wx.FocusEvent,
                               #wx.ChildFocusEvent,
                               wx.ShowEvent,
                               wx.PyEvent,
                               wx.MouseCaptureChangedEvent,
                               wx.ShowEvent,
                               wx.WindowDestroyEvent,
                               wx.WindowCreateEvent,
                                ] ) :
      #if isinstance ( evt, wx.UpdateUIEvent ) :
      print(evt)
    return -1


# ***********************************************************************
# demo program
# ***********************************************************************
def My_Main_Application ( My_Form,
                          config_file = None,
                          Splash      = None,
                          **kwargs ) :
  # we need an extra import here
  import wx

  app = wx.App ( redirect = False )
  """
  app = MyApp(redirect=False)
  app.SetCallFilterEvent(True)
  """

  if Splash :
    bmp = Get_Image_Resize ( Splash, 96 )
    SS = wx.SplashScreen ( bmp,
                      wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                      1000, None,
                      style = wx.NO_BORDER | wx.SIMPLE_BORDER | wx.STAY_ON_TOP )
    wx.Yield ()
    SS.SetPosition ( (100, -1 ) )

  if config_file :
    ini = inifile ( config_file )
  else :
    #v3print ( 'gfdsawer', sys._getframe().f_code.co_filename, sys._getframe(1).f_code.co_filename )
    #ini = inifile ( Change_FileExt ( sys.argv[0], '_Test.cfg' ) )
    ini = inifile ( Change_FileExt ( sys._getframe(1).f_code.co_filename, '_Test.cfg' ) )

  frame = My_Form ( ini = ini, **kwargs )
  frame.Show ( True )

  if Application.WX_Inspect_Mode :
    import wx.lib.inspection
    wx.lib.inspection.InspectionTool().Show()

  app.MainLoop ()
  ini.Close ()
# **********************************************************************


# ***********************************************************************
# ***********************************************************************
class weg_My_HtmlWindow ( html.HtmlWindow ) :

  def Load_CSS ( self, URL, CallBack_Html = None ) :
    import wxp_widgets
    #,style=wx.NO_FULL_REPAINT_ON_RESIZE
    name_to = 'CSS_translated.html'
    wxp_widgets.Translate_CSS ( URL, name_to, CallBack_Html )
    self.LoadPage ( name_to )

    from wxp_widgets import CallBack_Html_Pointer
    if CallBack_Html and not ( CallBack_Html_Pointer ) :
      CallBack_Html_Pointer = CallBack_Html
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
# DONT use a FlatNotebook because it misses some essential parts
#self.NB         ,GUI_Notebook   ,style = NB_Style
# Besides that, it's under a different location under Ubuntu
"""
GUI_EVT_CLOSE_PAGE = fnb.EVT_FLATNOTEBOOK_PAGE_CLOSING
import wx.lib.flatnotebook as fnb
class WEG_GUI_Notebook ( fnb.FlatNotebook ) :
  def __init__ ( self, parent = None, style = None  ) :
    if style == None :
      style = ( fnb.FNB_NO_X_BUTTON |
                fnb.FNB_X_ON_TAB |
                fnb.FNB_MOUSE_MIDDLE_CLOSES_TABS |
                fnb.FNB_DCLICK_CLOSES_TABS |
                fnb.FNB_DROPDOWN_TABS_LIST |
                fnb.FNB_ALLOW_FOREIGN_DND |
               0 )
    #            fnb.FNB_NO_NAV_BUTTONS |
    #            fnb.FNB_HIDE_ON_SINGLE_TAB |
    fnb.FlatNotebook.__init__ ( self, parent = parent, style = style )
"""
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class My_Frame_Class ( wx.Frame ) :

  # *****************************************************************
  # *****************************************************************
  def __init__( self, main_form = None, Title = '',
                ini = None, Ini_Section = 'MiniFrame', style = None, substyle = None, **kwargs ) :

    self.main_form = main_form
    self.My_Title = Title

    try :     # Python 2.7
      FormStyle = wx.DEFAULT_FRAME_STYLE | wx.TINY_CAPTION
    except :  # Python 3.4
      FormStyle = wx.DEFAULT_FRAME_STYLE | wx.TINY_CAPTION_HORIZ

    if style :
      FormStyle |= style
    #ifparent:
    #   FormStyle = FormStyle | wx.FRAME_FLOAT_ON_PARENT    # needs a parent
    if substyle :
      FormStyle ^= substyle

    Pos  = ( 100, 100 )
    Size = ( 600, 400 )
    self.Ini_File    = ini
    self.Ini_Section = Ini_Section
    self.Ini_File_String = None
    Maximized = False
    #from language_support import Language_Current
    if ini :
      ini.Section = self.Ini_Section
      self.Ini_File_String = 'self.Ini_File'
      DX, DY = wx.GetDisplaySize()

      Maximized  = ini.Read ( 'Maximized',  False )
      if Maximized :
        pass
      else :
        Pos  = list ( ini.Read ( 'Pos',  Pos  ) )
        if ( Pos[0] < 0 ) or ( Pos[0] > ( DX - 200 ) ) :
          Pos[0] = 0
        if ( Pos[1] < 0 ) or ( Pos[1] > ( DY - 200 ) ) :
          Pos[1] = 0

        Size = list ( ini.Read ( 'Size', Size ) )
        if ( Size[0] < 200 ) or ( Size[0] > DX ) :
          Size[0] = 200
        if ( Size[1] < 200 ) or ( Size[1] > DY ) :
          Size[1] = 200

      Language = ini.Read ( 'Language', Language_Current[0] )
      if Language != Language_Current[0] :
        Set_Language ( Language, True )

    wx.Frame.__init__ (
        self, None, -1, Title,
        size  = Size,
        pos   = Pos,
        style = FormStyle )

    if Maximized :
      self.Maximize ()

    try :
      #import site
      #import inspect
      #print inspect.currentframe().f_code.co_filename
      #print site.abs__file__()
      #print ' FNFN', __file__, '$$$', self.__file__, '$$'
      #Icon_File = Joined_Paths ( os.path.split ( __file__ )[0],
      #                           #'../pictures/vippi_bricks_323.ico' )
      #                           'pictures/vippi_bricks_323.ico' )
      Icon_File = Module_Absolute_Path ( '..', 'pictures', 'vippi_bricks_323.ico' )
      #Icon_File = os.path.join ( __init__.Top_Path, 'pictures','vippi_bricks_323.ico' )
      self.SetIcon ( wx.Icon ( Icon_File, wx.BITMAP_TYPE_ICO ) )
    except :
      traceback.print_exc ()
      pass

    self.Bind ( wx.EVT_CLOSE,  self.__On_Close  )

  # *********************************************************
  # *********************************************************
  def Set_Extra_Title ( self, Extra_Title ) :
    self.SetTitle ( self.My_Title + '  ' + Extra_Title )

  # *********************************************************
  # *********************************************************
  def __On_Close ( self, event ) :
    #print 'XXXX close my frame class'
    """
    try :
      print 'ap',self.Ini_File.Filename,self.Ini_File,self.Ini_File.Filename
      sys.exit()
    except :
      print 'problemssss'
    """

    event.Skip ()
    ini = self.Ini_File
    if ini :
      ini.Section = self.Ini_Section
      ini.Write ( 'Maximized', self.IsMaximized ())
      if not ( self.IsMaximized  ()  ) :
        ini.Write ( 'Pos',      self.GetPosition () )
        ini.Write ( 'Size',     self.GetSize ()     )
      ini.Write ( 'Language', Language_Current[0] )

      # automatic saving of GUI-settings
      try :
        self.wxGUI.Save_Settings ()
      except :
        traceback.print_exc ()
        pass  #print 'failed'

      ini.Flush()

    # if restart needed (i.e. in case of a language change)
    if Application.Restart :
      from system_support import Run_Python
      Run_Python ( Application.Application )


# ***********************************************************************


# ***********************************************************************
# Here are the definitions for saving and restoring settings
# For each item 2 strings need to be defined:
#   - the string to get the value from the component
#   - the string to set the value of the component
# There are substitutes possible:
#   %% will be replaced by the name of the component (as it used in the forms init)
#   %  will be replaced by the value read from the config-file
# ***********************************************************************
_Save_Restore = {
  'Base_RTC'          : ( '%%.GetFilename()',     '%%.LoadFile(%)'       ),
  'Base_RTC2'         : ( '%%.GetFilename()',     '%%.LoadFile(%)'       ),
  'Base_STC'          : ( '%%.GetFilename()',     '%%.LoadFile(%)'       ),
  'Base_STC_Plus'     : ( '%%.GetFilename()',     '%%.LoadFile(%)'       ),
#  'GUI_CheckListBox'  : ( '%%.GetValue()',        '%%.SetValue(%)'       ),
  'MultiSplitterHor'  : ( '%%.GetValue()',        'wx.CallLater ( 300, %%.SetValue, % )'  ),
  'MultiSplitterVer'  : ( '%%.GetValue()',        'wx.CallLater ( 300, %%.SetValue, % )'  ),
#  'wx.CheckBox'       : ( '%%.GetValue()',        '%%.SetValue(%)'       ),
#  'wx.ComboBox'       : ( '%%.GetValue()',        '%%.SetValue(%)'       ),
  'wx.Choice'         : ( '%%.GetStringSelection()', '%%.SetStringSelection(%)' ),
  'wx.Notebook'       : ( '%%.GetSelection()',    '%%.SetSelection(%)'   ),
  'wx.RadioBox'       : ( '%%.GetSelection()',    '%%.SetSelection(%)'   ),
#  'wx.SplitterWindow' : ( '%%.GetSashPosition()', 'wx.CallLater ( 2500, %%.SetSashPosition, % )' ),
#  'wx.SplitterWindow' : ( '%%.GetSashPosition()', 'wx.CallLater ( 2500, %%.SetSashPosition, 300 )' ),
  'wx.SplitterWindow' : ( '%%.GetSashPosition()', '%%.SetSashPosition(%)' ),
  'wx.TextCtrl'       : ( '%%.GetValue()',        '%%.SetValue(str(%))'  ),
#  'wx.ToggleButton'   : ( '%%.GetValue()',        '%%.SetValue(%)'       ),
}
# ***********************************************************************
#  'wx.ComboBox'       : ( 'GetStrings()',      'for V in %: %%.Append(V)' ),


# ***********************************************************************
# Special types for which an automatic import will be done
# ***********************************************************************
_Special_Types = {
'Base_RTC'             : [ 'from richedit_support import Base_RTC'          ,0 ],
'Base_RTC2'            : [ 'from richedit_support import Base_RTC2'         ,0 ],
'Base_RTC2_b'          : [ 'from richedit_support import Base_RTC2_b'       ,0 ],
'Base_STC'             : [ 'from Scintilla_support import Base_STC'         ,0 ],
'Base_STC_Plus'        : [ 'from Scintilla_support import Base_STC_Plus'    ,0 ],
'Base_Grid'            : [ 'from grid_support import Base_Grid'             ,0 ],
'Base_Table_Grid'      : [ 'from grid_support import Base_Table_Grid'       ,0 ],
'buttons.GenToggleButton' : ['import wx.lib.buttons as buttons'             ,0 ],
'Class_URL_Viewer'     : [ 'from help_support import Class_URL_Viewer'      ,0 ],
'Custom_TreeCtrl_Base' : [ 'from tree_support import Custom_TreeCtrl_Base'  ,0 ],
'DataBase_TreeCtrl'    : [ 'from tree_support import DataBase_TreeCtrl'     ,0 ],
'Float_Slider'         : [ 'from float_slider import Float_Slider'          ,0 ],
#'iewin.IEHtmlWindow'   : [ 'import wx.lib.iewin as iewin'                   ,0 ],
#'iewin.IEHtmlWindow'   : [ 'import wx.lib.iewin_old as iewin'                   ,0 ],
'iewin.IEHtmlWindow'   : [ 'import wx.lib.iewin as iewin'                   ,0 ],
'iepdf.pdfViewer'      : [ 'import wx.lib.pdfviewer as iepdf'                   ,0 ],
#'MultiSplitterWindow'  : [ 'from wx.lib.splitter import MultiSplitterWindow',0 ],
#'My_HtmlWindow'        : [ 'from gui_support  import My_HtmlWindow'         ,0 ],
'_My_IEHtmlWindow'     : [ 'from help_support import _My_IEHtmlWindow'      ,0 ],
'NavCanvas.NavCanvas'  : [ 'from wx.lib.floatcanvas import NavCanvas, FloatCanvas', 0 ],
'PDFWindow'            : [ 'from   wx.lib.pdfwin import PDFWindow'           ,0],
'_PlotCanvas'          : [ 'from scope_plot import _PlotCanvas'              ,0 ],
'_PlotCanvas_History'  : [ 'from scope_plot_hist import _PlotCanvas_History' ,0 ],
'ScrolledPanel'        : [ 'from wx.lib.scrolledpanel import ScrolledPanel' ,0 ],
'tBase_Scope_with_History' : ['from control_scope_base import tBase_Scope_with_History' ,0],
'wx.html.HtmlWindow'   : [ 'import wx.html'                                 ,0 ],

}
#    import  my_iewin   as iewin
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class wxGUI_String ( object ) :
  """
  Convenience class to create GUI-strings dynamically.
  """
  def __init__ ( self, line = '' ) :
    # we use 2 spaces as an indent
    self._IL = '  '
    self._GUI = ''
    # Due to a bug in Create_wxGUI, an indent of 0 is not accepted
    self._Indent = 1
    if line :
      self.Append ( line )

  def Append ( self, line, X = None ) :
    """
    This is
      GUI.Indent ()
      GUI += "self.Text ,wx.TextCtrl"
    equivalent to
      GUI.append ( 1, "self.Text ,wx.TextCtrl" )

    In case of appending a multi-line string,
    the base indent of this multi-line string is subtracted
      GUI += '''
      self.NB   ,wx.Notebook
        p4        ,wx.Panel ,name = 'First'
        p5        ,wx.Panel ,name = 'Second'
      '''
    """
    if X :
      self.Dedent ( -line )
      line = X

    #printt(line.count('\n')
    if line.count ( '\n' ) == 0 :
      self._GUI += self._Indent * self._IL + line + '\n'
    else:
      lines = line.strip('\n').split('\n')
      indent = len ( lines[0] ) - len ( lines[0].lstrip () )
      for sline in lines :
        self._GUI += self._Indent * self._IL + sline [indent:] + '\n'

  def __add__ ( self, line ) :
    """
    To support normal string addition:
      GUI += "self.Text ,wx.TextCtrl"
    """
    self.Append ( line )
    return self

  def Indent ( self, N = 1 ) :
    """
    Increase Indent
    """
    self._Indent += N

  def Dedent ( self, N = 1 ) :
    """
    Decrease indent by N.
    If N is negative, it becomes an indent !!
    """
    self._Indent -= N

  def __repr__ ( self ) :
    """
    Returns the _GUI string
    """
    return self._GUI
# ***********************************************************************


# ***********************************************************************
# You can specify any additional paramater,
# just in the order they would normally appear
# just DONT specify "self, parent", these are done automatically
#
# Example (see also at the bottom of this module)
#    GUI = """
#    self.NB       ,wx.Notebook   ,style = wx.NO_BORDER
#      self.Grid   ,Base_Table_Grid ,None, data_values, data_types, data_defs
#      Panel2      ,PanelVer, 11  ,name  = "Page2"
#        list1     ,wx.ListCtrl   ,style = wx.LC_REPORT
#    """
#    self.wxGUI = Create_wxGUI ( GUI )
# ***********************************************************************
_Unique_Name_Count = 0
class Create_wxGUI ( object ) :
  def __init__ ( self,
                 GUI,
                 Ini_File_String = '',
                 my_parent = 'self',
                 code      = '',
                 StackUp = 1  ) :
    """
    StackUp definies the stack in which the code will be executed.
    Normally this will be 1,
    but in case a form is based on an intermediate class,
    it might be necessary to execute one frame higher.
    """
    global _Unique_Name_Count

    # in case of a special GUI-string object
    if isinstance ( GUI, wxGUI_String ) :
      GUI = GUI._GUI

    self.code   = code
    new_globals = [ 'Main_P_box' ] #'Unique_NameName_0_box' ]
    Imports     = []
    Unique_Name       = 'Unique_NameName_'
    Scroll_Panels     = []

    # Clear the implicit import counter
    for typ in _Special_Types :
      _Special_Types [ typ ] [1] = 0

    # prepare Save / Restore settings parameters
    if Ini_File_String :
      IniFile_Read  = Ini_File_String + '.Read ( '
      IniFile_Write = Ini_File_String + '.Write ( '
      #Restore_Settings = ''
      #self.Current_Settings = ''
    self.Restore_Settings = ''
    self.Current_Settings = []

    # Initialize the stack with the input values
    stack = []
    stack.append ( [ 0, my_parent, None, [], '' ] )
    first_element = None

    # traverse to all the lines in the definition
    for lnr, defi in enumerate ( GUI.split('\n') ) :

      # stop if not enough elements
      if len ( defi.strip() ) == 0 :
        continue

      # ignore commented lines
      if defi.strip().startswith ( '#' ) :
        continue

      # split the line into elements
      defi = defi.split(',')

      # get the first element
      if not ( first_element ) :
        first_element = defi[0].strip()

      # determine the leading spaces
      indent = len ( defi[0] ) - len ( defi[0].lstrip() )

      # if Spacer-shortcut : "Spacer"
      # Create a unique name and update defi
      if defi[0].strip() in ( 'Spacer', 'HorSpacer' ) :
        Name = Unique_Name + str ( _Unique_Name_Count )
        _Unique_Name_Count += 1
        defi = [ Name ] + defi

      # if nameless components,
      # Create a unique name and update defi
      elif defi[0].strip().startswith ( 'NN_' ) :
        Name = Unique_Name + str ( _Unique_Name_Count )
        _Unique_Name_Count += 1
        defi[0] = defi[0].strip()[3:]
        defi = [ Name ] + defi

      # remove white space from all elements
      for i,item in enumerate ( defi ) :
        defi[i] = defi[i].strip()

      # parse the line: <name> <type> <params>
      name = defi[0]

      # special pre-processing of
      #   - SplitterWindow
      #   - Panels + Sizers
      weights = ''
      Panel_Aligns = ''

      if defi[1] in [ 'SplitterHor', 'SplitterVer' ] :
        typ = 'wx.SplitterWindow'

      ##elif defi[1] in [ 'MultiSplitterHor', 'MultiSplitterVer' ] :
      ##  typ = 'MultiSplitterWindow'

      elif defi[1] in [ 'PanelHor', 'PanelVer',
                        'PageHor', 'PageVer' ] :
        typ = 'wx.Panel'

        # get the ALIGN paramtere (if any) and remove them
        if len ( defi ) > 3 :
          parss = defi[3].split(',')
          new = ''
          for p in parss :
            if 'wx.ALIGN' in p :
              Panel_Aligns = p
            else :
              new += ',' + p
          if new :
            defi[3] = new [1:]

        # get the weight factors (if any) and remove them
        if len ( defi ) > 2 :
          weights = defi[2]
          del defi[2]

      elif defi[1] in [ 'ScrollHor', 'ScrollVer' ] :
        typ = 'ScrolledPanel'  #'wx.Panel'
        Scroll_Panels.append ( name )

      else :
        typ = defi[1]

      # parse the line: <name> <type> <params>
      ##name = defi[0]
      if len ( defi ) > 2 : params = ','+ ','.join ( defi[2:] )
      else :                params = ''

      # ****************************************************************
      # Also a good position to generate code to save / restore settings
      # Components are only added if the following conditions are met:
      #   - must have a name starting with "self." (otherwise we can't save it)
      #   - must be definied in the _Save_Restore dictionary
      # ****************************************************************
      from grid_support import Base_Grid
      from tree_support import Custom_TreeCtrl_Base
      if Ini_File_String and ( name.find ( 'self.' ) == 0 ) :
        Save_Restore = False
        try:
#          print ( 'Get/Setvalue available?', typ )
#          print ( '--', type(typ) )
#          print ( '--', eval(typ) )
#          print ( '--', 'GetValue' in dir(eval(typ)) )
#          print ( '--', 'SetValue' in dir(eval(typ)) )
          if 'GetValue' in dir ( eval ( typ ) ) and \
             'SetValue' in dir ( eval ( typ ) ) :
            Save_Restore = True
            SR = ( '%%.GetValue()', '%%.SetValue(%)')
          else :
            ##raise  # we need to enter the except loop !!
            if typ in _Save_Restore :
              Save_Restore = True
              SR = _Save_Restore [ typ ]
        except :
          print ( '::Get/Setvalue available?', typ )
          traceback.print_exc ()
          if typ in _Save_Restore :
            Save_Restore = True
            SR = _Save_Restore [ typ ]

        if Save_Restore :
          line = 'if ' + Ini_File_String + ':'
          self.Restore_Settings += line + '\n'
          line = '  Value = ' + IniFile_Read + '"' + name [ 5: ] + '", None )'
          self.Restore_Settings += line + '\n'
          line = '  if Value != None :'
          self.Restore_Settings += line + '\n'
          self.Restore_Settings +=  '    try :\n'
          ##Name = name
          ##line = ('    ' + SR[1] ).replace ( '%%', Name ).replace ( '%', 'Value' )
          line = ('      ' + SR[1] ).replace ( '%%', name ).replace ( '%', 'Value' )
          self.Restore_Settings += line + '\n'
          self.Restore_Settings +=  '    except :\n'
          self.Restore_Settings +=  '      traceback.print_exc ()\n'
          self.Restore_Settings +=  '      pass\n'

          line = 'Value = ' + SR[0].replace ( '%%', name ) + '\n'
          line += IniFile_Write + '"' + name [ 5: ] + '" , Value )' + '\n'
          self.Current_Settings.append ( line )
      # ****************************************************************

      # ****************************************************************
      # test for special types and do an explicit import
      # ****************************************************************
      #print 'Name, typ',name,typ
      if typ in _Special_Types :
        ST = _Special_Types [ typ ]
        #print 'SPECIAL', typ, ST
        if ST [1] == 0 :
          Imports.append ( ST[0] )
          ST [1] = 1
      # ****************************************************************


      # Get parent, by searching a parent (= lesser indent)
      self.code = self._Pop_For_Parent ( indent, stack, self.code )
      if self.code == False : return False
      parent = stack [-1]

      # If parent is one of the special ones,
      # Add all children to it's list
      if parent[2] in [ 'SplitterHor', 'SplitterVer', 'wx.SplitterWindow',
                        'PanelHor', 'PanelVer', 'ScrollHor', 'ScrollVer',
                        'wx.Notebook', 'GUI_Notebook' ] :
        stack [-1][3].append ( name )

      # Add the current component to the stack
      stack.append ( [ indent, name, defi[1], [], (weights, Panel_Aligns) ])


      #******************************************************************
      # Create the component
      #******************************************************************
      ##if typ in [ 'MultiSplitterWindow' ] :
      if typ in [ 'MultiSplitterHor, MultiSplitterVer' ] :
        self.code += name + '=' + typ + '( ' + parent[1] + params + ', style=wx.SP_LIVE_UPDATE)\n'
      else :
        self.code += name + '=' + typ + '( ' + parent[1] + params + ')\n'
      #******************************************************************


      ##if defi[1] in [ 'MultiSplitterVer' ] :
      ##  self.code += name + '.SetOrientation(wx.VERTICAL)\n'


      # if parent is multi-splitter, append component
      if parent[2] in [ 'MultiSplitterWindow', 'MultiSplitterHor', 'MultiSplitterVer' ]:
        self.code += parent[1] + '.AppendWindow' + '( ' + name + ')\n'

      #self.code += 'print "CREATE COMP",'+ name + '\n'

      # now if the component doesn't start with "self",
      # we need to add it to the global list
      if name.strip().find ( 'self.' ) != 0 :
        # but we are not allowed to add indexed variables
        n = name.split ( '[' )[0]
        new_globals.append ( n )

    # While there are still elements on the stack,
    # Remove them and perform the actions (Splitter / Sizers / ...)
    indent = 0
    self.code = self._Pop_For_Parent ( indent, stack, self.code )
    if self.code == False : return False

    # Size the main component on the parent
    # What if more than 1 component on the lowest level ??
    # only if main component is a wx.Window or wx.Sizer
    self.code += 'if isinstance (' + first_element +',wx.Window ) or '
    self.code +=    'isinstance (' + first_element + ',wx.Sizer ) :\n'
    self.code += '  Sizer = wx.BoxSizer ( ) \n'
    self.code += '  Sizer.Add ( ' + first_element + ', 1, wx.EXPAND ) \n'
    self.code += '  ' + my_parent + '.SetSizer ( Sizer ) \n'

    # and add the load setting from ini file
    if Ini_File_String :
      #v3print ('RESTORE', self.Restore_Settings )
      self.code += self.Restore_Settings

    # Add the globals to the code,
    # otherwise they are not (very well) visible in the parents namespace
    if len ( new_globals ) > 0 :
      self.code = 'global ' + ','.join( new_globals ) + '\n' + self.code

    #print 'Imports', Imports
    line = ''
    for item in Imports :
      #print 'Import',item
      line += item + '\n'
    if line :
      self.code = line + self.code

    # For scroll panels we need to setup scroll procedures
    for Panel in Scroll_Panels :
      self.code += Panel + '.SetupScrolling( scroll_x=False)'

    # now create the components on the form,
    # by executing the code in the parent's frame namespace
    p_locals  = sys._getframe ( StackUp ).f_locals
    p_globals = sys._getframe ( StackUp ).f_globals
    try :
      # The exec function is only available from 2.6,
      # but seems to already in 2.5 !!
      # It might be better to use the globals only, because
      #  - in the doc there's a warning when making changes to locals
      #  - it doesn't always work ????
      # No that doesn't work either !!!
      #exec self.code in p_globals, p_locals


      #print ( 'PARACHUTE UTYRYUUI', self.code )
      #print ( '----' )
      #print ( self.code )
      #print(exec,self.code)
      exec ( self.code, p_globals, p_locals )
      #exec ( self.code, p_globals )
    except:
      traceback.print_exc ()
      try:
        #import sys eror??
        Error_Info = sys.exc_info()
        tb = traceback.format_exc(Error_Info[2]).splitlines()

        #Error_Line_Nr = int ( tb [-2].split(',')[1].strip().split(' ')[1] )

        exc_type, exc_value, exc_traceback = Error_Info

        L = traceback.extract_tb(exc_traceback)

        Error_Line_Nr = L[1][1]#exc_traceback.tb_lineno
        print(Error_Line_Nr)
        Code = self.code.splitlines ()

        print('********** ERROR in GUI-string *************')
        for i,line in enumerate(Code):
          if i+1 == Error_Line_Nr:  print(2*'\n'+'*'*70)
          print(i + 1, line)
          if i+1 == Error_Line_Nr:  print('*'*70 + '\n'*2)

        print('**********')
        #sys.excepthook ( *sys.exc_info () )
        print(tb [-1])

        import inspect
        Frame_Info = inspect.getframeinfo ( sys._getframe (1) )
        print('Error File :', Frame_Info [0])
        print('Error Func :', Frame_Info [2])
        print('Error Line :', Frame_Info [1])
        print('Error Code :', Frame_Info [3] [ Frame_Info [4] ])

        print('********** End ERROR in GUI-string *************')
      except:
        print('An error in the error exception ?!?!?!?!')
        traceback.print_exc ()

  # ********************************************************
  # ********************************************************
  def Ready ( self ) :
    pass

  # ********************************************************
  # ********************************************************
  def __repr__ ( self ) :
    return self.code

  # ********************************************************
  # ********************************************************
  def Save_Settings ( self, Print = False ) :
    # now store the components settings
    # by executing the code in the parent's frame namespace
    p_locals  = sys._getframe(1).f_locals
    p_globals = sys._getframe(1).f_globals
    #v3print ('GUI saving', self.Current_Settings, '$$$' )
    if Print :
      print('GUI saving')
      print(self.Current_Settings, '$$$')
    for line in self.Current_Settings:
      try :
        exec ( line, p_globals, p_locals )
      except :
        print('=====  ERROR in gui_support.Save_Settings =====')
        print(line)
        traceback.print_exc ()

  # ********************************************************
  # ********************************************************
  def Load_Settings ( self ) :
    # now load the components settings
    # by executing the code in the parent's frame namespace
    p_locals  = sys._getframe(1).f_locals
    p_globals = sys._getframe(1).f_globals
    try    : exec ( self.Restore_Settings, p_globals, p_locals )
    except :
      traceback.print_exc ()
      pass

  # ********************************************************
  # ********************************************************
  def _Pop_For_Parent ( self, indent, stack, code ) :
    # Breakdown the stack until we find an element with a smaller indent
    # which is the parent or container
    while ( len ( stack ) > 0 ) and \
          ( stack [-1] [0] >= indent ):
      last = stack.pop()

      # If a SplitterWindow is popped, add the hor/ver setting
      # I don't find the names hor / ver very logical, so I exchanged them !!
      if last[2] in [ 'wx.SplitterWindow', 'SplitterVer', 'SplitterHor' ] :
        if last[2] in [ 'wx.SplitterWindow', 'SplitterVer' ] :
          code += last[1] + '.SplitHorizontally ( '
        elif last[2] in [ 'SplitterHor' ] :
          code += last[1] + '.SplitVertically ( '

        # Add the 2 elements to the Splitter
        # (The extra comma at the end doesn't seem to bother)
        for element in last[3] :
          code += element + ','
        code += ')\n'

        # ERROR
        if len ( last [3] ) != 2 :
          print('******* ERROR splitter " ' + last[1] + '"does not have 2 controls')
          return False

        # Add minimum panesize
        code += last[1] + '.SetMinimumPaneSize(20)\n'

      # If a Panel with a Sizer is popped from the stack
      # Create the sizer, add all the elements and assign the Sizer
      elif last[2] in [ 'PanelVer', 'PanelHor', ' ScrollHor', 'ScrollVer' ] :

        # Create the Sizer
        if last[2] in  [ 'PanelHor', ' ScrollHor' ] :
          code += last[1] + '_box = wx.BoxSizer ( wx.HORIZONTAL )\n'
        else :
          code += last[1] + '_box = wx.BoxSizer ( wx.VERTICAL )\n'

        # get weights, and be sure we have enough of them
        weights      = last[4][0]
        Panel_Aligns = last[4][1]
        while len ( weights ) < len ( last[3] ):
          weights += '1'

        # Add the elements to the Sizer and their weights
        for i,element in enumerate ( last[3] ) :
          code += last[1] + '_box.Add ( ' + element + ','+ str(weights[i])
          #if Panel_Aligns :
          #  #code += ', wx.EXPAND |' + Panel_Aligns + ' )\n'
          #  code += ', ' + Panel_Aligns + ' )\n'
          #else :
          #  code += ', wx.EXPAND )\n'
          code += ', wx.EXPAND )\n'

        # Assign the Sizer to its parent
        code += last[1] + '.SetSizer ( ' + last[1] + '_box )\n'

      # Add all elements as Pages to the Notebook
      # imageId is inserted as the page-index-number
      # (it won't harm if no imagelist is assigned)
      elif last[2] in [ 'wx.Notebook', 'GUI_Notebook' ] :
        line = last[1] + '.AddPage ( '
        for i, element in enumerate ( last[3] ) :
          code += 'name = ' + element + '.GetName() \n'

          # Changed to let it run under Ubuntu: don't specify the imageId
          #code += line + element + ', name, imageId = ' + str(i) + ') \n'
          code += line + element + ', name' + ') \n'
        ## Generated code for each page:
        ##   name = Panel1.GetName()
        ##   self.NB.AddPage ( self.Panel1, name, imageId = 0)
        ##   name = Panel2.GetName()
        ##   self.NB.AddPage ( self.Panel2, name, imageId = 1)

    return code
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def PreView_wxGUI ( Text ) :
  Text = Text.replace ( '\r', '' )
  Lines = Text.split ( '\n' )

  # first locate the instance creation
  for N, line in enumerate ( Lines ) :
    if line.find ( 'Create_wxGUI' ) > 0 :
      line = line.strip ()
      break
  else :
    return

  # parse the line, to find the name and the GUI-string
  i = line.find ( '=' )
  if i >= 0 :
    Name = line [ : i ].strip()
    line = line [ i+1 : ].strip()
  else :
    Name = None
  line = line.replace ( '(', ',' )
  line = line.replace ( ')', ',' )
  #print line
  GUI_String = line.split ( ',' ) [1].strip()

  # see if there is a Ready method
  for X, line in enumerate ( Lines [ N : ] ) :
    #print '***', line
    if line.find ( Name + '.Ready' ) > 0 :
      N += X
      break

  #print 'FIND',Name, GUI_String

  # find the start of the GUI_string
  for M, line in enumerate ( Lines ) :
    i = line.find ( GUI_String )
    if i >= 0 :
      #print i,M
      ii = line.find ( '=', i+1 )
      if ii > 0 :
        ii = line.find ( '"""', ii+1 )
        if ii >= 0 :
          GUI_Code = line [ ii + 3 : ].strip ()
          #print 'STRAT OF GUICODE',GUI_Code
          break
  else :
    return

  for line in Lines [ M+1 : N+1 ] :
    GUI_Code += line + '\n'

  #print 'GC',GUI_Code

  fh = open ( '../support/gui_template_dont_touch.py', 'r' )
  Text = fh.read ()
  fh.close ()

  Text = Text.replace ( '%%%"""', GUI_Code )
  #print 'Final',Text

  filename = '../support/gui_f12_templatetest.py'
  fh = open ( filename, 'w' )
  fh.write ( Text )
  fh.close ()
  from system_support import Run_Python
  Run_Python ( filename )
# ***********************************************************************

from picture_support import *

# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )



    GUI = """
    self.Splitter_Plots    ,SplitterVer
      self.Panel           ,PanelVer, 010
        self.Panel_Top     ,PanelHor, 11
          label1           ,wx.StaticText  ,label = "Signal1"
          label2           ,wx.StaticText  ,label = "Signal2"
        self.Panel_X       ,wx.Panel, 11
        self.Panel_Bottom  ,PanelHor
          label11          ,wx.StaticText  ,label = "Signal1b"
          label12          ,wx.StaticText  ,label = "Signal2b"
      Panel_B              ,wx.Panel
        Button_1           ,wx.Button      ,label = "Test"
        Button_2           ,wx.Button      ,label = "Test2", pos = (100,0)
    """

    GUI = """
    self.NB       ,wx.Notebook   ,style = wx.NO_BORDER
      self.Grid   ,Base_Table_Grid ,data_values, data_types, data_defs
      Panel2      ,PanelVer, 11  ,name  = "Page2"
        list1     ,wx.ListCtrl   ,style = wx.LC_REPORT
    """

    ##self.MenuBar = Class_Menus ( self )
    GUI = """
    NB            ,wx.Notebook   ,style = wx.NO_BORDER
      Panel1      ,PanelVer, 1   ,name  = "Hello"
        list1     ,wx.ListCtrl   ,style = wx.LC_REPORT
      Panel2      ,PanelVer, 11  ,name  = "Page2"
        window1   ,wx.Window
        window2   ,wx.Window
    """


    from tree_support import Custom_TreeCtrl_Base
    GUI = """
    self.SplitV            ,SplitterVer, style = wx.SP_LIVE_UPDATE | wx.SP_3DSASH
      self.Split           ,SplitterHor, style = wx.SP_LIVE_UPDATE | wx.SP_3DSASH
        self.Tree          ,Custom_TreeCtrl_Base
        self.NB            ,wx.Notebook, style = wx.NO_BORDER
          p1               ,wx.Panel, style = wx.NO_BORDER
          p2               ,wx.Panel, style = wx.NO_BORDER
      self.Error           ,PanelVer
        self.Log           ,wx.TextCtrl, style = wx.TE_MULTILINE | wx.TE_READONLY
    """

    GUI = """
    self.Split           ,SplitterHor, style = wx.SP_LIVE_UPDATE | wx.SP_3DSASH
      self.Tree          ,Custom_TreeCtrl_Base
      self.Log           ,wx.TextCtrl, style = wx.TE_MULTILINE | wx.TE_READONLY
    """
    """
    sel = self.Tree.root
    NewItem = self.Tree.AppendItem ( sel, 'new' )
    NewItem = self.Tree.AppendItem ( sel, 'new' )
    NewItem = self.Tree.AppendItem ( sel, 'new' )
    self.Tree.Bind ( wx.EVT_RIGHT_DOWN,            self.OnRightDown )
    self.Tree.Bind ( wx.EVT_CONTEXT_MENU, self.OnShowPopup )

    Set_Notebook_Images ( NB, ( 47, 76 ) )
    """

    GUI = """
    self.NB       ,wx.Notebook   ,style = wx.NO_BORDER
      self.Grid   ,Base_Table_Grid ,data_values, data_types, data_defs
      Panel2      ,PanelVer, 11  ,name  = "Page2"
        list1     ,wx.ListCtrl   ,style = wx.LC_REPORT
    """
    GUI = """
      Panel2      ,PanelVer, 11  ,name  = "Page2"
        list1     ,wx.ListCtrl   ,style = wx.LC_LIST
    """
    """
    list1.Append ( ('aap','beer','colaoa') )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap') )
    list1.Append ( ('aap') )
    list1.Append ( ('aap') )
    list1.Append ( ('aap') )
    list1.Append ( ('aap') )
    list1.Append ( ('aap') )
    list1.Append ( ('aap') )
    list1.Append ( ('aap') )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    #list1.InsertColumn ( 0, 'col1' )
    #list1.InsertColumn ( 1, 'col2' )
    """


    # ***********************************************************************
    #from   picture_support import *
    bmp_PW    = Get_Image_Resize ( 'vippi_bricks_64.png',          64 )
    bmp_IDE   = Get_Image_Resize ( 'applications-accessories.png', 48 )
    bmp_Lib   = Get_Image_Resize ( 'bieb.png',                     48 )
    bmp_Trans = Get_Image_Resize ( 'romanime0.ico',                48 )

    self.Flags = Flag_Object ()
    bmp_Flag = self.Flags.Get_Flag ( Language_Current[0] )
    #if not bmp_Flag.Ok():
    #  bmp_Flag = wx.EmptyBitmap(32,22)
    #  self.clearBmp ( bmp_Flag )

    import wx.html as  html
    #import  my_iewin   as iewin

    #self.NB         ,wx.Notebook   ,style = wx.NO_BORDER
    GUI = """
    self.NB         ,GUI_Notebook
     Panel2         ,PanelHor,  01  ,name  = 'Main'
      Panel_B       ,wx.Panel  ,size =( 120, -1)
        B_PW        ,BmpBut    ,bitmap = bmp_PW            ,pos = (24, 10) ,size = ( 70,70)
        self.B_Flag ,BmpBut    ,bitmap = bmp_Flag          ,pos = ( 0, 62) ,size = ( 20,14)
        B_PW_Run    ,wx.Button ,label = "PyLab Works"      ,pos = ( 0, 80) ,size = ( 120,20)

        B_IDE       ,BmpBut    ,bitmap = bmp_IDE           ,pos = (24,110) ,size=( 70,70)
        B_IDE_Run   ,wx.Button ,label = "IDE"              ,pos = ( 0,180) ,size=(120,20)

        B_Lib       ,BmpBut    ,bitmap = bmp_Lib           ,pos = (24,210) ,size=( 70,70)
        B_Lib_Run   ,wx.Button ,label = "Library Manager"  ,pos = ( 0,280) ,size=(120,20)

        B_Trans     ,BmpBut    ,bitmap = bmp_Trans         ,pos = (24,310) ,size=( 70,70)
        B_Trans_Run ,wx.Button ,label = "Translation Tool" ,pos = ( 0,380) ,size=(120,20)

        st1         ,wx.StaticText,label = 'CommandLine Flags'  ,pos = (5,410)
        cb1         ,wx.CheckBox ,label = 'debug'               ,pos = (5,425)
        cb1         ,wx.CheckBox ,label = 'debugfile'           ,pos = (5,440)
      self.IE       ,iewin.IEHtmlWindow, style = wx.NO_FULL_REPAINT_ON_RESIZE


     self.Split_Demo  ,SplitterHor, name = 'Demos'
       p4           ,PanelVer , 1000       ,name = 'Demos'
        self.Tree     ,Custom_TreeCtrl_Base
        p4b           ,PanelHor ,11       ,name = 'Demos'
          B_Expand    ,wx.Button ,label = "Expand"
          B_Expands    ,wx.Button ,label = "Collapse"
        p4bb           ,PanelHor ,11       ,name = 'Demos'
          B_Expandb    ,wx.ToggleButton ,label = "Application"
          B_Expandsb    ,wx.ToggleButton ,label = "Design"
        B_Restore    ,wx.Button ,label = "Restore Orginal"
       self.Html     ,html.HtmlWindow ,style=wx.NO_FULL_REPAINT_ON_RESIZE


     Split_V2       ,SplitterVer    ,name = 'Tests'
      self.List_Test,wx.ListCtrl    ,style = wx.LC_LIST
      p3            ,PanelHor,10    ,name = 'Demos'
       self.Log     ,wx.TextCtrl    ,style = wx.TE_MULTILINE
       p4           ,wx.Panel       ,name = 'Demos'
        B_Run_Sel   ,wx.Button      ,label = "Run Sel"          ,pos = (0,0)
        B_Run_All   ,wx.Button      ,label = "Run All"          ,pos = (0, 25)
        self.CB_Debug     ,wx.CheckBox ,label = 'debug'               ,pos = (0,50)
        self.CB_DebugFile ,wx.CheckBox ,label = 'debugfile'           ,pos = (0,70)
        self.RB_Tests     ,wx.RadioBox ,label='Tests', choices=['Original', 'All', 'Choice'] ,majorDimension=1 ,pos = (0,90)
        self.Test_Choice  ,wx.TextCtrl                          ,pos = (0,175), size =(75,-1)
    """
    #self.wxGUI = Create_wxGUI ( GUI )
    #from picture_support import Get_Image_List
    #self.NB.AssignImageList ( Get_Image_List () )
    # ***********************************************************************


    # ***********************************************************************
    from tree_support import Custom_TreeCtrl_Base


    # ***********************************************************************
    # Scope Display with History display
    # ***********************************************************************
    GUI = """
      self.Scope     ,tBase_Scope_with_History
    """
    GUI = """
      P1                  ,PanelVer  ,01
        P2                ,wx.Panel
          self.B_Record   ,wx.Button ,label = 'Record'  ,pos = (0,0)
          self.CB_Debug     ,wx.CheckBox ,label = 'debug'               ,pos = (0,50)
        self.Edit         ,Base_STC
    """

    xGUI = wxGUI_String ()
    xGUI.Append ( "P1 ,PanelVer  ,01" )
    xGUI.Append ( "  P2                ,wx.Panel" )
    xGUI.Append ( "    self.B_Record,wx.Button ,label = 'Record'  ,pos = (0,0)" )
    xGUI.Append ( "    self.CB_Debug     ,wx.CheckBox ,label = 'debug'               ,pos = (0,50)")
    xGUI.Append ( "  self.Edit         ,Base_STC" )

    zGUI = wxGUI_String ( "P1 ,PanelVer  ,01" )
    #print 'YYYY' ##, xGUI,zGUI
    #zGUI.Indent ()
    #zGUI.Append ( 1, "P2 ,wx.Panel" )
    #zGUI.Indent ()
    #zGUI.Append ( 1, "self.B_Record,wx.Button ,label = 'Record'  ,pos = (0,0)" )
    zGUI.Append ( "self.CB_Debug     ,wx.CheckBox ,label = 'debug'               ,pos = (0,50)")
    #zGUI.Dedent ()
    #zGUI.Append ( -1, "self.Edit         ,Base_STC" )

    # print 'AAA',GUI
    #print 'BBB\n',xGUI._GUI
    #print 'CCC\n',zGUI._GUI

    GUI = wxGUI_String ( "self.Splitter , SplitterHor" )
    GUI.Indent ()
    GUI.Append ( "self.Text ,wx.TextCtrl  ,style = wx.TE_MULTILINE | wx.TE_RICH" )
    GUI.Append ( "self.NB   ,wx.Notebook" )
    GUI.Indent ()
    GUI.Append ( "p4        ,wx.Panel ,name = 'First'"  )
    GUI.Append (    "self.RTC_Panel     ,Base_RTC   ,name='Html'" )
    GUI.Append ( "p5        ,wx.Panel ,name = 'Second'" )
    #self.wxGUI = Create_wxGUI ( GUI, Ini_File_String = 'self.Ini_File' )

    GUI = wxGUI_String ( "self.Splitter , SplitterHor" )
    GUI.Indent ()
    #GUI.Append (    "self.Text     ,Base_RTC   ,name='Html'" )
    import wx.richtext as rt
    GUI.Append ( "self.Text  ,rt.RichTextCtrl" )
    GUI.Append ( "self.Text2 ,wx.TextCtrl  ,style = wx.TE_MULTILINE | wx.TE_RICH" )
    #GUI.Append ( "self.NB   ,wx.Notebook" )
    #GUI.Indent ()
    #GUI.Append ( "p4        ,wx.Panel ,name = 'First'"  )
    #GUI.Append ( "p5        ,wx.Panel ,name = 'Second'" )

    XXX = 'aap,beer,cola'.split(',')
    GUI = """
#    self.Main_Window ,PanelVer
      self.Splitter    ,SplitterHor
        self.NB         ,wx.Notebook
          self.Memo        ,wx.TextCtrl
          P4               ,wx.Panel   ,name='aap'
        NN_PanelVer  ,0000000000000
          NN_PanelHor  ,00000
           NN_PanelVer  ,00000
            ok             ,wx.Button  ,label= 'OK'
            cancel         ,wx.Button  ,label= 'Cancel'
            save           ,wx.Button  ,label= 'Save'
          Spacer  ,10
          NN_PanelVer  ,0000000000000
#           NN_wx.Panel
#            self.T1        ,wx.TextCtrl   ,pos=(0,0)  ,size=(200,-1)
#            self.C1        ,wx.Choice     ,pos=(0,0)  ,size=(200,-1)  ,choices=XXX
           NN_PanelVer   ,0000
#            self.T1        ,wx.TextCtrl   ,pos=(0,0)
#            self.C1        ,wx.Choice     ,pos=(0,0)   ,choices=XXX
            self.T1        ,wx.TextCtrl
            self.C1        ,wx.Choice       ,choices=XXX
          Spacer  ,10
          self.CC   ,GUI_Choice   ,choices=XXX
          Spacer  ,10
          NN_PanelHor  ,0000000000000
            Test  ,wx.Button  ,label = 'Test'
    """
    """
    self.wxGUI = Create_wxGUI ( GUI, Ini_File_String = 'self.Ini_File' )
    Test.Bind( wx.EVT_BUTTON, self._On_Test )
    self.T1.SetBackgroundColour ( wx.RED )
    self.T1.SetEditable ( False )
    """


    GUI = """
        self.SplitterV       ,SplitterVer
          self.SplitterH       ,SplitterHor
            NN_PanelVer     ,0001
              Spacer ,5
              NN_wx.StaticText ,label = '  Answers'
              Spacer ,5
              self.Memo_Answers     ,wx.TextCtrl  ,style = wx.TE_MULTILINE
            NN_PanelVer     ,0001
              Spacer ,5
              NN_wx.StaticText ,label = '  Tasks'
              Spacer ,5
              self.Memo_Tasks       ,wx.TextCtrl  ,style = wx.TE_MULTILINE
          Memo_Start       ,wx.TextCtrl  ,style = wx.TE_MULTILINE
        """
    self.Filename = r'D:\__aap\FN1.png'
    import OGLlike as ogl
    import  wx.lib.scrolledpanel as scrolled
    ##Image = wx.Image ( self.Filename ).ConvertToBitmap()
    GUI = """
#      self.Pan  ,SplitterHor
   Pan ,PanelVer  ,11
#       self.Panel  ,scrolled.ScrolledPanel  ,size = (100,100)
       self.Panel   ,wx.PyScrolledWindow
#       ,size = (1000,1000)
#        self.OGL ,ogl.OGL_Picture_Edit  ,Filename = self.Filename
        self.OGL    ,wx.StaticBitmap  ,-1 ,wx.EmptyBitmap(1,1)
       self.Panel2  ,wx.ScrolledWindow  ,size = (100,100)
         self.OGL2    ,wx.StaticBitmap  ,-1 ,wx.EmptyBitmap(1,1)
    """


    GUI = """
    Splitter1       ,SplitterVer
      Panel_Top     ,wx.Panel
      Panel_Bottom  ,wx.Panel
        Button_1    ,wx.Button,  label = "Test"
#        Button_2    ,wx.Button,  label = "Test2", pos = (100,0)
        self.Tree          ,Custom_TreeCtrl_Base
    """

    self.wxGUI = Create_wxGUI ( GUI, Ini_File_String = 'self.Ini_File' )
    print(self.wxGUI)
    self.Tree.Root.AppendItem ( 'Root' )
    return

    Image = wx.Image ( self.Filename ).ConvertToBitmap()
    self.OGL.SetBitmap ( Image )
    #self.OGL2.SetBitmap ( Image )

    self.Panel.SetVirtualSize((100,400))
    self.Panel.SetAutoLayout(1)
    self.Panel2.SetVirtualSize((100,400))
    self.Panel2.SetAutoLayout(1)
    #self.Panel.SetupScrolling()

    self.SetAutoLayout(1)
    #self.SetupScrolling()

    '''
    GUI = wxGUI_String ( "self.Splitter , SplitterHor" )
    GUI.Append ( 1, "self.Text ,wx.TextCtrl" )
    GUI.Append (    "self.NB   ,wx.Notebook" )
    GUI.Append ( 1, "p4        ,wx.Panel ,name = 'First'"  )
    GUI.Append (    "p5        ,wx.Panel ,name = 'Second'" )
    self.wxGUI = Create_wxGUI ( GUI, Ini_File_String = 'self.Ini_File' )

    GUI = wxGUI_String ( "self.Splitter , SplitterHor" )
    GUI.Indent ()
    GUI += "self.Text  ,Base_STC"
    GUI += """
    self.NB   ,wx.Notebook
      p4        ,wx.Panel ,name = 'First'
      p5        ,wx.Panel ,name = 'Second'
    """
    print GUI
    self.wxGUI = Create_wxGUI ( GUI, Ini_File_String = 'self.Ini_File' )
    '''
    #self.Text.LoadFile ( 'aapjes.txt')


    #print self.wxGUI
    #self.Edit.Set_Lexer ( 'Psycho' )
    #self.B_Record.Bind ( wx.EVT_BUTTON, self._On_Record )
    #self.Record = False


    # ***********************************************************************


    # ***********************************************************************
    GUI = """
      self.SplitV         ,SplitterVer
        self.Edit         ,Base_STC
        self.Edit2         ,Base_STC
    """
    #from Scintilla_support import Base_STC
    #self.wxGUI = Create_wxGUI ( GUI )
    # ***********************************************************************

    # ***********************************************************************
    w = 85
    h = 24
    GUI = """
    self.Split                   ,SplitterHor
      self.Edit                  ,Base_STC
      p1                         ,PanelHor  ,01
        p2                       ,wx.Panel
          self.B_Calculate       ,wx.Button     ,label = 'Calculate'      ,pos = (0,0)   ,size = (w,h)
          self.B_Save_Settings   ,wx.Button     ,label = 'Save_Settings'  ,pos = (0,30)  ,size = (w,h)
          self.B_Load_Settings   ,wx.Button     ,label = 'Load_Settings'  ,pos = (0,60)  ,size = (w,h)
          self.B_Kill            ,wx.Button     ,label = 'Kill'           ,pos = (0,90)  ,size = (w,h)
          self.B_ForGroundColor  ,wx.Button     ,label = 'ForGroundColor' ,pos = (0,120) ,size = (w,h)
        p3                       ,PanelVer  ,010
          p5                     ,PanelHor  ,010
            self.B_GetValue      ,wx.Button     ,label = 'Get'                           ,size=(40,h)
            Label_Top            ,wx.StaticText ,label = 'Value'          ,style=wx.ALIGN_CENTER
            self.B_SetValue      ,wx.Button     ,label = 'Set'                           ,size=(40,h)
          self.Value             ,wx.TextCtrl   ,style = wx.TE_MULTILINE
          p4                     ,wx.Panel
            self.B_GetSize       ,wx.Button     ,label = 'GetSize'        ,pos = (0,0)   ,size =(50,h)
            self.L_GetSize       ,wx.StaticText ,label = 'GetSize'        ,pos = (55,5)
            self.B_GetID         ,wx.Button     ,label = 'GetID'          ,pos = (0,25)  ,size =(50,h)
            self.L_GetID         ,wx.StaticText ,label = 'GetID'          ,pos = (55,30)
    """
    #from Scintilla_support import Base_STC
    #self.wxGUI = Create_wxGUI ( GUI )
    # ***********************************************************************


    # ***********************************************************************
    GUI = """
    self.NB       ,wx.Notebook   ,style = wx.NO_BORDER
      p4           ,wx.Panel       ,name = 'Demos'
      Panel2      ,PanelVer, 11  ,name  = "Page2"
        list1     ,wx.ListCtrl   ,style = wx.LC_REPORT
    """
    #self.wxGUI = Create_wxGUI ( GUI )
    # ***********************************************************************

    #print self.wxGUI

    self.Bind ( wx.EVT_CLOSE, self._On_Close )
    print('DDDOONNNEE')
    #wx.CallAfter ( self._On_Test )
    #wx.CallLater ( 1000, self._On_Test )

  # ***********************************************************************
  def _On_Test ( self, event = None ) :
    Enable = self.T1.IsShown ()
    self.T1.Show ( not ( Enable ) )
    self.C1.Show ( Enable )
    self.T1.SetLabel ( self.C1.GetStringSelection () )

    self.CC.Set_Enable ( Enable )
    self.Splitter.SendSizeEvent ()

  # ***********************************************************************
  def _On_Close ( self, event ) :
    event.Skip ()
    print('wxguics', self.wxGUI.Current_Settings)
    self.wxGUI.Save_Settings ()

  # ***********************************************************************
  def _On_Record ( self, event ) :
    self.Record = not ( self.Record )
    """
    if self.Record :
      self.B_Record.SetLabel ( '--running--' )
      import pyaudio
      import wave
      import sys

      chunk = 1024
      FORMAT = pyaudio.paInt16
      CHANNELS = 1
      RATE = 44100
      #RECORD_SECONDS = 5
      WAVE_OUTPUT_FILENAME = "output.wav"
      p = pyaudio.PyAudio()
      stream = p.open(format = FORMAT,
                      channels = CHANNELS,
                      rate = RATE,
                      input = True,
                      frames_per_buffer = chunk)

      print "* recording"
      all = []
      wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
      wf.setnchannels(CHANNELS)
      wf.setsampwidth(p.get_sample_size(FORMAT))
      wf.setframerate(RATE)


      for i in range(0, RATE / chunk * RECORD_SECONDS):
          data = stream.read(chunk)
          wf.writeframes(data)
          #all.append(data)
      print "* done recording"

      stream.close()
      p.terminate()

      # write data to WAVE file
      #data = ''.join(all)
      wf.close()
    """


  # ***********************************************************************
  def OnRightDown ( self, event ) :
    print('MOUSE RIGHT')
    #event.Skip()

  def OnShowPopup ( self, event ) :
    print('POPUP')
    #event.Skip()
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class Test_Dynamic_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )

    GUI = """
    Splitter1         ,SplitterHor
      Panel_Left      ,wx.Panel
        self.N_Button ,wx.TextCtrl
        self.N_Slider ,wx.TextCtrl              ,pos = ( 0, 25 )
        Button_Go     ,wx.Button,  label = "Go" ,pos = ( 0, 50 )
      self.Panel      ,wx.ScrolledWindow
    """
    self.wxGUI = Create_wxGUI ( GUI )
    Button_Go.Bind ( wx.EVT_BUTTON, self._On_Go )
    self.Panel.Bind ( wx.EVT_SIZE, self._On_Size )
    #print self.wxGUI
    # ***********************************************************************

    self.Buttons = []
    self.Sliders = []

  def _On_Size ( self, event = None ) :
    x = 0
    w = event.GetSize () [0] - 15
    if len ( self.Buttons ) > 0 :
      x += 75
    w -= x
    for Slider in self.Sliders :
      Slider.SetPosition ( ( x, -1 ) )
      Slider.SetSize     ( ( w, -1 ) )

  def _On_Go ( self, event = None ) :
    N_Button = int ( self.N_Button.GetValue () )
    N_Slider = int ( self.N_Slider.GetValue () )

    # Correct the number of buttons
    N = len ( self.Buttons )
    BH = 25
    BW = 75
    if N_Button < N :
      for i in range ( N - N_Button ) :
        Button = self.Buttons.pop ()
        Button.Hide ()
        del Button
    elif N_Button > N :
      for i in range ( N_Button - N ) :
        N += 1
        Button = wx.Button ( self.Panel, label = 'Button ' + str ( N ),
                             pos= ( 0, (N-1)*BH ) )
        self.Buttons.append ( Button )

    from float_slider import Float_Slider
    N = len ( self.Sliders )
    x = 0
    SH = 55
    if N_Button > 0 :
      x = 75
    if N_Slider < N :
      for i in range ( N - N_Slider ) :
        Slider = self.Sliders.pop ()
        Slider.Hide ()
        del Slider
    elif N_Slider > N :
      for i in range ( N_Slider - N ) :
        N += 1
        Slider = Float_Slider ( self.Panel,
           caption  = 'Slider' + str (N),
           pos = ( x, (N-1) * SH ),
           size = ( self.Panel.GetSize () [0] - x, SH ) )
        if N % 2 > 0 :
          Slider.SetForegroundColour ( wx.BLUE )
          Slider.SetBackgroundColour ( wx.RED )
        self.Sliders.append ( Slider )

    maxH = max ( N_Button * BH, N_Slider * SH )
    self.Panel.SetScrollbars ( 1, 1, 10, maxH )

    # Repositioning and resizing doesn't happen automatically
    # SendSizeEvent doesn't work either
    if maxH > self.Panel.GetSize () [1] :
      Scroll = 15
    else :
      Scroll = 0
    for Slider in self.Sliders :
      Slider.SetSize ( ( self.Panel.GetSize () [0] - x - Scroll, -1 ) )
      Slider.SetPosition ( ( x, -1 ) )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Test_Control_Scope ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Test of Control_Scope', ini )

    import copy
    import wx
    import wx.grid as gridlib
    #from   grid_support    import *
    from   grid_support import MY_GRID_COL_TYPED, MY_GRID_FIXED_ROW, MY_GRID_TYPE_COLOR

    data_values = [
      [ 'Name', 'On', 'NumOn', 'Lower','Upper',
        'AC', 'AC[s]', 'Delay[s]',
        'LineColor', 'LineWidth',
        'World-1', 'Cal-1', 'World-2', 'Cal-2' ] ]
    data_values_default = [
      'Signal i', False, True, -10, 10,
      False, 1, 0,
      (200,0,0), 2, 0, 0, 1, 1 ]


    for i in range (16 ):
      default = copy.copy ( data_values_default )
      default[0] = ' Signal ' + str(i+1) + ' [Volt]'
      A, B = 100, 255

      if i < 3 :
        default [1] = True
        default [8] = ( (i*A)%B, ((i+1)*A)%B, ((i+2)*A)%B )
      data_values.append ( default ) #14*[''])
    #print data_values
    data_types = [
      gridlib.GRID_VALUE_STRING,
      gridlib.GRID_VALUE_BOOL,
      gridlib.GRID_VALUE_BOOL,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_BOOL,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      MY_GRID_TYPE_COLOR,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER ]
    data_defs = ( MY_GRID_FIXED_ROW, MY_GRID_COL_TYPED )

    Image_List = Get_Image_List ()
    bmp_Pause = Image_List.GetBitmap ( 49 )
    bmp_Run   = Image_List.GetBitmap ( 50 )
    bmp_Plus  = Image_List.GetBitmap ( 56 )
    bmp_Minus = Image_List.GetBitmap ( 57 )
    bmp_Up    = Image_List.GetBitmap ( 45 )
    bmp_Down  = Image_List.GetBitmap ( 44 )
    bmp_Color = Image_List.GetBitmap ( 48 )

    b_size = ( 22, 22 )
    GUI = """
    self.NB            ,wx.Notebook  ,style = wx.BK_LEFT
      self.Splitter      ,SplitterHor  ,name = 'Scope'  ,style = wx.NO_BORDER
        self.Panel_Left    ,wx.Panel
          B_Pause     ,BmpBut  ,bitmap = bmp_Pause  ,pos = (2,2)   ,size = b_size
          B_Run       ,BmpBut  ,bitmap = bmp_Run    ,pos = (2,27)  ,size = b_size
          B_Plus      ,BmpBut  ,bitmap = bmp_Plus   ,pos = (27,2)  ,size = b_size
          B_Minus     ,BmpBut  ,bitmap = bmp_Minus  ,pos = (27,27) ,size = b_size
          B_Up        ,BmpBut  ,bitmap = bmp_Up     ,pos = (52,2)  ,size = b_size
          B_Down      ,BmpBut  ,bitmap = bmp_Down   ,pos = (52,27) ,size = b_size
          B_Color     ,BmpBut  ,bitmap = bmp_Color  ,pos = (77,2)  ,size = b_size
          self.Sel_Signal  ,wx.StaticText, label = '--', pos = ( 77, 27 )
        self.Panel_Right   ,wx.Panel
          self.Scope       ,tBase_Scope_with_History
      self.Grid          ,Base_Table_Grid  ,data_values, data_types, data_defs, name='Settings'
    """
    self.wxGUI = Create_wxGUI ( GUI )
    print(self.wxGUI)

    self.Panel_Left.SetBackgroundColour ( wx.BLACK )

    """
    B_Pause.SetToolTipString ( _(0, 'Pause Recording'                    ) )
    B_Run  .SetToolTipString ( _(0, 'Start Recording'                    ) )
    B_Plus .SetToolTipString ( _(0, 'Increase selected signal Amplitude' ) )
    B_Minus.SetToolTipString ( _(0, 'Decrease selected signal Amplitude' ) )
    B_Up   .SetToolTipString ( _(0, 'Shift selected signal Up'           ) )
    B_Down .SetToolTipString ( _(0, 'Shift selected signal Down'         ) )
    B_Color.SetToolTipString ( _(0, 'Set Color of selected signal'       ) )
"""
    B_Pause.SetToolTip ( _(0, 'Pause Recording'                    ) )
    B_Run  .SetToolTip ( _(0, 'Start Recording'                    ) )
    B_Plus .SetToolTip ( _(0, 'Increase selected signal Amplitude' ) )
    B_Minus.SetToolTip ( _(0, 'Decrease selected signal Amplitude' ) )
    B_Up   .SetToolTip ( _(0, 'Shift selected signal Up'           ) )
    B_Down .SetToolTip ( _(0, 'Shift selected signal Down'         ) )
    B_Color.SetToolTip ( _(0, 'Set Color of selected signal'       ) )

    self.Sel_Signal.SetForegroundColour ( wx.WHITE )
    #self.Sel_Signal.SetToolTipString ( _( 0, 'Selected Signal') )
    self.Sel_Signal.SetToolTip ( _( 0, 'Selected Signal') )

    Set_Notebook_Images ( self.NB, ( 47, 67 ) )

    wx.CallLater ( wxGUI_Delay, self.Splitter.SetSashPosition, 102 )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Test_Control_Grid ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Test of Control_Scope', ini )

    import copy
    #import wx
    import wx.grid as gridlib
    #from   grid_support    import *
    from   grid_support import MY_GRID_COL_TYPED, MY_GRID_FIXED_ROW_COL, MY_GRID_TYPE_COLOR

    data_values = [ [ '', 'Low', 'High', 'Gain','Weight'] ]
    data_values_default = [ '', -10, 10, 1, 1 ]
    for i in range (3 ):
      default = copy.copy ( data_values_default )
      default[0] = ' Band ' + str(i+1)
      data_values.append ( default )

    #print data_values
    data_types = [
      gridlib.GRID_VALUE_STRING,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER ]
    data_defs = ( MY_GRID_FIXED_ROW_COL, MY_GRID_COL_TYPED )

    GUI = """
    Panel_Top  ,PanelVer, 10
      self.Grid   ,Base_Table_Grid  ,data_values, data_types, data_defs, name='Settings'
      Panel_Bottom  ,wx.Panel
        Button_1    ,wx.Button,  label = "Test"
    """
    self.wxGUI = Create_wxGUI ( GUI )
    print(self.wxGUI)

    self.Bind ( wx.EVT_SIZE, self._On_Size )

  def _On_Size ( self, event ) :
    event.Skip ()
    v3print ( 'OnSize' )

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Test_RVE ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Test of Control_Scope', ini )

    GUI = wxGUI_String ( "self.Splitter , SplitterHor" )
    GUI.Indent ()
    GUI.Append ( "self.Text1 ,wx.TextCtrl  ,style = wx.TE_MULTILINE | wx.TE_RICH" )
    GUI.Append ( "self.Dock ,wx.Panel" )
    self.wxGUI = Create_wxGUI ( GUI, Ini_File_String = 'self.Ini_File' )

    RVE = r'D:\DATA_actueel\D7_PyRichEdit\PyRichView.exe'
    subprocess.Popen ( [RVE,'test' ], shell=False )

    #self.Bind ( wx.EVT_SIZE, self._On_Size )
    self.Dock.Bind ( wx.EVT_SIZE, self._On_Size )
    print(Get_Process_PID ( 'PyRichView.exe' ))

    self.Bind ( wx.EVT_CLOSE, self._On_Close )

    # initialize the State_Machine and start the timer
    self.VP = None
    self.VP_State = 0
    self.Old_Size = ( 0, 0 )
    self.Timer = wx.Timer ( self )
    # the third parameter is essential to allow other timers
    # the third parameter is essential to allow other timers
    self.Bind ( wx.EVT_TIMER, self._On_Timer, self.Timer)
    self.Timer.Start ( 100 )

  # *****************************************************************
  # *****************************************************************
  def _On_Timer ( self, event ) :
    size = self.Dock.GetSize ()
    # Rest, wait till a resize is detected
    if self.VP_State == 0 :
      #print '*',
      if size != self.Old_Size :
        print('SIZE OLD',size,self.Old_Size)
        self.Old_Size = size
        self.VP_State = 1

        #visual.scene.visible = False

    # wait in this state until size remains stable
    elif self.VP_State == 1 :
      if size != self.Old_Size :
        self.Old_Size = size
      else :
        self.VP_State = 2

    # do an extra test if size is still unchanged
    elif self.VP_State == 2 :
      if size != self.Old_Size :
        self.Old_Size = size
        self.VP_State = 1
      else :
        self.VP_State = 3

    # now the size is stable for at least 2 clock cycli
    # so it's time to recreate the VPython window
    elif self.VP_State == 3 :
      #visual.scene.visible = True
      wx.CallLater ( 100, self.Fetch_VP )
      self.VP_State = 4

    # if we didn't find the VPython window previous time
    ##elif self.VP_State == 4 :
    ##  wx.CallLater ( 10, self.Fetch_VP )

  # *****************************************************************
  # Recreate and Position the VPython window
  # *****************************************************************
  def Fetch_VP ( self ) :
    print('Fetch')

    w = self.Old_Size[0]
    h = self.Old_Size[1]

    if Platform_Windows :
      import win32gui, win32con
      # Try to find the newly created VPython window
      # which is now a main-application-window
      if not ( self.VP ) :
        self.VP = win32gui.FindWindow ( None, 'Form5' )
        print('gdasyd',self.VP)

        if self.VP:
          # reset the State Machine
          self.VP_State = 0

          # get the handle of the dock container
          PP = self.Dock.GetHandle ()

          # Set Position and Size of the VPython window,
          # Before Docking it !!
          #flags = win32con.SWP_ASYNCWINDOWPOS or \
          #        win32con.SWP_SHOWWINDOW     or \
          #        win32con.SWP_FRAMECHANGED
          flags = win32con.SWP_SHOWWINDOW or \
                  win32con.SWP_FRAMECHANGED

          win32gui.SetWindowPos ( self.VP, win32con.HWND_TOPMOST,
                                  0,0,w, h, flags )
          #                        -4, -22, w+8, h+26, flags )
          #win32gui.MoveWindow ( self.VP, -4, -22, w+8, h+26, True )

          # Dock the VPython window
          win32gui.SetParent ( self.VP, PP )
          print('gdasyd--',self.VP)

        # Set focus to the main application window
        ##PG.Final_App_Form._On_Focus_VPython ()
      else :
        self.VP_State = 0


  def _On_Close ( self, event ) :
    event.Skip ()
    self.Timer.Stop ()
    #print 'KILL',
    Kill_Process ( 'PyRichView.exe' )

  def _On_Size ( self, event ) :
    event.Skip ()
    v3print ( 'OnSize', self.Dock.GetSize (), self.VP, self.VP_State )
    if self.VP :
      w, h = self.Dock.GetSize ()

      import win32gui, win32con
      flags = win32con.SWP_SHOWWINDOW or \
              win32con.SWP_FRAMECHANGED
      ##win32gui.SetWindowPos ( self.VP, win32con.HWND_TOPMOST,
      win32gui.SetWindowPos ( self.VP, 0,
                              30, -22, w+8, h+26, 0) #flags )
      print('zzz', Get_Process_PID ( 'PyRichView.exe' ), self.VP)

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Collapse_WEG ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Test of Collapse', ini )

    GUI = """
  self.Main_P  ,PanelVer       ,0000000
    NN_PanelHor     ,00000
      self.But1     ,wx.Button  ,label='een'
      self.But2     ,wx.Button  ,label='twee'
    """

    GUI += """
    Spacer  ,5
    self.FF  ,PanelVer     ,0001
      Spacer ,3
      NN_PanelHor  ,0000
        Spacer ,6
        self.CB1    ,wx.CheckBox   ,label=''
        Spacer ,6
        self.B1     ,wx.Button  ,label = 'def After_Init (self):'  ,size=(-1,18)
      Spacer ,3
      self.NN  ,PanelHor   ,01
        Spacer  ,25
        self.Split    ,SplitterHor
          self.Log         ,Base_STC
          self.Help        ,wx.TextCtrl
    """

    """
    self.N_Methods = 3
    self.CB    = self.N_Methods * [ None ]
    self.CB_ID = self.N_Methods * [ None ]
    self.Edit  = self.N_Methods * [ None ]
    self.Log   = self.N_Methods * [ None ]

    GUI = wxGUI_String ( 'self.Main_Panel ,MultiSplitterHor' )
    for i in range ( self.NServers ) :
      GUI.Append (  1, "P%i             ,PanelVer ,01" % ( i ) )
      GUI.Append (  1, "  Pb%i            ,PanelHor ,01" % ( i ) )
    """

    aGUI = """
    Spacer ,5
    self.FF2  ,PanelVer     ,0001
      Spacer ,3
      NN_PanelHor  ,0001
        self.B1     ,wx.Button  ,label = 'Expand'
        Spacer ,3
        self.CB2    ,wx.CheckBox   ,label='run'
      Spacer ,3
      self.Split2    ,SplitterHor
        self.Log2         ,Base_STC
        self.Help2        ,Base_STC
#    NN_PanelVer     ,01
#      self.But4     ,wx.Button  ,label='een'
    """
    self.wxGUI = Create_wxGUI ( GUI, Ini_File_String = 'self.Ini_File' )

    print(self.wxGUI.code)

    print('ZZZZ', self.Main_P.GetSizer ())
    self.SizerItem = self.Main_P_box.GetItem (1)

    self.But1.Bind ( wx.EVT_BUTTON, self._On_Button1 )
    self.But2.Bind ( wx.EVT_BUTTON, self._On_Button2 )

  def _On_Button1 ( self, event ) :
    print('piep')
    #self.Split.Show ( True )
    #self.Split.GetParent().Show ( True )
    self.NN.Show ( True )
    self.SizerItem.SetProportion ( 1 )
    self.Main_P.Layout ()

  def _On_Button2 ( self, event ) :
    print('piep')
    self.NN.Show ( False )
    self.SizerItem.SetProportion ( 0 )
    self.Main_P.Layout ()

# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class Collapse2 ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Test of Collapse', ini )

    GUI = """
  self.Main_P  ,PanelVer       ,00101010101000000000000000
    NN_PanelHor     ,00000
      self.But1     ,wx.Button  ,label='een'
      self.But2     ,wx.Button  ,label='twee'
    """

    self.N_Methods = 5
    self.CB      = self.N_Methods * [ None ]
    self.Buttons = self.N_Methods * [ None ]
    self.Split   = self.N_Methods * [ None ]
    self.Log     = self.N_Methods * [ None ]
    self.Help    = self.N_Methods * [ None ]

    for i in range ( self.N_Methods ) :
      GUI += """
    Spacer   ,3
    NN_PanelVer          ,0001
      Spacer ,3
      NN_PanelHor        ,0000
        Spacer ,6
        self.CB      [%i]  ,wx.CheckBox   ,label=''
        Spacer ,6
        self.Buttons [%i]  ,wx.Button  ,label = 'def After_Init (self):'  ,size=(-1,18)
      Spacer ,3
      NN_PanelHor        ,01
        HorSpacer ,25
        self.Split  [%i]   ,SplitterHor
          self.Log  [%i]     ,Base_STC
          self.Help [%i]     ,wx.TextCtrl  ,style = wx.NO_BORDER
    """ % ( i, i, i, i, i )

    GUI += """
    NN_PanelHor     ,00000
      self.But7     ,wx.Button  ,label='een'
    """

    self.wxGUI = Create_wxGUI ( GUI, Ini_File_String = 'self.Ini_File' )

    print(self.wxGUI.code)

    print('ZZZZ', self.Main_P.GetSizer ())
    #self.SizerItem = self.Main_P_box.GetItem (2)

    for i in range ( self.N_Methods ) :
      self.Buttons[i].Bind ( wx.EVT_BUTTON, self._On_Toggle_X )
      self.Split  [i].Bind ( wx.EVT_SPLITTER_SASH_POS_CHANGED, self._On_Splitter)


  # ********************************************************
  # ********************************************************
  def _On_Splitter ( self, event ) :
    Splitter = event.GetEventObject ()
    if Splitter not in self.Split :
      return

    Index = self.Split.index ( Splitter )
    Pos = self.Split [ Index ].GetSashPosition ()
    for Splitter in self.Split :
      Splitter.SetSashPosition ( Pos )

  # ********************************************************
  # ********************************************************
  def _On_Toggle_X ( self, event ) :
    Button = event.GetEventObject ()
    if Button not in self.Buttons :
      return

    Index = self.Buttons.index ( Button )

    Hidden = not ( self.Split [ Index ].IsShown () )
    self.Split [ Index ].Show ( Hidden )

    self.SizerItem = self.Main_P_box.GetItem ( 2*Index + 2 )
    self.SizerItem.SetProportion ( int ( Hidden ) )
    print(' JJJJ', self.SizerItem.GetProportion (), int ( Hidden ))


    self.Main_P.Layout ()
    #self.Layout ()

    for i in range ( self.N_Methods  ) :
      Sizer_Item = self.Main_P_box.GetItem ( 2*i+2 )
      print(i, Sizer_Item.GetProportion ())
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class Collapse ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Test of Collapse', ini )

    GUI = """
  self.Main_P  ,PanelVer       ,010
    NN_PanelHor     ,00000
      self.But1     ,wx.Button  ,label='een'
      self.But2     ,wx.Button  ,label='twee'
    self.Main_Splitter   ,MultiSplitterVer
    """

    self.N_Methods = 5
    self.CB      = self.N_Methods * [ None ]
    self.Buttons = self.N_Methods * [ None ]
    self.Split   = self.N_Methods * [ None ]
    self.Log     = self.N_Methods * [ None ]
    self.Help    = self.N_Methods * [ None ]

    for i in range ( self.N_Methods ) :
      GUI += """
      NN_PanelHor        ,001
        Spacer ,6
        self.CB      [%i]  ,wx.CheckBox   ,label=' '
        self.Split  [%i]   ,SplitterHor
          self.Log  [%i]     ,Base_STC
          self.Help [%i]     ,wx.TextCtrl  ,style = wx.NO_BORDER
    """ % ( i, i, i, i )

    GUI += """
    NN_PanelHor     ,00000
      self.But7     ,wx.Button  ,label='een'
    """
    self.wxGUI = Create_wxGUI ( GUI, Ini_File_String = 'self.Ini_File' )

    for i in range ( self.N_Methods ) :
      self.Split  [i].Bind ( wx.EVT_SPLITTER_SASH_POS_CHANGED, self._On_Splitter)

    self._Read_Source ()

  # ********************************************************
  # ********************************************************
  def _Read_Source ( self ) :
    #Filename =
    inspect.getsourcelines ()

  # ********************************************************
  # ********************************************************
  def _On_Splitter ( self, event ) :
    Splitter = event.GetEventObject ()
    if Splitter not in self.Split :
      return

    Index = self.Split.index ( Splitter )
    Pos = self.Split [ Index ].GetSashPosition ()
    for Splitter in self.Split :
      Splitter.SetSashPosition ( Pos )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Thumbnail_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Test of Collapse', ini )

    import wx.lib.agw.thumbnailctrl as TC
    GUI = """
  self.Main_P  ,PanelVer       ,010
    NN_PanelVer  ,10
      self.Thumbs   ,TC.ThumbnailCtrl
      NN_PanelHor     ,00
        self.But1     ,wx.Button  ,label='een'
        self.But2     ,wx.Button  ,label='twee'
    """

    self.wxGUI = Create_wxGUI ( GUI, Ini_File_String = 'self.Ini_File' )
    print(self.wxGUI.code)
    self.But1.Bind ( wx.EVT_BUTTON, self._On )

    Default_Location = 'C:\\D\Data_Python_25\\TO_aggregatie\\html_out\\images'
    Default_Location= "C:\\Users\Mattijs\Pictures"
    #Default_Location = 'D:/Data_Python_25/TO_aggregatie/html_out/images'
    #self.Thumbs.EnableToolTips ()
    self.Thumbs.ShowDir ( Default_Location )
    self.Thumbs.Show ()

  def _On ( self, event ) :
    pass
# ***********************************************************************


# ***********************************************************************
class HL7_View ( My_Frame_Class ):
  def __init__ ( self, ini = None, Msg = 'No HL-7 Message', Title = 'No Title' ) :
    My_Frame_Class.__init__ ( self, None, Title, size=(100,100))

    from tree_support import CT
    style_sub = CT.TR_EDIT_LABELS | CT.TR_HIDE_ROOT
    GUI = """
  self.Main_P  ,SplitterVer
    self.Tree    ,Custom_TreeCtrl_Base    ,style_sub = style_sub
    self.Memo    ,wx.TextCtrl, style = wx.TE_MULTILINE | wx.TE_READONLY
    """
    self.wxGUI = Create_wxGUI ( GUI )
    print(self.wxGUI.code)
# ***********************************************************************


# ***********************************************************************
class Test_CMD ( My_Frame_Class ):
  def __init__ ( self, ini = None, Msg = 'No HL-7 Message', Title = 'No Title' ) :
    My_Frame_Class.__init__ ( self, None, Title, size=(100,100))

    from tree_support import CT
    style_sub = CT.TR_EDIT_LABELS | CT.TR_HIDE_ROOT
    GUI = """
  self.Main_P  ,SplitterVer
    self.Memo1    ,wx.TextCtrl, style = wx.TE_MULTILINE
    self.Memo2    ,wx.TextCtrl, style = wx.TE_MULTILINE
    """
    self.wxGUI = Create_wxGUI ( GUI )
    print(self.wxGUI.code)
# ***********************************************************************


# ***********************************************************************
class Test_IE ( My_Frame_Class ):
  def __init__ ( self, ini = None, Title = 'No Title' ) :
    My_Frame_Class.__init__ ( self, None, Title, size=(600,100))

    GUI = """
  self.Main_P  ,SplitterHor
    self.Memo1    ,wx.TextCtrl, style = wx.TE_MULTILINE
    self.IE       ,iewin.IEHtmlWindow, style = wx.NO_FULL_REPAINT_ON_RESIZE
    """

    self.wxGUI = Create_wxGUI ( GUI )
    #print(self.wxGUI.code)

# self.IE2=iepdf.pdfViewer( Panel2, wx.NewId(), wx.DefaultPosition,
#                             wx.DefaultSize, wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)


    #self.IE.LoadUrl ( 'file://D:/Data_Python_25/Teamsite/MTKF_Documents_Help.html' )
    Filename = 'file://C:/D/Data_Python_25/Web2Py/doc/3_5237282.pdf'
    #NEE Filename = 'D:\\Data_Python_25\Web2Py\doc\3_5237282.pdf'
    #NEE Filename = 'file://D:\\Data_Python_25\Web2Py\doc\3_5237282.pdf'
    self.IE.LoadUrl ( Filename )
    #Filename = 'D:/Data_Python_25/Web2Py/doc/3_5237282.pdf'
    #self.IE2.LoadFile ( Filename )
    #print ( self.IE)
    print ( Filename )

# ***********************************************************************


class GUI_Choice ( wx.Choice ) :
  def __init__ ( self, *args, **kwargs ) :
    wx.Choice.__init__ ( self, *args, **kwargs )
    #print 'args',args
    #print 'kwargs', kwargs
    self.State_Enabled = True
    self.T = wx.TextCtrl ( parent = args[0] )
  def Set_Enable ( self, State ) :
    #print State
    self.State_Enabled = State

# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( -1,-2,-3,-4,5,6,7,8,9,10,11,12 )

  if Test ( 1 ) :
    print('piopp')
    My_Main_Application ( Simple_Test_Form )
    print('hdasdas; ')

  if Test ( 2 ) :
    My_Main_Application ( Test_Dynamic_Form )

  if Test ( 3 ) :
    My_Main_Application ( Test_Brick_BP_Form )

  if Test ( 4 ) :
    My_Main_Application ( Test_Control_Scope )

  if Test ( 5 ) :
    My_Main_Application ( Test_Control_Grid )

  if Test ( 6 ) :
    My_Main_Application ( Test_RVE )

  if Test ( 7 ) :
    My_Main_Application ( Collapse )

  if Test ( 8 ) :
    My_Main_Application ( Collapse )

  if Test ( 9 ) :
    My_Main_Application ( Thumbnail_Form )

  if Test ( 10 ) :
    My_Main_Application ( HL7_View )

  if Test ( 11 ) :
    My_Main_Application ( Test_CMD )

  if Test ( 12 ) :
    My_Main_Application ( Test_IE )

# ***********************************************************************
##pd_Module ( __file__ )
