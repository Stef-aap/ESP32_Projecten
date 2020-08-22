from __future__ import print_function
from __future__ import absolute_import
#from __future__ import absolute_import
from builtins import str
from builtins import chr
from builtins import range
from builtins import object
import __init__

import wx
import os
import webbrowser

from  language_support import  _
from  help_support     import Launch_CHM
from  dialog_support   import AskFileForOpen, Show_Message
from  General_Globals  import Iterable

__doc__ = """
"""

_Version_Text = [

[ 1.8 , '6-6-2012', 'Stef Mientki',
'Test Conditions:???', (2,),
"""
- Bind_MenuItem now returns the menu item
"""],

[ 1.7 , '23-04-2010', 'Robbert Mientki',
'Test Conditions:???', (2,),
"""
- Changed Popup menu item (backwards compatible)
  - now finds functions automaticly (with no parameters)
  - Assigns accelerators keys automaticly)
  - When multiple items are specified and 1 function,
    the item string(text) will be returned instead of the ID
"""],

[ 1.6 , '23-03-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- added menuitem "Settings / Font"
"""],

[ 1.5 , '18-01-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Create_ToolBar_Items
"""],

[ 1.4 , '27-09-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Bind_MenuItem, extended with focused element
  ( For wx.grid.Grid we need to bind to GridWindow !! )
- extra menu items, added with Bind_MenuItem,
  are now added before the last one (Help)
- Class_StatusBar added
"""],

[ 1.3 , '12-05-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
 - Help menu extended with chm-files and links from global config
"""],

[ 1.2 , '20-11-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - Create Menus bug solved
 - Create Menus now defined as a class, with more interfaces
""")],

[ 1.1 , '27-07-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - Some code restyling
 - Append_Item added
""")],

[ 1.0 , '14-07-2007', 'Stef Mientki',
'Test Conditions:', (),
_(0, ' - orginal release')]
]
# ***********************************************************************


from gui_support import *
from picture_support import *
import copy
## This imports Alot of PyLab_Works, and it is only used once
## in Menu_Event_Handler.OnMenu_About (So import it on the fly in OnMenu_About)
##import PyLab_Works_Globals as PG


import wx


def String2KeyCode(a):
  if not a: return []
  aa = a.split('-')
  bb = a.split('+')
  keys = [a]
  if len(aa)>1: keys = aa
  if len(bb)>1: keys = bb
  keymap = []
  for key in keys:
    if len(key)==1:
      keymap.append(key.lower())
    elif key.lower() in ['ctrl','control','ctr']:
      keymap.append('ctrl')
    elif key.lower() in ['alt']:
      keymap.append('alt')
    elif key.lower() in ['shift','sft','shft']:
      keymap.append('shift')
    else:
      for name in dir(wx):
        if name.startswith('WXK_') and not name.startswith('WXK_NUMPAD'):
          if key.upper() in name:
            keymap.append(name)
            break
  return keymap
