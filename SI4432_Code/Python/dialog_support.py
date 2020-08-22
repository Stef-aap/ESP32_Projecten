from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from builtins import zip
from builtins import str
from builtins import range
from past.builtins import basestring
from past.utils import old_div
from builtins import object
import __init__

# ***********************************************************************
from language_support import _
from system_support import Run

__doc__ = """
License: freeware, under the terms of the BSD-license
Copyright (C) 2008 Stef Mientki
"""

_Version_Text = [

[ 1.13 , '08-05-2012', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- ListDialog, bug when multi column
"""],

[ 1.12 , '19-11-2011', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Email_Dialog added
"""],

[ 1.11 , '10-11-2011', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- _Multi_List_Dialog, Cancel-Button relaunched the dialog
"""],

[ 1.10 , '03-10-2011', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Calendar dialog, extended with clear
- Calendar dialog, Highlight corrected when coming back to the month
  were the day was selected
"""],

[ 1.9 , '12-7-2011', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- MultiLineDialog, added Color Type
"""],

[ 1.8 , '22-3-2011', 'Gert van Voorst',
'Test Conditions:', (2,),
"""
- Added:
  Message_Exclamation ( title, text ): Show_Message with title and exclamation icon
  Message_Information ( title, text ): Show_Message with title and information icon
  Password_Form ( parent = None, title = 'title', subtitle = 'subtitle' ) : PassWord input, returns actionresult and PassWord
"""],

[ 1.7 , '03-11-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- If the explaining text before a textctrl is "password"
  (case insensitive), a password textctrl is shown.
"""],

[ 1.6 , '19-10-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- @_Wrap_No_GUI wrapper added (allows dialogs without wx.App)
  around: Show_Message, AskYesNo
"""],

[ 1.5 , '25-08-2009', 'Stef Mientki',
'Test Conditions:', (3,),
"""
 - added "Parent" to MultiLineDialog, AskFileForOpen
   to prevent bringing to front main application window.
"""],

[ 1.4 , '11-04-2009', 'Stef Mientki',
'Test Conditions:', (3,),
"""
 - Color_Dialog now alwaays returns None, if canceled
"""],

[ 1.3 , '06-12-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - Multiline dialog, if just 1 preset item, OK-button gets focus
""")],

