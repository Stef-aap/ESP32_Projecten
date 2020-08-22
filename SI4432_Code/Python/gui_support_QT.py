# -*- coding: utf-8 -*-
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from builtins import object
"""
from past.utils import old_div
from past.builtins import basestring
import __init__

_Version_Text = [

[ 0.3 , '9-1-2012', 'Stef Mientki',
'Test Conditions:', (),"""
 - TreeCtrl.InsertTopItem    added
 - TextCtrl.AppendText       added
"""],

[ 0.2 , '2010', 'Robbert Mientki',
'Test Conditions:', (),
' - almost everything in this file !!'
],

[ 0.1 , '23-12-2010', 'Stef Mientki',
'Test Conditions:', (),
' - test release']
]
global gui_support_version

import sys
if not getattr(sys,'gui_support_version',None):
  sys.gui_support_version = 'QT'
import os
from General_Globals import Application, Iterable, Test, Test_Defs
import Base_GUI
import traceback
try:
  sys.qt_api
except :
  sys.qt_api = 'PySide'
print ( "gui_support_QT.py, sys.qt_api = ", sys.qt_api )   

if sys.qt_api == 'PySide' :
  import PySide2.QtGui    as     QtGui
  import PySide2.QtCore   as     QtCore
  from   PySide2.QtCore   import QEvent,QSize,Qt
  from   PySide2.QtGui    import QIcon, QKeySequence
  ##from   PySide          import QAxContainer
  
  from   PySide2.QtWidgets import QMainWindow, QFrame, QScrollArea, QSplitter, QTabWidget, QLineEdit
  from   PySide2.QtWidgets import QLabel, QListWidget, QProgressBar, QTextEdit, QComboBox, QRadioButton
  from   PySide2.QtWidgets import QCheckBox, QGroupBox, QPushButton, QTableWidget, QTableWidgetItem
  from   PySide2.QtWidgets import QListView, QTreeWidget, QTreeWidgetItem, QApplication
  from   PySide2.QtWidgets import QVBoxLayout, QHBoxLayout

  #from   PySide.QtWebKit import QWebView,QWebSettings,QWebPage
  from   PySide2.QtWebEngineWidgets import QWebEngineView as QWebView
  from   PySide2.QtWebEngineWidgets import QWebEngineSettings as QWebSettings
  from   PySide2.QtWebEngineWidgets import QWebEnginePage as QWebPage

  from   PySide2.QtGui    import QPalette
  from   PySide2.QtCore   import Signal
  from   PySide2.QtCore   import QUrl

else :
  import PyQt4.QtGui    as     QtGui
  import PyQt4.QtCore   as     QtCore
  from   PyQt4.QtCore   import QEvent,QSize,Qt
  from   PyQt4.QtGui    import QIcon, QKeySequence
  from   PyQt4          import QAxContainer
  from   PyQt4.QtWebKit import QWebView,QWebSettings,QWebPage
  from   PyQt4.QtGui    import QPalette
  from   PyQt4.QtCore   import pyqtSignal as Signal
  from   PyQt4.QtCore   import QUrl

from inifile_support import inifile
from file_support    import Change_FileExt
import picture_support
from  Robbie_support  import Make_Iterable

from os.path import isfile
from time import perf_counter
import pickle

# ***********************************************************************
# ***********************************************************************
## ICO_files are not supported, try:
#QImageReader.supportedImageFormats()
# this seems to a bug inone of the DLL files
# can be solved to use the orginal DLL file of pyQT
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
## Used to create frames, without starting wx.App explictly
Dummy_App = None
Dummy_Main_Window_Show = None
def Dummy_Show () :
  Dummy_Main_Window_Show ()
  #Dummy_App.MainLoop()
  QtCore.QCoreApplication.instance ().exec_()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def GetFont ( PointSize = -1, Family = -1, Italic = False, Bold = False ) :
  return QtGui.QFont( family = Family, pointSize = PointSize, weight = Bold, italic = Italic )
# ***********************************************************************


class KeyPress(object):
  def __init__(self,key,func):
    self.func = func
    self.key = key
  def __call__(self,event):

# this worked in 1.0.7, not in 1.1.0    s1 = QKeySequence(event.modifiers() + event.key());
    s1 = QKeySequence(int(event.modifiers()) + event.key());
    s2 = QKeySequence(self.key);

    #print event.modifiers(),event.key(),event.modifiers() + event.key(),s1.matches(s2),s1,s2
    ## Only some numpad problems
    if s1==s2:#s1.matches(s2):
      return self.func(event)
    return False


# ***********************************************************************
class _Base_QT_Widget ( object ) :
  Named_Events = {}
  def __init__ ( self, **kwargs ) :
    self.SBox = self
    self.events = {}  ## No dict, because of multiple binds
    #self.Named_Events = {}
    if 'setValue' in dir(self):
      self.SetValue = self.setValue

    self._Hint      = kwargs.get ( 'hint'     , ''   )
    self._Label     = kwargs.get ( 'label'    , ''   )
    self._Bitmap    = kwargs.get ( 'bitmap'   , ''   )
    self._Bind      = kwargs.get ( 'bind'     , None )
    self._Bind_Name = kwargs.get ( 'bind_Name', ''   )
    self._Style     = kwargs.get ( 'style'    , 0    )
    self._Style_Sub = kwargs.get ( 'style_sub', None )

    clas = self.__class__
    while not _Base_QT_Widget in clas.__bases__:
      if clas is object:
        print('error')
        return
      clas = clas.__bases__[0]

    for clas1 in clas.__bases__:
      #print clas1,
      if clas1!=_Base_QT_Widget:
       self.BaseClass = clas1
       break;

  def event(self,event):
    if event.type() in self.events:
      for evt in self.events[event.type()]:
        if evt(event):
          print('piep', evt)
          return True
      else:
        return self.BaseClass.event(self,event)
    else:
      return self.BaseClass.event(self,event)

##        else:
##          return self.BaseClass.event(self,event)
##          return False
##        ## TODO: check for event==True...
##      else:
##        return self.BaseClass.event(self,event)
##        print 'error'

  def Bind(self,typ,func=None):

    """
    Super bind function
    To bind keys in Qt, use a string as an event like 'Ctrl+f9' (do not use '-', use '+')

    TODO:
    - Named events via bind method : <object>.Bind('Alias', func)
    """
    typ = Make_Iterable(typ)
    for i in typ:
      if func==None and 'bind' in self.Named_Events:
        func = i
        i = self.Named_Events['bind']
        print('CC', func,i)

      if isinstance(i,basestring):
        if i in self.Named_Events: ## Found named_event, parse again
          return self.Bind( self.Named_Events[i], func)

      if isinstance(i,basestring) or isinstance(i,QKeySequence):
        try:
          a =  self.__getattribute__(i)
          a.connect(func)
          ##print('Connect of ',i ,'Succesfull')
          continue
        except AttributeError:
          #import traceback
          #traceback.print_exc ()
          print('Not a slot',i)
          try:
              print(i,type(a))
              from types import FunctionType,BuiltinFunctionType
              if isinstance(a,(FunctionType,BuiltinFunctionType)):
                print('OK')
                self.__setattr__(i,func)
                continue
              else:
                print('No function')
          except:
            pass
            ## Important debug statements, leave (commented)
            #import traceback
            #traceback.print_exc ()


        print('>>', i,func)
        func = KeyPress(i,func)
        i  = QEvent.KeyPress

      self.events[i] = self.events.get(i,[]) + [func]

  def SetValue ( self, Value ) :
    pass
  def GetValue ( self ) :
    return None



class _Base_QT_Widget_init(object):
  """
    New way of initializing the widgets.
    This method gives the Base Widget the power to do things before *and* after
     the init of the inherited widget(s). ( => Less redundancy)

    # NEW Use:
    with _Base_QT_Widget_init(self, **kwargs):
      QtGui.QTextEdit.__init__ ( self, Parent )

    # OLD use:
    _Base_QT_Widget.__init__ ( self, **kwargs )
    QtGui.QTextEdit.__init__ ( self, Parent )

    And remember: _Base_QT_Widget must be the first inherited object !!!!!!!!!!!

    Note: We could have integrated this structure in to _Base_QT_Widget,
      but then your widget self cannot have a 'with' structure. Also then you
      could not do anything before the init of _Base_QT_Widget.
  """
  def __init__(self,*args,**kwargs):
    self.args = args
    self.kwargs = kwargs
  def __enter__(self):
    "Function executed before widget's init"
    _Base_QT_Widget.__init__(*self.args,**self.kwargs)
  def __exit__(self, type, value, traceback):
    "Function executed after widgets's init (usefull for things like autobind)"
    if type: return False ## This is to raise the error (and not creating an other one)
    # Just fake the variables, so it looks like a normal init
    #  def __init__(self, *args, **kwargs):
    args = self.args[1:]
    kwargs = self.kwargs
    self = self.args[0]
    # Usefull code from here:

    # AutoBind
    for key,event in list(self.Named_Events.items()):
      #print '::',key,event,kwargs
      if key in kwargs:
        ##print('Bind (Named_Events in GUI_string)',event, 'to',kwargs[key])

        self.Bind(event,kwargs[key])

    if 'label' in kwargs :
     self.setWindowTitle ( kwargs [ 'label' ] )
    if 'size' in kwargs :
      self.resize ( *kwargs [ 'size' ] )


# ***********************************************************************
#class MainWindow ( _Base_QT_Widget, QtGui.QMainWindow ) :
class MainWindow ( _Base_QT_Widget, QMainWindow ) :
  Named_Events = {'close':QEvent.Close}
  def __init__ ( self, Parent, **kwargs ) :
##    _Base_QT_Widget.__init__ ( self )
##    QtGui.QMainWindow.__init__ ( self )
##    if 'label' in kwargs :
##      self.setWindowTitle ( kwargs [ 'label' ] )
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QMainWindow.__init__ ( self )
      QMainWindow.__init__ ( self )
    self.SBox = self

  def addWidget ( self, Widget ) :
    self.setCentralWidget ( Widget )

  def Show ( self, Visible = True ) :
    if Visible :
      self.show ()
    else :
      self.hide ()

  def GetValue ( self ) :
    d = self.saveGeometry ().data ()
    #print('MainWindowGeometry',type(d),d)
    return d

  def SetValue ( self, Value ) :
    if Value:
      if isinstance(Value, (str,bytes)):
        #Data = QtCore.QByteArray ( Value )
        Data = Value
        self.restoreGeometry ( Data )
      else:
        print('Error gui_support_QT MainWindow, wrong datatype:', type(Value))

# ***********************************************************************
#class PanelHor ( _Base_QT_Widget, QtGui.QFrame ) :
class PanelHor ( _Base_QT_Widget, QFrame ) :
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QFrame.__init__ ( self, Parent )
      QFrame.__init__ ( self, Parent )
    #self.SBox = QtGui.QHBoxLayout()
    self.SBox = QHBoxLayout()
    self.SBox.setAlignment ( QtCore.Qt.AlignTop )
    self.SBox.setContentsMargins(0,0,0,0)
    self.SBox.setSpacing(0) # Between objects
    self.setLayout ( self.SBox )


# ***********************************************************************
#class PanelVer ( _Base_QT_Widget, QtGui.QFrame ) :
class PanelVer ( _Base_QT_Widget, QFrame ) :
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QFrame.__init__ ( self, Parent )
      QFrame.__init__ ( self, Parent )
    #self.SBox = QtGui.QVBoxLayout()
    self.SBox = QVBoxLayout()
    self.SBox.setAlignment ( QtCore.Qt.AlignLeft )
    self.SBox.setSpacing(0) # Between objects
    self.setLayout ( self.SBox )
    self.SBox.setContentsMargins(0,0,0,0)

  def Show ( self, Visible = True ) :
    if Visible :
      self.show ()
    else :
      self.hide ()
  def Hide ( self ) :
    self.hide ()


# ***********************************************************************
#class Scrollable ( _Base_QT_Widget, QtGui.QScrollArea ) :
class Scrollable ( _Base_QT_Widget, QScrollArea ) :
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QScrollArea.__init__ ( self, Parent )
      QScrollArea.__init__ ( self, Parent )

  def addWidget ( self, Widget, *args, **kwargs ) :
    print('**'*100)
    self.setWidget ( Widget )
    #Widget.setMinimumSize(100,100)
  def sizeHint(self, *args,**kwargs):
    x = self.widget().sizeHint(*args,**kwargs)
    self.widget().setMinimumSize(x)

    print('IEPE', x)
    return x



## Dit werkt niet of zo?
#class Scrollable_PanelVer ( _Base_QT_Widget, QtGui.QScrollArea ) :
class Scrollable_PanelVer ( _Base_QT_Widget, QScrollArea ) :
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QScrollArea.__init__ ( self, Parent )
      QScrollArea.__init__ ( self, Parent )
    #self.SBox = QtGui.QVBoxLayout()
    self.SBox = QVBoxLayout()
    self.SBox.setAlignment ( QtCore.Qt.AlignLeft )
    self.SBox.setSpacing(0) # Between objects
    self.setLayout ( self.SBox )
    self.SBox.setContentsMargins(0,0,0,0)

  def Show ( self, Visible = True ) :
    if Visible :
      self.show ()
    else :
      self.hide ()
  def Hide ( self ) :
    self.hide ()

# ***********************************************************************
#class SplitterHor ( _Base_QT_Widget, QtGui.QSplitter  ) :
class SplitterHor ( _Base_QT_Widget, QSplitter  ) :
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QSplitter.__init__ ( self, QtCore.Qt.Horizontal, Parent )
      QSplitter.__init__ ( self, QtCore.Qt.Horizontal, Parent )
    self.setStyleSheet("QSplitter::handle {background-color: grey}")

  def GetValue ( self ) :
    return self.saveState().data()

  def SetValue ( self, Value ) :
    if Value:
      if isinstance(Value, (str,bytes)):
        #Data = QtCore.QByteArray ( Value )
        Data = Value
        self.restoreState ( Data )
      else:
        print('Error gui_support_QT SplitterHor, wrong datatype:', type(Value))


# ***********************************************************************
#class SplitterVer ( _Base_QT_Widget, QtGui.QSplitter  ) :
class SplitterVer ( _Base_QT_Widget, QSplitter  ) :
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QSplitter.__init__ ( self, QtCore.Qt.Vertical, Parent )
      QSplitter.__init__ ( self, QtCore.Qt.Vertical, Parent )
    self.setStyleSheet("QSplitter::handle {background-color: grey}")

  def GetValue ( self ) :
    return self.saveState().data()

  def SetValue ( self, Value ) :
    if Value:
      if isinstance(Value, (str,bytes)):
        #Data = QtCore.QByteArray ( Value )
        Data = Value
        self.restoreState ( Data )
      else:
        print('Error gui_support_QT SplitterHor, wrong datatype:', type(Value))

# ***********************************************************************
#class Notebook ( _Base_QT_Widget, QtGui.QTabWidget ) :
class Notebook ( _Base_QT_Widget, QTabWidget ) :
  Named_Events = {'bind':'currentChanged'}
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QTabWidget.__init__ ( self , Parent) ##, QtCore.Qt.Vertical )
      QTabWidget.__init__ ( self , Parent) ##, QtCore.Qt.Vertical )

  def addWidget ( self, Widget, *args, **kwargs ) :
    self.addTab ( Widget, Widget.windowTitle() or 'No Title' )

  def SetSelection ( self, Index ) :
    self.setCurrentIndex ( Index )

# ***********************************************************************
#class LineEdit (_Base_QT_Widget,QtGui.QLineEdit):
class LineEdit (_Base_QT_Widget,QLineEdit):
  Named_Events = {'bind':'return', 'changed':'textChanged'}
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QLineEdit.__init__ ( self, Parent )
      QLineEdit.__init__ ( self, Parent )
  def GetValue ( self ) :
    return self.text ()
  def SetValue ( self, Value ) :
    self.setText ( Value )




# ***********************************************************************
#class Label (_Base_QT_Widget, QtGui.QLabel ):
class Label (_Base_QT_Widget, QLabel ):
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QLabel.__init__ ( self, self._Label, Parent )
      QLabel.__init__ ( self, self._Label, Parent )
  def SetValue(self,value):
    self.setText(value)


# ***********************************************************************
#class ListBox (_Base_QT_Widget, QtGui.QListWidget ):
class ListBox (_Base_QT_Widget, QListWidget ):
  Named_Events = {'bind':'itemClicked'}
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QListWidget.__init__ ( self, Parent )
      QListWidget.__init__ ( self, Parent )


  def Set ( self, ListItems ) :
    self.clear ()
    self.addItems ( ListItems )

  def GetStringSelection ( self ) :
    if self.currentItem () :
      return self.currentItem ().text()
    return ''

# ***********************************************************************
class _StatusBar ( _Base_QT_Widget ) :
  def __init__ ( self, Parent, **kwargs ) :
    _Base_QT_Widget.__init__ ( self, **kwargs )
    self.Status = Parent.window().statusBar()

  def addWidget ( self, Component, **kwargs ) :
    Component.setParent(self.Status)
    self.Status.addWidget(Component)

class StatusBar(PanelHor):
  def __init__(self, Parent,*args,**kwargs):
    PanelHor.__init__(self, Parent,*args,**kwargs)
    self.status = _StatusBar(Parent,**kwargs)
    self.addWidget = self.status.addWidget
    self.GetValue = self.status.GetValue
    self.SetValue = self.status.SetValue
    self.SBox = self


# ***********************************************************************
#class ProgressBar(_Base_QT_Widget, QtGui.QProgressBar):
class ProgressBar(_Base_QT_Widget, QProgressBar):
  def __init__(self, Parent,**kwargs):
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QProgressBar.__init__(self, Parent)
      QProgressBar.__init__(self, Parent)


# ***********************************************************************
#class TextCtrl ( _Base_QT_Widget, QtGui.QTextEdit ) :
class TextCtrl ( _Base_QT_Widget, QTextEdit ) :
  Named_Events = { 'bind': 'return' }
  def __init__ ( self, Parent, **kwargs ) :

    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QTextEdit.__init__ ( self, Parent )
      QTextEdit.__init__ ( self, Parent )

##    _Base_QT_Widget.__init__ ( self, **kwargs )
####    _Base_QT_Widget.__init__ ( self )
##    QtGui.QTextEdit.__init__ ( self, Parent )

  def GetValue ( self ) :
    #return self.toHtml ()
    return self.toPlainText ()

  def SetValue ( self, Value ) :
    ##print 'TEXTCTRL.SETVALUE', Value
    #self.setHtml ( Value )
    ##print(type(Value),Value)
    try:
      self.setText ( Value )
    except:
      import traceback
      traceback.print_exc ()



  def AppendText ( self, Line ) :
    Text = self.GetValue () + '\n' + Line
    self.SetValue ( Text )

  def GetStringSelection ( self ) :
    Selected = self.textCursor().selectedText()
    Selected = Selected.replace ( u'\u2029', u'\n' )
    return Selected


# ***********************************************************************
#class Choice ( _Base_QT_Widget, QtGui.QComboBox ) :
class Choice ( _Base_QT_Widget, QComboBox ) :
  Named_Events = { 'bind': 'highlighted(unicode)'}##return' }
  Named_Events = { 'bind': 'currentIndexChanged(unicode)'}##return' }
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QComboBox.__init__ ( self, Parent )
      QComboBox.__init__ ( self, Parent )
    self.setEditable ( False )

  """
  def GetValue ( self ) :
    #return self.toHtml ()
    return self.toPlainText ()

  def SetValue ( self, Value ) :
    print 'TEXTCTRL.SETVALUE', Value
    #self.setHtml ( Value )
    self.setPlainText ( Value )
  """


# ***********************************************************************
# ***********************************************************************
#class RadioButton ( _Base_QT_Widget, QtGui.QRadioButton) :
class RadioButton ( _Base_QT_Widget, QRadioButton) :
  Named_Events = {'bind':'clicked'}      ## SM
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      Title = kwargs.get ( 'label', 'No Title' )
      #QtGui.QRadioButton.__init__ ( self, Title, Parent )
      QRadioButton.__init__ ( self, Title, Parent )
  def SetValue ( self, Value ) :
    self.setChecked ( Value )
  def GetValue ( self ) :
    return self.isChecked ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
#class CheckBox ( _Base_QT_Widget, QtGui.QCheckBox ) :
class CheckBox ( _Base_QT_Widget, QCheckBox ) :
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      Title = kwargs.get ( 'label', 'No Title' )
      #QtGui.QCheckBox.__init__ ( self, Title, Parent )
      QCheckBox.__init__ ( self, Title, Parent )
  def SetValue ( self, Value ) :
    self.setChecked ( Value )
  def GetValue ( self ) :
    return self.isChecked ()
# ***********************************************************************


# ***********************************************************************
#class RadioBox_New_Robbert ( _Base_QT_Widget, QtGui.QGroupBox ) :
class RadioBox_New_Robbert ( _Base_QT_Widget, QGroupBox ) :
  Named_Events = {'bind':'clicked'}
  clicked = Signal(int)
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      Title = kwargs.get ( 'label', 'No Title' )
      #QtGui.QGroupBox.__init__ ( self, Title, Parent )
      QGroupBox.__init__ ( self, Title, Parent )

    #vbox = QtGui.QVBoxLayout()
    vbox = QVBoxLayout()

    Choices = kwargs.get ( 'choices', '1,2,3,4'.split(','))  ## SM
    self.Radio = []
    for Choice in Choices :                                  ## SM
      #self.Radio.append ( QtGui.QRadioButton( Choice, **kwargs ))  ## <===
      self.Radio.append ( QRadioButton( Choice, **kwargs ))  ## <===
      vbox.addWidget ( self.Radio [-1] )                               ## SM

    vbox.addStretch(1)
    self.setLayout(vbox)

  def clickEvent(self, event=None):
    for i, Rad in enumerate ( self.Radio ) :
      if Rad.isChecked() :
        self.clicked.emit(i)
        print('......RadioBox', i)


# ***********************************************************************
# ***********************************************************************
#class RadioBox ( _Base_QT_Widget, QtGui.QGroupBox ) :
class RadioBox ( _Base_QT_Widget, QGroupBox ) :
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      Title = kwargs.get ( 'label', 'No Title' )
      #QtGui.QGroupBox.__init__ ( self, Title, Parent )
      QGroupBox.__init__ ( self, Title, Parent )

    Orientation = kwargs.get ( 'orientation', Qt.Vertical )
    if Orientation == Qt.Vertical :
      #vbox = QtGui.QVBoxLayout()
      vbox = QVBoxLayout()
    else :
      #vbox = QtGui.QHBoxLayout()
      vbox = QHBoxLayout()

    """