# ***********************************************************************
# ***********************************************************************
class My_Popup_Menu_Robbie ( wx.Menu ) :
  default = {}

  # edit
  default[0] = [
      _(0,'Cut'), _(0,'Copy'), _(0,'Paste'), _(0,'Delete')]

  # extended edit
  default[1] = [
      '-', _(0,'Cut'), _(0,'Copy'), _(0,'Paste'), _(0,'Delete'), '-' ]

  # tree
  default[2] = [
      _(0,'Insert New\tIns'), _(0,'Edit\tSpace'),
      '-', _(0,'Cut\tCtrl-X'), _(0,'Copy\tCtrl-C'),
      _(0,'Paste\tCtrl-V'), _(0,'Delete\tDel') ]

  # *************************************************************
  # itemset = None,  doesn't use a default set
  # *************************************************************
  def __init__ ( self, parent, itemset = 0, func=None, pre = None, post = None ):
    """
Automatically binds the event to the right-mouse-dwon event.
parent  :  ??
itemset : number specifying the itemset
          iterable object, filled with strings
func    :
pre     : iterable object with strings, will be inserted before itemset
post    : iterable object with strings, will be inserted after itemset
    """
    wx.Menu.__init__ ( self )
    self.parent = parent

    self.funcs = []
    self.params= []
    self.items = []
    self.keys  = []

    # Bind myself:
    self.parent.Bind ( wx.EVT_RIGHT_DOWN, self.OnShowPopup )

    self.parent.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
    items = []
    if pre :
      items = pre
    if isinstance ( itemset, int ) :
      items += self.default [ itemset ]
    elif Iterable ( itemset ) :
      items += itemset

    if post :
      items += post

    #print 'asdfafasdf' ,func
    if func:
      self.Append_Item(items,func = func)
    else:
      for item in items:
        self.Append_Item(item)

  def OnShowPopup ( self, event ) :
    self.parent.PopupMenu ( self )

  def OnKeyDown(self,evt):
    keycode = evt.GetKeyCode()
    great = False
    for i,keymap in enumerate(self.keys):
      if 'ctrl'  in keymap and not evt.ControlDown(): continue
      if 'alt'   in keymap and not evt.AltDown()    : continue
      if 'shift' in keymap and not evt.ShiftDown()  : continue
      if 'meta'  in keymap and not evt.MetaDown()   : continue  #Dont ask me what key it is

      for key in keymap:
        try:
          if wx.__getattribute__(key)==keycode:
            great = True
        except:
          if not (keycode==0 or keycode>=256):
            if keycode < 27:
              char = chr(ord('a') + keycode-1)
            else:
              char = chr(keycode).lower()
            if char==key:
              great = True
      if great:
        print('Key combination triggered function:',self.funcs[i])
        self.funcs[i](evt,**self.params[i])
        break
    else:
       evt.Skip()


  # *************************************************************
  # *************************************************************
  def Append_Item(self, text ,func = None ,param = {} , menu_item = None):
    """
    text   : Text of the menu-item, use & to underline a letter
    func   : The function to be called when the users activates the menu
    params : The parameters for this funcion.
    item   : If specified, append the new item, after 'item'
    """
    if menu_item:
      for id,item in enumerate(self.items):
        if item == menu_item:
          break
      id = id + 1
    else:
      id = len(self.items)
    #print text,func

    # If no function specified, use the function of the item above
    if not ( func ) :
      func = self.funcs [ -1 ]
      param['text'] = text

    ##if isinstance(text,list) and func:
    ##if isinstance(text,list) :
    if Iterable ( text ) :
      for item in text:
        #print item
        self.Append_Item(item, func = func, param = {'text':item})
    else:
      self.Insert_Item(text, func, param, id)

  def Insert_Item(self, text ,func = None ,param = {} , menu_item = None):
    if isinstance(menu_item,int):
      id = menu_item
    if text == '-':
      return self.InsertSeparator(id)

    try:
      name,key = text.split('\t')
    except:
      name = text
      key  = ''
    keys = String2KeyCode(key)
    #print 'KEYS', keys
    if not func:
      # Lets find a nice function for this menu item
      cname = name.strip().replace(' ','_')
      func_names = ['On'+cname, 'On_'+cname,'On_'+name.split()[0]]
      for func_name in func_names:
        for i in dir(self.parent):
          if func_name.lower() == i.lower():
            func = self.parent.__getattribute__(i)
            break;
        if func: break;
      else:
        print("didn't find a function for this menu item:",name)
      #if func: print 'Hello, I found a nice function accompanying your menu item:'+i


    #item = self.Append ( wx.ID_ANY, text )
    item = self.AppendCheckItem ( wx.ID_ANY, text )
    ##self.parent.Bind ( wx.EVT_MENU, self.OnSelect, item )
    self.Bind ( wx.EVT_MENU, self.OnSelect, item )


    self.items.append ( item ) # We dont need IDs, we can always get them from items
    self.funcs.append ( func )
    self.keys.append  ( keys )
    self.params.append( param )

  def Prepend_Item(self,text,func = None, param = {}, item = None):
    print('Prepend_Item not yet available')

  # *************************************************************
  # *************************************************************
  def Get_Index_by_ID ( self, ID_sel ) :
    for i, item in enumerate ( self.items ) :
      if item.GetId() == ID_sel :
        break
    return i

  # *************************************************************
  # *************************************************************
  def Get_Item_by_ID ( self, ID_sel ) :
    i = self.Get_Index_by_ID ( ID_sel )
    return self.items [i]

  # *************************************************************
  # *************************************************************
  def OnSelect ( self, event ) :
    ID_sel = event.GetId ()
    for i, item in enumerate ( self.items ) :
      if item.GetId() == ID_sel :
        break