[ 1.2 , '23-11-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - ColorDialog added
 - Ask_File_For_Save, now also accepts an integer for the filetype
""")],

[ 1.1 , '10-03-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, ' - AskYesNo, now returns True or False')],

[ 1.0 , '09-04-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, ' - orginal release')]
]
# ***********************************************************************


from General_Globals import *
from file_support    import Nice_Path

# ***********************************************************************
# ***********************************************************************
import wx
import os

_Wrap_No_GUI_Active = False

global MLD_LBOOL, MLD_FILE, MLD_PATH, MLD_TextArea
MLD_FILE  = 1
MLD_PATH  = 2
MLD_LBOOL = 3
MLD_TextArea = 4


FT_IMAGE_FILES = 1
FT_ALL_FILES   = 2
FT_DBASE_FILES = 3
FT_PY_FILES    = 4
FT_DOC_FILES   = 5


_FT_IMAGE_FILES =\
   'All Image Files|*.ani;*.bmp;*.cur;*.gif;*.ico;*.iff;'\
                   '*.jp*;*.pcx;*.png;*.pnm;*.tif;*.xpm'\
  '|ANI format|*.ani'\
  '|BMP format|*.bmp'\
  '|CUR format|*.cur'\
  '|GIF format|*.gif'\
  '|ICO format|*.ico'\
  '|IFF format|*.iff'\
  '|JPG format|*.jp*'\
  '|PCX format|*.pcx'\
  '|PNG format|*.png'\
  '|PNM format|*.pnm'\
  '|TIF format|*.tif*'\
  '|XPM format|*.xpm'\
  '|All Files (*.*)|*.*'

_FT_ALL_FILES =\
  'All Files (*.*)|*.*'

_FT_DBASE_FILES =\
  'dBase Files (*.db)|*.db|' \
  'All Files (*.*)|*.*'


_FT_PY_FILES =\
  'Python Files (*.py)|*.py|' \
  'All Files (*.*)|*.*'

_FT_DOC_FILES =\
  'HTML Files (*.html)|*.html|' \
  'Text Files (*.txt)|*.txt|'\
  'PDF Files (*.pdf)|*.pdf|'\
  'Flash Files (*.swf)|*.swf|'\
  'Windows Help Files (*.chm)|*.chm|'\
  'Doc Files (*.doc*)|*.doc*|'\
  'Excel Files (*.xls*)|*.xls*|'\
  'PowerPoint Files (*.ppt*)|*.ppt*|'\
  'All Files (*.*)|*.*'

_FT_Collection = {
  FT_IMAGE_FILES : _FT_IMAGE_FILES,
  FT_ALL_FILES   : _FT_ALL_FILES,
  FT_DBASE_FILES : _FT_DBASE_FILES,
  FT_PY_FILES    : _FT_PY_FILES,
  FT_DOC_FILES   : _FT_DOC_FILES,
  }

# ***********************************************************************
# ***********************************************************************
_Color_Set = []
def Color_Dialog ( Parent = None, Color = None ) :
  ## Doesnt work?!
  #global gui_support_version
  #gui_support_version = globals().get('gui_support_version',None)
  #print gui_support_version#,globals()
  ##import sys

  # for programs like test_dock_hole,
  # you primarely run QT,
  # but you can launch wxPython windows,
  # which require wxColour
  Use_QT = True
  if isinstance ( Color, wx.Colour ) :
    Use_QT = False
  else :
    Use_QT = sys.gui_support_version == 'QT'

  if Use_QT :
    from PySide.QtGui  import QColorDialog,QColor
    Color = QColorDialog.getColor(initial = Color or QColor(), parent = Parent)
    if Color.isValid():
      return Color
    return None
  else:
    colordlg = wx.ColourDialog ( Parent )
    colordlg.GetColourData().SetChooseFull ( True )

    global _Color_Set
    if _Color_Set :
      for i,color in enumerate ( _Color_Set ) :
        colordlg.GetColourData().SetCustomColour ( i, color )

    colordlg.GetColourData().SetColour ( Color )
    Color = None
    if colordlg.ShowModal() == wx.ID_OK:
      Color = colordlg.GetColourData().GetColour()

      _Color_Set = []
      for i in range ( 16 ):
        _Color_Set.append ( colordlg.GetColourData().GetCustomColour (i) )

    colordlg.Destroy()
    return Color
# ***********************************************************************


#_Color_Set = []
# ***********************************************************************
# ***********************************************************************
class  aColor_Dialog (object):
  def __init__(self,*args,**kwargs) :
    self.args   = args
    self.kwargs = kwargs

  def __enter__(self):
    return Color_Dialog(*self.args, **self.kwargs)

  def __exit__(self,*args,**kwargs):
    pass
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def _Wrap_No_GUI_oud ( target ):
  """
  Decorator that creates an wx.App is it's not yet there,
  so wx functions can be used in terminal mode applications.
  The actions that are performed:
    - Create the wx.App, it it doesn't exist
    - run the normal wx-dialog function (or any other wx-form)
    - Kill the application if it was created here
  """
  def wrapper ( *args, **kwargs ) :
    if not ( wx.GetApp () ):
      import threading
      class WaveformThread( threading.Thread ):
        def __init__( self, target,*args, **kwargs ):
          self.args = args
          self.kwargs = kwargs
          self.running = True
          threading.Thread.__init__( self )
        def run( self ):
          app = wx.App()
          #global _dummy_result
          self.result = target(*args,**kwargs)

          app.Destroy()

        def stop( self ):
          self.running = False
      t = WaveformThread(target,*args,**kwargs)
      t.start()
      t.join() # Wait for the thread to end
      result = t.result # Read the result from the thread
    else:
      # perform the called target function
      result = target ( *args, **kwargs )
      #pass

    # return the result to the calling application
    return result

  # ???? don't know what this is for ????
  return wrapper
# ***********************************************************************

_a = None
# ***********************************************************************
# ***********************************************************************
def _Wrap_No_GUI ( target ):
  """
  Decorator that creates an wx.App is it's not yet there,
  so wx functions can be used in terminal mode applications.
  The actions that are performed:
    - Create the wx.App, it it doesn't exist
    - run the normal wx-dialog function (or any other wx-form)
    - Kill the application if it was created here
  """
  def wrapper ( *args, **kwargs ) :
    if not ( wx.GetApp () ):

      print('*** there is NOT an app for that!')
      ##app = wx.App()
      app = wx.App ( False )  ##<<< NO redirection

      ## is this really nescessary?
      ## 3-10-2011, YES !! Robbert + Stef
      global _a
      _a = app


      result = target(*args,**kwargs)
      ##app.MainLoop()
##
##      print '*** there is NOT an app for that!'
##      import threading
##      class WaveformThread( threading.Thread ):
##        def __init__( self, target,*args, **kwargs ):
##          self.args = args
##          self.kwargs = kwargs
##          self.running = True
##          threading.Thread.__init__( self )
##          #self.result = None
##        def run( self ):
##          print '*** creating app'
##          app = wx.App() #App() it's a difference
##          print '*** creating app done.'
##          #global _a
##          #_a = app
##          #global _dummy_result
##          print '*** Calling func'
##
##          self.result = target(*args,**kwargs)
##          print '*** Calling func done.'
##          ## Preserve app ? or not?
##          #app.MainLoop()#Destroy()
##
##          app.Destroy()
##
##        def stop( self ):
##          self.running = False
##      t = WaveformThread(target,*args,**kwargs)
##      t.start()
##      print '*** Thread started'
##
##      from time import sleep
##      #t.join() # Wait for the thread to end
##      #
##      while not 'result' in t.__dict__:
##        print 'piep','result' in t.__dict__
##        sleep(1)
##      global _a
##      #_a.Destroy()
##      #_a = None
##
##      print '*** Thread Ended'
##      result = t.result # Read the result from the thread
##      print '*** read result done.'
    else:
      print('*** there is an app for that!')
      # perform the called target function
      result = target ( *args, **kwargs )
      #pass
    print('done with dialog')
    # return the result to the calling application
    return result


##      print '*** there is NOT an app for that!'
##      import threading
##      class WaveformThread( threading.Thread ):
##        def __init__( self, target,*args, **kwargs ):
##          self.args = args
##          self.kwargs = kwargs
##          self.running = True
##          threading.Thread.__init__( self )
##          #self.result = None
##        def run( self ):
##          print '*** creating app'
##          app = wx.App() #App() it's a difference
##          print '*** creating app done.'
##          global _a
##          _a = app
##          #global _dummy_result
##          print '*** Calling func'
##
##          self.result = target(*args,**kwargs)
##          print '*** Calling func done.'
##          ## Preserve app ? or not?
##          #app.MainLoop()#Destroy()
##          app.Destroy()
##
##        def stop( self ):
##          self.running = False
##      t = WaveformThread(target,*args,**kwargs)
##      t.start()
##      print '*** Thread started'
##
##      from time import sleep
##      t.join() # Wait for the thread to end
##      #
####      while not 'result' in t.__dict__:
####        print 'piep','result' in t.__dict__
####        sleep(1)
####      global _a
##      #_a.Destroy()
##      #_a = None
##
##      print '*** Thread Ended'
##      result = t.result # Read the result from the thread
##      print '*** read result done.'
##    else:
##      print '*** there is an app for that!'
##      # perform the called target function
##      result = target ( *args, **kwargs )
##      #pass
##
##    # return the result to the calling application
##    return result

  # ???? don't know what this is for ????
  return wrapper
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def Show_Message (  text ) :
  dialog = wx.MessageDialog ( None, text, style = wx.OK )
  dialog.ShowModal()
  dialog.Destroy ()
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def Message_Exclamation ( title, text ) :
  dialog = wx.MessageDialog ( None, text, title, wx.OK | wx.ICON_EXCLAMATION )
  dialog.ShowModal ( )
  dialog.Destroy ( )

# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def Message_Information ( title, text ) :
  dialog = wx.MessageDialog ( None, text, title, wx.OK | wx.ICON_INFORMATION )
  dialog.ShowModal ( )
  dialog.Destroy ( )


# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def AskYesNo ( Question = 'Some Question', Title = 'Please answer this question' ) :
  """
  Yes-No Dialog,  returns :
    True   if Yes is pressed
    False  if No  is pressed
  """
  dialog = wx.MessageDialog ( None, Question, Title,
                              wx.YES_NO | wx.ICON_QUESTION)
  answer = dialog.ShowModal() == wx.ID_YES
  dialog.Destroy ()
  return answer
# ***********************************************************************


# ***********************************************************************
# Asks to select a directory
# ***********************************************************************
@_Wrap_No_GUI
def AskDirectory ( DefaultLocation = '', Title = '' ) :
  dialog = wx.DirDialog ( None, Title, defaultPath = DefaultLocation )

  if dialog.ShowModal () == wx.ID_OK:
    File =  dialog.GetPath()
  else:
    File = None

  dialog.Destroy ()
  return File
# ***********************************************************************


# ***********************************************************************
# Asks for 1 file for saving information
# ***********************************************************************
@_Wrap_No_GUI
def Ask_File_For_Save ( DefaultLocation = '', DefaultFile = '',
                        FileTypes = '*.*',    Title = '' ) :

  if isinstance ( FileTypes, int ) :
    FileTypes = _FT_Collection [ FileTypes ]
  dialog = wx.FileDialog ( None, Title,
           defaultDir = DefaultLocation,
           defaultFile = DefaultFile,
           wildcard = FileTypes,
           style = wx.FD_SAVE ,
           )
  if dialog.ShowModal () == wx.ID_OK:
    File =  dialog.GetPath()
  else:
    File = None

  dialog.Destroy ()
  return File
# ***********************************************************************


# ***********************************************************************
# Asks for 1 file to open
#    FileTypes = 'PNG format|*.png'
#                '|BMP format|*.bmp'
#                '|All Files (*.*)|*.*'
# ***********************************************************************
@_Wrap_No_GUI
def AskFileForOpen ( DefaultLocation = '', DefaultFile = '',
                     FileTypes = '*.*', Title = '',
                     Parent = None ) :
  if isinstance ( FileTypes, int ) :
    FileTypes = _FT_Collection [ FileTypes ]
  dialog = wx.FileDialog ( Parent,
           Title,
           defaultDir = DefaultLocation,
           defaultFile = DefaultFile or '',
           wildcard = FileTypes,
           style = wx.FD_OPEN ,
           )
  if dialog.ShowModal () == wx.ID_OK:
    File =  dialog.GetPath()
  else:
    File = None

  dialog.Destroy ()
  return File
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class _Thumbnail_Dialog ( wx.Dialog ):
  def __init__ ( self, Names, Values, Types,
                 Title = 'Edit Values Below',
                 Help = '',
                 width = -1,
                 pos = wx.DefaultPosition,
                 Parent = None ) :
    style = wx.DEFAULT_FRAME_STYLE | \
                    wx.SUNKEN_BORDER | \
                    wx.CLIP_CHILDREN | \
                    wx.STAY_ON_TOP
    #wx.Dialog.__init__( self, None, title = Title,
    width = 300
    wx.Dialog.__init__( self, Parent, title = Title,
                        size = ( width, 500 ),
                        pos = pos,
                        style = style )

    Help = """dasdjasd  das]\n adsdasdasamsdn sdna ndna dnasnd ad asdna dasn amsnd as"""
    if Help:
      help = wx.StaticText ( self, -1, Help )

    # be sure we have enough values
    #while len(Values) < len (Names) : Values.append ( '' )
    #while len(Types)  < len (Names) : Types.append ( None )
    #self.Values = Values
    #self.Types = Types
    #self.T = []

    Default_Location = r'D:/Data_Python_25/TO_aggregatie/html_out/images'

    import wx.lib.agw.thumbnailctrl as TC
    self.Thumbs = TC.ThumbnailCtrl ( self )
    self.Thumbs.EnableToolTips ()
    self.Thumbs.ShowDir ( Default_Location )
    self.Thumbs.Show ()

    Buttons = wx.StdDialogButtonSizer ()
    Button_OK = wx.Button ( self, wx.ID_OK )
    Buttons.AddButton ( Button_OK )
    Buttons.AddButton ( wx.Button ( self, wx.ID_CANCEL ) )
    Buttons.Realize()

    Sizer = wx.BoxSizer ( wx.VERTICAL )
    if Help:
      Sizer.Add ( help, 0, wx.ALL, 5 )
      Sizer.Add ( wx.StaticLine ( self ), 0, wx.EXPAND | wx.ALL, 5)
    Sizer.Add ( self.Thumbs, 0, wx.EXPAND | wx.ALL, 10 )
    Sizer.Add ( Buttons, 0, wx.EXPAND | wx.ALL, 10 )
    self.SetSizer ( Sizer )
    Sizer.Fit ( self )

    # if just 1 element with a preset value
    # than give ok_button focus
    # (specially for search dialog)
    if ( len ( Names ) == 1 ) and \
       isinstance ( self.T[0], wx.TextCtrl ) and \
       ( self.T[0].GetValue () ) :
      Button_OK.SetFocus ()

  # **********************************************************************
  # **********************************************************************
  def OnButton ( self, event ) :
    ID = event.GetId()
    if self.Types[ID] == MLD_FILE :
      filepath, filename = path_split ( self.T[ID].GetValue() )
      filename= AskFileForOpen ( filepath, filename )
    elif self.Types[ID] == MLD_PATH :
      filename= AskDirectory ( self.T[ID].GetValue() )
    if filename: self.T[ID].SetValue ( filename )
    '''
    import wx.lib.agw.thumbnailctrl as TC
    self.Thumbs = TC.ThumbnailCtrl ( Parent )

    """
    Sizer = wx.BoxSizer ( wx.VERTICAL )
    if Help:
      Sizer.Add ( help, 0, wx.ALL, 5 )
      Sizer.Add ( wx.StaticLine ( self ), 0, wx.EXPAND | wx.ALL, 5)
    Sizer.Add ( grid, 0, wx.EXPAND | wx.ALL, 10 )
    Sizer.Add ( Buttons, 0, wx.EXPAND | wx.ALL, 10 )
    self.SetSizer ( Sizer )
    Sizer.Fit ( self )
    """

    self.Thumbs.EnableToolTips ()
    self.Thumbs.ShowDir ( Default_Location )
    self.Thumbs.Show ()
    '''
  # **********************************************************************
  # **********************************************************************
  def ShowModal ( self ) :
    Default_Location = r'D:/Data_Python_25/TO_aggregatie/html_out/images'
    self.Thumbs.EnableToolTips ()
    self.Thumbs.ShowDir ( Default_Location )
    self.Thumbs.Show ()

    if wx.Dialog.ShowModal ( self ) == wx.ID_OK:
      result = []
      for item in self.T:
        result.append ( item.GetValue () )
      return True, result
    else:
      return False #, self.Values

  # **********************************************************************
  # **********************************************************************
  def ShowModal ( self ) :
    if wx.Dialog.ShowModal ( self ) == wx.ID_OK:
      result = []
      for item in self.T:
        result.append ( item.GetValue () )
      return True, result
    else:
      return False, self.Values

'''
def Ask_Image_File_For_Open ( Default_Location = '',
                              DefaultFile = '',
                              Title = '',
                              Parent = None ) :
'''
@_Wrap_No_GUI
def Ask_Image_File_For_Open ( Names = [''], Values = [''], Types = [],
                      Title = 'Unknown Title',
                      HelpText = None,
                      width = -1,
                      pos = wx.DefaultPosition,
                      Parent = None ):
  """
  If the Parent is not specified,
  the main window will come to the front !
  """
  #dlg = _Thumbnail_Dialog ( Default_Location, Parent )
  dlg = _Thumbnail_Dialog ( Names, Values, Types, Title, HelpText, width, pos, Parent )
  OK, Values = dlg.ShowModal()
  dlg.Destroy()
  return OK, Values


# ***********************************************************************

# ***********************************************************************
# Same as AskFileForOpen, but can open multi files
# ***********************************************************************
def AskFilesForOpen ( DefaultLocation = '', DefaultFile = '',
                     FileTypes = '*.*', Title = '' ) :

  dialog = wx.FileDialog ( None, Title,
           defaultDir = DefaultLocation,
           defaultFile = DefaultFile,
           wildcard = FileTypes,
           style = wx.FD_OPEN | wx.FD_MULTIPLE,
           )

  if dialog.ShowModal () == wx.ID_OK:
    Files = dialog.GetFilenames ()
    Path = dialog.GetPath ()
  else:
    Files = None
    Path = None

  dialog.Destroy ()
  return Files, Path
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class _MultiLineDialog ( wx.Dialog ):
  def __init__ ( self, Names = None, Values = [], Types = [],
                 Title = 'Edit Values Below',
                 Help = '',
                 width = -1,
                 pos = wx.DefaultPosition,
                 Parent = None ) :
    #import _images
    style = wx.DEFAULT_FRAME_STYLE | \
                    wx.SUNKEN_BORDER | \
                    wx.CLIP_CHILDREN | \
                    wx.STAY_ON_TOP
    #wx.Dialog.__init__( self, None, title = Title,
    wx.Dialog.__init__( self, Parent, title = Title,
                        size = ( width, -1 ),
                        pos = pos,
                        style = style )
    self.IDs = {}
    self.Types = Types

    if Help:
      help = wx.StaticText ( self, -1, Help )

    if width == -1 : S =  ( 400   ,24 )
    else :           S =  ( width ,24 )

    if Names is None :
      Names = ['']

    # be sure we have enough values
    while len(Values) < len (Names) : Values.append ( '' )
    #while len(Types)  < len (Names) : Types.append ( None )
    while len(Types)  < len (Names) : Types.append ( str )
    self.Values = Values
    self.Types = Types
    self.T = []
    grid = wx.FlexGridSizer ( len(Names), 3, 10, 10 )
    for i, item in enumerate ( Names ) :

      if   Types[i] == bool :
        B = wx.StaticText ( self, -1, Names[i]  )
        grid.Add ( B, flag = wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL )
        self.T.append ( wx.CheckBox ( self, -1, '' ) )
        self.T[i].SetValue ( bool ( self.Values[i] ) )
        grid.Add ( self.T[i], 0, wx.ALIGN_LEFT | wx.ALL, 0)
        grid.Add ( wx.StaticText ( self, -1, ''  ) )

      elif Types[i] == MLD_LBOOL  :
        B = wx.StaticText ( self, -1, ''  )
        grid.Add ( B, flag = wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL )
        self.T.append ( wx.CheckBox ( self, -1,  Names[i]  ) )
        self.T[i].SetValue ( bool ( self.Values[i] ) )
        grid.Add ( self.T[i], 0, wx.ALIGN_LEFT | wx.ALL, 0)
        grid.Add ( wx.StaticText ( self, -1, '' ) )

      elif Types[i] in ( wx.Colour, wx.Colour )  :
        B = wx.StaticText ( self, -1, Names[i]  )
        grid.Add ( B, flag = wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL )

        self.T.append ( wx.TextCtrl   ( self, -1, str(self.Values[i]), size = S ))
        grid.Add ( self.T[i], flag = wx.EXPAND )
        self.T[-1].SetBackgroundColour ( self.Values[i] )
        self.T[-1].Bind ( wx.EVT_LEFT_DOWN, self._On_Color ) #, id=i )
        self.IDs [ self.T[-1].GetId () ] = self.T[-1]
        grid.Add ( wx.StaticText ( self, -1, '' ) )


      elif Types[i] == MLD_TextArea  :
        B = wx.StaticText ( self, -1, Names[i]  )
        grid.Add ( B, flag = wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL )
        if not ( isinstance ( self.Values[i], basestring ) ) :
          self.Values[i] = str ( self.Values [i] )
        Style = wx.TE_MULTILINE | wx.TE_PROCESS_ENTER   ##wx.WANTS_CHARS
        S2 = ( S[0], 100 )
        self.T.append ( wx.TextCtrl   ( self, -1, self.Values[i], size = S2,
                                        style = Style ))
        grid.Add ( self.T[i], flag = wx.EXPAND )
        grid.Add ( wx.StaticText ( self, -1, ''  ) )

      else :
        B = wx.StaticText ( self, -1, Names[i]  )
        grid.Add ( B, flag = wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL )
        #if type ( self.Values[i] ) != basestring :
        if not ( isinstance ( self.Values[i], basestring ) ) :
          self.Values[i] = str ( self.Values [i] )
        ##if width == -1 : S = (400,24)
        ##else :           S = (width,24)
        if 'password' in Names[i].lower() :
          self.T.append ( wx.TextCtrl   ( self, -1, self.Values[i], size = S,
                          style=wx.TE_PASSWORD ))
        else :
          self.T.append ( wx.TextCtrl   ( self, -1, self.Values[i], size = S ))
        grid.Add ( self.T[i], flag = wx.EXPAND )

        if Types[i] == MLD_FILE :
          bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON, (16,16))
          B = wx.BitmapButton ( self, i ,bmp)
          grid.Add ( B, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
          self.Bind ( wx.EVT_BUTTON, self.OnButton, id=i )

        elif Types[i] == MLD_PATH :
          bmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_BUTTON, (16,16))
          B = wx.BitmapButton ( self, i ,bmp)
          grid.Add ( B, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
          self.Bind ( wx.EVT_BUTTON, self.OnButton, id=i )

        else:
          grid.Add ( wx.StaticText ( self, -1, ''  ) )
    grid.AddGrowableCol ( 1 )

    Buttons = wx.StdDialogButtonSizer ()
    Button_OK = wx.Button ( self, wx.ID_OK )
    Buttons.AddButton ( Button_OK )
    Buttons.AddButton ( wx.Button ( self, wx.ID_CANCEL ) )
    Buttons.Realize()

    Sizer = wx.BoxSizer ( wx.VERTICAL )
    if Help:
      Sizer.Add ( help, 0, wx.ALL, 5 )
      Sizer.Add ( wx.StaticLine ( self ), 0, wx.EXPAND | wx.ALL, 5)
    Sizer.Add ( grid, 0, wx.EXPAND | wx.ALL, 10 )
    Sizer.Add ( Buttons, 0, wx.EXPAND | wx.ALL, 10 )
    self.SetSizer ( Sizer )
    Sizer.Fit ( self )

    # if just 1 element with a preset value
    # than give ok_button focus
    # (specially for search dialog)
    if ( len ( Names ) == 1 ) and \
       isinstance ( self.T[0], wx.TextCtrl ) and \
       ( self.T[0].GetValue () ) :
      Button_OK.SetFocus ()
  # **********************************************************************
  # **********************************************************************
  def ShowModal ( self ) :
    if wx.Dialog.ShowModal ( self ) == wx.ID_OK:
      result = []
      for i, item in enumerate ( self.T ):
        if self.Types[i] in ( wx.Colour, )  :
          result.append ( wx.Colour ( *eval ( item.GetValue () )))
        else :
          result.append ( item.GetValue () )
      return True, result
    else:
      return False, self.Values

  # **********************************************************************
  # **********************************************************************
  def _On_Color ( self, event ) :
    ID = event.GetId()
    Ctrl = self.IDs [ ID ]
    Color = Color_Dialog ( self, wx.Colour ( *eval ( Ctrl.GetValue ())))
    if Color :
      Ctrl.SetValue ( str( Color ))
      Ctrl.SetBackgroundColour ( Color )

  # **********************************************************************
  # **********************************************************************
  def OnButton ( self, event ) :
    ID = event.GetId()
    if self.Types[ID] == MLD_FILE :
      filepath, filename = path_split ( self.T[ID].GetValue() )
      filename= AskFileForOpen ( filepath, filename )
    elif self.Types[ID] == MLD_PATH :
      filename= AskDirectory ( self.T[ID].GetValue() )
    if filename: self.T[ID].SetValue ( filename )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def MultiLineDialog ( Names = [''], Values = [''], Types = [],
                      Title = 'Unknown Title',
                      HelpText = None,
                      width = -1,
                      pos = wx.DefaultPosition,
                      Parent = None ):
  """
  If the Parent is not specified,
  the main window will come to the front !
  """
  dlg = _MultiLineDialog ( Names, Values, Types, Title, HelpText, width, pos, Parent )
  OK, Values = dlg.ShowModal()
  dlg.Destroy()
  return OK, Values
# ***********************************************************************




# ***********************************************************************
# ***********************************************************************
class _Password_Form ( wx.Dialog ) :
  def __init__ ( self, parent = None, title = 'title', subtitle = 'subtitle') :

    Style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
    #Style ^= wx.CLOSE_BOX
    Style ^= wx.SYSTEM_MENU
    wx.Dialog.__init__ ( self, None, title = title,
                         size = ( 300, 200 ),
                         style = Style )

    Font = wx.Font ( 10, wx.SWISS, wx.NORMAL, wx.NORMAL )
    self.SetFont( Font )
    self.PassWord = ""

    GUIpw = """
    PW1                   ,PanelVer  ,0
      NN_PanelHor, 010
        PVR1             ,PanelVer  ,0
          Spacer, 10
        PVR2             ,PanelVer  ,000000
          Spacer ,20
          Label_Subtitle  ,wx.StaticText  ,label='Wachtwoord ', size=(250, -1)
          Spacer ,5
          Edit_Password ,wx.TextCtrl, -1, "", size=(125, -1), style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER
          Spacer ,30
          NN_PanelHor, 000
            Knop_OK                 ,wx.Button, label='Ok'
            Spacer ,10
            Knop_Cancel             ,wx.Button, label='Annuleren'
        PVR3             ,PanelVer  ,0
          Spacer, 10
    """

    # TODO TODO from gui_support import *
    self.wxGUI = Create_wxGUI ( GUIpw )
    Edit_Password.Bind ( wx.EVT_TEXT_ENTER, self._On_PasswordEnter )
    Knop_OK.Bind ( wx.EVT_BUTTON, self._On_KnopOK )
    Knop_Cancel.Bind ( wx.EVT_BUTTON, self._On_KnopCancel )
    Label_Subtitle.SetLabel ( subtitle )

    #Vaste instellingen programmavenster
    self.SetDimensions ( -1, -1, 300, 200 )
    self.Center ()

  # ****************************************************************
  def _On_PasswordEnter ( self, event ) :
    self.EndModal ( wx.ID_OK )

  # ****************************************************************
  def _On_KnopOK ( self, event ) :
    self.EndModal ( wx.ID_OK )

  # ****************************************************************
  def _On_KnopCancel ( self, event ) :
    self.EndModal ( wx.ID_CANCEL )

  # **********************************************************************
  def ShowModal ( self ) :
    if wx.Dialog.ShowModal ( self ) == wx.ID_OK:
      return True, Edit_Password.GetValue ()
    else:
      return False, ""
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def Password_Form ( parent = None, title = 'Password', subtitle = 'Password' ) :
  dlg = _Password_Form ( parent, title, subtitle )
  actionresult, PassWord = dlg.ShowModal ( )
  dlg.Destroy ( )
  return actionresult, PassWord

# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
import  wx.lib.mixins.listctrl  as  listmix
class _ExtraListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
# ***********************************************************************



@_Wrap_No_GUI
def saveSnapshot(dcSource,Filename):
    # based largely on code posted to wxpython-users by Andrea Gavana 2006-11-08
    size = dcSource.Size

    # Create a Bitmap that will later on hold the screenshot image
    # Note that the Bitmap must have a size big enough to hold the screenshot
    # -1 means using the current default colour depth
    #bmp = wx.EmptyBitmap(size.width, size.height)
    bmp = wx.Bitmap(size.width, size.height)

    # Create a memory DC that will be used for actually taking the screenshot
    memDC = wx.MemoryDC()

    # Tell the memory DC to use our Bitmap
    # all drawing action on the memory DC will go to the Bitmap now
    memDC.SelectObject(bmp)

    # Blit (in this case copy) the actual screen on the memory DC
    # and thus the Bitmap
    memDC.Blit( 0, # Copy to this X coordinate
        0, # Copy to this Y coordinate
        size.width, # Copy this width
        size.height, # Copy this height
        dcSource, # From where do we copy?
        0, # What's the X offset in the original DC?
        0  # What's the Y offset in the original DC?
        )

    # Select the Bitmap out of the memory DC by selecting a new
    # uninitialized Bitmap
    memDC.SelectObject(wx.NullBitmap)

    img = bmp.ConvertToImage()
    img.SaveFile(Filename, wx.BITMAP_TYPE_PNG)



# ***********************************************************************
# ***********************************************************************
class _ListDialog ( wx.Dialog ):
  def __init__ ( self, List_Values,
                 Title = 'Edit Values Below',
                 Help = '',
                 size = ( -1, -1 ),
                 pos = wx.DefaultPosition ) :
    style = wx.DEFAULT_FRAME_STYLE | \
                    wx.SUNKEN_BORDER | \
                    wx.CLIP_CHILDREN | \
                    wx.STAY_ON_TOP
    #print '\\\\\\\\\\\\\\\\\\\width',width
    self._Size_Not_Working = size

    wx.Dialog.__init__( self, None, title = Title,
##                        size = ( width, -1 ),
                        pos = pos,
                        style = style )

    if Help:
      help = wx.StaticText ( self, -1, Help )

    #self.List = wx.ListCtrl(self, -1,
    self.List = _ExtraListCtrl(self, -1,
                             style=wx.LC_REPORT
                             #| wx.BORDER_SUNKEN
                             | wx.BORDER_NONE
                             | wx.LC_EDIT_LABELS
                             #| wx.LC_SORT_ASCENDING   ## << gives problems
                             #| wx.LC_NO_HEADER
                             #| wx.LC_VRULES
                             #| wx.LC_HRULES
                             #| wx.LC_SINGLE_SEL
                             )
    # fill the list, first test of it has just 1 column
    if isinstance ( List_Values[0], basestring ) :
      self.List.InsertColumn ( 0, List_Values[0] )
      for item in List_Values [1:] :
        self.List.Append ( ( item, ) )
    else :
      for i,cols in enumerate ( List_Values [0] ) :
        self.List.InsertColumn ( i, cols )
      for item in List_Values [1:] :
        self.List.Append ( item )

    Buttons = wx.StdDialogButtonSizer ()
    Buttons.AddButton ( wx.Button ( self, wx.ID_OK ) )
    Buttons.AddButton ( wx.Button ( self, wx.ID_CANCEL ) )
    Buttons.Realize()

    Sizer = wx.BoxSizer ( wx.VERTICAL )
    if Help:
      Sizer.Add ( help, 0, wx.ALL, 5 )
      Sizer.Add ( wx.StaticLine ( self ), 0, wx.EXPAND | wx.ALL, 5)
    Sizer.Add ( self.List, 1, wx.EXPAND | wx.ALL, 10 )
    Sizer.Add ( Buttons, 0, wx.EXPAND | wx.ALL, 10 )
    self.SetSizer ( Sizer )
    Sizer.Fit ( self )

    # Doubleclick or ENTER will also select and end the modal dialog
    self.List.Bind ( wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated )

  # **********************************************************************
  # **********************************************************************
  def ShowModal ( self ) :
    self.SetSize ( self._Size_Not_Working )
    if wx.Dialog.ShowModal ( self ) == wx.ID_OK:
      item = self.List.GetFirstSelected()
      if item >= 0 :
        return True, self.List.GetItemText(item)
    return False, None

  # **********************************************************************
  # Doubleclick or ENTER will also select and end the modal dialog
  # **********************************************************************
  def OnItemActivated ( self, event ) :
    print('Active')
    self.EndModal ( wx.ID_OK )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def ListDialog ( List_Values, Title,
                      HelpText = None,
                      size = ( -1, -1 ),
                      pos = wx.DefaultPosition ):
  dlg = _ListDialog ( List_Values, Title, HelpText, size, pos )
  OK, Values = dlg.ShowModal()
  dlg.Destroy()
  return OK, Values
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class _Multi_List_Dialog ( wx.Dialog ):
  def __init__ ( self, Lists,
                 Title = 'Edit Values Below',
                 size = ( -1, -1 ),
                 pos = wx.DefaultPosition ) :

    style = wx.DEFAULT_FRAME_STYLE | \
                    wx.SUNKEN_BORDER | \
                    wx.CLIP_CHILDREN | \
                    wx.STAY_ON_TOP
    wx.Dialog.__init__( self, None, title = Title,
                        size  = size,
                        pos   = pos,
                        style = style )
    GUI = """
    Splitter   ,SplitterVer
      NN_PanelHor  ,11
    """
    self.N_List = len ( Lists )
    self.RB = self.N_List * [ None ]

    for i in range ( self.N_List ) :
      GUI += """
        self.RB[%s] ,wx.RadioBox ,label='%s'  ,size=(300,-1) ,choices = %s ,majorDimension=1  ,style=wx.NO_BORDER
      """ % ( i, Lists[i][0], Lists[i][1:] )
    GUI += """
      NN_PanelHor  ,100
        self.Edit    ,wx.TextCtrl
        NN_wx.Button  ,wx.ID_CANCEL   ,label = 'Cancel'
        NN_wx.Button  ,wx.ID_OK       ,label = 'Ok'
    """
    from gui_support import Create_wxGUI, BmpBut, HorSpacer
    self.wxGUI = Create_wxGUI ( GUI )
    Splitter.SetSashPosition ( -24 )

    for i in range ( self.N_List ) :
      self.RB[i].Bind ( wx.EVT_RADIOBOX, self._On_RadioBox )

    self._On_RadioBox ()

  # **********************************************************************
  # **********************************************************************
  def _On_RadioBox ( self, event = None ) :
    Line = ''
    for i in range ( self.N_List ) :
      Line += self.RB[i].GetStringSelection () + ' // '
    self.Edit.SetLabel( Line )

  # **********************************************************************
  # **********************************************************************
  def ShowModal ( self ) :
    #self.SetSize ( self._Size_Not_Working )
    dlg = wx.Dialog.ShowModal ( self )
    if dlg == wx.ID_OK:
      Answers = []
      Strings = []
      for i in range ( self.N_List ) :
        Answers.append ( self.RB[i].GetSelection () )
        Strings.append ( self.RB[i].GetStringSelection () )
      return True, Answers, Strings
    elif dlg == wx.ID_CANCEL:
      Answers = []
      Strings = []
      return False, Answers, Strings
    """
    if wx.Dialog.ShowModal ( self ) == wx.ID_OK:
      print '_Multi_List_Dialog?????111'
      Answers = []
      Strings = []
      for i in range ( self.N_List ) :
        Answers.append ( self.RB[i].GetSelection () )
        Strings.append ( self.RB[i].GetStringSelection () )
      return True, Answers, Strings
    elif wx.Dialog.ShowModal ( self ) == wx.ID_CANCEL:
      print '_Multi_List_Dialog?????222'
      Answers = []
      Strings = []
      return False, Answers, Strings
    else :
      print '_Multi_List_Dialog?????333'
    #return False, None
    """

  # **********************************************************************
  # Doubleclick or ENTER will also select and end the modal dialog
  # **********************************************************************
  def OnItemActivated ( self, event ) :
    print('Active')
    self.EndModal ( wx.ID_OK )
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def Multi_List_Dialog ( Lists, Title = '',
                       size = ( -1, -1 ),
                       pos = wx.DefaultPosition ):
  dlg = _Multi_List_Dialog ( Lists, Title, size, pos )
  OK = dlg.ShowModal()
  dlg.Destroy()
  return OK
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class _Multi_CheckList_Dialog ( wx.Dialog ):
  def __init__ ( self, Names, Values,
                 Title = 'Edit Values Below',
                 size = ( -1, -1 ),
                 pos = wx.DefaultPosition ) :

    style = wx.DEFAULT_FRAME_STYLE | \
                    wx.SUNKEN_BORDER | \
                    wx.CLIP_CHILDREN | \
                    wx.STAY_ON_TOP
    wx.Dialog.__init__( self, None, title = Title,
                        size  = size,
                        pos   = pos,
                        style = style )
    GUI = """
    main, PanelVer  ,10
      NN_PanelHor  ,11
        NN_PanelVer  ,00000000000000000000000000000000000000000000000000000000
          Spacer  ,10
    """

    self.N_List = len ( Names [0] )
    self.CB1 = self.N_List * [ None ]
    for i in range ( self.N_List ) :
      GUI += """
          self.CB1[%s] ,wx.CheckBox ,label = '%s'
          Spacer  ,10
      """ % ( i, Names[0][i] )

    GUI += """
        NN_PanelVer  ,00000000000000000000000000000000000000000000000000000000
          Spacer  ,10
    """

    self.N_List = len ( Names [1] )
    self.CB2 = self.N_List * [ None ]
    for i in range ( self.N_List ) :
      GUI += """
          self.CB2[%s] ,wx.CheckBox ,label = '%s'
          Spacer  ,10
      """ % ( i, Names[1][i] )


    GUI += """
      NN_PanelHor  ,0000000
        Spacer  ,20
        NN_wx.Button  ,wx.ID_CANCEL   ,label = 'Cancel'
        NN_wx.Button  ,wx.ID_OK       ,label = 'Ok'
    """
    from gui_support import Create_wxGUI, BmpBut, HorSpacer, Spacer
    self.wxGUI = Create_wxGUI ( GUI )
    ##print 'gdashgdasds', self.wxGUI.code
    ##print Names
    ##print Values
    ##print self.CB1
    ##print self.CB2

    for CB, Value in zip ( self.CB1, Values [0] ) :
      CB.SetValue ( bool ( Value ) )
    for CB, Value in zip ( self.CB2, Values [1] ) :
      CB.SetValue ( bool ( Value ) )

  # **********************************************************************
  # **********************************************************************
  def ShowModal ( self ) :
    #self.SetSize ( self._Size_Not_Working )
    if wx.Dialog.ShowModal ( self ) == wx.ID_OK:
      Answers = [ [], [] ]
      for CB in self.CB1 :
        Answers [0].append ( CB.GetValue ())
      for CB in self.CB2 :
        Answers [1].append ( CB.GetValue ())

      return True, Answers
    else :
      return False, []
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def Multi_CheckList_Dialog ( Names, Values, Title = '',
                       size = ( -1, -1 ),
                       pos = wx.DefaultPosition ):
  dlg = _Multi_CheckList_Dialog ( Names, Values, Title, size, pos )
  OK, Values = dlg.ShowModal()
  dlg.Destroy()
  return OK, Values
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def DropDown_List_Dialog ( Parent,
                           CallBack,
                           Lists,
                           Title = '',
                           MaxLen = 10,
                           size = ( -1, -1 ),
                           pos  = wx.DefaultPosition ):
  """
