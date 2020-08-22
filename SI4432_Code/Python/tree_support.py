from __future__ import print_function
from __future__ import absolute_import
#from __future__ import absolute_import
from builtins import str
from builtins import range
# ***********************************************************************
import __init__
from language_support import  _

# ***********************************************************************
__doc__ = """
TreeControl with drag and drop, RM-menu, etc
based on CT.CustomTreeCtrl

License: freeware, under the terms of the BSD-license
Copyright (C) 2008 Stef Mientki
"""

# ***********************************************************************
_Version_Text = [

[ 1.18, '18-08-2015', 'Stef Mientki',
'Test Conditions:', (),
"""
 -  On Delete Item: Callback parameters changed
       self.Tree_Completion_CallBack ( 'Deleted', itemtext, level, parent )
"""  ],

[ 1.17, '18-09-2012', 'Stef Mientki',
'Test Conditions:', (),
"""
- Tree_2_Html_File added
"""  ],

[ 1.16, '6-5-2012', 'Stef Mientki',
'Test Conditions:', (),
"""
- Enable_External_Drop added
"""  ],

[ 1.15, '03-08-2011', 'Stef Mientki',
'Test Conditions:', (),
"""
- Tree_2_Inifile, had a huge bug, when there were subnodes !!
"""  ],

[ 1.14, '30-01-2011', 'Stef Mientki',
'Test Conditions:', (),
"""
- Get_Children_Expanded, added
- Set_Children_Expanded, added
"""  ],


[ 1.13, '14-12-2010', 'Stef Mientki',
'Test Conditions:', (),
"""
- Lines_2_Tree: image indices -1 are not anymore replaced by 15/16
- Tree_2_IniFile replaced by a version dat also stores extended pydata for root nodes
"""  ],

[ 1.12, '19-10-2010', 'Stef Mientki',
'Test Conditions:', (),
"""
- String_2_TreeExpand and TreeExpand_2_String added
  can be used to save and restore the tree expansion in a config file
"""  ],


[ 1.11, '10-09-2010', 'Stef Mientki',
'Test Conditions:', (),
"""
- Enumerate_Copy2 added (also copies images, but not PyData)
- Delete function can be blocked by setting ReadOnly Flag
- Delete_Allowed added, another way to block del of indivudual nodes
"""  ],

[ 1.10, '02-08-2010', 'Stef Mientki',
'Test Conditions:', (),
"""
- IniFile_2_Tree returns True when succeeded
"""  ],

[ 1.9, '12-05-2010', 'Stef Mientki',
'Test Conditions:', (),
"""
- Enumerate_Node added
"""  ],

[ 1.8, '04-02-2010', 'Stef Mientki',
'Test Conditions:', (),
"""
- Delete_Item extended with return values :
      return True, level, itemtext, parent
"""  ],

[ 1.7, '10-01-2010', 'Stef Mientki',
'Test Conditions:', (),
"""
- added DataBase_TreeCtrl
- bug in using style_sub, blocking editing still doesn't work,
  other than by catching key events
"""  ],

[ 1.6, '13-10-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
 - CollapseAll added
""" ) ],

[ 1.5, '10-10-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
 - Autoread of JALcc trees added
""" ) ],

[ 1.4, '29-07-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
   - Lines_2_Tree     added
   - Add_PyFile_Info  added
""" ) ],

[ 1.3, '05-06-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
   - ',' not longer supported as splitter character
""" ) ],

[ 1.2, '27-05-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
   - Get_Item_Level_MainParent bug if no root or root changed
""" ) ],

[ 1.1, '24-05-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
   - uses '~' instead of ',' as the splitter character
   - uses LAST '=' as name-value splitter
   - old files are still read correctly
   - edit spaces in treenode possible
   - fileextension can be specified (default = '.tree' )
""" ) ],