#    self.funcs[i](event, item) #Launch event
    #print 'S:??',self.funcs[i]
    #self.funcs[i](**self.params[i]) #Launch event
    #print 'EVVVENT', ID_sel, i, self.params, self.funcs
    self.funcs[i] ( event, **self.params[i] ) #Launch event


    # return the index
    # event.Int is only used in very special cases (what?)
    # so it's valid to use it here to transport the index
    ##event.Int = i
    event.Skip ()


  # *************************************************************
  # *************************************************************
  def SetEnabled ( self, index, value = True ) :
    item = self.items [ index ]
    item.Enable( bool(value) )
    #print dir(item)
    #ID = self.IDs [ index ]
    #value = bool ( value )
    #self.Enable ( ID, value )

  # *************************************************************
  # *************************************************************
  def SetChecked ( self, index, value = True ) :
    item = self.items [ index ]
    #print dir(item)
    item.SetCheckable ( True )
    if value :
      item.Check ( True )
    else :
      item.Check ( False )

# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class My_Popup_Menu_Stef ( wx.Menu ) :

  default = {}

  # edit
  default[0] = [
      _(0,'Cut'), _(0,'Copy'), _(0,'Paste'), _(0,'Delete')]

  # extended edit
  default[1] = [
      '-', _(0,'Cut'), _(0,'Copy'), _(0,'Paste'), _(0,'Delete'), '-' ]

  # tree
  default[2] = [
      _(0,'Insert New\tIns'), _(0,'Edit\tSpace'),
      '-', _(0,'Cut\tCtrl-X'), _(0,'Copy\tCtrl-C'),
      _(0,'Paste\tCtrl-V'), _(0,'Delete\tDel') ]

  # *************************************************************
  # itemset = None,  doesn't use a default set
  # *************************************************************
  def __init__ ( self, OnSelect, itemset = 0, pre = None, post = None ):
    wx.Menu.__init__ ( self )

    # Determine the itemlist = pre + set + after
    items = []
    if pre :
      items = pre
    if isinstance ( itemset, int ) :
      items += self.default [ itemset ]
    if post :
      items += post

    # generate the menu
    self.IDs = []
    self.items = []
    for text in items :
      if text == '-' :
        item = self.AppendSeparator()
      else :
        ##item = self.Append ( wx.ID_ANY, text )
        item = self.AppendCheckItem ( wx.ID_ANY, text)




        # order of these bindings is important
        # to be sure we get it first
        self.Bind ( wx.EVT_MENU, OnSelect, item )
        self.Bind ( wx.EVT_MENU, self.OnSelect, item )

        # only save IDs of real items
        self.IDs.append ( item.GetId() )
        self.items.append ( item )

      #UBUNTU problems: item.SetCheckable ( True )


  # *************************************************************
  # *************************************************************
  def Append_Item ( self, item ) :
    self.AppendItem ( item )
    #UBUNTU problems: item.SetCheckable ( True )

  # *************************************************************
  # *************************************************************
  def Get_Index_by_ID ( self, ID_sel ) :
    for i, ID in enumerate ( self.IDs ) :
      if ID == ID_sel :
        break
    return i

  # *************************************************************
  # *************************************************************
  def Get_Item_by_ID ( self, ID_sel ) :
    i = self.Get_Index_by_ID ( ID_sel )
    return self.items [i]

  # *************************************************************
  # *************************************************************
  def OnSelect ( self, event ) :
    ID_sel = event.GetId ()
    for i, ID in enumerate ( self.IDs ) :
      if ID == ID_sel :
        #Value = self.items [i]
        break
    # return the index
    # event.Int is only used in very special cases (what?)
    # so it's valid to use it here to transport the index
    event.Int = i
    #event.Value = Value
    event.Skip ()

  # *************************************************************
  # *************************************************************
  def SetEnabled ( self, index, value = True ) :
    ID = self.IDs [ index ]
    value = bool ( value )
    self.Enable ( ID, value )

  # *************************************************************
  # *************************************************************
  def SetChecked ( self, index, value = True ) :
    item = self.items [ index ]
    ##item.SetCheckable ( True )    bestaat niet meer in Python 3
    ##item.Kind = wx.ITEM_CHECK     can't set attribute
    if value :
      item.Check ( True )
    else :
      item.Check ( False )


## Backwards compatibility function
def My_Popup_Menu(self,*args, **kwargs):
  #print 'DE COMMANDOS', self, args, kwargs
  if 'Bind' in dir(self):
    return My_Popup_Menu_Robbie(self,*args,**kwargs)
  else:
    ##print '***** Decepr. Warning: Old My_Popup_Menu Used'
    return My_Popup_Menu_Stef(self,*args,**kwargs)