Depending on the number of Lists and
the number of items in the Lists,
either a drop-down is showed or a modal dialog.

Selected values are always returned through the function CallBack.

The first element of each list is used as the Radiobox header
or ignored if a dropdown is created.
  """
  # be sure we have a list of lists
  if not Iterable ( Lists[0] ) :
    Lists = [ Lists ]

  N_Lists = len ( Lists )
  if N_Lists == 1 :
    DropDown = True
  elif N_Lists == 2 :
    DropDown = ((len(Lists[0])-1) * (len (Lists[1])-1)) <= MaxLen
  else :
    DropDown = False

  if DropDown :
    Items = []
    if N_Lists == 1 :
      Items = Lists [0][1:]
    else :
      for First in Lists [0][1:] :
        for Second in Lists [1][1:] :
          Items.append ( First + ' / ' + Second )

    # *********************************************************
    def _OnPopup ( event ) :
      ID = event.Int
      Select = Items [ ID ].split ( ' / ')
      CallBack ( [ID], Select )

    from menu_support import My_Popup_Menu
    Popup_Menu = My_Popup_Menu ( _OnPopup, None, pre = Items )
    Parent.PopupMenu ( Popup_Menu )

  # Modal Dialog
  else :
    dlg = _Multi_List_Dialog ( Lists, Title, size, pos )
    OK = dlg.ShowModal()
    OK, Values, Strings = OK
    dlg.Destroy ()
    if OK :
      CallBack ( Values, Strings )


# ***********************************************************************



try:
  import ctypes as ct

  My_Path = os.path.split ( __file__ )[0]
  MimeTex = Nice_Path ( My_Path, 'MimeTex.dll' )
  print(MimeTex)
  MimeTexDLL = ct.CDLL(MimeTex)
  getattr(MimeTexDLL, 'CreateGifFromEq')


except:
  print('Error, reverting to normal Mimetex')
  MimeTexDLL = None


# ***********************************************************************
# ***********************************************************************
class _Formula_Dialog ( wx.Dialog ):
  def __init__ ( self, Formula, Filename, Size, Parent ) :
    self.Filename  = Filename
    self.Font_Size = Size

    style = wx.DEFAULT_FRAME_STYLE | \
                    wx.SUNKEN_BORDER | \
                    wx.CLIP_CHILDREN | \
                    wx.STAY_ON_TOP
    #wx.Dialog.__init__( self, Parent, title = 'Formula Editor',
    wx.Dialog.__init__( self, Parent, title = Filename,
                        style = style )

    from gui_support import Create_wxGUI # TODO TODO 3
    GUI = """
    self.aap, PanelVer, 10
      self.SplitVer   ,SplitterVer
        self.Edit       ,wx.TextCtrl       ,style=wx.TE_MULTILINE
        self.Panel_Picture ,PanelVer,100
          self.Picture    ,wx.StaticBitmap
      NN_PanelVer, 00
        NN_PanelHor  ,00
            Button_OK           ,wx.Button, wx.ID_OK    , label = 'OK'
            Button_Cancel       ,wx.Button, wx.ID_CANCEL, label = 'Cancel'
            HorSpacer
            NN_wx.StaticText    ,label = 'Size: '
            self.Spin_Size      ,wx.SpinCtrl ,style=wx.SP_VERTICAL, size=(50,-1), min=0, max=7

    """
    from gui_support import Create_wxGUI
    Create_wxGUI ( GUI )
    self.Edit.SetValue ( Formula )

    wx.CallLater( 400, self.SplitVer.SetSashPosition, 100 )

    self.Edit.Bind ( wx.EVT_TEXT, self._Redraw_Image )
    self.Spin_Size.Bind ( wx.EVT_SPINCTRL, self._Redraw_Image )
    self.Spin_Size.SetValue ( self.Font_Size )

    wx.CallLater( 500, self._Redraw_Image  )

  # **********************************************************************
  # **********************************************************************
  def _Redraw_Image ( self, event = None ):
    Size_String = [ r'\tiny', r'\small', r'\normalsize', r'\large', r'\Large',
                    r'\LARGE', r'\huge', r'\HUGE' ]
    if event :
      event.Skip ()
    Formula = self.Edit.GetValue ()
    Formula = Formula.replace ( r'\n', r'\\' )
    Size    = self.Spin_Size.GetValue ()
    Formula = Size_String [ Size ] + ' ' + Formula


    if MimeTexDLL:
      Formula = str(Formula)

      print('Formula', Formula, self.Filename, repr(Formula))
      MimeTexDLL.CreateGifFromEq(Formula, str(self.Filename))
    else:
      My_Path = os.path.split ( __file__ )[0]
      MimeTex = Nice_Path ( My_Path, 'mimetex.exe' )
      Process = Run ( [ MimeTex, Formula, '-e',
                                  self.Filename, '-s', '7'],show='hidden' )
      #add -o for white background
      Process.wait ()

    from file_support import File_Exists
    if File_Exists ( self.Filename ) :
      Bmp = wx.Bitmap ( self.Filename )
      self.Picture.SetBitmap ( Bmp )
      self.Panel_Picture.Refresh ()

  # **********************************************************************
  # **********************************************************************
  def ShowModal ( self ) :
    Result = wx.Dialog.ShowModal ( self ) == wx.ID_OK
    return Result, self.Edit.GetValue (), self.Spin_Size.GetValue ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def Formula_Dialog ( Formula, Filename, Size = 2, Parent = None ) :
  """
  If the Parent is not specified,
  the main window will come to the front !
  """
  dlg = _Formula_Dialog ( Formula, Filename, Size, Parent )
  OK, Formula, Size = dlg.ShowModal()
  dlg.Destroy()
  #Formula = Formula.replace ( '\f', '\\f' )
  return OK, Formula, Size
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class _Log_Dialog ( wx.Dialog ):
  def __init__ ( self, Parent = None, Title = 'Modal Log') :
    style = wx.DEFAULT_FRAME_STYLE | \
                    wx.SUNKEN_BORDER | \
                    wx.CLIP_CHILDREN | \
                    wx.STAY_ON_TOP
    wx.Dialog.__init__( self, Parent, title = Title,
                        style = style )

    from gui_support import Create_wxGUI # * TODO TODO TODO
    GUI = """
    Main           ,PanelVer, 10
      self.Log       ,wx.TextCtrl       ,style=wx.TE_MULTILINE
      NN_PanelHor    ,000
        Button_Print    ,wx.Button,               label = 'Print'
        Button_Cancel   ,wx.Button, wx.ID_CANCEL, label = 'Cancel'
        Button_OK       ,wx.Button, wx.ID_OK    , label = 'OK'
    """
    from gui_support import Create_wxGUI
    Create_wxGUI ( GUI )


  # **********************************************************************
  def ShowModal ( self ) :
    Result = wx.Dialog.ShowModal ( self ) == wx.ID_OK
    #return Result, self.Edit.GetValue (), self.Spin_Size.GetValue ()

  # **********************************************************************
  def Append_Text ( self, Text ) :
    self.Log.AppendText ( Text+ '\n' )

  # **********************************************************************
  def Close_Form ( self ) :
    self.EndModal ( wx.ID_OK )
# ***********************************************************************
@_Wrap_No_GUI
def Test_Modal_Log () :
  def Write () :
    dlg.Append_Text ( 'regel tekst')
    dlg.Append_Text ( 'regel tekst')
  def Kill () :
    print('Finish')
    dlg.Close_Form ()
    dlg.Destroy ()
  dlg = _Log_Dialog ( Title = 'Rapport generator log')
  wx.CallLater ( 1000, Write )
  wx.CallLater ( 4000, Kill )
  dlg.ShowModal()



# ***********************************************************************
# ***********************************************************************
#class _Screen_Capture ( wx.Frame ) :
class _Screen_Capture ( wx.Dialog ) :

  def __init__(self, Filename, parent = None ) :
    self.Filename = Filename
    self.c1 = None
    self.c2 = None
    wx.Dialog.__init__( self, parent, -1, '', size=wx.DisplaySize(),
                       style = wx.SYSTEM_MENU | wx.FRAME_NO_TASKBAR | wx.NO_BORDER    )

    self.panel = wx.Panel (self, size=self.GetSize () )
    self.SetTransparent ( 50 )

    self.panel.Bind ( wx.EVT_LEFT_DOWN, self.OnMouseDown )
    self.panel.Bind ( wx.EVT_MOTION   , self.OnMouseMove )
    self.panel.Bind ( wx.EVT_LEFT_UP  , self.OnMouseUp   )
    self.panel.Bind ( wx.EVT_PAINT    , self.OnPaint     )

    self.SetCursor ( wx.StockCursor ( wx.CURSOR_CROSS ) )
    self.Show ()

  def OnMouseDown ( self, event ) :
    self.c1 = event.GetPosition()

  def OnMouseMove ( self, event ) :
    if event.Dragging() and event.LeftIsDown():
      self.c2 = event.GetPosition()
      self.Refresh()

  def OnMouseUp ( self, event ) :
    ## Don't know for sure that +(1,1) is correct ??
    self.c1 = self.ClientToScreen ( self.c1 ) + ( 1, 1 )
    self.c2 = self.ClientToScreen ( self.c2 ) + ( 1, 1 )
    x0 = self.c1.x
    x1 = self.c2.x
    y0 = self.c1.y
    y1 = self.c2.y
    if x0 == x1 or y0 == y1 :
      self.c1 = None
      self.c2 = None
      return

    if x0 > x1 :
      x  = x0
      x0 = x1
      x1 = x
    if y0 > y1 :
      y  = y0
      y0 = y1
      y1 = y

    from PIL import ImageGrab
    bbox = ( x0, y0, x1, y1 )
    # For bounded bbox, yields, x0, y0 is included, x1, y1 is excluded !!
    ImageGrab.grab ( bbox ).save ( self.Filename )
    self.Close()

  def OnPaint ( self, event ) :
    if ( self.c1 is None ) or ( self.c2 is None ) :
      return

    dc = wx.PaintDC ( self.panel )
    dc.SetPen ( wx.Pen ( 'red', 1 ) )
    dc.SetBrush ( wx.Brush ( wx.Colour ( 0, 0, 0 ), wx.TRANSPARENT ))

    dc.DrawRectangle ( self.c1.x, self.c1.y,
                       self.c2.x - self.c1.x, self.c2.y - self.c1.y )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def Screen_Capture ( Filename, parent = None ) :
  dlg = _Screen_Capture ( Filename, parent )
  dlg.ShowModal()
  dlg.Destroy()
# ***********************************************************************




# ***********************************************************************
# ***********************************************************************
class _Picture_Edit ( wx.Dialog ) :

  def __init__(self, Filename, Picture_Info = [], parent = None ) :
    self.Return_Orginal = False
    self.Filename = Filename
    if Picture_Info :
      # generate the original filename
      File, Ext = os.path.splitext ( self.Filename )
      self.Org_Filename = File [ :-5 ] + Ext
    else :
      self.Org_Filename = Filename

    style = wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER
    #style = wx.FRAME_NO_TASKBAR | wx.SUNKEN_BORDER
    if parent :
      style |= wx.FRAME_FLOAT_ON_PARENT
    else :
      style |= wx.STAY_ON_TOP
    style ^= wx.MAXIMIZE_BOX
    style ^= wx.MINIMIZE_BOX
    style ^= wx.CLOSE_BOX
    wx.Dialog.__init__( self, parent, -1, 'Picture Edit', style=style )

    from picture_support import Get_Image_List
    Image_List = Get_Image_List ()
    b_size = ( 22, 22 )

    self.Colors = []
    self.Colors.append ( wx.BLACK )
    self.Colors.append ( wx.LIGHT_GREY )
    self.Colors.append ( wx.WHITE )
    self.Colors.append ( wx.RED )
    self.Colors.append ( wx.Colour (   0, 128,   0 )) # donkergroen
    self.Colors.append ( wx.GREEN )
    self.Colors.append ( wx.CYAN )
    self.Colors.append ( wx.BLUE )
    self.Colors.append ( wx.Colour ( 255,   0, 255 )) # purple

    self.Colors += [ 645, 45, 29, 57, 56 ]
    self.Colors.append ( wx.RED )
    Bmps = []
    self.B = len ( self.Colors ) * [0]
    print(self.B)

    GUI = """
    aap  ,PanelVer  ,0001
      NN_PanelHor  ,00000000000000000
    """
    for i, Nr in enumerate ( self.Colors ) :
      if isinstance ( Nr, int ) :
        Bmps.append ( Image_List.GetBitmap ( Nr ) )
        GUI += """
        self.B[%i]  ,BmpBut  ,bitmap = Bmps[%i]  ,size = b_size""" %( i, i )
      else :
        Bmps.append ( 0 )
        GUI += """
        self.B[%i]  ,wx.Button ,size = b_size""" %(i)

    GUI += """
      NN_PanelHor  ,00001
        Button_Org     ,wx.Button,               label = 'Orginal'
        Button_Cancel  ,wx.Button, wx.ID_CANCEL, label = 'Cancel'
        Button_OK      ,wx.Button,               label = 'OK'
        HorSpacer      ,10
        self.Text      ,wx.TextCtrl  ,style = wx.TE_PROCESS_ENTER
      Spacer        ,5
    """

    import OGLlike as ogl
    GUI += """
      self.Panel  ,wx.Panel
        self.OGL ,ogl.OGL_Picture_Edit  ,Filename = self.Org_Filename
    """
    from gui_support import Create_wxGUI, BmpBut, HorSpacer, Spacer
    self.wxGUI = Create_wxGUI ( GUI )

    self.OGL.Notify_Parent_One_Select = self._On_Select_One
    self.Text.Bind ( wx.EVT_KEY_DOWN, self._On_Text_Key_Down )

    self.B_IDs = []
    for i, Button in enumerate ( self.B ) :
      if not ( isinstance ( self.Colors[i], int ) ) :
        Button.SetBackgroundColour ( self.Colors[i] )
      self.B_IDs.append ( Button.GetId () )
      Button.Bind ( wx.EVT_BUTTON, self._On_Button )
    self.B[-1].SetLabel ( '5' )
    self.OGL.Set_LineWidth ( 5 )
    self.OGL.Set_Color ( self.Colors [-1] )
    self.Current_Color = self.Colors [-1]
    self.OGL.SetCursor ( wx.StockCursor ( wx.CURSOR_CROSS ) )

    # Scale myself to the perfect size
    self.Layout()
    Bmp = wx.Bitmap ( self.Filename )
    BSize = list ( Bmp.GetSize () )
    self.BSize = ( BSize[0], BSize[1] )
    MinW = 330
    if BSize [0] < MinW :
      BSize[0] = MinW
    PSize = self.Panel.GetClientSize()
    dx = BSize[0] - PSize [0]
    dy = BSize[1] - PSize [1]
    Size = self.GetSize ()
    self.SetSize ( ( Size[0] + dx, Size[1] + dy ))

    if Picture_Info :
      self.OGL.Set_Info ( Picture_Info )
    else :
      # generate a new filename
      File, Ext = os.path.splitext ( self.Filename )
      self.Filename = File + '_XXX_' + Ext

    Button_Org.Bind ( wx.EVT_BUTTON, self._On_Button_Org )
    Button_OK .Bind ( wx.EVT_BUTTON, self._On_Button_OK  )

  #***************************************************
  #***************************************************
  def _On_Button_Org ( self, event ) :
    Info = self.OGL.Get_Info () [0]
    if len ( Info ) > 0 :
      self.Filename = Info [0]
      self.Return_Orginal = True
      self.EndModal ( wx.ID_OK )

  #***************************************************
  #***************************************************
  def _On_Button_OK ( self, event ) :
    self.OGL.Deselect_All ()
    self.OGL.Refresh ()
    x0, y0, x1, y1 = self.OGL.GetRect ()
    x0, y0 = self.OGL.ClientToScreen ( ( x0, y0 ) )
    x1 = x0 + self.BSize [0]
    y1 = y0 + self.BSize [1]
    ##print 'QQQQ', x0, y0, x1,y1, self.BSize

    from PIL import ImageGrab
    bbox = ( x0, y0, x1, y1 )
    # For bounded bbox, yields, x0, y0 is included, x1, y1 is excluded !!
    ImageGrab.grab ( bbox ).save ( self.Filename )

##    a = wx.ClientDC ( self.OGL )  # Size klopt niet
##    saveSnapshot(a,self.Filename)

    self.EndModal ( wx.ID_OK )

  #***************************************************
  #***************************************************
  def _On_Text_Key_Down ( self, event = None ) :
    if event.KeyCode == wx.WXK_RETURN :
      New = self.Text.GetValue ()
      self.OGL.Change_Text ( New )
    else :
      event.Skip ()

  # ********************************************
  # ********************************************
  def _On_Select_One ( self, item ) :
    import OGLlike as ogl
    if isinstance ( item, ogl.Overlay_Text ) :
      self.Text.SetValue ( item.Text )

  # ********************************************
  # ********************************************
  def _On_Button ( self, event ) :
    indx = self.B_IDs.index ( event.GetId () )
    if   indx < 9   : # set Color
      Color = self.Colors [ indx ]
      print(Color)
      self.B[-1].SetBackgroundColour ( Color )
      self.OGL.Set_Color ( Color )
      self.Current_Color = Color
    elif indx == 9  :
      self.OGL.Add_Rectangle ()
    elif indx == 10 :
      self.OGL.Add_Arrow ()
    elif indx == 11 :
      line = self.Text.GetValue ()
      if line :
        self.OGL.Add_Text ( line )
    elif indx == 12 :
      B = self.B[-1]
      LW = int ( B.GetLabel () )
      if LW > 2 :
        LW -= 2
      elif LW > 1 :
        LW = 1
      B.SetLabel ( str ( LW ) )
      self.OGL.Set_LineWidth ( LW )
    elif indx == 13 :
      B = self.B[-1]
      LW = int ( B.GetLabel () )
      if LW < 10 :
        LW += 2
      B.SetLabel ( str ( LW ) )
      self.OGL.Set_LineWidth ( LW )
    else :
      B = self.B[-1]
      LW = int ( B.GetLabel () )
      self.OGL.Set_LineWidth_Color ( LW, self.Current_Color )

  # **********************************************************************
  # **********************************************************************
  def ShowModal ( self ) :
    Result = wx.Dialog.ShowModal ( self ) == wx.ID_OK
    if self.Return_Orginal :
      return Result, [], self.Org_Filename
    else :
      return Result, self.OGL.Get_Info (), self.Filename
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def Picture_Edit ( Filename, Picture_Info = [], parent = None ) :
  dlg = _Picture_Edit ( Filename, Picture_Info, parent )
  OK, Picture_Info, Filename = dlg.ShowModal()
  dlg.Destroy()
  return OK, Picture_Info, Filename
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
#class _Show_Picture ( wx.Dialog ) :
class _Show_Picture ( wx.Frame ) :

  def __init__(self, Filename, parent = None ) :
    self.Filename = Filename

    style = wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER
    #style = wx.FRAME_NO_TASKBAR | wx.SUNKEN_BORDER
    if parent :
      style |= wx.FRAME_FLOAT_ON_PARENT
    else :
      style |= wx.STAY_ON_TOP
    #wx.Dialog.__init__( self, parent, -1, 'Picture Edit', style=style )
    wx.Frame.__init__( self, parent, -1, 'Picture Edit', style=style )

    import OGLlike as ogl
    import  wx.lib.scrolledpanel as scrolled
    Image = wx.Image ( self.Filename ).ConvertToBitmap()
    GUI = """
      self.Panel  ,wx.Panel