In RadioButton toegevoegd
  Named_Events = {'bind':'clicked'}      ## SM
"""
    Choices = kwargs.get ( 'choices', '1,2,3,4'.split(','))  ## SM
    self.Radio = []
    for Choice in Choices :                                  ## SM
      kwargs ['label'] = Choice
      self.Radio.append ( RadioButton ( Parent, **kwargs ))
      vbox.addWidget ( self.Radio [-1] )                               ## SM

    """ SM
    radio1 = QtGui.QRadioButton("&Radio button 1")
    radio2 = QtGui.QRadioButton("R&adio button 2")
    radio3 = QtGui.QRadioButton("Ra&dio button 3")
    radio1.setChecked(True)
    vbox.addWidget(radio1)
    vbox.addWidget(radio2)
    vbox.addWidget(radio3)
    """

    vbox.addStretch(1)
    self.setLayout(vbox)

    ##../../_images/windowsxp-groupbox.png

  """
  def GetValue ( self ) :
    for i,Radio in enumerate ( self.Radio ) :
      if Radio.isChecked () :
         return i
   """

  def GetValue ( self ) :
    for i, Radio in enumerate ( self.Radio ) :
      if Radio.isChecked() :
        return i

  def SetValue ( self, Value ) :
    self.Radio[Value].setChecked(True)

# ***********************************************************************


# ***********************************************************************
#class Button ( _Base_QT_Widget, QtGui.QPushButton ) :
class Button ( _Base_QT_Widget, QPushButton ) :
  Named_Events = {'bind':'clicked'}
  def __init__ ( self, Parent, **kwargs ) :
    Label = kwargs.get('label','')
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QPushButton.__init__ ( self, Label, Parent)
      QPushButton.__init__ ( self, Label, Parent)

    self.SBox.setContentsMargins(0,0,0,0)
    if 'bitmap' in kwargs:
      self.setIcon( QIcon( kwargs['bitmap'] ) )

    ToolTip = kwargs.get('hint','')
    if ToolTip :
      self.setToolTip ( ToolTip )

    #self.setSizePolicy( QSizePolicy( QSizePolicy.Minimum, QSizePolicy.Preferred ) )
  def sizeHint(self):
    if not self.icon().isNull():
      return self.iconSize() + QSize(6, 6)
    else:
      #org = QtGui.QPushButton.sizeHint(self)
      org = QPushButton.sizeHint(self)
      #a = QtGui.QPushButton(self.text()*10)
      a = QPushButton(self.text()*10)
      org.setWidth(old_div((a.sizeHint().width()-6),10)+6)
      return org

#QSize sizeHint() const { return m_pixmap.size(); }

  def SetImage ( self, Filename ) :
    self.setIcon( QIcon( Filename ) )


# ***********************************************************************
#class Table ( _Base_QT_Widget, QtGui.QTableWidget ) :
class Table ( _Base_QT_Widget, QTableWidget ) :
##class Table ( _Base_QT_Widget, QtGui.QTableView ) :
  def __init__ ( self, Parent, **kwargs ) :
    Label = kwargs.get ( 'label', '' )

    with _Base_QT_Widget_init ( self, **kwargs ) :
      #QtGui.QTableWidget.__init__ ( self, Parent )
      QTableWidget.__init__ ( self, Parent )
      ##QtGui.QTableView.__init__ ( self, Parent )

    self.setSortingEnabled ( True )
    self.Col_Headers = True
    self.Row_Headers = False

  # **********************************
  def Get_Data ( self ) :
    Data = []
    for Row in range ( self.rowCount () ) :
      New = []
      for Col in range ( self.columnCount () ) :
        ##item = self.cellWidget ( Row, Col )
        item = self.item ( Row, Col )
        if item :
          item = item.text ()
        else :
          item = ''
        New.append ( item )
      Data.append ( New )
    return Data

  # **********************************
  def Fill_Data ( self, Data ) :
    if not ( Data ) :
      self.setRowCount    ( 0 )
      self.setColumnCount ( 0 )
      return

    ##import meet
    ##meet.Start_Profiler ()
    from date_time_support import ptime
    #ptime ( '1' )
    ##print dir(self)
    Old_Sort = self.isSortingEnabled ()
    self.setSortingEnabled ( False )

    if self.Col_Headers :
      Col_Header = []
      for item in Data [ 0 ] :
         Col_Header.append ( str ( item ) )
      Data = Data [ 1: ]

    if self.Row_Headers :
      RH = 1
    else :
      RH = 0

    NRow = len ( Data )
    NCol = len ( Data [0] ) - RH
    ##print NRow, NCol
    ##self.setUniformRowHeights ( True )

    self.setRowCount    ( NRow )
    self.setColumnCount ( NCol )

    if self.Col_Headers :
      self.setHorizontalHeaderLabels ( Col_Header [ RH: ] )

    Row_Header = []
    for R, Row in enumerate ( Data ) :
      if self.Row_Headers :
        Row_Header.append ( str ( Row[0] ))
      for C, Col in enumerate ( Row [ RH: ] ) :
        ##print R,C,Col
        #item = QtGui.QTableWidgetItem ()
        item = QTableWidgetItem ()
        item.setText ( str ( Col ) )
        self.setItem ( R, C, item )
      #self.setRowHeight ( R, 40 )
      self.setRowHeight ( R, 20 )
    self.setVerticalHeaderLabels ( Row_Header )

    self.setSortingEnabled ( Old_Sort )

    ##self.setRowCount    ( NRow )
    ##self.setColumnCount ( NCol )
    #ptime ( '6' )
    ##meet.Stop_Profiler ()

  # **********************************
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

    if len ( args ) == 1 :
      if Iterable ( args [0] ) :
        args = args [0]
    Widths = list ( args )

    N = self.columnCount ()

    if len ( Widths ) == 0 :
      Widths.append ( 80 )

    while len ( Widths ) < N :
      Widths.append ( Widths [ -1 ] )

    for i in range ( N ) :
      self.setColumnWidth ( i, Widths [ i ] )


# ***********************************************************************
#class IconSelectWidget ( _Base_QT_Widget, QtGui.QListView ) :
class IconSelectWidget ( _Base_QT_Widget, QListView ) :
##class Table ( _Base_QT_Widget, QtGui.QTableView ) :
  def __init__ ( self, Parent, **kwargs ) :
    Label = kwargs.get ( 'label', '' )
    self.dirr  = kwargs.get ( 'dirr', '.' )
    self.size  = kwargs.get ( 'size', (16,16) )
    #self.N = N


    with _Base_QT_Widget_init ( self, **kwargs ) :
      #QtGui.QListView.__init__ ( self, Parent )
      QListView.__init__ ( self, Parent )
      ##QtGui.QTableView.__init__ ( self, Parent )

    self.dirModel = QtGui.QDirModel()
    self.setModel(self.dirModel)
    self.setRootIndex(self.dirModel.index(self.dirr))
    """
    Traceback (most recent call last):
  File "d:/data_python_25/support/Robbie_support.py", line 86, in __call__
    return self.Func(*self.args,**self.kwargs)
  File "d:/projecten/docsystem/DocSystem2.py", line 919, in __init__
    self.GUI = Create_GUI ( GUI )
  File "d:/data_python_25/support/gui_support_QT.py", line 1069, in __init__
    Component = eval ( defi[1], self.p_globals, self.p_locals ) ( Parent, **Kwargs )
  File "d:/data_python_25/support/gui_support_QT.py", line 670, in __init__
    self.setViewMode(1)