default_menus = [
      ['&File',     [ ( '&New/Open\tCtrl+O', 'Open'),
                      ( '&Save\tCtrl+S',     'Save'),
                      ( 'Save &As ...',      'Save_As'),
                      ( '-' ),
                      ( '&Print\tCtrl+P',    'Print'),
                      ( 'Pr&int Preview',    'Print_Preview'),
                      ( 'Page Setup',        'Page_Setup'),
                      ( '-' ),
                      ( 'Export-Launch\tF8',     'Export_Launch'),
                      ( '&Export',           'Export'),
                      ( '-' ),
                      ( '&Close',            'Close') ]],
      ['&Edit',     [ ( '&ToDo',             'ToDo'),
                      ( '&Edit',             'Edit') ]],
      ['&Settings', [ ( '&ToDo',             'ToDo'),
                      ( '&Font',             'Font') ]],
      ['&View',     [ ( '&ToDo',             'ToDo'),
                      ( '&View',             'View') ]],
      ['&Help',     [ ( 'PyLab_&Works'           ,'PyLab_Works_Help' ),
                      ( 'Many Links'             ,'Flappie_Links'    ),
                      ( '-' ),
                      ( 'Send &Bug Report'       ,'Send_Bug_Report'  ),
                      ( '&Ask OnLine Assistance' ,'Ask_Assistance'   ),
                      ( 'Check For &New Version' ,'Check_New_Version'),
                      ( '&About'                 ,'About'            ) ]]]


# ***********************************************************************
# Dummy Menu Event Handler
# ***********************************************************************
class Menu_Event_Handler(object):
  #def OnMenu_Print ( self, event ) :
  #  print 'Print_WEG'

  #def OnMenu_Print_Preview ( self, event ) :
  #  print 'Print Pre WEG'

  def OnMenu_Font ( self, event ) :
    data = wx.FontData ()
    data.EnableEffects ( True )
    #data.SetColour ( self.curClr )
    data.SetInitialFont ( self.My_Frame.GetFont () )

    dlg = wx.FontDialog ( self, data )

    if dlg.ShowModal() == wx.ID_OK:
      data = dlg.GetFontData()
      font = data.GetChosenFont()
      colour = data.GetColour()
      self.My_Frame.SetFont ( font )
      Show_Message ( """Het ingestelde font wordt pas aktief
Nadat het programma opnieuw is gestart.""")

  def OnMenu_Flappie_Links ( self, event ) :
    webbrowser.open ( 'http://pic.flappie.nl' )

  def OnMenu_PyLab_Works_Help ( self, event ) :
    webbrowser.open ( 'http://pic.flappie.nl' )

  def OnMenu_Check_New_Version ( self, event ) :
    pass

  def OnMenu_About ( self, event ) :
    import PyLab_Works_Globals as PG
    from wx.lib.wordwrap import wordwrap
    width = 450
    info = wx.AboutDialogInfo()
    info.Name =  'PyLab Works'

    Path = sys._getframe().f_code.co_filename
    Path = os.path.split ( Path ) [0]
    info.SetIcon ( wx.Icon (
      Nice_Path ( Path,
      '../pictures/ph_32.ico'), wx.BITMAP_TYPE_ICO ) )
    info.Version = PG.Version_Nr
    info.Copyright = "(C) 2007 .. 2008 Stef Mientki"
    info.Description = wordwrap(
      _(0, 'PyLab_Works is easy to use, highly modular,'
      'visual development enviroment,'
      'specially aimed at education and (scientific) research.' )
      , width, wx.ClientDC(self))
    info.WebSite = ("http://pic.flappie.nl/", "Home Page")

    info.Developers = [
      _(0, "Stef Mientki, special thanks to :\n"
      "\n"
      "the people who created Python\n"
      "python-list@python.org\n"
      "wxPython-users-list (especially Robin Dunn)\n"
      "and Erik Lechak for creating OGLlike.py" )
       ]
    licenseText = "for all I added: BSD\n" \
      "Python: Python Software Foundation License (PSFL)\n" \
      "MatPlotLib: Python Software Foundation License (PSFL)\n" \
      "wxPython: L-GPL\n" \
      "openGL: Free Software Foundation License B (BSD / Mozilla)"
    info.License = wordwrap(licenseText, width, wx.ClientDC(self))
    wx.AboutBox ( info )


  def OnMenu_Ask_Assistance ( self, event ) :
    os.system ( 'TeamViewer_Setup.exe' )

  def OnMenu_Send_Bug_Report ( self, event ) :
    import win32api
    win32api.ShellExecute ( 0,'open','mailto: punthoofd@fastmail.fm', None,None,0)
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Class_StatusBar ( self, N_or_Widths = 3 ) :
  """
  Creates a statusbar, with default 3 equally sized fields.
  For equally sized fields you can specify another number of fields
  or you can specify a list of field-widths.
  ( Negative field-widths will claim a fraction )
  In the latter case the number of fields is automatically calculated.
  """
  SB = self.CreateStatusBar ()
  if isinstance ( N_or_Widths, int ) :
    SB.SetFieldsCount ( N_or_Widths )
  else :
    SB.SetFieldsCount  ( len ( N_or_Widths ) )
    SB.SetStatusWidths ( N_or_Widths )
  return SB