#   Pan ,PanelVer  ,10
#      self.Panel  ,scrolled.ScrolledPanel  ,size = (100,100)
#        self.OGL ,ogl.OGL_Picture_Edit  ,Filename = self.Filename
#        self.OGL    ,wx.StaticBitmap  ,-1 ,wx.EmptyBitmap(1,1)
    """
    from gui_support import Create_wxGUI, BmpBut, HorSpacer, Spacer
    self.wxGUI = Create_wxGUI ( GUI )
    print(self.wxGUI)

    #self.OGL.SetBitmap ( Image )

    ##self.Panel.SetSizer( fgs1 )
    #self.Panel.SetAutoLayout(1)
    #self.Panel.SetupScrolling()

    #self.SetAutoLayout(1)
    #self.SetupScrolling()

    #self.Show ( True )
  # **********************************************************************
  # **********************************************************************
  def XShow (self ) : ##Modal ( self ) :
    wx.Dialog.ShowModal ( self )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
##@_Wrap_No_GUI
def XXShow_Picture ( Filename, parent = None ) :
  if os.path.exists ( Filename ) :
    dlg = _Show_Picture ( Filename, parent )
    ##OK, Picture_Info, Filename =
    dlg.Show(True) ##Modal()
    #dlg.Destroy ()
    ##return OK, Picture_Info, Filename
# ***********************************************************************


# ***********************************************************************
class DragScrollWindow ( wx.ScrolledWindow ) :
  def __init__ ( self, parent, Filename ) : #, id = -1 ) :
    import wx
    wx.ScrolledWindow.__init__ ( self, parent ) #, id )
    #self.My_Parent = parent
    self.Scale = 11
    self.Filename = Filename
    #self.Image = wx.StaticBitmap ( self, -1, wx.EmptyBitmap(1,1) )
    self.Image = wx.StaticBitmap ( self, -1, wx.Bitmap(1,1) )
    self.On_Min ()

    self.Image.Bind ( wx.EVT_LEFT_DOWN, self.OnRightDown )
    self.      Bind ( wx.EVT_LEFT_UP,   self.OnRightUp   )
    self.Image.Bind ( wx.EVT_LEFT_UP,   self.OnRightUp   )
    import wx.lib.dragscroller
    self.scroller = wx.lib.dragscroller.DragScroller(self)


  def OnRightDown(self, event):
    #print event.GetPosition(), self.Image.GetSize (), self.GetSize()
    #print dir(self.scroller)
    #print 'pos=',self.scroller.pos
    self.scroller.Start(event.GetPosition())

  def OnRightUp(self, event):
    self.scroller.Stop()

  def On_Plus ( self, event = None ) :
    if self.Scale >= 10 :
      return
    self.Scale += 1
    self._Redraw ()

  def On_Min ( self, event = None ) :
    if self.Scale <= 1 :
      return
    self.Scale -= 1
    self._Redraw ()

  def _Redraw ( self ) :
    Image = wx.Image ( self.Filename )
    w, h = Image.GetSize ()
    w2 = w * ( old_div(self.Scale, 10.0) )
    h2 = h * ( old_div(self.Scale, 10.0) )
    print(self.Scale, w2,h2)
    Image = Image.Scale ( w2, h2 )
    self.SetScrollbars ( 1, 1, w2, h2 ) ##, 0, 0)
    ##self.scroller = wx.lib.dragscroller.DragScroller(self)

    Image = Image.ConvertToBitmap()
    self.Image.SetBitmap ( Image )
    ##self.Parent.Parent.Parent.Resize ()
    self.Refresh()

# ***********************************************************************
##@_Wrap_No_GUI    ## werk niet
class Show_Picture ( wx.Frame ) :
  def __init__( self, Filename, size = ( 600, 400 ) ) :
    wx.Frame.__init__ ( self, None, -1, size = size )
    GUI = """
    NN_PanelVer  ,10
      self.Image   ,DragScrollWindow  ,Filename
      NN_PanelHor  ,00000
        self.B_Plus  ,wx.Button  ,label = '+'
        self.B_Min   ,wx.Button  ,label = '-'
    """
    from gui_support import Create_wxGUI # TODO TODO 3
    self.wxGUI = Create_wxGUI ( GUI )
    self.B_Plus.Bind ( wx.EVT_BUTTON, self.Image.On_Plus )
    self.B_Min .Bind ( wx.EVT_BUTTON, self.Image.On_Min  )
    self.Show ()
# ***********************************************************************
def Show_Picture_App ( Filename ) :
  app = wx.App ()
  frame = Show_Picture ( Filename )
  app.MainLoop ()


# ***********************************************************************
# ***********************************************************************
import wx
try:
  import wx.calendar as wx_calendar
except:
  import wx.adv      as wx_calendar

from date_time_support import Delphi_Date
class My_Calendar ( wx.Panel ) :
  def __init__ ( self, *args, **kwargs ) :

    if 'Date' in kwargs :
      Date = kwargs.pop ( 'Date' )
    else :
      Date = Delphi_Date ()
    Cal_Date = Delphi_Date ( Date ).to_wxTime ()
    self._Set_Date ( Date )
    self.Cleared = False

    if 'Show_Weeks' in kwargs :
      self.Show_Weeks = kwargs.pop ( 'Show_Weeks' )
    else :
      self.Show_Weeks = True

    wx.Panel.__init__ ( self, *args, **kwargs )

    Cal_Style = wx_calendar.CAL_SHOW_HOLIDAYS \
                | wx_calendar.CAL_MONDAY_FIRST \
                | wx_calendar.CAL_SEQUENTIAL_MONTH_SELECTION

    GUI = """
      P1 ,PanelHor  ,0000
        self.Cal           ,wx_calendar.CalendarCtrl  ,date=Cal_Date  ,style = Cal_Style
      """

    if self.Show_Weeks :
      GUI += """
        Spacer   , 10
        self.Weeks         ,Base_Grid  ,editor=None
      """

    from gui_support import Create_wxGUI, Spacer
    self.wxGUI = Create_wxGUI ( GUI )

    if self.Show_Weeks :
      self.Weeks.Set_BG_Color_From_Parent ()


    self.Cal.Bind ( wx_calendar.EVT_CALENDAR_MONTH ,self._On_Change_Month )
    self.Cal.Bind ( wx_calendar.EVT_CALENDAR_DAY   ,self._On_Day_Select   )
    self._Show_HL ()
    self._Update_Weeks ()

  # **********************************************************************
  def _Set_Date ( self, Date ) :
    self.Date = Date
    self.Year, self.Month, self.Day = Delphi_Date ( self.Date ).to_Month()

  # **********************************************************************
  def _Update_Weeks ( self ) :
    if self.Show_Weeks :
      Date = Delphi_Date ( self.Cal.GetDate () )
      StartWeek = Date.Get_First_Week_In_Month ()
      Weeks = [['W']]
      for i in range ( 6 ) :
        Weeks.append ( [ str ( StartWeek + i ) ] )

      self.Weeks.Fill_Data ( Weeks )
      self.Weeks.SetColLabelSize ( 32 )
      self.Weeks.Set_Col_Widths ( 20 )
      self.Weeks.SetDefaultRowSize ( 14, True )
      self.Weeks.Set_Region_Color ( 0, 0, 6, 0, wx.Colour( 255, 255, 0 ) )

    Cur_Month = self.Cal.GetDate().GetMonth() + 1
    Cur_Year  = self.Cal.GetDate().GetYear()
    ##print 'llll',cur_month,cur_year,Delphi_Date(self.Date).to_Iso(),Delphi_Date(self.Date).to_Month()
    if ( Cur_Year == self.Year ) and ( Cur_Month == self.Month ) and\
       not ( self.Cleared ) :
      self._Show_HL ()
    else :
      self._Hide_HL ()

  # **********************************************************************
  def Clear ( self ) :
    self.Cleared = True
    self._Hide_HL ()

  # **********************************************************************
  def _On_Change_Month ( self, event ) :
    event.Skip ()
    self._Update_Weeks ()

  # **********************************************************************
  def _On_Day_Select ( self, event ) :
    event.Skip ()
    Date = self.Cal.GetDate ()
    self._Set_Date ( Date )
    self._Update_Weeks ()

  # **********************************************************************
  def _Hide_HL ( self ) :
    # MOET NOG WEEK EN ZON/ZAT ONDERSCHEIDEN
    self.Cal.SetHighlightColours ( wx.Colour ( 0, 0, 0 ),
                                   wx.Colour ( 255, 255, 255 ) )
    self.Cal.Refresh ()

  # **********************************************************************
  def _Show_HL ( self) :
    self.Cleared = False
    self.Cal.SetHighlightColours ( wx.Colour ( 255, 255, 255 ),
                                   wx.Colour ( 0, 0, 255) )
    self.Cal.Refresh ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class _Calendar_Gesprek_Dialog ( wx.Dialog ) :
  def __init__ ( self, Parent = None, Pos = (-1,-1), Show_Weeks = True,
                  Date = None, Gesprek = 0, Gesprekken = [] ) :

    style = wx.DEFAULT_DIALOG_STYLE
    if Parent :
      style |= wx.FRAME_FLOAT_ON_PARENT
    else :
      style |= wx.STAY_ON_TOP
    style ^= wx.MAXIMIZE_BOX
    style ^= wx.MINIMIZE_BOX
    style ^= wx.CLOSE_BOX
    style ^= wx.SYSTEM_MENU
    wx.Dialog.__init__( self, Parent,
                        size  = ( 400, 210 ),
                        pos   = Pos,
                        style = style )

    GUI = """
  self.Main_P     ,PanelHor       ,0000
    NN_PanelVer  ,0000
      self.Cal      ,My_Calendar  ,Show_Weeks = True ,Date = Date
      Spacer    ,10
      NN_PanelHor     ,00000
        Spacer  ,5
        self.Knop_Cancel   ,wx.Button  ,wx.ID_CANCEL      ,label = 'Cancel'
        Spacer  ,5
        self.Knop_Ok       ,wx.Button  ,wx.ID_OK  ,label = 'Ok'