TypeError: 'PySide.QtGui.QListView.setViewMode' called with wrong argument types:
  PySide.QtGui.QListView.setViewMode(int)
Supported signatures:
  PySide.QtGui.QListView.setViewMode(PySide.QtGui.QListView.ViewMode)
  """
    #self.setViewMode(QtGui.QListView.IconMode)
    self.setViewMode(QListView.IconMode)
    self.setWrapping(True)
    self.dirModel.setNameFilters('*.ico')

    #self.setSortingEnabled ( True )
    #self.Col_Headers = True
    #self.Row_Headers = False


# ***********************************************************************
#class TreeCtrlItem( QtGui.QTreeWidgetItem, object ) :
class TreeCtrlItem( QTreeWidgetItem, object ) :
  def  __init__(self, *args,**kwargs):
    #QtGui.QTreeWidgetItem.__init__ ( self, *args,**kwargs )
    QTreeWidgetItem.__init__ ( self, *args,**kwargs )
    self.PyData = {}
    ## This doesn't work, you need to inherit, <BUT> without it, you can't rename
    self.setFlags( QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | \
                   QtCore.Qt.ItemIsDragEnabled |  QtCore.Qt.ItemIsDropEnabled )

 #   self.setFlags ( self.flags () | QtCore.Qt.ItemIsUserCheckable )
##    print dir(self)
##    print '#'* 100
##    widget = self.treeWidget()
##    if widget:
##      try:
##        self.setFlags(widget.default_flags)
##      except:
##        pass
##    print 'PPP', self.treeWidget()
##    if self.treeWidget():
##      if self.treeWidget().CheckBoxes == True:
##        self.setCheckState(0,QtCore.Qt.Unchecked)

    # Renamed functions
    ##self.GetParent  = self.parent
    self.IsExpanded = self.isExpanded

  def GetParent(self):
    if self.parent():
      return self.parent()
    elif self.treeWidget():
      return self.treeWidget().invisibleRootItem()
    else:
      return None


  def SetText(self, Text):
    self.setText(0,Text)
  def SetBold(self,Enable = True):
    font = self.font(0)
    font.setBold(Enable)
    self.setFont(0,font)
  def IsBold(self):
    return self.font(0).bold()

  def SetItalic(self,Enable = True):
    font = self.font(0)
    font.setItalic(Enable)
    self.setFont(0,font)
  def IsItalic(self):
    return self.font(0).italic()
  def SetTextColor(self, Color):
    if isinstance(Color,tuple):
      Color = QtGui.QColor(*Color)
    self.setForeground(0, Color)
  def SetTextBackground(self, Color):
    print(self, Color)
    if isinstance(Color,tuple):
      Color = QtGui.QBrush(QtGui.QColor(*Color))
    self.setBackground(0, Color)
  def SetData(self,Data):
    self.PyData = Data
  def GetData(self):
    return self.PyData
  def Expand ( self, Expand = True ):
    self.setExpanded ( Expand )

  def IsChecked ( self ) :
    return False
  def assflags(self, *args,**kwargs):
    return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


  def HasChildren(self,*args,**kwargs):
    return self.childCount() > 0

  def GetChildren(self,*args,**kwargs):
    children = []
    for i in range(self.childCount()):
      children.append(self.child(i))
    return children
  def GetText(self):
    return self.text(0)

  def remove(self):
    #self.parent().removeChild(self)
    self.GetParent().removeChild(self)

  def __eq__(self,b):
    # Comparison to none doesn't work...
    #print type(self),type(b)
    if b is None :
      return False
    else :
      return self is b

# ***********************************************************************
from   tree_support         import Custom_TreeCtrl_Base


#class TreeCtrl(  _Base_QT_Widget, QtGui.QTreeWidget):#, Custom_TreeCtrl_Base  ) :
class TreeCtrl(  _Base_QT_Widget, QTreeWidget):#, Custom_TreeCtrl_Base  ) :
  Named_Events = {'Activate':'doubleClicked', 'Click':'clicked','DoubleClick':'doubleClicked',\
                  'SelectionChanged':'itemSelectionChanged'}
  def __init__ ( self, Parent, **kwargs ) :
##    QtGui.QTreeWidget.__init__ ( self, Parent )
##    _Base_QT_Widget.__init__ ( self, **kwargs)
    with _Base_QT_Widget_init(self, **kwargs):
      #QtGui.QTreeWidget.__init__ ( self, Parent )
      QTreeWidget.__init__ ( self, Parent )
    self.CheckBoxes = True

    self.setColumnCount ( 1 )
    self.header().hide();
    # = TreeCtrlItem()
    self.root = self.AppendItem(self.invisibleRootItem(),'root')
    #self.GetRootItem = self.invisibleRootItem
    self.GetSelection = self.currentItem
    #self.clicked.connect(self.OnClick )
    #self.setEditTriggers(QtGui.QTreeView.Clicked)


##  def flags(self, index):
##     if not index.isValid():
##       return QtCore.Qt.NoItemFlags
##
##     return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
##  def setData(self, index, value, role):
##     if index.isValid() and role == QtCore.Qt.EditRole:
##
##         prev_value = self.getValue(index)
##
##         item = index.internalPointer()
##
##         item.setData(unicode(value.toString()))
##
##         return True
##     else:
##               return False


##  def OnClick(self,index):
##    item = self.itemFromIndex(index)
##    print item
##    print self.currentItem()

  def GetRootItem(self):
    return self.root
  def DeleteAllItems(self):
    self.GetRootItem().takeChildren()

    #return TreeCtrlItem.__init__(self.invisibleRootItem)
  def Refresh(self):
    pass # Not needed in QT

  def AppendItem ( self, ParentNode, Text ) :
    #child_item = self.AppendItem(item, 'a')
    #if isinstance(Text,QtGui.QTreeWidgetItem):
    if isinstance(Text,QTreeWidgetItem):
      item = Text
    elif isinstance(Text,list):
      item = TreeCtrlItem(Text)
    else:
      item = TreeCtrlItem([Text])
    if self.CheckBoxes == True:
      item.setCheckState(0,QtCore.Qt.Unchecked)
    ParentNode.addChild(item)
    return item


  # ***************************************************
  # Added SM, don't know if this is correct ???
  # ***************************************************
  def InsertTopItem ( self, ParentNode, Text ) :
    return self.InsertItem ( ParentNode, ParentNode, Text )

  def InsertItem ( self, ParentNode, Prev, Text ) :
    #child_item = self.AppendItem(item, 'a')
    #if isinstance(Text,QtGui.QTreeWidgetItem):
    if isinstance(Text,QTreeWidgetItem):
      item = Text
    elif isinstance(Text,list):
      item = TreeCtrlItem(Text)
    else:
      item = TreeCtrlItem([Text])

    if self.CheckBoxes == True:
      item.setCheckState(0,QtCore.Qt.Unchecked)
    Indx = ParentNode.indexOfChild ( Prev )
    ParentNode.insertChild ( Indx+1, item )

    return item

  def InsertBeforeItem ( self, Prev, Text ) :
    ParentNode = Prev.GetParent()
    #child_item = self.AppendItem(item, 'a')
    #if isinstance(Text,QtGui.QTreeWidgetItem):
    if isinstance(Text,QTreeWidgetItem):
      item = Text
    elif isinstance(Text,list):
      item = TreeCtrlItem(Text)
    else:
      item = TreeCtrlItem([Text])

    if self.CheckBoxes == True:
      item.setCheckState(0,QtCore.Qt.Unchecked)
    Indx = ParentNode.indexOfChild ( Prev )
    ParentNode.insertChild ( Indx, item )

    return item

  def SetItemTextColour(self,item,Color):
    item.SetTextColor(Color)
  def GetItemTextColour(self,item):
    c = item.foreground(0).color()
    return (c.red(),c.green(),c.blue())
  def GetItemBackgroundColour(self,item):
    c = item.background(0).color()
    d = item.background(0)
    #print d.isOpaque(), d.matrix()
    #print c, c.isValid(),c.toTuple(),c.alpha(),c.alphaF(),c.alphaF() == 1.0
    #if c.alphaF() == 1:
    #if c == QtGui.QColor(0, 0, 0, 1):
    if not d.isOpaque():
      return (-1,-1,-1)
    else:
      return c.toTuple()[:-1]

  def SetItemBackgroundColour(self,item,Color):
    #item.setBackground(0, QBrush(QColor(*Color)))
    item.SetTextBackground(Color)
#zxc
  def SetOwnBackgroundColour(self,Color):
    if isinstance(Color,tuple):
      Color = QtGui.QColor(*Color)
    self.setStyleSheet("QWidget { background-color: %s }" %  Color.name() )
  #def SetPyData(self,*args,**kwargs): pass
  def SetItemImage(self,*args,**kwargs): pass
  def ExpandAll(self,*args,**kwargs):
    self.GetRootItem().setExpanded(True)## Is this correct, does ExpandAll means only the root??

  def Expand(self,*args,**kwargs):
    self.GetRootItem().setExpanded(True)## Is this correct, does ExpandAll means only the root??



  def UnPack_Node(self,item , data):

    item_data, child_data = data
    if isinstance(item_data,int):
        # TreeItemView
        ##child_item = self.AppendItem(item, 'a')
        #self.Views[item_data] = item #child_item
        pass
    else:
        item.SetText                (item_data[0])
        item.SetData                (item_data[1])
        if item_data[2]: item.Expand()
        item.SetBold                (item_data[3])
        item.SetItalic              (item_data[4])
        if item_data[5]!=(-1, -1, -1): self.SetItemTextColour      (item, item_data[5])
        if item_data[6]!=(-1, -1, -1): self.SetItemBackgroundColour(item, item_data[6])
        PyData = item_data[1]
        #print type(PyData),PyData
        if not isinstance(PyData,dict): PyData = {}
        PyData['Application'] =  PyData.get('Application','Default')
        PyData['Filename']    =  PyData.get('Filename','Default').strip('"')
        if len(item_data)>=8:
          PyData['ID']          =  item_data[7]
          self.IDs[ PyData['ID'] ] = item
        for i in child_data:
          child_item = self.AppendItem(item, 'a')
          if isinstance(item_data ,int):
            # View item
            ##self.Views[item_data] = child_item
            pass

          else:
            self.UnPack_Node(child_item, i)
  def Load(self,Filename):
    if isfile(Filename):
      with open(Filename,'rb') as fh:
        version, data = pickle.load(fh)

      #if version != Tree_Version:
      #  print('Error version',Tree_Version,'expected, got verion', version, 'still trying to load anyway')
      self.Views = {}
      self.IDs   = {}
      self.UnPack_Node(self.GetRootItem(),data)

  def Pack_Node(self,item):
    if False:#isinstance(item,TreeItemView):
        ID = id(item.item)
        item_data = ID
        return [ item_data , [] ]
    else:
        ID = id(item)
        color = self.GetItemTextColour(item)
        if not(isinstance(color,tuple)): color = color.Get()
        bcolor = self.GetItemBackgroundColour(item)
        if not(isinstance(bcolor,tuple)): bcolor = bcolor.Get()
        item_data = [ item.GetText(),item.GetData(), item.IsExpanded(), item.IsBold(),\
                      item.IsItalic(),color ,bcolor,ID,]
        child_data = []
        for item in item.GetChildren():
        #item, cookie = self.GetFirstChild ( item )
        #while item:
          child_data.append(self.Pack_Node(item))
        #  item = self.GetNextSibling ( item )
        return [ item_data , child_data ]

  def Save(self,Filename):
    data = [ 0.0 , self.Pack_Node(self.GetRootItem()) ]
    ##print('PPPP save tree', Filename, data)
    if isfile(Filename):
      import shutil,time
      date = os.path.getmtime(Filename)
      shutil.copyfile(Filename,Filename+time.strftime('.%d-%m-%Y %H-%M.Deleted',time.localtime(date)))
    fh = open(Filename,'wb')
    pickle.dump(data,fh)
    fh.close()


class Webkit( _Base_QT_Widget, QWebView ):
  def __init__ ( self, Parent, **kwargs ) :
    with _Base_QT_Widget_init(self, **kwargs):
      QWebView.__init__ ( self, Parent )

    # Enable plugins (Flash and others)
    web_Settings = self.settings ()
    web_Settings.setAttribute ( QWebSettings.PluginsEnabled, True )

    self.show()

    #self.load ( QUrl( "file:///AN440_registers.pdf"))

#web = QWebView()
#web.settings().setAttribute(QWebSettings.PluginsEnabled, True)
#web.show()
#web.load(QUrl('file:///C:/data/progetti_miei/python/test.pdf')) # Change path to actual file.


##    if not Filename:
##      Filename = unicode(self.web.url().toString())
##    if Filename.startswith('file:'):
##      Filename = url2pathname(Filename[5:])
##      if isfile(Filename):
##        print 'PPPPPPP',Filename
##        if gui_support_version == 'WX' :
##          self._Message_2_WebKit('import codecs') ### Should be first
##        codecs = ProxyObject('codecs')
##        fh = codecs.open(Filename,'w','utf-8-sig')
##        fh.write(self.web.page().mainFrame().toHtml())
##        fh.close()


class Spacer(PanelVer):
  pass
  def event(self,event):
    return True
# ***********************************************************************
# ***********************************************************************
class Create_GUI ( Base_GUI._Prepare_GUI_Lines ) :
  def __init__ ( self, *args, **kwargs ) :

    if 'Font' in kwargs :
      Font = kwargs [ 'Font' ]
    else :
      Font = None

    # preprocess the GUI lines
    t = perf_counter()
    Base_GUI._Prepare_GUI_Lines.__init__ ( self, *args, **kwargs ) #GUI, StackUp )
    print('_Prepare_GUI_Lines',perf_counter()-t)
    t = perf_counter()

    # for simple applications, where not a wx.App is created,
    # we create it here
    if not ( QtCore.QCoreApplication.instance () ) :
##      Text_Start_Dummy_App = """
##import gui_support_QT
##import PySide.QtCore   as     QtCore
##gui_support_QT.Dummy_App = QtGui.QApplication ( sys.argv )
##"""
##      #exec ( Text_Start_Dummy_App, self.p_globals, self.p_locals )
      global Dummy_App
      #Dummy_App = QtGui.QApplication ( sys.argv )
      Dummy_App = QApplication ( sys.argv )


      # the topwindow must be a MainWindow,
      # so insert a frame, only if also the application is created
      # because otherwise the GUI might be a part of a larger GUI
      indent, defi, Args, Kwargs, Expand = self.GUI [0]
      if defi[1] != 'MainWindow' :
        indent = 0
        defi = [ 'self.Main_Window', 'MainWindow', None ]
        Args = []
        Kwargs = { 'label' : 'QT application' }
        Expand = 0
        self.GUI.insert ( 0, ( indent, defi, Args, Kwargs, Expand ) )

    # ***************************
    # Create the components
    # ***************************
    for indent, defi, Args, Kwargs, Expand in  self.GUI :
      Indx = self.Update_Stack (indent)
      if Indx >= 0:
        Parent = self.stack [ Indx ] [1]
      else:
        Parent = None
      #print defi[1]
      Component = eval ( defi[1], self.p_globals, self.p_locals ) ( Parent, **Kwargs )
      #for debug print Comonent, kwargs, isinstance(Component, QtGui.QWidget)p

      # Remember the main window if any
      if defi[1] == 'MainWindow' :
        self.Main_Window = Component

      self.p_locals[ 'dummy' ] = Component
      exec ( '%s = dummy' %( defi[0] ), self.p_globals, self.p_locals )

      if ( defi[1] == 'MainWindow' ) and Font :
        print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ", defi[0])
        SetFont = '%s.setFont( Font )' %defi[0]
        exec ( SetFont, self.p_globals, self.p_locals )

      if 'self' in defi[0] :
        UserName = defi[0][5:]
        line = 'Value = My_IniFile.Read ( "' + defi[0] [ 5: ] + '", None )'
        self.Restore_Settings += line + '\n'
        self.Restore_Settings += 'if Value != None :\n'
        self.Restore_Settings += '  ' + defi[0] + '.SetValue ( Value )\n'

        #line = 'My_IniFile.Write ( "' + defi[0] [ 5: ] + '",' + defi[0]+ '.GetValue() )\n'
        line = 'Value = ' +  defi[0] + '.GetValue ()\n'
        line += 'if Value != None :\n'
        line += '  My_IniFile.Write ( "'+ defi[0] [ 5: ] + '", Value)\n'
        self.Current_Settings.append ( line )
      else :
        UserName = defi[0]

      # Search for autobind events,
      # i.e. there's no explicit bind in the GUI-string for this component,
      # but there exists a method 'self._On_%s' % ( UserName )'
      Key = 'bind'
      if ( UserName in self.Event_Methods ) and not ( Key in Kwargs ) :
        Bind_Event = Component.Named_Events.get('bind', None)
        if Bind_Event:
          Func = self.p_locals['self'].__dict__.get('_On_' + UserName, None)
          #try:
          #  Func = eval ( 'self._On_%s' % UserName, self.p_globals, self.p_locals )
          #except:
          #  Func = None
          if Func:
            Component.Bind( Bind_Event, Func)

      Indx = self.Update_Stack ( indent, Component )
      if Indx >= 0 :
        try:
          if Expand:
            try:
              self.stack [ Indx ] [1].SBox.addWidget ( Component ,stretch = 1)
            except:
              self.stack [ Indx ] [1].SBox.addWidget ( Component )
          else:
            #for debug
            """
            print('AA',Component, type(Component),isinstance(Component, QtGui.QWidget))
            print('BB',self.stack [ Indx ] [1], type(self.stack [ Indx ] [1]))
            try:
              print(Component.Label)
            except:
              print("NoLabel")
            print(args[0])
            """
            self.stack [ Indx ] [1].SBox.addWidget ( Component )
        except:
          import traceback
          traceback.print_exc ()
          print('**** Error adding ', defi, 'to parent, probably wrong indentation')
          if Indx - 1 >= 0:
            print('Trying to add widget to previous parent....')
            self.stack[Indx-1] [1].SBox.addWidget ( Component )
            print('Worked!')

    if self.Icon and self.Main_Window :
      Icon_File = os.path.join ( picture_support.Image_Path,self.Icon )
      self.Main_Window.setWindowIcon (QtGui.QIcon ( Icon_File ))

    # be sure we've an inifile
    if not ( self.IniFile ) and \
       not ( sys.gui_support_version in [ 'PYJD', 'PYJS' ] ) :
      Filename = Change_FileExt ( Application.Application, '_GUI_default.cfg' )
      self.IniFile = inifile ( Filename )
    print ( "<<<<<<<<<  GUI INIFILE =", self.IniFile.Filename )
    # **********************************************
    # Restore the settings from the inifile
    # **********************************************
    #if self.IniFile :
    # Bind MY onclose procedure to save all settings
    if self.Main_Window :
      self.Main_Window.Bind ( QEvent.Close, self._On_Close_ )

    self.IniFile.Section = 'Create_GUI_QT'
    self.p_globals [ 'My_IniFile' ] = self.IniFile

    #print self.IniFile,self.IniFile.Filename
    #print 'LLLLOOOAAD', self.Restore_Settings
    exec ( self.Restore_Settings, self.p_globals, self.p_locals )
    # **********************************************

    '''
    if self.IniFile :
      # Bind MY onclose procedure to save all settings
      ##eval ( self.Main_Window, self.p_globals, self.p_locals) .Bind (
      ##  QEvent.Close, self.__On_Close )
      if self.Main_Window :
        self.Main_Window.Bind (QEvent.Close, self.__On_Close )

      self.IniFile.Section = 'Create_GUI_QT'
      self.p_globals [ 'My_IniFile' ] = self.IniFile
      print 'Restore_Settings',self.Restore_Settings
      exec ( self.Restore_Settings, self.p_globals, self.p_locals )
    '''

    # for a dummy application (i.e. without an explicit wx.App)
    # we start the mainloop through the procedure Dummy_Show in this module
    if Dummy_App :
      Other_Self = eval( 'self', self.p_globals, self.p_locals )
      Other_Self.Show = Dummy_Show
      global Dummy_Main_Window_Show
      if self.Main_Window:
        Dummy_Main_Window_Show = self.Main_Window.Show

    # normally method Show must be coupled to the main window
    elif self.Main_Window :
      Other_self = eval ( 'self', self.p_globals, self.p_locals )
      Other_self.Show = self.Main_Window.Show
    print('De rest',perf_counter()-t)

  # ********************************************************
  # ********************************************************
  def _On_Close_ ( self, event ) :
    if self.Main_Window:
      self.Main_Window._On_Close ()    # actions needed before the final closure
    
    self.IniFile.Section = 'Create_GUI_QT'

    self.p_globals [ 'My_IniFile' ] = self.IniFile
    for line in self.Current_Settings:
      #print ( "Write INI", line )
      try :
        exec ( line, self.p_globals, self.p_locals )
      except :
        print('=====  ERROR in gui_support.Save_Settings =====')
        print(line)
        import traceback
        traceback.print_exc ()

    self.IniFile.Flush ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