# ***********************************************************************
# ***********************************************************************
class Class_Menus ( wx.MenuBar, Menu_Event_Handler ) :
  def __init__ ( self, My_Frame, My_Menus = default_menus ) :
    wx.MenuBar.__init__ ( self )
    self.My_Frame = My_Frame
    self.My_Menus = My_Menus
    self.Menu_Owners = {}
    self.My_Frame.Bind ( wx.EVT_MENU, self._Event_Distributor )

    Help_Menu = None
    Menu_Events = dir ( Menu_Event_Handler )
    for menu in My_Menus:
      menu_top = wx.Menu ()

      if menu [0] == '&Help' :
        Help_Menu = menu_top

      for item in menu [ 1 ] :
        if item[0] == '-' :
          menu_item = menu_top.AppendSeparator ()
        else :
          #menu_item = menu_top.Append ( wx.ID_ANY, item[0] )
          menu_item = menu_top.AppendCheckItem ( wx.ID_ANY, item[0] )

          ## MOET DIT NOG ??
          # assign the menu-ID to "My_Frame.ID_...."
          #   My_Frame.ID_Send_Bug_Report = menu_item.GetId()
          setattr ( self.My_Frame, 'ID_' + item[1], menu_item.GetId() )
          ## einde moet dit nog ??

          # First test if My_Frame has a method for this menu-item
          if hasattr ( self.My_Frame, 'OnMenu_'+item[1] ) :
            OnMenu_Function = getattr ( self.My_Frame, 'OnMenu_'+item[1] )
            # should work both :
            self.My_Frame.Bind ( wx.EVT_MENU, OnMenu_Function, id = menu_item.GetId() )
            #My_Frame.Bind ( wx.EVT_MENU, OnMenu_Function, menu_item )

          else : # Test if myself has a method for this menu-item
            Event = 'OnMenu_'+item[1]
            if Event in Menu_Events :
              self.My_Frame.Bind ( wx.EVT_MENU, eval ( 'self.' + Event ),
                                   id = menu_item.GetId() )
            else :
              menu_item.Enable ( False )

      self.Append ( menu_top, menu[0] )
      #self.AppendCheckItem ( menu_top, menu[0] )

    # Search CHM files, Add from globals config file
    self.Extra_Help_Items = {}
    if Help_Menu :
      #print 'PPPP3',Application.Application
      Help_Anchor = 2

      # find CHM help files in own program section
      CHM_Files = Find_Files ( '../chm_help', '*.chm', RootOnly = True )
      for file in CHM_Files :
        menu_item = Help_Menu.Insert ( Help_Anchor, wx.ID_ANY, file[1] )
        ID = menu_item.GetId()
        self.My_Frame.Bind ( wx.EVT_MENU, self.OnMenu_Extra_Help, id = ID )
        self.Extra_Help_Items [ ID ] =  \
          os.path.join ( '..', 'chm_help', file [1] + '.chm' ).replace('\\','/')
        Help_Anchor += 1

      # Get items from gloabls config file
      Ini = Application.General_Global_Settings
      Ini.Section = 'Help Paths'
      Sections = Ini.Get_Section ()
      for Section in Sections :
        menu_item = Help_Menu.Insert ( Help_Anchor, wx.ID_ANY, Section[0] )
        ID = menu_item.GetId()
        self.My_Frame.Bind ( wx.EVT_MENU, self.OnMenu_Extra_Help, id = ID )
        self.Extra_Help_Items [ ID ] = Section[1]
        Help_Anchor += 1

    #for item in self.Extra_Help_Items :
    #  v3print ( 'HELP:', item, self.Extra_Help_Items [item] )

    # apply the menubar
    self.My_Frame.SetMenuBar ( self )
    self.My_Frame.Bind ( wx.EVT_MENU_OPEN, self._On_Menu_Popup )
    #self.My_Frame.Bind ( wx.EVT_MENU, self.test1 )

  # *******************************************************
  def OnMenu_Extra_Help ( self, event ) :
    """
    Extra items in the Help-menu
    """
    ID = event.GetId ()
    if ID in self.Extra_Help_Items :
      v3print ( self.Extra_Help_Items [ ID ] )

      URL = self.Extra_Help_Items [ ID ].replace ( '\\', '/' )
      if '.chm' in URL :
        Launch_CHM ( URL )

      elif not ( os.path.isfile ( URL ) ) :
        webbrowser.open ( URL )

      else :
        webbrowser.open ( URL )

  # *******************************************************
  def _On_Menu_Popup (self, event ) :
    """
    Searches for the focussed control,
    Steps through all the items in the selected menu
    and Enables the menu-item, if the focussed control supports it
    Or if
    """
    #Control = self.FindFocus()
    # Sometimes event.GetMenu = None !!
    ##print 'HHHYY',self.FindFocus(), event.GetMenu()
    if event.GetMenu () :
      Control = self.My_Frame.FindFocus()
      MO = self.Menu_Owners

      #print 'Focusedz', Control

      """
      v3print ( 'Focused', Control )
      for i in MO :
        v3print ( i,':',MO[i][0] )
        for item in MO[i][1:] :
          v3print ( '   ', item )
      """

      ##print event.GetMenu().GetMenuItems()
      for item in event.GetMenu().GetMenuItems() :
        ID = item.GetId()
        if ID in MO :
          item.Enable ( ( Control in MO [ID] [0] ) or \
                        ( self.My_Frame in MO [ID] [0] ) )

  # ************************************************
  def _Event_Distributor ( self, event ) :
    ID = event.GetId ()
    MO = self.Menu_Owners
    if ID in MO :
      Control = self.My_Frame.FindFocus()

      # first test if the event is bound to the mainframe
      if self.My_Frame in MO [ID] [0] :
        i = MO [ID] [0].index ( self.My_Frame )
        MO [ID] [1][i] ( event )

      # if not, test if it's bound to the focussed control
      elif Control in MO [ID] [0] :
        i = MO [ID] [0].index ( Control )
        MO [ID] [1][i] ( event )

    # To prevent double triggers, no Skip
    # but it doesn't work perfectly !!
    #event.Skip ()

  # ************************************************
  def Bind_MenuItem ( self, Menu, Item, Completion, Owner = None ) :
    """
    Bind the function Completion to Menu | Item event
    and enables this menu item.
    It's possible to add new Menus and Items
    """
    #v3print ( 'Bind_Menu',Menu,Item,Completion,Completion.im_self )
    menu_ID = self.FindMenuItem ( Menu, Item )
    #v3print ( 'Bind_MenuItem', Menu, Item, menu_ID )
    if menu_ID == wx.NOT_FOUND :
      # if menu doesn't exists, create it
      if self.FindMenu ( Menu ) == wx.NOT_FOUND :
        menu_top = wx.Menu ()
        # insert the items before the last one (Help)
        self.Insert ( self.GetMenuCount () - 1, menu_top, Menu )

      menu_ID = self.FindMenuItem ( Menu, Item )
      # if menuitem doesn't exists, create it
      if menu_ID == wx.NOT_FOUND :
        pos = self.FindMenu ( Menu )
        menu_top = self.GetMenu ( pos )

        ##menu_item = menu_top.Append ( wx.ID_ANY, Item )
        menu_item = menu_top.AppendCheckItem ( wx.ID_ANY, Item )

        menu_ID = self.FindMenuItem ( Menu, Item )

    if menu_ID != wx.NOT_FOUND :
      menu_item = self.FindItemById ( menu_ID )
      menu_item.Enable ( True )
      #self.My_Frame.Bind ( wx.EVT_MENU, Completion, id = menu_ID )

      # add owner and completion to list
      if not ( Owner ) :
        Owner = Completion.__self__
      MO = self.Menu_Owners
      if not ( menu_ID in MO ) :
        MO [ menu_ID ] = ( [], [] )
      MO = self.Menu_Owners [ menu_ID ]
      if not ( Owner in MO [0] ) :
        MO[0].append ( Owner )
        MO[1].append ( Completion )

      """
      print Completion,Completion.im_self.GetName()
      try :
        print Completion.im_self.Filename,Completion.im_self.GetName()
      except:
        pass
      """

    return menu_item