#        Spacer  ,10
    self.Action_List ,GUI_ListBox ,size = ( 400, 100 )    , style=wx.LB_SINGLE
    """
    from gui_support import Create_wxGUI, GUI_ListBox, Spacer
    self.wxGUI = Create_wxGUI ( GUI )

    self.Action_List.Set ( Gesprekken )
    self.Action_List.SetSelection ( Gesprek )

  # **********************************************************************
  def ShowModal ( self ) :
    from date_time_support import Delphi_Date
    Result = wx.Dialog.ShowModal ( self ) == wx.ID_OK
    return Result,\
           Delphi_Date ( self.Cal.Cal.GetDate ()),\
           self.Action_List.GetSelection ()

  # **********************************************************************
  def _On_Cal_Selected ( self, event ) :
    self.EndModal ( wx.ID_OK )

  # **********************************************************************
  def _On_Change_Month ( self, event ) :
    self._Hide_HL ()

  # **********************************************************************
  def _On_Day_Select ( self, event ) :
    self._Show_HL ()

  # **********************************************************************
  def _Hide_HL ( self ) :
    self.Cal.SetHighlightColours ( wx.Colour ( 0, 0, 0 ),
                                   wx.Colour ( 255, 255, 255 ) )

  # **********************************************************************
  def _Show_HL ( self) :
    self.Cal.SetHighlightColours ( wx.Colour ( 255, 255, 255 ),
                                   wx.Colour ( 0, 0, 255) )

# ***********************************************************************
@_Wrap_No_GUI
def Calendar_Gesprek_Dialog ( Parent     = None,
                              Pos        = (-1,-1),
                              Date       = None,
                              Gesprekken = [],
                              Gesprek    = 0 ) :
  dlg = _Calendar_Gesprek_Dialog ( Parent     = Parent,
                                   Pos        = Pos,
                                   Date       = Date,
                                   Gesprekken = Gesprekken,
                                   Gesprek    = Gesprek,
                                   Show_Weeks = True )
  OK, Date, Gesprek = dlg.ShowModal()
  dlg.Destroy()
  return OK, Date, Gesprek
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class _Calendar_Dialog ( wx.Dialog ) :
  def __init__ ( self, Parent = None, Pos = (-1,-1), Show_Weeks = True,
                  Date = None ) :

    style = wx.DEFAULT_DIALOG_STYLE
    if Parent :
      style |= wx.FRAME_FLOAT_ON_PARENT
    else :
      style |= wx.STAY_ON_TOP
    style ^= wx.MAXIMIZE_BOX
    style ^= wx.MINIMIZE_BOX
    style ^= wx.CLOSE_BOX
    style ^= wx.SYSTEM_MENU
    wx.Dialog.__init__( self, Parent,
                        size  = ( 220, 190 ),
                        pos   = Pos,
                        style = style )

    GUI = """
  self.Main_P     ,PanelVer       ,0000
      self.Cal      ,My_Calendar  ,Show_Weeks = True ,Date = Date
      Spacer    ,10
      NN_PanelHor     ,00000
        Spacer  ,5
        Knop_Cancel   ,wx.Button  ,wx.ID_CANCEL ,label = 'Cancel'
        Spacer  ,5
        Knop_Ok       ,wx.Button  ,wx.ID_OK     ,label = 'Ok'
        Spacer  ,5
        Knop_Clear    ,wx.Button  ,label = 'Clear'
    """
    from gui_support import Create_wxGUI, Spacer
    self.wxGUI = Create_wxGUI ( GUI )

    Knop_Clear.Bind ( wx.EVT_BUTTON, self._On_Clear )

  # **********************************************************************
  def _On_Clear ( self, event ) :
    self.Cal.Clear ()

  # **********************************************************************
  def ShowModal ( self ) :
    from date_time_support import Delphi_Date
    Result = wx.Dialog.ShowModal ( self ) == wx.ID_OK
    if self.Cal.Cleared :
      return Result, None
    else :
      return Result,\
           Delphi_Date ( self.Cal.Cal.GetDate ())


# ***********************************************************************
@_Wrap_No_GUI
def Calendar_Dialog ( Parent     = None,
                              Pos        = (-1,-1),
                              Date       = None,
                              Gesprekken = [],
                              Gesprek    = 0 ) :
  dlg = _Calendar_Dialog ( Parent     = Parent,
                                   Pos        = Pos,
                                   Date       = Date,
                                   Show_Weeks = True )
  OK, Date = dlg.ShowModal()
  dlg.Destroy()
  return OK, Date
# ***********************************************************************




# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def Multi_List_Dialog ( Lists, Title = '',
                       size = ( -1, -1 ),
                       pos = wx.DefaultPosition ):
  dlg = _Multi_List_Dialog ( Lists, Title, size, pos )
  OK = dlg.ShowModal()
  dlg.Destroy()
  return OK
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class _Matrix_CheckList_Dialog ( wx.Dialog ):
  def __init__ ( self, Row_Names, Col_Names, Values,
                       Title = 'Check the appropriate cells',
                       Help = '',
                       Size = ( -1, -1 ),
                       Pos = wx.DefaultPosition ) :

    Style = wx.DEFAULT_FRAME_STYLE | \
                    wx.SUNKEN_BORDER | \
                    wx.CLIP_CHILDREN | \
                    wx.STAY_ON_TOP
    wx.Dialog.__init__( self, None, title = Title,
                        size  = Size,
                        pos   = Pos,
                        style = Style )

    # Font van de hoogste parent overnemen
    Font = wx.GetApp().GetTopWindow().GetFont()
    self.SetFont ( Font )

    GUI = """
    main, PanelVer  ,00010
      Spacer  , 10
      NN_PanelHor  , 010
        HorSpacer  ,10
        NN_wx.StaticText   ,label = Help
        HorSpacer  ,10
      Spacer  , 10
      self.Grid          ,Base_Grid   ,editor=None
      NN_PanelHor, 1000
        HorSpacer ,10
        Knop_Cancel             ,wx.Button  ,wx.ID_CANCEL ,label='Annuleren'
        Spacer ,10
        Knop_OK                 ,wx.Button  ,wx.ID_OK     ,label='Ok'
    """
    from gui_support import Create_wxGUI, BmpBut, HorSpacer, Spacer
    self.wxGUI = Create_wxGUI ( GUI )

    import  wx.grid as gridlib
    self.Grid.Bind ( gridlib.EVT_GRID_CELL_LEFT_CLICK, self._On_Left_Click )
    self.Grid.Bind ( wx.EVT_KEY_DOWN                 , self._On_Key )
    self.Grid.Bind ( gridlib.EVT_GRID_SELECT_CELL    , self._On_Cell_Selected )

    self.Grid.Set_All_ReadOnly ()
    self.Grid.SetRowLabelSize ( 260 )
    #self.Grid.Random_Select = True
    #self.Grid.Random_Select_Color = wx.Colour ( 200, 100, 100 )

    self.Color_Selected = wx.Colour ( 200, 250, 250 )
    self.Color_Selected = wx.Colour ( 0xF0, 0xF0, 0xE0 )
    self.Color_True     = wx.Colour ( 164, 255, 164 )
    self.Color_False    = wx.WHITE
    self.Color_Disable  = wx.Colour ( 200,200,200 )

    self.Data = []
    self.Data.append ( [''] + Col_Names )
    N = len ( Col_Names )
    for Row_Name in Row_Names :
      self.Data.append ( [Row_Name] + N * [None] )

    self.Col_Sel = -1 #None
    self.Row_Sel = -1#None

    self.Grid.Fill_Data ( self.Data )
    self.Grid.Set_Col_Widths ( 28 )
    self.Grid.Set_BG_Color_From_Parent ()

    Max = 0
    self.Values = Values
    for Col, Line in enumerate ( Values ) :
      for Row, Value in enumerate ( Line ) :
        if Value :
          self.Grid.Set_Cell_Color ( Col, Row, self.Color_True )
          Max = max ( Max, Col )
        else :
          self.Grid.Set_Cell_Color ( Col, Row, self.Color_False )

    # Color the columns at the end where there's is no data
    for Col in range ( len ( Values ), N ) :
      for Row in range ( len ( Values[0]) ):
        self.Grid.Set_Cell_Color ( Col, Row, self.Color_False )

    # Column 0 is special: which row is enabled
    for Row, Value in enumerate ( Values[0] ) :
      if not ( Value ) :
        self.Grid.Set_Region_Color ( Row, 0, Row, N, self.Color_Disable )
      else :
        self.Grid.Set_Cell_Color ( 0, Row, self.Color_False )

    self.Grid.SetGridCursor ( 0, Max + 1 )

  # ****************************************************************
  # ****************************************************************
  def _On_Cell_Selected ( self, event ) :
    event.Skip ()
    Col = event.Col
    Row = event.Row
    self.Cell_Select ( Row, Col )

  # ****************************************************************
  # ****************************************************************
  def Cell_Select ( self, Row, Col ) :
    ##print 'OOOOP', Col, Row, self.Col_Sel, self.Row_Sel
    if Row != self.Row_Sel :
      self._HL_Row ( self.Row_Sel, False )
    if Col != self.Col_Sel :
      self._HL_Col ( self.Col_Sel, False )

    self._HL_Row ( Row, True )
    self._HL_Col ( Col, True )

    self.Row_Sel = Row
    self.Col_Sel = Col

  # ****************************************************************
  # ****************************************************************
  def _HL_Row ( self, Row, HL = True ) :
    #return
    if HL :
      Color = self.Color_Selected
    else :
      Color = self.Color_False
    N = len ( self.Data [0] )
    for Col in range ( 0, N-1 ) :
      #print  HL, Color, Row, Col
      if not ( self.Grid.GetCellBackgroundColour ( Row, Col ) in
           ( self.Color_True, self.Color_Disable ) ) :
        self.Grid.SetCellBackgroundColour ( Row, Col, Color )
    self.Grid.ForceRefresh()

  # ****************************************************************
  # ****************************************************************
  def _HL_Col( self, Col, HL = True ) :
    if HL :
      Color = self.Color_Selected
    else :
      Color = self.Color_False
    N = len ( self.Data )
    for Row in range ( 0, N-1 ) :
      #print  HL, Color, Row, Col
      if not ( self.Grid.GetCellBackgroundColour ( Row, Col ) in
           ( self.Color_True, self.Color_Disable )) :
        self.Grid.SetCellBackgroundColour ( Row, Col, Color )
    self.Grid.ForceRefresh()

  # **********************************************************************
  # **********************************************************************
  def _On_Key ( self, event = None ) :
    Key = event.GetKeyCode ()
    if Key == 32 :
      Row = self.Grid.GetGridCursorRow()
      Col = self.Grid.GetGridCursorCol()
      self._Toggle_Cell_Selected ( Row, Col )
    else :
      event.Skip ()

  # **********************************************************************
  # **********************************************************************
  def _On_Left_Click ( self, event = None ) :
    event.Skip ()
    Row = event.GetRow ()
    Col = event.GetCol ()
    self._Toggle_Cell_Selected ( Row, Col )

  # **********************************************************************
  # **********************************************************************
  def _Toggle_Cell_Selected ( self, Row, Col ) :
    if Col == 0 :
      print('special', Row)
    elif self.Grid.GetCellBackgroundColour ( Row, 0 ) != self.Color_Disable :

      Color = self.Grid.GetCellBackgroundColour ( Row, Col )
      if Color == self.Color_True :
        if ( Row == self.Row_Sel ) or ( Col == self.Col_Sel ) :
          self.Grid.SetCellBackgroundColour ( Row, Col, self.Color_Selected )
        else :
          self.Grid.SetCellBackgroundColour ( Row, Col, self.Color_False )
      else :
        self.Grid.SetCellBackgroundColour ( Row, Col, self.Color_True )
      self.Grid.ForceRefresh()

  # **********************************************************************
  # **********************************************************************
  def ShowModal ( self ) :
    if wx.Dialog.ShowModal ( self ) == wx.ID_OK:
      Changed_Cols = []
      N = len ( self.Values[0] )
      Empty = N * [0]
      for Col in range ( 1, self.Grid.GetNumberCols() ) :
        New = []
        for i in range ( N ) :
          Color = self.Grid.GetCellBackgroundColour ( i, Col )
          if Color == self.Color_True :
            New.append ( 1 )
          else :
            New.append ( 0 )
        if Col >= len ( self.Values ) :
          if 1 in New :
            while len ( self.Values ) <= Col :
              self.Values.append ( Empty )
        if ( Col < len (self.Values)) and ( New != list(self.Values [ Col ]) ) :
          ##print 'OLD', self.Values[Col]
          ##print 'NEW', New
          self.Values [ Col ] = New
          Changed_Cols.append ( Col )
      return True, Changed_Cols
    else :
      return False, []
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def Matrix_CheckList_Dialog ( Row_Names, Col_Names, Data,
                              Title = '',
                              Help = '',
                              Size = ( -1, -1 ),
                              Pos = wx.DefaultPosition ) :
  dlg = _Matrix_CheckList_Dialog ( Row_Names, Col_Names, Data, Title, Help, Size, Pos )
  OK, Data = dlg.ShowModal()
  dlg.Destroy()
  return OK, Data
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class  _Email_Dialog ( wx.Dialog ) :
  def __init__ ( self, To, From, Subject, Content, SubConts, Substitutes ) :
    Style = wx.DEFAULT_FRAME_STYLE | \
                    wx.SUNKEN_BORDER | \
                    wx.CLIP_CHILDREN | \
                    wx.STAY_ON_TOP
    wx.Dialog.__init__( self, None, title = 'Email Versturen',
                        size  = ( 900, 700 ),
                        pos   = ( 100, 100 ),
                        style = Style )

    # Font van de hoogste parent overnemen
    Font = wx.GetApp().GetTopWindow().GetFont()
    self.SetFont ( Font )

    self.To          = To
    self.From        = From
    self.Subject     = Subject
    self.Content     = Content
    self.SubConts    = SubConts
    self.Substitutes = Substitutes

    GUI = """
    self.Main, PanelVer  ,0001000000
      Spacer  , 10
      NN_PanelHor  , 00010
        Spacer ,20
        NN_PanelVer
          NN_wx.StaticText  ,label = 'from'
          NN_wx.StaticText  ,label = 'to'
          NN_wx.StaticText  ,label = 'subject'
        Spacer ,10
        NN_PanelVer
          self.Edit_From    ,wx.TextCtrl
          self.Edit_To      ,wx.TextCtrl
          self.Edit_Subject ,wx.TextCtrl
        Spacer ,20
      Spacer  ,20

      NN_PanelHor  ,010
        Spacer ,20
        self.Edit_Content         ,wx.TextCtrl  ,style=wx.TE_MULTILINE
        Spacer ,20

      Spacer  ,10
      NN_PanelHor  ,10
        self.Knoppen_Panel ,PanelHor
          Knop_0             ,wx.Button
          Knop_1             ,wx.Button
          Knop_2             ,wx.Button
          Knop_3             ,wx.Button
          Knop_4             ,wx.Button
          Knop_5             ,wx.Button
          Knop_6             ,wx.Button
          Knop_7             ,wx.Button
          Knop_8             ,wx.Button
          Knop_9             ,wx.Button
          HorSpacer ,10
        NN_PanelHor, 000000
          Knop_Cancel        ,wx.Button  ,wx.ID_CANCEL ,label='Cancel'
          Spacer ,10
          Knop_Send          ,wx.Button  ,wx.ID_OK     ,label='Send'
          Spacer ,10
    """
    from gui_support import Create_wxGUI, BmpBut, HorSpacer, Spacer
    self.wxGUI = Create_wxGUI ( GUI )

    self.Knop_Content = []
    for i in range (10) :
      eval ( 'self.Knop_Content.append ( Knop_%s )' % i )
      self.Knop_Content [-1].Bind ( wx.EVT_BUTTON, self._On_Knop_Template )

    # if do the fill right here, the rendering isn't done well
    wx.CallAfter ( self._Fill_Data )

  def _Fill_Data ( self ) :
    self.Edit_To.SetValue   ( self.To   )
    self.Edit_From.SetValue ( self.From )

    # if only content and no subject
    # exchange content and subject
    if self.Content and not self.Subject :
      self.Subject = self.Content
      self.Content = ''

    # if only Subject and no Content
    # first line of Subject contains the Subject
    # rest of the Subject contains the Content
    if self.Subject and not self.Content :
      Lines = self.Subject.splitlines ()
      self.Subject = Lines[0]
      self.Content = '\n'.join ( Lines[1:] )

    self.Edit_Subject.SetValue ( self.Subject )
    self.Edit_Content.SetValue ( self.Content )

    if self.SubConts :
      self.Knop_Content = []
      for i in range (10) :
        eval ( 'self.Knop_Content.append ( Knop_%s )' % i )
      for i, SC in enumerate ( self.SubConts ) :
        self.Knop_Content [i].SetLabel ( SC )
        self.Knop_Content [i].Show ()
        self.Knop_Content [i].Bind ( wx.EVT_BUTTON, self._On_Knop_Template )
      for i in range ( len ( self.SubConts ), 10 ) :
        self.Knop_Content [i].Hide ()

    else :
      for i in range ( 10 ) :
        self.Knop_Content [i].Hide ()

    self.Knoppen_Panel.SendSizeEvent ()
    self.Edit_Content.SetFocus ()

  # **********************************************************************
  # **********************************************************************
  def _On_Knop_Template ( self, event ) :
    if self.Edit_Content.GetValue () :
      if not ( AskYesNo ( """