#class Main_Application ( QtGui.QApplication ) :
class Main_Application ( QApplication ) :
  def __init__ ( self, IniFile = '', Splash = None,**kwargs ) :
    print('SYSSSARGV', sys.argv)
    #QtGui.QApplication.__init__ ( self, sys.argv )
    QApplication.__init__ ( self, sys.argv )

    if Splash :
      Icon_File = os.path.join ( picture_support.Image_Path, Splash )
      pixmap = QtGui.QPixmap ( Icon_File )
      splash = QtGui.QSplashScreen ( pixmap )
      splash.show()
      self.processEvents()

      ## MOET NOG ERGENS: splash.finish(&window)

    if not ( IniFile ) :
      IniFile = Base_GUI.Create_IniFileName ()

    self.IniFile = inifile ( IniFile )

  def MainLoop ( self ) :
    #sys.exit ( self.exec_() )
    self.exec_()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def My_Main_Application ( Form, **kwargs ) :
  app = Main_Application ( **kwargs )
  Frame = Form ( app.IniFile )
  Frame.Show ()
  app.MainLoop ()
  app.IniFile.Close ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Example(object):
  def __init__ ( self, IniFile = None ):
    GUI = """
    self.Main_Window2 ,MainWindow   ,label= 'Test QT'
#    self.Main_Window2 ,PanelHor   ,label= 'Test QT'
     PanelVer
      self.Splitter    ,SplitterVer
        self.Memo        ,TextCtrl
        PanelHor
          PanelVer
            ok             ,Button  ,label= 'OK'     ,bind= self._On_Ok
            cancel       ,X,Button  ,label= 'Cancel' ,bind= self._On_Cancel
            save           ,Button  ,label= 'Save'
      self.Splitter    ,SplitterHor
        self.Memo        ,TextCtrl
        PanelVer
            ok             ,Button  ,label= 'OK2'     ,bind= self._On_Ok
            cancel       ,X,Button  ,label= 'Cancel2' ,bind= self._On_Cancel
            save           ,Button  ,label= 'Save2'
    """
    self.wxGUI = Create_GUI ( GUI , IniFile, Icon = 'vippi_bricks.png' )

  def _On_Ok ( self, event = None ) :
    self.Memo.append ( 'OK!' )
    self.Memo.append ( '%s' %sys.gui_support_version )
    
#    from . import gui_support
#    from .dialog_support import Show_Message
    import gui_support
    from dialog_support import Show_Message
    
    Show_Message ( 'aap')
    self.Memo.append ( '%s' %sys.gui_support_version )

  def _On_Cancel ( self, event = None ) :
    self.Memo.append ( 'Cancel..' )
# ***********************************************************************


## ***********************************************************************
## VERY VERY IMPORTANT
## because there are wx libs imported, it switches to WX here above
## ***********************************************************************
sys.gui_support_version = 'QT'
## ***********************************************************************

# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 2 )

  if Test ( 1 ) :
    #app = Main_Application ( Splash = 'vippi_bricks.png' )
    Frame = Example ( ) #app.IniFile )
    Frame.Show()
    #app.MainLoop ()

  if Test ( 2 ) :
   My_Main_Application ( Example ) #, Splash = 'vippi_bricks.png' )

