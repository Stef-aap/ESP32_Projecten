from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from past.builtins import basestring
from builtins import object

import sys
import os
import __main__

from   completer_support import Find_Classes_Fast

from   General_Globals   import Application
from   system_support    import Get_User

_Version_Text = [
[ 1.2 , '11-8-2020', 'Stef Mientki',
'Test Conditions:???', (2,),
"""
- Create_IniFileName modified for python 3
"""],

[ 1.1 , '25-8-2011', 'Stef Mientki',
'Test Conditions:???', (2,),
"""
- self.stack uitgebreid met de naam van de component
- Extra in self.GUI, vervangen door Args, Kwargs
"""],

[ 1.0 , '19-07-2011', 'Robbert Mientki',
'Test Conditions:???', (2,),
"""
- Initial release
"""]
]


# ***********************************************************************
# ***********************************************************************
_U_N  = '_UN_'
_U_Nr = 0

def _Get_UN () :
  global _U_N, _U_Nr
  Name = _U_N + str ( _U_Nr )
  _U_Nr += 1
  return Name
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Create_IniFileName () :
  Filename =  __main__.__file__ 

  User = Application.Alt_User
  if not User :
    User = Get_User ()

  IniFile_Name = os.path.splitext ( Filename )[0] + '_' + User + '.cfg'
  ##IniFile_Name = os.path.splitext ( Filename )[0] + '_Test.cfg'
  print('>>>> USER & Inifile', User, IniFile_Name)
  return IniFile_Name

# ***********************************************************************


from time import perf_counter
# ***********************************************************************
# ***********************************************************************
class _Prepare_GUI_Lines ( object ) :
  def __init__ ( self,
                 GUI,
                 IniFile = None,
                 StackUp = 1,
                 Icon    = None,
                 **kwargs  ) :
    self.GUI              = GUI
    self.Icon             = Icon
    self.IniFile          = IniFile
    self.Current_Settings = []
    self.Restore_Settings = ''

    # Determine all classes in the GUI library
    #tt = clock()
    My_GUI = sys._getframe (1).f_globals['__file__']
    My_GUI = os.path.splitext ( os.path.split ( My_GUI )[1] ) [0]
    FC = Find_Classes_Fast ( My_GUI )
    #print 'Findclasses BaseGUI',clock() - tt

    StackUp += 1
    self.p_locals  = sys._getframe ( StackUp ).f_locals
    self.p_globals = sys._getframe ( StackUp ).f_globals

    # search for evnt handlers that can be used by autobind,
    # i.e. methods that start with '_On_'
    Methods = dir ( self.p_locals [ 'self' ] )
    self.Event_Methods = []
    for Method in Methods :
      if Method.startswith ( '_On_' ) :
        self.Event_Methods.append ( Method [ 4: ] )
    ##print 'Event_Methods =', self.Event_Methods

    # Initialize the stack with the input values
    self.stack        = []
    self.Main_Window  = None

    # traverse to all the lines in the definition
    self.GUI = []
    for defi in GUI.splitlines() :

      # ignore commented and empty lines
      if defi.strip().startswith ( '#' ) or not ( defi.strip() ):
        continue
      #print defi
      # ignore comment part of a line
      if '#' in defi :
        defi = defi.split ( '#' )[0]

      # split the line into elements
      defi = defi.split(',')

      # replace some KNOWN shortcuts, only used by PyJamas
      ##print 'DDEFI', defi
      try :
        for i, d in enumerate ( defi ) :
          d = d.strip()
          if d in self.ShortCuts :
            defi [i] = self.ShortCuts [ d ]
      except :
        #import traceback
        #traceback.print_exc()
        pass

      # determine the leading spaces
      indent = len ( defi[0] ) - len ( defi[0].lstrip() )

      # if nameless components,
      # Create a unique name and update defi
      if defi[0].strip() in FC :
        defi = [ _Get_UN () ] + defi
      #elif defi[0].strip().startswith ( 'NN_' ) :
      #  defi[0] = defi[0].strip()[3:]
      #  defi = [ _Get_UN () ] + defi

      #elif defi[0].strip() in ( [ 'Spacer', 'SpacerVer', 'SpacerHor' ] + Nameless_Objects ):
      #  defi = [ _Get_UN () ] + defi

      # remove white space from all elements
      for i,item in enumerate ( defi ) :
        defi[i] = defi[i].strip()

      """
      # parse the line: <name> <type> <params>
      if not ( self.Main_Window  ) :
        self.Main_Window = defi[0]
      """

      # ***************************
      # expand component ? read and remove it
      # ***************************
      Expand = 0
      #print '>*>DEFI',defi
      if defi[1].lower() == 'x' :
        Expand = 1
        defi = defi [:1] + defi [2:]
      # for nameless components the 'X' might occur 1 position further
      elif ( len (defi) > 2 ) and ( defi[2].lower() == 'x' ):
        Expand = 1
        defi = defi [:2] + defi [3:]

      # ***************************
      # get the extra parameters
      # ***************************
      #Kwargs = {}
      arguments = ','.join(defi[2:])
      exec('def dummy(*args,**kwargs): return args,kwargs',self.p_globals, self.p_locals)

      ##print defi
      ##print 'PPPPPGGGG','dummy('+arguments+')',
      Args, Kwargs = eval('dummy('+arguments+')',self.p_globals,self.p_locals)

      ##print args,Extra
      ##if args:
      ##  print '**** Non keyword arguments (evaluated):',args

      # ***************************
      # ***************************
      if not ( defi[1] in FC ) :
        print('***** DEPRECEATED Component :', defi[1])

      # ***************************
      # ***************************
      self.GUI.append ( ( indent, defi, Args, Kwargs, Expand ) )

    # if we have a sub-gui, docked on some previous definied panel
    # throw the docking panel on the stack with indent = 0
    # ( so a sub-gui must have an indent > 0 !!! )
    Parent = kwargs.get ( 'Parent', None )
    if Parent :
      self.stack.insert ( 0, [ 0, Parent, 'Dock' ] )

  # ********************************************************
  # ********************************************************
  ##def Update_Stack ( self, My_Indent, Me = None ) :
  def Update_Stack ( self, My_Indent, Me = None, MyName = '' ) :
    # remove all elements at the end of the stack,
    # with a larger indent than myself
    while ( len ( self.stack ) > 0 ) and ( self.stack [-1][0] > My_Indent ) :
      self.stack.pop ()

    # Add myself to the stack
    if Me :
      self.stack.append ( [ My_Indent, Me, MyName
       ] )

    # Find my Parent
    i = len ( self.stack )
    while i > 0 :
      i -= 1
      if self.stack [i][0] < My_Indent :
        if self.stack [i][0] > 0 :
          return i
        else :
          return i
    return -1

  # ********************************************************
  # ********************************************************
  def __repr__ ( self ) :
    Text = ''
    Text += '------ parsed GUI-string  --------------------------------------\n'
    for item in self.GUI :
      Line = ( 2 + item[0] ) * ' '
      Line += '  ,'.join ( item[1] )
      ##Line += str ( item[2] )
      if item[4] :
        Line += '  ,EXPAND'
      ##Line += ' :::' + str ( item[3] )
      Text += Line + '\n'
    Text += '------ end parsed GUI-string  --------------------------------------\n'
    return Text
# ***********************************************************************