De inhoud van de mail bavet reeds data,
Wilt u die overschrijven ?""" ) ) :
        return

    Template = event.EventObject.GetLabel ()
    Subject  = self.SubConts [ Template ]

    for item in self.Substitutes :
      try :
        if self.Substitutes [ item ] is None :
          self.Substitutes [ item ] = ''
        print('======dsd==',item, item in self.Substitutes, self.Substitutes [ item ])
        ##Subject = Subject.replace ( '$$$' + item + '$$$', self.Substitutes [ item ].encode('Windows-1252') )
        Subject = Subject.replace ( '$$$' + item + '$$$', self.Substitutes [ item ] )
      except :
        print('ERRRORR, Create_Doc_From_Template', item)


    Lines = Subject.lstrip().splitlines ()
    Subject = Lines[0]
    Content = '\n'.join ( Lines[1:] )

    self.Edit_Subject.SetValue ( Subject )
    self.Edit_Content.SetValue ( Content )


  # **********************************************************************
  # **********************************************************************
  def ShowModal ( self ) :
    if wx.Dialog.ShowModal ( self ) == wx.ID_OK :

      from mail_support import RadQuest_Email
      From    = self.Edit_From.GetValue ()
      To      = self.Edit_To.GetValue ()
      Subject = self.Edit_Subject.GetValue ()
      Content = self.Edit_Content.GetValue ()
      RadQuest_Email ( From, To, Subject, Content )

      from utility_support import NoCase_Dict
      Data = NoCase_Dict ()
      Data.From    = From
      Data.To      = To
      Data.Subject = Subject
      Data.Content = Content

      return True, Data
    return False, None
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def Email_Dialog ( To          = '',
                   From        = '',
                   Subject     = '',
                   Content     = '',
                   SubConts    = None,
                   Substitutes = None ) :
  dlg = _Email_Dialog ( To, From, Subject, Content, SubConts, Substitutes )
  OK = dlg.ShowModal()
  dlg.Destroy()
  return OK
# ***********************************************************************



# ***********************************************************************
# for test, read and print some ini file
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 1 )

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 0 ) :
    '''
    Names = [ 'Compiler', 'CheckBox', 'Library Path', 'CMD line', 'Uploader', 'CMD line']
    Values = []
    Types = [ MLD_FILE, bool, MLD_PATH, None, MLD_FILE]
    HelpText = \
"""
The following substitutes are valid
  %F = JAL source file  (JAL compiler) / Generated Hex file  (uploader)
  %L = JAL library path (JAL compiler)