# ***********************************************************************


# ***********************************************************************
# TODO: Toggling should be done on each group within separators
# TODO: different sizes 16/24/32
# TODO: more types than "Toggle"
# ***********************************************************************
class Create_ToolBar_Items ( object ) :
  def __init__ ( self, ToolBar, ToolItems, On_Event, parent, size = 24,
                 Dont_Group = False ) :
    self.ToolBar    = ToolBar
    self.ToolItems  = ToolItems
    self.User_Event = On_Event
    self.IDs        = []
    self.Dont_Group = Dont_Group

    tsize = ( size, size )
    self.IL = Get_Image_List ( size )
    ToolBar.SetToolBitmapSize ( tsize )

    self.Enabled_Tools = []

    # *******************************************************
    # determine the groups and their sizes
    # *******************************************************
    self.groups = []
    counter     = 0
    for item in ToolItems :
      if item :
        counter += 1
      elif not ( Dont_Group ) :
        self.groups.append ( counter )
        counter = 0
    if counter > 0 :
      self.groups.append ( counter )
    #print groups


    # *******************************************************
    # add the toolbar items, select the first one
    # and for groups of size 1, implement the togglebutton
    # *******************************************************
    group = 0
    First = True
    Accel_Table = []
    for item in ToolItems :
      if item :

        bmp = self.IL.GetBitmap ( item[0] )
        ID = wx.NewId()

        if Dont_Group or self.groups [ group ] == 1 :
          ToolBar.AddCheckLabelTool ( ID, item[1], bmp, shortHelp = item[1] )
        else :
          ToolBar.AddLabelTool      ( ID, item[1], bmp, shortHelp = item[1] )
          ToolBar.EnableTool ( ID, First )
          First = False
        self.IDs.append ( ID )
        ToolBar.GetParent().Bind ( wx.EVT_TOOL, self.My_On_Click, id = ID )

        # test if there's a accelerator key
        b = item[1].split ( '(' )
        if len ( b ) > 1 :
          b = b[1].split ( ')' ) [0]
          if b :
            #print 'ACCEL',b
            b = b.split ( '-' )

            # get all special flags
            Accelerator_Flags = {
               'Ctrl' : wx.ACCEL_CTRL,
               'Shift': wx.ACCEL_SHIFT,
               'Alt'  : wx.ACCEL_ALT }
            flags = wx.ACCEL_NORMAL
            while len(b) > 1 :
              flag = b.pop ( 0 )
              flags |= Accelerator_Flags [ flag ]

            # determine the key
            if ( b[0][0] == 'F' ) and ( len ( b[0] ) > 1 ) :
              key = eval ( 'wx.WXK_' + b[0] )
            else :
              key = ord ( b[0][0] )

            Accel_Table.append ( ( flags, key, ID ))
            #print 'ACCELERATION',flags, key, ID
            parent.Bind ( wx.EVT_TOOL, self.My_On_Click_Accelerator, id=ID )
            #parent.Bind ( wx.EVT_TOOL, On_Event, id=self.TB.IDs [ 1 ] )
      else :
        ToolBar.AddSeparator ()
        if not ( Dont_Group ) :
          group += 1
          First = True

    # now realize the toolbar
    ToolBar.Realize()

    if Accel_Table :
      #ToolBar.SetAcceleratorTable ( wx.AcceleratorTable ( Accel_Table ) )
      #ToolBar.GetParent().SetAcceleratorTable ( wx.AcceleratorTable ( Accel_Table ) )
      parent.SetAcceleratorTable ( wx.AcceleratorTable ( Accel_Table ) )
      print('TOOLBAR, redefining Accelerator table !!')
    self.Accel_Table = Accel_Table

  # *******************************************************
  # *******************************************************
  def Enable_Buttons ( self, values ) :
    if not ( isinstance ( values, list ) ) :
      values = list ( values )
    self.Enabled_Tools = values
    TF = [ False, True ]
    for i in range ( len ( values ) ) :
      self.ToolBar.EnableTool ( self.IDs [i], TF [ values [i] ] )

  # *******************************************************
  # intercepts the key press, calculates the absolute index
  # disables the selected item and
  # enables all the other items in the group
  # calls the user completion routine
  # If the button is "pressed" through an accellerator key,
  # an extra flag is set
  #   (special meant for 2 buttons having the same accellerator key)
  # *******************************************************
  def My_On_Click_Accelerator ( self, event ) :
    event.Accelerator = True
    self.My_On_Click ( event )

  def Set_Tool_State ( self, My_Index, State ) :
    index = self.IDs [ My_Index ]
    self.ToolBar.ToggleTool ( index, State )

  def My_On_Click ( self, event ) :
    try :
      event.Started_by_Accelerator = event.Accelerator
      event.Accelerator = None
    except :
      event.Accelerator = None
      event.Started_by_Accelerator = event.Accelerator


    self.Old_Enabled_Tools = copy.copy ( self.Enabled_Tools )

    event.My_Index = self.IDs.index ( event.GetId () )
    print('jkal', self.ToolBar.GetToolState( event.GetId()))

    # determine the group
    group = 0
    total = self.groups [ group ]
    while total <= event.My_Index :
      group += 1
      total = total + self.groups [ group ]
    start = total - self.groups [ group ]

    # enable every group member except itself
    if not ( self.Dont_Group ) :
      if self.groups [ group ] > 1 :
        for i in range ( self.groups [ group ] ) :
          #print 'mmmmenu',group,i,start,self.Enabled_Tools
          # Enabled_Tools is an empty list ERRRRRR
          self.ToolBar.EnableTool ( self.IDs [ start + i ], True )
          self.Enabled_Tools [ start + i ] = 1

        self.ToolBar.EnableTool ( event.GetId (), False )
        self.Enabled_Tools [ event.My_Index ] = 0

    #print start, self.groups [ group ], event.My_Index, group, total, self.groups
    self.User_Event ( event )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( My_Frame_Class ) :
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )

    # Add a dynamic menu to the menubar
    menu_dynamic_items = []
    for i in range ( 10 ) :
      menu_dynamic_items.append ( ( 'Demo ' + str(i) , 'Demo' + str(i) ) )
    default_menus.insert ( 1, ['Demos', menu_dynamic_items ] )

    GUI = """
#    NN_SplitterHor
    self.Splitter  ,SplitterHor
      NN_wx.Panel
        NN_wx.StaticText  ,label = "Signal1b", pos = (10, 50)
      NN_PanelVer, 01
        tb         ,wx.ToolBar
        NN_PanelVer  ,01
          NN_wx.StaticText  ,label = "Signal1b", pos = (10, 50)
          self.Memo   ,wx.TextCtrl
    """
    #exec ( Create_wxGUI ( GUI ) )
    self.wxGUI = Create_wxGUI ( GUI ) #, Ini_File_String = 'self.Ini_File' )

    # Create the menu
    MenuBar = Class_Menus ( self )

    # *******************************************************
    # *******************************************************
    ToolItems = [
      ( 83, 'Disable Breakpoints'   ),
      (                             ),
      ( 91, 'Pauze  (F9)'           ),
      ( 90, 'Run in Debugger  (F9)' ),
      ( 92, 'Step  (F8)'            ),
      ( 93, 'Step Into  (Ctrl-F8)'  ),
      (                             ),
      ( 22, 'Restart (Shift-F9)'    ),
      (                             ),
      ( 65, 'Run Extern  (Alt-F9)'  ),
    ]
    self.TB = Create_ToolBar_Items  ( tb, ToolItems, self.On_ToolBar, self )
    Debug_Button_Init    = ( 1,  0,1,1,1,  0 )
    self.TB.Enable_Buttons ( Debug_Button_Init )
    # *******************************************************

    # Bind events, for the dymanic menu-items, through the whole range
    self.Bind ( wx.EVT_MENU, self.OnMenu_Demos, id=self.ID_Demo0, id2=self.ID_Demo9  )
    MenuBar.Bind_MenuItem ( 'File', 'Save', self._On_Menu_FileSave )


    # *************************************************************
    self.Popup_Menu_Test = My_Popup_Menu (  self.Memo, 2, func = self.CallBack )

  # ******************************************************
  def CallBack ( self, event, text ) :
    print(' asasa', text, event)
    if text.startswith ( 'Copy' ) :
      self.Popup_Menu_Test.Append_Item ( 'Beer')

  # ******************************************************
  def OnMenu_numpy_Help ( self, event ) :
    pass

  # ******************************************************
  def OnMenu_Open ( self, event = None ) :
    DefaultLocation = ''
    FileName = AskFileForOpen ( DefaultLocation, FileTypes = '*.py' )
    if FileName :
      print(FileName)

  # ******************************************************
  def _On_Menu_FileSave ( self, event = None ):
    print('lsdfsa')

  # ******************************************************
  # ******************************************************
  def On_ToolBar ( self, event ) :
    #tb = event.GetEventObject()

    _ID = event.GetId()
    ID  = event.My_Index
    State= self.TB.ToolBar.GetToolState ( _ID )

    #print 'TOOL', ID, State

    if ID == 0 :
      bmp = self.TB.IL.GetBitmap ( ( 83, 88 )[ State ] )
      self.TB.ToolBar.SetToolNormalBitmap ( _ID, bmp )

    else :
      pass
    #tb.EnableTool ( ID, not( tb.GetToolEnabled ( ID ) ) )

  # *******************************************************
  # *******************************************************
  # Action for dynamic events
  def OnMenu_Demos ( self, event ) :
    print(event.GetId() - self.ID_Demo0)
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == '__main__':
  My_Main_Application ( Simple_Test_Form )
# ***********************************************************************
pd_Module ( __file__ )