[ 1.0, '10-03-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
    - orginal release
""" ) ]
]
# ***********************************************************************

import os
import sys

import wx

"""
subdirs = [ '../Lib_Extensions' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""

#import customtreectrl_SM as CT


from   inifile_support import inifile
#from   picture_support import Get_Image_List_16
from   picture_support import Get_Image_List
from   file_support    import *
from   menu_support    import My_Popup_Menu # **** TODO more
from   dialog_support  import *
from   doc_support     import *
from   grid_support    import CT_Names
from   utility_support import NoCase_List
from   html_support    import RGB_2_HTML_Color


# ***********************************************************************
# ***********************************************************************
class Tree_DropTarget ( wx.PyDropTarget ) :
  """
Implements drop target functionality to receive files, bitmaps and text
  """
  def __init__ ( self, parent ) :
    wx.PyDropTarget.__init__ ( self )
    self.parent = parent
    self.Data_Object = wx.DataObjectComposite()  # the dataobject that gets filled with the appropriate data

    self.Data_Object_File = wx.FileDataObject()
    self.Data_Object_Text = wx.TextDataObject()
    self.Data_Object.Add ( self.Data_Object_File )
    self.Data_Object.Add ( self.Data_Object_Text )
    #self.Data_Object_Bmp = wx.BitmapDataObject()
    #self.Data_Object_Url = wx.URLDataObject()
    self.SetDataObject ( self.Data_Object )

    """
DF_BITMAP 2
DF_DIB 8
DF_DIF 5
DF_ENHMETAFILE 14
DF_FILENAME 15
DF_HTML 30
DF_INVALID 0
DF_LOCALE 16
DF_MAX 31
DF_METAFILE 3
DF_OEMTEXT 7
DF_PALETTE 9
DF_PENDATA 10
DF_PRIVATE 20
DF_RIFF 11
DF_SYLK 4
DF_TEXT 1
DF_TIFF 6
DF_UNICODETEXT 13
DF_WAVE 12
   """

  def OnData ( self, x, y, Data ):
    """
Handles drag/dropping files/text or a bitmap
    """
    if self.GetData():
      Data_Format = self.Data_Object.GetReceivedFormat().GetType()
      print(Data_Format)

      Filenames = []
      if Data_Format in [ wx.DF_UNICODETEXT, wx.DF_TEXT ] :

        text = self.Data_Object_Text.GetText()
        text = text.replace('\r\n','\n')
        text = text.replace('\r','\n')
        Filenames = text.split('\n')

      elif Data_Format == wx.DF_FILENAME:
        Filenames = self.Data_Object_File.GetFilenames()

      if Filenames:
        HitTest = self.parent.HitTest( wx.Point(x,y) )
        item = HitTest[0]
        print(HitTest)
        print('DROP Files:', Filenames)
        ##print dir(item)
        self.parent.Drop_Items ( item, Filenames )
        return
        HitTest = self.parent.Tree.HitTest( wx.Point(x,y) )
        item = HitTest[0]
        self.parent.AddItem(item,filenames)

    return Data  # you must return this
# ***********************************************************************


# ***********************************************************************
# CustomTreeCtrl Demo Implementation
# !!!!!!!! CHANGES to CustomTreeCtrl: !!!!!!!!!!!!
# line 949 removed  "|wx.TE_MULTILINE"
# line 1042 ...

# PyData [0] = X X X X   X X X X
#                            | +--- True = Node Checked (not used at this moment)
#                            +----- True = Node Expanded
# PyData [1] = Normal Node Icon
# PyData [2] = Expanded Node Icon
"""
 |  HitTest(self, point, flags=0)
 |      Calculates which (if any) item is under the given point, returning the tree item
 |      at this point plus extra information flags. Flags is a bitlist of the following:
 |
 |      TREE_HITTEST_ABOVE            above the client area
 |      TREE_HITTEST_BELOW            below the client area
 |      TREE_HITTEST_NOWHERE          no item has been hit
 |      TREE_HITTEST_ONITEMBUTTON     on the button associated to an item
 |      TREE_HITTEST_ONITEMICON       on the icon associated to an item
 |      TREE_HITTEST_ONITEMCHECKICON  on the check/radio icon, if present
 |      TREE_HITTEST_ONITEMINDENT     on the indent associated to an item
 |      TREE_HITTEST_ONITEMLABEL      on the label (string) associated to an item
 |      TREE_HITTEST_ONITEMRIGHT      on the right of the label associated to an item
 |      TREE_HITTEST_TOLEFT           on the left of the client area
 |      TREE_HITTEST_TORIGHT          on the right of the client area
 |      TREE_HITTEST_ONITEMUPPERPART  on the upper part (first half) of the item
 |      TREE_HITTEST_ONITEMLOWERPART  on the lower part (second half) of the item
 |      TREE_HITTEST_ONITEM           anywhere on the item
 |
 |      Note: both the item (if any, None otherwise) and the flag are always returned as a tuple.
 |
"""
# ***********************************************************************
#class Custom_TreeCtrl_Base ( CT.CustomTreeCtrl_Modified_SM ) :
from wx.lib.agw import customtreectrl as CT
class Custom_TreeCtrl_Base ( CT.CustomTreeCtrl ) :

  # *************************************************************
  # Creation of the treecontrol
  # *************************************************************
  def __init__( self, parent, root_title = _(0,'No Root Title' ),
                name          = 'CT-Tree',
                No_Image_List = False,
                style_add     = None,
                style_sub     = None ) :

    self.parent        = parent


    self.ReadOnly      = False

    self.Popup_Allowed  = True
    self.Cut_Allowed    = True
    self.Insert_Allowed = True
    self.Edit_Allowed   = True
    self.Cut_Allowed    = True
    self.Paste_Allowed  = True
    self.Del_Allowed    = True

    self.Tree_Completion_CallBack = None


    # *************************************************************
    # tree style to be used
    # *************************************************************
    tree_style = \
                  CT.TR_HAS_BUTTONS \
                 | CT.TR_FULL_ROW_HIGHLIGHT \
                 | CT.TR_HIDE_ROOT \
                 | CT.TR_LINES_AT_ROOT \
                 | CT.TR_SINGLE \
                 | wx.WANTS_CHARS \
                 | CT.TR_EDIT_LABELS \
                 | CT.TR_HAS_VARIABLE_ROW_HEIGHT \
                 | wx.NO_BORDER
                 #| wx.NO_3D \
                 #| wx.SUNKEN_BORDER \
    #"""
    if style_add :
      tree_style |= style_add

    # Remove the styles "style_sub", by performing
    # style = ( style OR sub_style ) XOR sub_style
    if style_sub :
      tree_style |= style_sub
      tree_style ^= style_sub
    #"""
    ##tree_style = wx.TR_HIDE_ROOT

    # *************************************************************
    # For some reason the tree styles are now splited in
    # a general wx-style (style), and a specific tree_style (agwStyle)
    # For now just hope, the styles dont overlap
    #
    # *************************************************************
    Base_Tree_Styles = 0
    for i in (dir(CT)):
      if i.startswith('TR_'):
        Base_Tree_Styles |= CT.__getattribute__(i)
    agwStyle =  Base_Tree_Styles & tree_style
    wxStyle  = ~Base_Tree_Styles & tree_style




    # *************************************************************
    # create the tree and assign imagelist
    # *************************************************************
    #CT.CustomTreeCtrl_Modified_SM.__init__ ( self, parent,
    CT.CustomTreeCtrl.__init__ ( self, parent,
                                 style = wxStyle,
                                 agwStyle = agwStyle,
                                 name = name )
    self.No_Image_List = No_Image_List
    self.SetFont ( self.Parent.GetFont () )

    self.AddRoot ( root_title )
    Root = self.GetRootItem ()
    if not ( self.No_Image_List ) :
      self.imagelist = Get_Image_List ()
      self.SetImageList ( self.imagelist )
    self.Item_Copy = False
    self.Move_Action = False

    # we also give the root images, so we can use it as copy source
    PyData = []
    PyData.append ( 0 )
    PyData.append ( 78 )
    PyData.append ( 79 )
    self.SetPyData ( Root, PyData )


    # *************************************************************
    # popup menus
    # *************************************************************
    PU = My_Popup_Menu ( self.OnPopupItemSelected, 2 )
    self.Popup_Menu_Tree = PU

    #self.Bind ( wx.EVT_CONTEXT_MENU, self.OnShowPopup )
    #In Ubuntu context menu doesn't appear
    #self.Bind ( wx.EVT_RIGHT_DOWN, self.OnShowPopup )
    #self.Bind ( wx.EVT_RIGHT_UP, self.OnShowPopup )
    self.Bind ( wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnShowPopup )

    """
    default[2] = [
      'Insert New\tIns', 'Edit',
      '-',
      'Cut\tCtrl-X', 'Copy\tCtrl-C', 'Paste\tCtrl-V', 'Delete\tDel' ]
    """
    self.Popup_Menu_Tree.SetEnabled ( 4, self.Item_Copy )

    ### IS DONE BY POPUP MENU
##    # Create Bindings for the menu events
##    self.Bind ( wx.EVT_MENU, self.On_Insert, PU.items [0] ) # Ins
##    self.Bind ( wx.EVT_MENU, self.On_Edit,   PU.items [1] ) # Ins
##    self.Bind ( wx.EVT_MENU, self.On_Cut,    PU.items [2] ) # ^X
##    self.Bind ( wx.EVT_MENU, self.On_Copy,   PU.items [3] ) # ^C
##    self.Bind ( wx.EVT_MENU, self.On_Paste,  PU.items [4] ) # ^V
##    self.Bind ( wx.EVT_MENU, self.On_Delete, PU.items [5] ) # Del

    ### IS DONE BY POPUP MENU
##    # Create bindings for accelerator keys
##    aTable = wx.AcceleratorTable ( [ \
##        ( wx.ACCEL_NORMAL, wx.WXK_INSERT, PU.items[0].GetId() ),
##        #( wx.ACCEL_NORMAL, wx.WXK_SPACE,  PU.items[1].GetId() ),
##        ( wx.ACCEL_CTRL,   ord('X'),      PU.items[2].GetId() ),
##        ( wx.ACCEL_CTRL,   ord('C'),      PU.items[3].GetId() ),
###        ( wx.ACCEL_CTRL,   ord('V'),      PU.items[4].GetId() ),
##        #( wx.ACCEL_NORMAL, wx.WXK_DELETE, PU.items[5].GetId() ),
##        ])
##    self.SetAcceleratorTable ( aTable )

    # *************************************************************
    # Event Bindings
    # *************************************************************
    self.Bind ( wx.EVT_NAVIGATION_KEY,        self.OnTreeNavigate )

    ### IS DONE BY POPUP MENU
##    self.Bind ( wx.EVT_KEY_DOWN, self.OnMyKeyDown)

    self.Bind ( CT.EVT_TREE_BEGIN_DRAG,       self.OnBeginDrag )
    self.Bind ( CT.EVT_TREE_END_DRAG,         self.OnEndDrag )

    self.Bind ( wx.EVT_LEFT_DOWN,             self.OnClick )


    # *************************************************************
    # Event Bindings, Not Used in this library
    # *************************************************************
    """
    self.Bind ( CT.EVT_TREE_ITEM_GETTOOLTIP,  self.OnToolTip )

    self.Bind ( wx.EVT_KEY_DOWN,              self.OnKeyDown )
    self.Bind ( CT.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit )

    self.Bind ( wx.EVT_MIDDLE_DOWN,           self.OnMiddleDown )
    self.Bind ( wx.EVT_RIGHT_DOWN,            self.OnRightDown )

    self.Bind ( CT.EVT_TREE_SEL_CHANGED,      self.OnChanged )
    self.Bind ( CT.EVT_TREE_SEL_CHANGING,     self.OnChanging )
    self.Bind ( CT.EVT_TREE_ITEM_ACTIVATED,   self.OnActivated )
    self.Bind ( CT.EVT_TREE_STATE_IMAGE_CLICK,self.OnActivated )
    """

    self.Bind ( CT.EVT_TREE_SEL_CHANGED,      self.On_Sel_Changed    )

  # *************************************************************
  # *************************************************************
  """
    -- Case insensitive sorting
  """
  def OnCompareItems(self, item1, item2):
      t1 = self.GetItemText(item1).lower()
      t2 = self.GetItemText(item2).lower()
      ##self.log.WriteText('compare: ' + t1 + ' <> ' + t2 + '\n')
      if t1 < t2: return -1
      if t1 == t2: return 0
      return 1

  # *************************************************************
  # *************************************************************
  def On_Sel_Changed ( self, event ) :
    #print self.GetItemText ( event.GetItem())
    event.Skip()

  """
    # implemented as dummy procedures,
    # so they can easily taken over by the children
    #self.Bind ( CT.EVT_TREE_SEL_CHANGING,     self.OnChanging   )
    #self.Bind ( CT.EVT_TREE_ITEM_ACTIVATED,   self.OnActivated  )
    #self.Bind ( CT.EVT_TREE_STATE_IMAGE_CLICK,self.OnStateImage )

  # *************************************************************
  # dummy procedures,
  # so they can easily taken over by the children
  # *************************************************************
  def OnChanged ( self, event ) :
    print ' piep'
    event.Skip()
    pass
  def OnChanging ( self, event ) :
    event.Skip()
    pass
  def OnActivated ( self, event ) :
    pass
  def OnStateImage ( self, event ) :
    print ' SDTTSTTTTSTTTS'
  """


  # *************************************************************
  # *************************************************************
  def OnMyKeyDown ( self, event ) :
    if not ( self.GetEditControl () ) :
      if event.GetKeyCode() == wx.WXK_DELETE :
        if not ( self.ReadOnly ) and self.Del_Allowed :
          self.Delete_Item ( self.GetSelection () )
      # goto or stay in edit mode
      elif event.GetKeyCode() == wx.WXK_SPACE :
        if not ( self.ReadOnly ) and self.Edit_Allowed :
          self.Do_Edit ( self.GetSelection () )
      else :
        event.Skip()
    else :
      event.Skip()

  # *************************************************************
  # *************************************************************
  def On_Icon_Click ( self, item ) :
    pass

  # *************************************************************
  # *************************************************************
  def OnClick ( self, event ) :
    item, hit = self.HitTest ( event.GetPosition () )
    #print 'Click',item,hit
    if hit and \
       (( hit & CT.TREE_HITTEST_ONITEMICON ) != 0 ) :
      self.On_Icon_Click ( item )
    event.Skip()

  # *************************************************************
  # Get all parents texts in a NoCase_List
  # *************************************************************
  def Get_Parents ( self, item ) :
    Parents = NoCase_List ()
    Root = self.GetRootItem ()
    while item and ( item != Root ) :
      item = item.GetParent ()
      Parents.append ( self.GetItemText ( item ) )
    return Parents

  # *************************************************************
  # *************************************************************
  def Get_Children ( self, Node ) :
    Result = []
    if self.HasChildren ( Node ) :
      item, cookie = self.GetFirstChild ( Node )
      while item :
        Result.append ( self.GetItemText ( item ))
        item = self.GetNextSibling ( item )
    return Result

  # *************************************************************
  # *************************************************************
  def Get_Children_Expanded ( self, Node ) :
    Result = []
    if self.HasChildren ( Node ):
      item, cookie = self.GetFirstChild ( Node )
      while item :
        if self.IsExpanded ( item ) :
          Result.append ( self.GetItemText ( item ))
        item = self.GetNextSibling ( item )
    return Result

  # *************************************************************
  # *************************************************************
  def Set_Children_Expanded ( self, Node, Expanded ) :
    #print 'EXP', Expanded
    if self.HasChildren ( Node ):
      item, cookie = self.GetFirstChild ( Node )
      while item :
        if self.GetItemText( item ) in Expanded :
          self.Expand ( item )
        item = self.GetNextSibling ( item )

  # *************************************************************
  # determines the level of a treenode,
  # and the text of the main parent
  # root: level = 0
  # *************************************************************
  def Get_Item_Level_MainParent ( self, item ) :
    level = 0
    MainParent = ''
    Root = self.GetRootItem ()
    while item and  ( item != Root ) :
      if item != Root :
        MainParent = item
      item = item.GetParent()
      level += 1
    if MainParent : MainParent = self.GetItemText ( MainParent)
    return level, MainParent

  # *************************************************************
  # Find the parent at level=level
  # *************************************************************
  def Get_Parent_At_Level (self, item, level ):
    my_level, Parent = self.Get_Item_Level_MainParent ( item )
    Parent = item
    for i in range ( my_level - level ) :
      Parent = Parent.GetParent ()
    return Parent

  # *************************************************************
  # *************************************************************
  def Find_Label ( self, Label ) :
    """
    Searches a node with the specified name.
    For now only the root is searched, must be extended by recursion !!
    """
    Found = False
    Root = self.GetRootItem ()
    if self.HasChildren ( Root ):
      item, cookie = self.GetFirstChild ( Root )
      while item and not ( Found ) :
        if self.GetItemText ( item ) == Label :
          return item
        item = self.GetNextSibling ( item )


  # *************************************************************
  # *************************************************************
  def CollapseAll ( self ) :
    Root = self.GetRootItem ()
    if self.HasChildren ( Root ):
      item, cookie = self.GetFirstChild ( Root )
      while item :
        item.Collapse ()
        item = self.GetNextSibling ( item )
      self.Refresh ()

  # *************************************************************
  # *************************************************************
  def On_Insert ( self, event ) :
    self.Do_Insert ( self.GetSelection () )

  # *************************************************************
  def Enable_External_Drop ( self, Drop_Enable = True ) :
    if Drop_Enable :
      self.SetDropTarget ( Tree_DropTarget ( self ) )
    else :
      self.SetDropTarget ( None )

  # *************************************************************
  # *************************************************************
  def Drop_Items ( self, item, filenames):
    if not isinstance(filenames,list): filenames = [filenames]
    for file in filenames:
      filename = os.path.splitext(os.path.split(file)[-1])[0]
      if file.startswith('http'):
        try:
          filename = GetTitle(file).replace('\r','').replace('\n','').replace('\t','')
        except:
          pass


      if not filename.strip(): filename = split(file)[-2]
      if item:
        item = self.AppendItem(item,filename)
      else:
        item = self.AppendItem(self.GetRootItem(),filename)
      item.SetData({'Filename':file})
      print(('Adding:',file))

  # *************************************************************
  # *************************************************************
  def Do_Insert ( self, Item, Hit = None ) :
    self.Insert_New ( Item, Hit )

  # *************************************************************
  # *************************************************************
  def On_Edit ( self, event ) :
    self.Do_Edit ( self.GetSelection () )

  # *************************************************************
  # *************************************************************
  def Do_Edit ( self, Item ) :
    self.Edit ( Item )

  # *************************************************************
  # *************************************************************
  def On_Cut ( self, event ) :
    self.Do_Cut ( self.GetSelection () )

  # *************************************************************
  # *************************************************************
  def Do_Cut ( self, Item ) :
    self.Move_Action = True
    self.Item_Copy = Item

  # *************************************************************
  # *************************************************************
  def On_Copy ( self, event ) :
    self.Do_Copy ( self.GetSelection () )

  # *************************************************************
  # *************************************************************
  def Do_Copy ( self, Item ) :
    self.Move_Action = False
    self.Item_Copy = Item

  # *************************************************************
  # *************************************************************
  def On_Paste ( self, event ) :
    self.Do_Paste ( self.GetSelection () )

  # *************************************************************
  # *************************************************************
  def Do_Paste ( self, Item ) :
    if self.Item_Copy :
      self.Enumerate_Copy ( self.Item_Copy, Item, False )
      self.Item_Copy = False

  # *************************************************************
  # *************************************************************
  def On_Delete ( self, event ) :
    self.Do_Delete ( self.GetSelection () )

  # *************************************************************
  # *************************************************************
  def Do_Delete ( self, event ) :
    if not ( self.GetEditControl () ) :
      self.Delete_Item ( Item )


  # *************************************************************
  # *************************************************************
  def Copy_PyData ( self, Source, Dest ) :
    # now add PyData and icons (deepcopy gives problems)
    PyData = []
    data = self.GetPyData ( Source )
    if data :
      for i in data :
        PyData.append ( i )
    if len (PyData) < 1 : PyData.append ( 0 )
    if len (PyData) < 2 : PyData.append ( 23 )
    if len (PyData) < 3 : PyData.append ( 14 )
    self.SetPyData    ( Dest, PyData )
    self.SetItemImage ( Dest, int(PyData[1]), CT.TreeItemIcon_Normal )
    self.SetItemImage ( Dest, int(PyData[2]), CT.TreeItemIcon_Expanded )

  # *************************************************************
  # *************************************************************
  def Insert_New ( self, sel, hit = None ) :
    # if OnIcon, add as a child
    if hit and \
       (( hit & CT.TREE_HITTEST_ONITEMICON ) != 0 ) :
          NewItem = self.AppendItem ( sel, _(0,'new' ))
          self.Expand ( NewItem )
    else :
      # if no node is selected, just add to the root
      if not ( sel ) :
        sel = self.GetRootItem ()
        NewItem = self.AppendItem ( sel, _(0,'new' ))
      else:
        prev = self.GetPrevSibling ( sel )
        if not ( prev ) :
          itemParent = self.GetItemParent ( sel )
          NewItem = self.PrependItem ( itemParent, _(0,'new') )
        else :
          itemParent = self.GetItemParent ( prev )
          NewItem = self.InsertItem ( itemParent, prev, _(0,'new') )
        """
        NewItem = self.InsertItemBefore ( itemParent, sel, _(0,'new') )
        """
    self.Copy_PyData ( sel, NewItem )
    self.SelectItem ( NewItem, True )
    self.Edit ( NewItem )


  # *************************************************************
  # *************************************************************
  def Delete_Allowed ( self, item ) :
    # Can be overriden by the owner
    return True

  # *************************************************************
  # *************************************************************
  def Delete_Item ( self, item ) :
    if self.ReadOnly or not ( self.Delete_Allowed ( item ) ):
      return

    itemtext = self.GetItemText ( item )
    level, parent = self.Get_Item_Level_MainParent ( item )

    line = _(0,'Delete "' + itemtext + \
               '" and all its Children\n' \
               'Are you sure ?')
    if AskYesNo (line) :
      # after deleting we want to goto the element above it
      prev   = self.GetPrevVisible ( item )
      PyData = self.GetPyData ( item )
      self.Delete ( item )
      self.SelectItem ( prev, True )
      if self.Tree_Completion_CallBack :
        self.Tree_Completion_CallBack ( 'Deleted', itemtext, level, parent, PyData )
      return True, level, itemtext, parent

  # *************************************************************
  # Stop editing when moved away form this node
  # *************************************************************
  def OnTreeNavigate ( self, event ) :
    if self.GetEditControl():
      self.GetEditControl().AcceptChanges()
      self.GetEditControl().StopEditing()

  # *************************************************************
  # *************************************************************
  def Enable_Popup ( self, Allow ) :
    self.Popup_Allowed = Allow

  # *************************************************************
  # *************************************************************
  def OnShowPopup ( self, event ) :
    """
EVT_TREE_ITEM_RIGHT_CLICK: dir ( event )
['Allow', 'Checked', 'ClassName', 'ClientData', 'ClientObject', 'Clone',
'Destroy', 'EventObject', 'EventType', 'ExtraLong', 'GetClassName',
'GetClientData', 'GetClientObject', 'GetEventObject', 'GetEventType',
'GetExtraLong', 'GetId', 'GetInt', 'GetItem', 'GetKeyCode', 'GetKeyEvent',
 'GetLabel', 'GetNotifyEvent', 'GetOldItem', 'GetPoint', 'GetSelection',
 'GetSkipped', 'GetString', 'GetTimestamp', 'GetToolTip', 'Id', 'Int',
 'IsAllowed', 'IsChecked', 'IsCommandEvent', 'IsEditCancelled',
 'IsSameAs', 'IsSelection', 'ResumePropagation', 'Selection',
 'SetClientData', 'SetClientObject', 'SetEditCanceled', 'SetEventObject',
 'SetEventType', 'SetExtraLong', 'SetId', 'SetInt', 'SetItem',
 'SetKeyEvent', 'SetLabel', 'SetOldItem', 'SetPoint', 'SetString',
 'SetTimestamp', 'SetToolTip', 'ShouldPropagate', 'Skip', 'Skipped',
 'StopPropagation', 'String', 'Timestamp', 'Veto', '_GetSelf', '_SetSelf',
  '__class__', '__del__', '__delattr__', '__dict__', '__doc__',
  '__getattribute__', '__hash__', '__init__', '__module__', '__new__',
  '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__str__',
  '__swig_destroy__', '__weakref__', '_evtKey', '_item', '_label',
  '_pointDrag', 'notify', 'this', 'thisown']

    #print dir(event)
    print self.GetItemText ( event.GetItem() )
    pos = event.GetPosition ()
    pos = self.ScreenToClient ( pos )
    self.Tree_Hit_Pos = pos

    item, hit = self.HitTest(self.Tree_Hit_Pos)
    v3print ( 'PPPP', self.GetItemText ( item ) )
    v3print ( self.GetItemText ( self.GetSelection () ))

    v3print ( 'pUUU', event.GetPoint())
    item, hit = self.HitTest( event.GetPoint())
    v3print ( 'poooo', item, hit, self.GetItemText (item) )

    self.Right_Clicked_Item = event.GetItem ()
    v3print ( 'Right Clicked on:', self.GetItemText ( self.Right_Clicked_Item ))
    """
    #print 'RRRRRRRRRRR',event.GetPoint()
    if not ( self.Popup_Allowed ) :
      return
    self.Tree_Hit_Pos = event.GetPoint ()
    if self.ReadOnly :
      # only allow copy
      for i in range ( 6 ) :
        self.Popup_Menu_Tree.SetEnabled ( i , False )
      self.Popup_Menu_Tree.SetEnabled ( 3 , True )
    else :
      self.Popup_Menu_Tree.SetEnabled ( 0 , self.Insert_Allowed )
      self.Popup_Menu_Tree.SetEnabled ( 1 , self.Edit_Allowed )
      self.Popup_Menu_Tree.SetEnabled ( 2 , self.Cut_Allowed )
      self.Popup_Menu_Tree.SetEnabled ( 3 , self.Paste_Allowed )
      self.Popup_Menu_Tree.SetEnabled ( 4 , self.Item_Copy   )
      self.Popup_Menu_Tree.SetEnabled ( 5 , self.Del_Allowed )
    self.PopupMenu ( self.Popup_Menu_Tree )

  # *************************************************************
  # *************************************************************
  def OnPopupItemSelected ( self, event ) :
    item, hit = self.HitTest(self.Tree_Hit_Pos)
    #item = self.Right_Clicked_Item
    #hit = None

    i = event.Int
    if   i == 0 : # Insert New
      self.Do_Insert ( item, hit )

    elif i == 1 : # Edit
      self.Do_Edit ( item )

    elif i == 2 : # Cut
      self.Do_Cut ( item )

    elif i == 3 : # Copy
      self.Do_Copy ( item )

    elif i == 4 : # Paste
      self.Do_Paste ( item )

    elif i == 5 : # Delete
      self.Delete_Item ( item )

  # *************************************************************
  # *************************************************************
  def OnBeginDrag ( self, event ) :
    self.Item_Copy = event.GetItem ()
    print('Begin Drag', self.GetItemText ( self.Item_Copy ))
    if self.Item_Copy:
#      wx.SetCursor ( wx.StockCursor ( wx.CURSOR_BULLSEYE ) )
      event.Allow()
      # allow the parent to Veto the drag
      # BUT: the parent must implement and Bind an (empty) method
      # otherwise the drag won't start
      event.Skip ()

  # *************************************************************
  # *************************************************************
  def OnEndDrag(self, event):
    x, y = event.GetPoint()
    item, hit = self.HitTest ( wx.Point ( x, y ) )
    print('End Drag', self.GetItemText(item))
    self.Move_Action = True
    if item :
      self.Copy_Item ( item, hit )

  # *************************************************************
  # RECURSION !!
  # *************************************************************
  def Enumerate_Node ( self, Node, Level = None ) :
    """
    Enumerates over a Node and all it's children,
    returns Level, Icon, Text
    """
    if not Level :
      Level, MainParent = self.Get_Item_Level_MainParent ( Node )
    yield Level, self.GetItemImage ( Node ), self.GetItemText ( Node )

    if self.HasChildren ( Node ):
      item, cookie = self.GetFirstChild ( Node )
      while item :
        for Result in self.Enumerate_Node ( item, Level + 1 ):
          yield Result
        item = self.GetNextSibling ( item )

  # *************************************************************
  # RECURSION !!
  # *************************************************************
  def Enumerate_Copy ( self, source, dest, AsChild = True ) :
    Text  = self.GetItemText  ( source )
    Image = self.GetItemImage ( source )
    ##print 'Image', Image, Text
    if AsChild : # insert as child of the destination
      NewItem = self.AppendItem ( dest, Text )
      # be sure the parent will be expanded
      self.Expand ( dest )

    else : #insert before drop target
      itemParent = self.GetItemParent ( dest )
      prev = self.GetPrevSibling ( dest )
      if not ( prev ) :
        NewItem = self.PrependItem ( itemParent, Text )
      else :
        NewItem = self.InsertItem (itemParent, prev, Text )

    ##print 'Image', Image, Text
    self.SetItemImage ( NewItem, Image )
    self.Copy_PyData ( source, NewItem )

    if self.HasChildren ( source ):
      item, cookie = self.GetFirstChild ( source )
      while item :
        self.Enumerate_Copy ( item, NewItem, True )
        item = self.GetNextSibling ( item )

  # *************************************************************
  # RECURSION !!
  # *************************************************************
  def Enumerate_Copy2 ( self, source, dest, AsChild = True ) :
    Text  = self.GetItemText  ( source )
    Image = self.GetItemImage ( source )
    #print 'CopyImage', Image
    if AsChild : # insert as child of the destination
      NewItem = self.AppendItem ( dest, Text )

    else : #insert before drop target
      itemParent = self.GetItemParent ( dest )
      prev = self.GetPrevSibling ( dest )
      if not ( prev ) :
        NewItem = self.PrependItem ( itemParent, Text )
      else :
        NewItem = self.InsertItem (itemParent, prev, Text )

    self.SetItemImage ( NewItem, Image )

    if self.HasChildren ( source ):
      item, cookie = self.GetFirstChild ( source )
      while item :
        self.Enumerate_Copy2 ( item, NewItem, True )
        item = self.GetNextSibling ( item )

  # *************************************************************
  # RECURSION !!
  # *************************************************************
  def Dropped_On_Myself ( self, source, dest ) :
    if dest == source :
      return True
    if self.HasChildren ( source ):
      item, cookie = self.GetFirstChild ( source )
      while item :
        if self.Dropped_On_Myself ( item, dest ) :
          return True
        item = self.GetNextSibling ( item )
    return False

  # *************************************************************
  # *************************************************************
  def Copy_Item ( self, item, hit ):
    # test if not copied / moved to itself or one of it's children
    if self.Dropped_On_Myself ( self.Item_Copy, item ) :
      self.Move_Action = False
      return

    OnIcon = ( hit & CT.TREE_HITTEST_ONITEMICON ) != 0
    self.Enumerate_Copy ( self.Item_Copy, item, OnIcon )
    if self.Move_Action :
      self.Delete ( self.Item_Copy )
      self.Move_Action = False
    self.Item_Copy = None

  # *****************************************************************
  # Transports all Expanded Nodes
  # *****************************************************************
  def _Enum_TreeExpand_2_String ( self, Node, Line, Result ) :
    Node, cookie = self.GetFirstChild ( Node )
    while Node :
      if self.IsExpanded ( Node ) :
        Result.append ( Line + '/' + self.GetItemText ( Node ) )
      if self.HasChildren ( Node ) :
        self._Enum_TreeExpand_2_String (
          Node, Line + '/'+ self.GetItemText ( Node ), Result )
      Node = self.GetNextSibling ( Node )
  # *****************************************************************
  def TreeExpand_2_String ( self ) :
    # assume root always expanded
    Line = self.GetItemText ( self.GetRootItem () )
    Result= [ Line ]

    Node, cookie = self.GetFirstChild ( self.GetRootItem () )
    while Node :
      # Store the expansion of the mainnode
      if self.IsExpanded ( Node ) :
        Result.append ( Line + '/' + self.GetItemText ( Node ) )
      if self.HasChildren ( Node ) :
        self._Enum_TreeExpand_2_String ( Node,
            Line + '/' + self.GetItemText ( Node ) , Result )
      Node = self.GetNextSibling ( Node )
    return Result




  # *****************************************************************
  # Printss all Expanded Nodes
  # *****************************************************************
  def Tree_2_Html_File ( self, fh, Node = None, Indent = 0 ) :
    if not ( Node ) :
      Node = self.GetRootItem ()

    Color = self.GetItemTextColour ( Node )

    Pre = '<span STYLE="color: %s;">' % RGB_2_HTML_Color ( Color )
    Pre += 2 * Indent * '&nbsp;' + '%s --- ' % Indent
    Text = self.GetItemText ( Node )
    Text = Text.replace ( '\n\n', '\n' )
    Text = Text.replace ( '\n', '<br>\n' )
    Bold = self.IsBold ( Node )
    if Bold :
      Text = '<b>' + Text + '</b>'


    fh.write ( Pre + Text + '<br>\n</span>' )

    if Node.IsExpanded () :
      Indent += 1
      Node, cookie = self.GetFirstChild ( Node )
      while Node :
        self.Tree_2_Html_File ( fh, Node, Indent )
        Node = self.GetNextSibling ( Node )
    # *****************************************************************





  # *****************************************************************
  # *****************************************************************
  def _Enum_String_2_TreeExpand ( self, Node, Line, Expansion ) :
    Node, cookie = self.GetFirstChild ( Node )
    while Node :
      if  Line + '/' + self.GetItemText ( Node ) in Expansion :
        self.Expand ( Node )
      if self.HasChildren ( Node ) :
        self._Enum_String_2_TreeExpand (
          Node, Line + '/'+ self.GetItemText ( Node ),Expansion )
      Node = self.GetNextSibling ( Node )
  # *****************************************************************
  def String_2_TreeExpand ( self, Expansion ) :
    if not ( Expansion ) :
      return

    Root = self.GetRootItem ()
    #if self.IsVisible ( Root ) :
    try:
      self.Expand ( Root )
    except :
      pass
    Line = self.GetItemText ( Root )
    Result= [ Line ]

    Node, cookie = self.GetFirstChild ( Root )
    while Node :
      if  Line + '/' + self.GetItemText ( Node ) in Expansion :
        self.Expand ( Node )
      if self.HasChildren ( Node ) :
        self._Enum_String_2_TreeExpand ( Node,
            Line + '/' + self.GetItemText ( Node ) , Expansion )
      Node = self.GetNextSibling ( Node )

  # *****************************************************************
  # Transports all parameters from the TREE to the INIFILE.
  # Recursion !! Only used by Tree_2_IniFile.
  # *****************************************************************
  def _Enum_Tree_2_IniFile_OLD ( self, treefile, start, line='' ):
    item, cookie = self.GetFirstChild ( start )
    while item :
      state = self.IsItemChecked ( item ) + 2*self.IsExpanded ( item )
      data = self.GetPyData ( item )
      #print 'Kloadasd',self.GetItemText ( item ), data
      if data :
        if len ( data ) < 1 :
          data.append ( state )
        else :
          data [0] = state
      else :
        data =[]
        data.append ( state )

      dataline =  ''
      for elem in data :
        #dataline += str(elem) + ','
        dataline += str(elem) + '~'
      if len( dataline ) > 0 : dataline = dataline [:-1]

      treefile.write ( line + self.GetItemText ( item ) + '=' + dataline+'\n' )

      if self.HasChildren ( item ) :
        self._Enum_Tree_2_IniFile_OLD (
          treefile, item, line + self.GetItemText ( item ) + '~' )
        #  treefile, item, line + self.GetItemText ( item ) + ',' )
      item = self.GetNextSibling ( item )

  # *****************************************************************
  # Transports all parameters from the TREE to the INIFILE.
  # *****************************************************************
  def Tree_2_IniFile_OLD ( self, ini_filename, ext = 'tree' ) :
    # inifile doesn't accept double key-values,
    # therefor we use normal text file
    fne, fe = os.path.splitext ( ini_filename )
    treefile = open ( fne + '.' + ext, 'w')

    MainNode, cookie = self.GetFirstChild ( self.GetRootItem () )
    while MainNode :
      # Store the expansion of the mainnode
      state = self.IsItemChecked ( MainNode ) + 2*self.IsExpanded ( MainNode )
      treefile.write ( '[' + self.GetItemText ( MainNode ) + '=' +  str ( state ) + '\n' )
      self._Enum_Tree_2_IniFile_OLD ( treefile, MainNode )
      MainNode = self.GetNextSibling ( MainNode )
    treefile.close()



  # *****************************************************************
  # Transports all parameters from the TREE to the INIFILE.
  # Recursion !! Only used by Tree_2_IniFile.
  # *****************************************************************
  def _Enum_Tree_2_IniFile ( self, treefile, item, line='' ):
    ##item, cookie = self.GetFirstChild ( start )
    while item :
      state = self.IsItemChecked ( item ) + 2*self.IsExpanded ( item )
      data = self.GetPyData ( item )
      #print 'Kloadasd',self.GetItemText ( item ), data
      if data :
        if len ( data ) < 1 :
          data.append ( state )
        else :
          data [0] = state
      else :
        data =[]
        data.append ( state )

      dataline =  ''
      for elem in data :
        #dataline += str(elem) + ','
        dataline += str(elem) + '~'
      if len( dataline ) > 0 : dataline = dataline [:-1]

      if item.GetParent () == self.GetRootItem () :
        treefile.write ( '[' + self.GetItemText ( item ) + '=' + dataline+'\n' )
        line = ''
      else :
        treefile.write ( line + self.GetItemText ( item ) + '=' + dataline+'\n' )

      if self.HasChildren ( item ) :
        nextitem, cookie = self.GetFirstChild ( item )    ## <<NEW
        if item.GetParent () == self.GetRootItem () :
          newline = line
        else :
          newline = line + self.GetItemText ( item ) + '~'

        self._Enum_Tree_2_IniFile (
          treefile, nextitem, newline )
        #  treefile, item, line + self.GetItemText ( item ) + ',' )
      item = self.GetNextSibling ( item )

  # *****************************************************************
  # Transports all parameters from the TREE to the INIFILE.
  # *****************************************************************
  def Tree_2_IniFile ( self, ini_filename = None, ext = 'tree' ) :
    if not ini_filename :
      return
    # inifile doesn't accept double key-values,
    # therefor we use normal text file
    fne, fe = os.path.splitext ( ini_filename )
    treefile = open ( fne + '.' + ext, 'w')

    MainNode, cookie = self.GetFirstChild ( self.GetRootItem () )
    self._Enum_Tree_2_IniFile ( treefile, MainNode )
    treefile.close()

  # *****************************************************************
  #
  # *****************************************************************
  def Add_PyFile_Info ( self, underscore = None ) :
    MainNode, cookie = self.GetFirstChild ( self.GetRootItem () )
    while MainNode :
      #MainName = self.GetItemText ( MainNode )
      FileNode, cookie = self.GetFirstChild ( MainNode )
      while FileNode :
        # Get classes and functions
        filename = self.GetItemText ( FileNode )
        FL,CL = Get_Classes_And_Functions_Split ( filename, underscore )
        for F in FL :
          newnode = self.AppendItem ( FileNode, F )
          self.SetItemImage ( newnode, 33, CT.TreeItemIcon_Normal )
        for F in CL :
          newnode = self.AppendItem ( FileNode, F )
          self.SetItemImage ( newnode, 34, CT.TreeItemIcon_Normal )

          # For Classes get the methods
          #print '^^^^',filename,F
          CFL = Get_Class_Methods ( filename, F )
          for CF in CFL :
            CFnode = self.AppendItem ( newnode, CF )
            self.SetItemImage ( CFnode, 22, CT.TreeItemIcon_Normal )

        FileNode = self.GetNextSibling ( FileNode)
      MainNode = self.GetNextSibling ( MainNode )

  # *****************************************************************
  # *****************************************************************
  def IniFile_2_Tree ( self, ini_filename, ext = 'tree' ) :
    fne, fe = os.path.splitext ( ini_filename )
    filename = fne + '.'+ ext
    #print 'Inifilke2Tree', ini_filename
    if File_Exists ( filename ) :
      # *****************************************************************
      # parse the inifile to create the tree
      # ****************************************************************
      treefile = open ( filename, 'r')
      lines = treefile.readlines ()
      treefile.close ()
      #print 'TREELINES',lines
      self.Lines_2_Tree ( lines )
      return True

  # *****************************************************************
  # *****************************************************************
  def Lines_2_Tree ( self, lines ) :
    Expand = []
    N = 0
    for r in lines :
     if r:
      #print ' lOPII',r
      r = r.rstrip ("\n\r")    # remove CR, LF
      # split at the last "="
      if r.find ('=') > 0 :
        #key, val = r.split('=')
        key, val = r.rsplit ( '=', 1 )
      else :
        key = r
        val = ''
      # newer version uses '~'  instead of ','
      #if ( val.find ('~') >= 0 ) or ( key.find ('~') >=0 ):
      key = key.split ( '~' )
      val = val.split ( '~' )
      #else :
      #  key = key.split ( ',' )
      #  val = val.split ( ',' )
      if len ( val ) < 2 : val.append ( -1 )
      if len ( val ) < 3 : val.append ( -1 )

      if key[0][0] == '[':
        node_name = key[0][1:]
        MainNode = self.AppendItem ( self.GetRootItem (), node_name )
        ##val[1] = 15
        ##val[2] = 16
        self.SetPyData ( MainNode, val )
        self.SetItemImage ( MainNode, int( val[1] ), CT.TreeItemIcon_Normal )
        self.SetItemImage ( MainNode, int( val[2] ), CT.TreeItemIcon_Expanded )

        # set the expansion Mainnode that just has finished
        if len(Expand) > 0 :
          nod, exp = Expand[0]
          if exp: self.Expand ( nod )
        Expand = []
        #print val
        Expand.append ( (MainNode, bool ( int(val[0]) & 2 )) )
        N = 0
        node = NODE = MainNode
      else :
        # keep track of nesting
        if len( key ) == N :
          nod, exp = Expand.pop()
          if exp: self.Expand ( nod )
        elif len( key ) > N :
          NODE = node
          N += 1
        elif len( key ) < N :
          for i in range ( N - len(key) + 1 ):
            nod, exp = Expand.pop()
            if exp: self.Expand (nod)
          for i in range ( N - len(key)):
            NODE = NODE.GetParent()
          N = len ( key )

        node = self.AppendItem ( NODE, key [-1] )
        self.SetPyData ( node, val )
        try:
          self.SetItemImage ( node, int( val[1] ), CT.TreeItemIcon_Normal )
          self.SetItemImage ( node, int( val[2] ), CT.TreeItemIcon_Expanded )
        except :
          pass
        Expand.append ( ( node, bool(int(val[0]) & 2) ))

      # set the expansion last Mainnode that just has finished
      # SMALL BUG: if the last element a node with children,
      # it will never be expanded ???
      if len(Expand) > 0 :
        nod, exp = Expand[0]
        if exp: self.Expand ( nod )

  # *****************************************************************
  # *****************************************************************
  def Set_PuntHoofd_Tree ( self, html_tree ) :
    # read a PuntHoofd Tree
    #from .web_support import Read_PuntHoofd_Tree
    from web_support import Read_PuntHoofd_Tree
    tree_items = Read_PuntHoofd_Tree ( html_tree )

    # Create a root element (real root is not shown
    self.DeleteAllItems()
    self.AddRoot ( 'Root will not be shown' )
    #Root = Tree.AppendItem ( Tree.root, tree_items[0][1] [ 8 : -5 ] )
    Root = self.GetRootItem ()


    #Colors = ( wx.RED, wx.BLUE, "#00F FFF", wx.RED, wx.BLUE, "#00FFFF",wx.RED, wx.BLUE, "#00FFFF",  "#00FFFF",wx.RED, wx.BLUE, "#00FFFF")
    Colors = ( (9,193,9), (0,0,255), (232,145,52), (2,6,166), (255,0,0),
               wx.BLACK, (173,140,107), (9,193,9), (197,199,3), (255,0,0),
               (232,102,238), (160,160,160), (48,179,240), (0,0,255), (48,239,48),
               (15,183,122), wx.BLACK, wx.BLACK, wx.BLACK )
    Color_Index = -1
    #Icons = ( 202, 239, 108, 145, 147, 102, 201, 163, 99, 136, 141, 1, 1, 1 )
    #Icons = ( 202, 239, 121, 145, 147, 102, 201, 163, 163, 99, 136, 141, 1, 1, 1 )
    Icons = ( 538, 239, 121, 145, 147,
              402, 201, 65, 163, 523,
              99, 136, 131, 500, 1,
              1, 1 )

    # Create the Tree elements
    for item in tree_items [ 1: ] :
      #v3print ( 'TTTREITEM', item )
      text =  item [1] [8].upper() + item [1] [ 9 : -5 ]
      if item[0] == 1 :
        Color_Index += 1
        Color_Index %= len ( Colors )
        Lib_Color = Colors [ Color_Index ]
        Icon      = Icons  [ Color_Index ]
        Parent = self.AppendItem ( Root, text )
        self.SetItemBold       ( Parent )
        self.SetItemTextColour ( Parent, Lib_Color )
        self.SetItemImage      ( Parent, Icon ) #15 )
      else :
        Node = self.AppendItem ( Parent, text )
        #self.SetItemTextColour ( Node, Lib_Color )
        self.SetItemImage      ( Node, Icon )

    # expand the main tree
    #Tree.Expand ( Root )

# ***********************************************************************


# ***********************************************************************
# A simple form to test the control
# ***********************************************************************
class Simple_Test_Form ( wx.MiniFrame ):
  def __init__ ( self, ini = None ):
    # restore position and size
    self.ini = ini
    if ini :
      ini.Section = 'Test'
      pos  = ini.Read ( 'Pos'  , ( 50, 50 ) )
      size = ini.Read ( 'Size' , ( 500, 300 ) )

    wx.MiniFrame.__init__(
      self, None, -1, 'Test PyLab Works GUI Control',
      size  = size,
      pos   = pos,
      style = wx.DEFAULT_FRAME_STYLE )

    # *****************************************************************
    Splitter = wx.SplitterWindow ( self )

    # Create the control to be tested and read old settings
    self.Tree = Custom_TreeCtrl_Base ( Splitter, style_add = CT.TR_HIDE_ROOT )
    self.Tree.On_Icon_Click = self.On_Icon_Click
    if ini: self.Tree.IniFile_2_Tree ( ini.filename )

    self.Editor = wx.TextCtrl ( Splitter, -1,
      "Here iscontrol.\n\n"
      "The quied over the lazy dog...",
      size=(200, 100),
      #style = wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.NO_3D | wx.NO_BORDER)
      style = wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.NO_BORDER)
    Splitter.SplitVertically ( self.Tree, self.Editor )
    # *****************************************************************

    self.     Bind ( wx.EVT_CLOSE,           self.OnCloseWindow )
    self.     Bind ( CT.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag   )
    self.Tree.Bind ( CT.EVT_TREE_END_DRAG,   self.OnEndDrag     )
    Splitter.Bind  ( wx.EVT_SPLITTER_DCLICK, self._Block_This )

    self.Tree.Bind ( wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnShowPopup )

  # *************************************************************
  # *************************************************************
  def OnShowPopup ( self, event ) :
    #print 'GGGGGGGGRRRRRRRRRRR',event.GetPoint(), self.Tree.GetItemText(event.GetItem())
    self.Tree_Hit_Pos = event.GetPoint ()
    #self.Popup_Menu_Tree.SetEnabled ( 4 , self.Item_Copy )
    #self.PopupMenu ( self.Popup_Menu_Tree )

  # *************************************************************
  # *************************************************************
  def OnPopupItemSelected ( self, event ) :
    item, hit = self.Tree.HitTest(self.Tree_Hit_Pos)


  # *************************************************************
  # *************************************************************
  def _Block_This ( self, event ) :
    event.Veto ()

  # *************************************************************
  # Change the icon if clicked on it
  # *************************************************************
  def On_Icon_Click ( self, item ) :
    #print ' JOEPIE...', self.Tree.GetItemImage(item)
    if self.Tree.GetItemImage ( item ) == 80 :
      Icon = 83
    else :
      Icon = 80
    self.Tree.SetItemImage ( item, Icon, CT.TreeItemIcon_Normal )
    self.Tree.SetItemImage ( item, Icon, CT.TreeItemIcon_Expanded )

  # *****************************************************************
  # You can block the start of a drag event
  # *****************************************************************
  def OnBeginDrag ( self, event ) :
    #event.Veto()
    pass

  # *****************************************************************
  # You can block the end of a drag event
  # NOTE: the binding must be "self.Tree.Bind"
  # *****************************************************************
  def OnEndDrag ( self, event ) :
    event.Skip()

  def OnCloseWindow ( self, event ) :
    self.Tree.Tree_2_IniFile ( self.ini.filename )
    event.Skip ()
# ***********************************************************************


DB_TREE_UNCHECKED    = 80  # open square
DB_TREE_CHECKED      = 85  # blue
DB_TREE_DATEFIELD    = 88  # green
DB_TREE_TABLE_SELECT = 83  # red

##DB_TREE_ICONS = [ DB_TREE_CHECKED, DB_TREE_DATEFIELD, DB_TREE_UNCHECKED ]

# ***********************************************************************
# ***********************************************************************
class DataBase_TreeCtrl ( Custom_TreeCtrl_Base ) :
  """
  A tree-control for displaying the meta-data of a database.
  """
  def __init__ ( self, parent ) :
    self.Table_Info        = {}
    self.Tree_Path         = None
    self.No_History_Tables = True
    # Create TreeCtrl, disable editing
    style_sub = CT.TR_EDIT_LABELS  ##| CT.TR_HIDE_ROOT
    Custom_TreeCtrl_Base.__init__ ( self,
                                    parent,
                                    root_title = 'No-Root',
                                    #name       = 'CT-Tree',
                                    style_sub  = style_sub,
                                     )
    self.Bind ( wx.EVT_KEY_DOWN, self._On_Key_Down )
    self.Bind ( CT.EVT_TREE_ITEM_ACTIVATED,   self._On_Tree_Select )
    self.On_Icon_Click = self._On_Tree_Icon_Click

    # Override popup event
    self.Bind ( wx.EVT_TREE_ITEM_RIGHT_CLICK, self._On_Tree_RM )
    PU = My_Popup_Menu ( self._On_Popup_Item_Selected,
                         itemset = None, pre = CT_Names )
    self.Popup_Menu_Tree = PU

  # ********************************************
  def _On_Key_Down ( self, event ) :
    Key  = event.GetKeyCode()

    if Key in [ wx.WXK_RETURN, wx.WXK_SPACE ] :
      item = self.GetSelection ()

      # Ctrl-Enter jumps to another widget ??
      Meta_Key = event.ShiftDown () or event.ControlDown ()

      self._Set_Selected_Table ( item, Meta_Key )
    else :
      event.Skip ()

  # ********************************************
  def _Set_Selected_Table ( self, item, Meta_Key = False ) :
    # ********************************************
    def _Select_Table ( table ) :
      # Deselect all tables
      MainNode, cookie = self.GetFirstChild ( table.GetParent().GetParent() )
      while MainNode :
        Table_View, cookie = self.GetFirstChild ( MainNode )
        while Table_View :
          self.SetItemImage ( Table_View, DB_TREE_UNCHECKED, CT.TreeItemIcon_Normal )
          self.SetItemImage ( Table_View, DB_TREE_UNCHECKED, CT.TreeItemIcon_Expanded )
          Table_View = self.GetNextSibling ( Table_View )
        MainNode = self.GetNextSibling ( MainNode )

      # Select the current table
      self.SetItemImage ( table, DB_TREE_TABLE_SELECT, CT.TreeItemIcon_Normal )
      self.SetItemImage ( table, DB_TREE_TABLE_SELECT, CT.TreeItemIcon_Expanded )

      self.Notify_Owner ( table, Meta_Key )
    # ********************************************

    level, main_parent = self.Get_Item_Level_MainParent ( item )
    # ********************************************
    # If FIELD selected
    # ********************************************
    table = item
    if level == 3 :
      table = item.GetParent ()

      # if this table is already selected,
      # step to the next field state
      if ( self.GetItemImage ( table ) == DB_TREE_TABLE_SELECT  ) \
         and not ( Meta_Key  ) :
          Image = self.GetItemImage ( item )
          if Image == DB_TREE_UNCHECKED :
            Icon = DB_TREE_CHECKED
            Data = self.GetPyData ( item )
            Data [0] = 0
            self.SetPyData ( item, Data )
          elif Image == DB_TREE_CHECKED :
            Icon = DB_TREE_DATEFIELD
            Data = self.GetPyData ( item )
            Data [0] = 5
            self.SetPyData ( item, Data )
          else :
            Icon = DB_TREE_UNCHECKED
          self.SetItemImage ( item, Icon, CT.TreeItemIcon_Normal )

    # ********************************************
    # Now update the tree and its selection
    # ********************************************
    _Select_Table ( table )

  # *************************************************************
  # if selection changed, set Params,
  # so Output Value will be changed
  # highlight it on the canvas
  # *************************************************************
  def _On_Tree_Select ( self, event ) :
    item = event.GetItem ()
    self._Set_Selected_Table ( item )

  # *************************************************************
  # Change the icon if clicked on it
  # *************************************************************
  def _On_Tree_Icon_Click ( self, item ) :
    level, main_parent = self.Get_Item_Level_MainParent ( item )
    if level > 1 :
      self._Set_Selected_Table ( item )

  # *************************************************************
  # *************************************************************
  def _On_Tree_RM ( self, event ) :
    item = event.GetItem ()
    level, main_parent = self.Get_Item_Level_MainParent ( item )
    if level < 3 :
      return

    # Check the correct Field-Type
    for i in range ( len ( CT_Names ) ) :
      self.Popup_Menu_Tree.SetChecked ( i, False )
    Field_Type = self.GetPyData ( item ) [0]
    self.Popup_Menu_Tree.SetChecked ( Field_Type, True )

    # Show the Popup
    self.Popup_Item = item
    self.PopupMenu( self.Popup_Menu_Tree )

  # *************************************************************
  # *************************************************************
  def _On_Popup_Item_Selected ( self, event ) :
    """
    If a new Field-Type is selected, store in in pydata.
    """
    New_Data = self.GetPyData ( self.Popup_Item )
    New_Data [0] = event.Int + 1
    self.SetPyData ( self.Popup_Item, New_Data )

  # *************************************************************
  # *************************************************************
  def Notify_Owner ( self, Node, Meta_Key = False ) :
    table_name = self.GetItemText ( Node )
    if ' ' in table_name :
      table_name  = '"' + table_name + '"'

    # Generate SQL statement
    Fields          = []
    Disabled_Fields = None
    Sorted          = None
    Reversed        = False
    Field_Types     = []
    Node, cookie = self.GetFirstChild ( Node )
    while Node :
      item  = self.GetItemImage ( Node )
      if item != DB_TREE_UNCHECKED :
        field = self.GetItemText ( Node )
        if '/' in field :
          field = '"' + field + '"'
        Fields.append ( field )
      else :
        Disabled_Fields = True

      Field_Types.append ( self.GetPyData ( Node ) [0] )

      Node = self.GetNextSibling ( Node )

    # if no Fields selected, select them all
    if not ( Disabled_Fields ) :
      Fields = '*'
    self.SQL = 'SELECT ' + ' ,'.join ( Fields ) + '\n' + \
               'FROM ' + table_name
    if Sorted :
      self.SQL += '\n' + 'ORDER BY ' + Sorted
    if Reversed :
      self.SQL += ' DESC'

    Table_Info = self.Table_Info [ table_name ]  ##self.GetPyData ( table )[1]

    self._On_Tree_Change ( self.SQL, table_name, Table_Info, Field_Types, Meta_Key )


  # *************************************************************
  def _On_Tree_Change ( self, SQL, Table_Name, MetaData, Field_Types, Meta_Key ) :
    """
    This is the CallBack method on every event.
    This method should be taken over by the parent.
      SQL         = generated SQL statement
      Table_Name  = name of the active Table
      MetaData    = MetaData of the selected table/view
      Field_Types = field types for ordening and displaying
      Meta_Key    = if extra key was pressed,
                    indicating the user wants to see the MetaData
    """
    pass

  # ********************************************
  def Fill ( self, DB, FilePath = '' ) :
    self.DB        = DB
    self.MetaData  = self.DB.Get_MetaData ()
    self.Tree_Path = FilePath

    self.DeleteAllItems ()
    Root = self.AddRoot ( 'ROOT' )

    # ********************************************
    def Add_To_Tree ( Parent, item, Icon, PyData = None ) :
      NewItem = self.AppendItem ( Parent, item )
      if PyData :
        self.SetPyData ( NewItem, PyData )
      self.SetItemImage ( NewItem, Icon, CT.TreeItemIcon_Normal )
      self.SetItemImage ( NewItem, Icon, CT.TreeItemIcon_Expanded )
      return NewItem
    # ********************************************

    Parent = Root
    from .db_support import _DB_Groups, _DB_Groups_Icons

    # Ignore the last item(s),
    # because these are special ones, like "Natural_JOIN"
    for main_index, Group in enumerate ( _DB_Groups [ : -1 ] ) :
      if Group in self.MetaData :
        Group_Info = self.MetaData [ Group ]
        Header = Group_Info [0]
        NewItem = Add_To_Tree ( Parent, Group, _DB_Groups_Icons [ main_index ] )

        #Parent = NewItem
        for table in Group_Info [1:]  :
          # Create metadata about this table

          ##print '.rLAP',main_index,Group,table
          table_info = copy.copy ( table [2] )
          table_info.insert ( 0,
            [ 'Prim Key', 'Name', 'Type', 'NotNull', 'Default' ] )
          self.Table_Info [ table[0] ] = table_info

          if self.No_History_Tables and\
             'history' in table[0].lower() :
            continue

          Icon = DB_TREE_UNCHECKED
          NewItem2 = Add_To_Tree ( NewItem, table[0], Icon ) ##, table_info )

          Icon = DB_TREE_CHECKED
          for field in table[2] :
            Field_Type = 0
            #Add_To_Tree ( NewItem2, field[1], Icon, [ table_info, Field_Type ] )
            Add_To_Tree ( NewItem2, field[1], Icon, [ Field_Type ] )

        # expand the first group ( Tables )
        if main_index == 0 :
          self.Expand( NewItem )

    #temp expand
    #self.Expand ( Root )
    #self.ExpandAll ()

    # After filling the DB-tree,
    # check if there's layout information available
    if self.Tree_Path :
      filename = os.path.splitext ( self.DB.filename )[0] +'.tree'
      filename = filename.replace ( '\\', '~' )
      filename = filename.replace ( ':', '~' )
      self.Tree_File = os.path.join ( self.Tree_Path, filename )
      self.IniFile_2_Tree ()

  # *****************************************************************
  # Transports all parameters from the TREE to the INIFILE.
  # Recursion !! Only used by Tree_2_IniFile.
  # *****************************************************************
  def _Enum_Tree_2_IniFile ( self, treefile, Node, Level, line='' ):
    Node, cookie = self.GetFirstChild ( Node )
    while Node :
      State = self.IsExpanded   ( Node )
      Image = self.GetItemImage ( Node )
      Data  = self.GetPyData    ( Node )

      DataLine =  str(State) +'~'+ str(Image)
      if Data :
        DataLine += '~' + str ( Data )
      else :
        DataLine += '~[0]'

      Default_Image = False
      if (( Level == 1 ) and ( Image == DB_TREE_UNCHECKED )) or\
         (( Level == 2 ) and ( Image == DB_TREE_CHECKED   )) :
        Default_Image = True
      Real_Data = True
      if not ( Data ) or\
         ( Data and ( len ( Data ) == 1 ) and not ( Data[0] ) ) :
        Real_Data = False
      if State or not ( Default_Image ) or Real_Data :
        treefile.write ( line + self.GetItemText ( Node ) + '=' + DataLine+'\n' )
        print(Level, State, Image, Data)

      if self.HasChildren ( Node ) :
        self._Enum_Tree_2_IniFile (
          treefile, Node, Level+1, line + self.GetItemText ( Node ) + '~' )
      Node = self.GetNextSibling ( Node )

  # *****************************************************************
  # Transports all parameters from the TREE to the INIFILE.
  # *****************************************************************
  def Tree_2_IniFile ( self ) :
    """
    Override the ancestors method.
    """
    if not ( self.Tree_Path ) :
      return

    # inifile doesn't accept double key-values,
    # therefor we use normal text file
    treefile = open ( self.Tree_File, 'w')

    MainNode, cookie = self.GetFirstChild ( self.GetRootItem () )
    while MainNode :
      # Store the expansion of the mainnode
      state = self.IsExpanded ( MainNode )
      NodeName = self.GetItemText ( MainNode )
      treefile.write ( NodeName + '=' +  str ( state ) + '\n' )
      self._Enum_Tree_2_IniFile ( treefile, MainNode, 1, NodeName + '~' )
      MainNode = self.GetNextSibling ( MainNode )
    treefile.close()



  # *****************************************************************
  # Transports all parameters from the TREE to the INIFILE.
  # Recursion !! Only used by
  # *****************************************************************
  def _Enum_IniFile_2_Tree ( self, Settings, Node, line='' ):
    Node, cookie = self.GetFirstChild ( Node )
    while Node :
      Key = line + self.GetItemText ( Node )
      if Key in Settings :
        Expand, Image, Data = Settings [Key].split('~')

        if Expand == 'True' :
          self.Expand ( Node )
        else :
          self.Collapse ( Node )

        if Image :
          self.SetItemImage ( Node, int(Image), CT.TreeItemIcon_Normal )
          self.SetItemImage ( Node, int(Image), CT.TreeItemIcon_Expanded )

        if Data :
          # As the data is stored as a string,
          # we have to evaluate the string to get a list
          self.SetPyData ( Node, eval ( Data ) )

      if self.HasChildren ( Node ) :
        self._Enum_IniFile_2_Tree ( Settings, Node, Key + '~' )
      Node = self.GetNextSibling ( Node )

  # *****************************************************************
  # *****************************************************************
  def IniFile_2_Tree ( self ) :
    """
    Override the ancestors method.
    """
    if not ( self.Tree_File ) or \
       not ( File_Exists ( self.Tree_File ) ):
      return

    fh = open ( self.Tree_File, 'r' )
    lines = fh.readlines ()
    fh.close ()

    Settings = {}
    for line in lines :
      line = line.replace ('\n','').replace('\r','')
      key,value = line.split('=')
      Settings [key] = value

    MainNode, cookie = self.GetFirstChild ( self.GetRootItem () )
    while MainNode :
      NodeName = self.GetItemText ( MainNode )
      if NodeName in Settings :
        Expand = Settings [ NodeName ]
        if Expand == 'True' :
          self.Expand ( MainNode )
        else :
          self.Collapse ( MainNode )

      self._Enum_IniFile_2_Tree ( Settings, MainNode, NodeName + '~' )
      MainNode = self.GetNextSibling ( MainNode )
# ***********************************************************************





# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 2 )

  if Test ( 1 ) :
    app = wx.App ()
    ini = inifile ( 'test_My_Custom_TreeCtrl.cfg' )
    frame = Simple_Test_Form (ini = ini)
    frame.Show ( True )
    app.MainLoop ()
    ini.Close ()

  if Test ( 2 ) :
    app = wx.App ()
    ini = inifile ( 'test_My_Custom_TreeCtrl.cfg' )
    frame = Simple_Test_Form (ini = ini)

    html_tree = '../PyLab_Works/html/pw_demos_tree_index.html'
    frame.Tree.Set_PuntHoofd_Tree ( html_tree )
    frame.Tree.Enable_External_Drop ()

    frame.Show ( True )


    app.MainLoop ()
    ini.Close ()

# ***********************************************************************
pd_Module ( __file__ )