Commandline examples
  -long-start -d  -clear -s%L %F  (JAL compiler)
  %F uploader 115200  (UPD)\
"""
    OK, Values = MultiLineDialog ( Names, Values, Types,
                                   'Compile and Upload Settings',
                                   HelpText )
                                   # width = 200 )
    if OK: print Values
    '''

    DD_Research = ['', u'FAC', u'ACON', u'SMRI', u'CAF', u'INTERFAT', u'ZBI', u'Procesonderzoek', u'TDT', u'Groepsond.CVS', u'Com.Analyse.VNK', u'FITNET', u'FSHD', u'Inspanningsonderzoek', u'Traponderzoek', u'VR', u'FICS']
    DDi_Research = [None, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56]
    Names = DD_Research [1:]
    N = len ( Names )
    Values = N * [ False ]
    Types = N * [ bool ]
    Values[3] = True
    Values[4] = True
    HelpText = 'blabla\nmohgdmeer'
    OK, Answers = MultiLineDialog ( Names, Values, Types,
                  Title = 'Starten van een nieuwe vragenlijst',
                  HelpText = HelpText )
    #              Parent = self.Top_Window )
    if OK :
      print(Values)


  # ***********************************************************************
  # ***********************************************************************
  if Test ( 1 ) :
    Line  = 'DB_Active-1,DB_Name-1,Table_Name-1,Condition-1,'
    Line += 'DB_Active-2,DB_Name-2,Table_Name-2,Condition-2,'
    Line += 'DB_Active-3,DB_Name-3,Table_Name-3,Condition-3,'
    Names = Line[:-1].split(',')

    Line  = 'bool,str,str,str,'
    Line += 'bool,str,str,str,'
    Line += 'bool,str,str,str,'
    #Types = eval ( Line[:-1].split(',') )
    Types = eval ( '[' + Line[:-1] + ']' )

    OK, Values = MultiLineDialog ( Names = Names, Values = [], Types = Types,
                                   Title = 'Data Sources to use for substitution',
                                   width = 170 )
    if OK: print(Values)

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 2 ) :
    # *******************
    # Single FileOpen test
    # *******************
    FileType = "Python Files (*.py)|*.py|"\
               "All Files (*.*)|*.*"
    File = AskFileForOpen ( FileTypes = FileType )
    if File:
      print(File)
    else:
      print('wrong')

  if Test ( 3 ) :
    # *******************
    # Multi FileOpen test
    # *******************
    FileType = "Python Files (*.py)|*.py|"\
               "All Files (*.*)|*.*"
    Files, Path = AskFilesForOpen ( FileTypes = FileType )
    if Files:
      print(Path, Files)
    else:
      print('wrong')

  if Test ( 5 ) :
    # *******************
    # Yes-No test
    # *******************
    if AskYesNo ('Is this ok') :
      print('Yes')
    else:
      print('No')


  # ***********************************************************************
  # ***********************************************************************
  if Test ( 6 ):
    from db_support import Find_ODBC
    ODBC_DBs = Find_ODBC ()
    ODBC_DBs.insert ( 0, [ 'ODBC Name', 'Filename'])

    HelpText = \
"""
The list below, shows both the
  - user databases ( HKEY_CURRENT_USER\Software\ODBC\ODBC.INI  )
  - system databases ( HKEY_LOCAL_MACHINE\Software\ODBC\ODBC.INI )"""


    OK, Values = ListDialog ( ODBC_DBs,
                              'Select ODBC Database',
                              HelpText )
                              # width = 200 )
    if OK: print(Values)

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 7 ) :
    app = wx.App ()
    # **************************************************
    # Generate a sorted fontlist
    # **************************************************
    fonts = wx.FontEnumerator ()
    fonts.EnumerateFacenames ()
    fontList = fonts.GetFacenames ()
    fontList.sort()
    # **************************************************
    print(fontList)

  # ***********************************************************************
  # Search Dialog
  # ***********************************************************************
  if Test ( 8 ) :
    Prev_Search = 'Find'
    OK, Values = MultiLineDialog ( Values = [ Prev_Search ],
                                   Title  = 'Enter Search String',
                                   width  = 200 )
    if OK:
      Prev_Search = Values [0]
    print(Prev_Search)

  # ***********************************************************************
  # TextArea Dialog
  # ***********************************************************************
  if Test ( 9 ) :
    Types = [ MLD_TextArea ]
    OK, Values = MultiLineDialog ( Types = Types,
                                   Title = 'My Title',
                                   HelpText = 'Help Info' )
    if OK:
      print(Values)

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 10 ) :
    Names = [ 'DataBase 17-12-2009', 'Programma Versie 0.4', 'Iets anders']
    Values = []
    Types = [ MLD_LBOOL, MLD_LBOOL, MLD_FILE ]
    HelpText = \
"""
Er zijn een aantal nieuwe programma onderdelen gevonden.
Hieronder kunt u aangeven wat u vernieuwd wilt hebben.
Of U kunt op Cancel drukken op niets te vernieuwen.
"""
    OK, Values = MultiLineDialog ( Names, Values, Types,
                                   'Programma Vernieuwingen',
                                   HelpText )
                                   # width = 200 )
    if OK: print(Values)

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 11 ) :
    OK, Choice, Omschrijving = RadQuest_Status_Dialog (
        Title         = 'Wijzigen van TestBatterij "Breath-1"',
        Status_Labels = ( 'Ontwikkeling', 'Test', 'Productie', 'Uit Produktie' ),
        Status        = 1,
        User          = 'z571117',
        Version       = 12 )
    print(OK, Choice, Omschrijving)

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 12 ) :
    Filename = r'D:\Data_Python_25\support\aapjexyz.gif'
    Formule = r'\frac{(a+b)}{(c-d)}'
    OK, Formula, Size = Formula_Dialog ( Formule, Filename )

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 13 ) :
    Screen_Capture ( "sc-555.png" )

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 14 ) :
    OK, Values = MultiLineDialog ( ['Password'],
      Values = [''],
      Title = 'Password for VPN and Shares')
    if OK :
      print('piep', Values)
    exit()

    Filename = r'D:\Data_Python_25\support\aapjexyz.png'
    Filename = r'D:\Data_Python_25\pictures\HealthXOLogo.png'

    Picture_Info = [
[1, 216.0, 106.0, 266.0, 156.0, 5, wx.Colour(0, 255, 0, 255), ''],
[1, 64.0, 170.0, 114.0, 220.0, 5, wx.Colour(0, 0, 255, 255), ''],
[2, 183.0, 207.0, 233.0, 257.0, 5, wx.Colour(0, 0, 255, 255), ''],
[3, 238.0, 40.0, 325.0, 93.0, 5, wx.Colour(0, 0, 255, 255), u'sdfs'],
    ]
    Picture_Info = []

    OK, Picture_Info, Filename = Picture_Edit ( Filename, Picture_Info )
    print(OK, Filename)
    for item in Picture_Info :
      print(item)

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 15 ) :
    List1 = 'Behandel Fase,Choice 1,Choice 2,Choice 3,Choice 4'.split(',')
    List2 = 'Rapport,Keuze 11,Keuze 22,Keuze 33,Keuze 44'.split(',')
    Lists = [ List1, List2 ]
    OK, Values, Strings = Multi_List_Dialog ( Lists, size = ( 400, 600 ) )
    print(OK, Values, Strings)

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 16 ) :
    from date_time_support import Delphi_Date
    import datetime

    """
    Gesprekken = ',hdjsd,dasdasd,dsdas,sdfgsd,gfgdgg,gdfgd,gd,gdfg,dgdfg,df'.split(',')
    OK, Date, Gesprek = Calendar_Gesprek_Dialog (
                          Pos        = ( 20, 20 ),
                          Date       = Delphi_Date (),
                          Gesprek    = 4,
                          Gesprekken = Gesprekken )

    print OK, Date.to_String (), Gesprek
    """

    OK, Date = Calendar_Dialog (
                          Pos        = ( 20, 20 ),
                          Date       = Delphi_Date ())

    print(OK, Date) ##.to_String ()

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 17 ) :
    Names1  = 'Behandel Fase,Choice 1,Choice 2,Choice 3,Choice 4'.split(',')
    Names2  = 'Rapport,Keuze 11,Keuze 22,Keuze 33'.split(',')
    Names   = [ Names1, Names2 ]
    Values1 = [ 0, 1, 1, 1, 1 ]
    Values2 = [ 0, 1, 0, 0    ]
    Values  = [ Values1, Values2 ]

    Names = [['dummy', 'Marlies Peters', 'FSHD', 'CureStudy', 'Ouderen_Oncologie',
               'wacht2.000', 'wacht2.001', 'wacht2.002', 'wacht2.003', 'wacht2.004',
               'wacht2.005', 'wacht2.006', 'wacht2.007', 'wacht2.008', 'wacht2.009',
               'wacht2.010', 'wacht2.011', 'FICSpoli', 'Fics', 'VNK Screening',
               'Driebergen VNK', 'Driebergen CGT', 'CZ', 'VNK', 'CGT'],
              [u'T.B.M. Berends', u'J.A. Knoop', u'H. Voskamp', u'- -', u'Groep -',
               u'G. Bleijenberg', u'Gerrie -', u'Hanneke -', u'J.M.J. de la Fonteijne',
               u'D.J.P. Marcelissen', u'A.J.M. van Dijk', u'J.W.C. van Bussel-Lagarde',
               u'S.M. Steur', u'A.L. Janse', u'P.N. Kruiswijk', u'P.N. Hellingman',
               u'S.M. Bouman']]
    Values = [[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]]

    OK, Values = Multi_CheckList_Dialog ( Names, Values, size = ( 400, 600 ) )
    print(OK, Values)

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 18 ) :
    Title = 'Componenten Analyse VNK'

    Row_Names = []
    Row_Names.append ( 'Verhaal van de patient' )
    Row_Names.append ( 'Tweede aspect' )
    Row_Names.append ( 'Tweede aspect' )
    Row_Names.append ( 'Tweede aspect' )
    Row_Names.append ( 'Tweede aspect' )
    Row_Names.append ( 'Tweede aspect' )
    Row_Names.append ( 'Tweede aspect' )

    Col_Names = 'X,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,F1,F2'.split(',')

    Data = []
    Data.append ( ( 1,1,1,1,1,1,1 ) )
    Data.append ( ( 0,0,1,1,0,1,0 ) )
    Data.append ( ( 0,0,1,1,0,1,0 ) )
    Data.append ( ( 0,0,1,1,0,1,0 ) )
    Data.append ( ( 1,0,1,1,0,1,0 ) )
    Data.append ( ( 0,0,0,0,0,1,0 ) )
    Data.append ( ( 1,1,1,1,0,1,0 ) )

    OK, Changed_Cols = Matrix_CheckList_Dialog ( Row_Names, Col_Names, Data,
                                           Title = Title,
                                           Help = 'Help\ngdhsd\n\n dhsadajsd',
                                           Size = ( 800, 400 ),
                                           Pos  = ( 100, 100 ) )
    print(OK, Changed_Cols)
    for Row in Data :
      print(Row)

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 19 ) :
    To = 'Stef.Mientki@gmail.com'
    From = 'S.Mientki@sb.umcn.nl'
    SubConts = {}
    SubConts [ 'Screen -CVS' ] = """
Screening CVS
$$$Aanhef$$$,

De door u gegeven antwoorden geven geen indicatie voor CVS.
Wij adviseren u dit verder te bespreken met uw huisarts.

met vriendelijke groet,
dr. Jan Jansen
klinisch psycholoog
    """
    SubConts [ 'Screen +CVS' ] = """
Screening CVS
$$$Aanhef$$$,

De door u gegeven antwoorden geven een indicatie voor CVS.
Wij zullen u dan ook binnen enkele weken oproepen voor een uitgebreide diagnostische test.

met vriendelijke groet,
dr. Jan Jansen
klinisch psycholoog
    """
    SubConts [ 'Test1' ] = """
Onderwerp van de Mail
Beste Piet,

zou je op onderstaande link willen klikken ?
$$$LINK$$$

groeten,
Sint
    """
    Substitutes = {}
    Substitutes [ 'LINK' ] = 'http://pic.flappie.nl'
    Substitutes [ 'Aanhef' ] = 'Beste heer Mientki'
    OK = Email_Dialog ( To = To,
                   From = From,
                   Subject = '',
                   Content = '',
                   SubConts = SubConts,
                   Substitutes = Substitutes )
    print(OK)

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 20 ) :
    Filename = r'D:\__aap\FN1.png'
    app = wx.App ()
    frame = Show_Picture ( Filename )
    app.MainLoop ()

# ***********************************************************************

# ***********************************************************************
pd_Module ( __file__ )
