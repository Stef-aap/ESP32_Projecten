from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
import __init__

# ***********************************************************************
# This lowest level library should not import language support !!
# So it also can't use translated doc-strings
# ***********************************************************************
#from language_support import  _
__doc__ = """
This is very low level module,
to support several basic settings and debug features.
Every PyLab_Works module should import this module as the first import
in general even before the language translation module.
(Sorry, because it's low level, this string can't be translated.)
"""
# ***********************************************************************

_Version_Text = [

[ 0.3 , '07-07-2013', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- argument -userdir- added to application (WP 2.0)
""" ],

[ 0.2 , '03-06-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Version Text added
- All commandline arguments (lowercase) stored in dictionair Application.Args
    e.g. argument "-cfg-aap-beer" is stored as
    Application.Args { 'cfg' : 'aap-beer' }
""" ]

]

import os, sys
import time

Platform_Windows = sys.platform == "win32"


# ***********************************************************************
# Delay used for wx.CallLater
# ***********************************************************************
wxGUI_Delay = 100
if not ( Platform_Windows ) :
  wxGUI_Delay = 500
# ***********************************************************************




# ***********************************************************************
# ***********************************************************************
def v3print ( *args, **kwargs ) :
  """
  Print procedure equivalent to Python's version 3.
  """
  for arg in args :
    try:
      print(arg, end=' ')
    except:
      pass

  # if 'end' specified, use it
  if 'end' in kwargs :
    # if 'end' not an empty string, print it, followed by a comma
    if kwargs ['end'] :
      print(kwargs['end'], end=' ')
  # otherwise print an end-of-line
  else :
    print()
# ***********************************************************************

Global_Log = v3print


# ***********************************************************************
# ***********************************************************************
def Iterable ( var ) :
  """
Test if a variable is iterable.
Although strings are iterable, this function will return False for strings
(which is good !!)
"""
  return hasattr ( var, '__iter__')
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Ensure_Iterable ( var ) :
  """
Returns a var which is a iterable,
a string is put in a stringlist !!
"""
  if Iterable ( var ) :
    return var
  else :
    return [ var ]
# ***********************************************************************




# ***********************************************************************
# ***********************************************************************
def Module_Absolute_Path ( *args ) :
  """
  Calculate an absolute filename or path,
  from arguments relative to the module.
  Example:
    My_File = Module_Absolute_Path ( '..', 'sounds', 'T53.txt' )
  will generate, the normalized form of :
    <modules path> / .. / sounds / T53.txt
  """
  # find from which file this function is called
  My_Path = sys._getframe(1).f_code.co_filename
  My_Path = os.path.split ( My_Path ) [0]
  My_File = os.path.join ( My_Path, *args )
  My_File = os.path.normpath ( My_File )
  return My_File
# ***********************************************************************


# ***********************************************************************
# Functions that give problems accross OSs
# Always use these functions instead of the orginals !!
# ***********************************************************************
def path_split ( filename ) :
  # under Ubuntu a filename with both
  # forward and backward slashes seems to give trouble
  # already in os.path.split
  filename = filename.replace ( '\\','/')

  return os.path.split ( filename )
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def What_DO_I_Call ( Thing, Limit_Lines = None ) :
  import inspect
  SL = inspect.getsourcelines ( Thing )
  v3print ( 'Thing = ', Thing.__name__, '\n',
            '  File =', inspect.getmodule ( Thing ), '\n',
            '  Line Number =', SL[1] )
  for line in SL[0] [ : Limit_Lines ] :
    v3print ( line.rstrip() )
# ***********************************************************************


"""
# *******_***************************************************************
# First add all the paths to the Python Path
# we don't use file_support here,
# because we want this to be and stay a low level module
# ***********************************************************************
import os, sys

def Find_Paths ( path , Paths ) :
  files = os.listdir ( path )
  for f in files :
    file = os.path.join ( path, f )
    if os.path.isdir ( file ) :
      Paths.append ( os.path.abspath ( file ) )
      Find_Paths ( file, Paths )

Paths = []
Find_Paths ( '../', Paths )

for subdir in Paths :
  if not ( subdir in sys.path) :
    sys.path.append ( subdir )
#print sys.path
# ***********************************************************************
"""

# ***********************************************************************
# WHAT TO DEBUG ( if Debug flag on )
# Just (un-)comment the following lines
# ***********************************************************************
Debug_What = set ()
#Debug_What.add ( 'Load_Save' )
#Debug_What.add ( 'TIO-Read' )
#Debug_What.add ( 'TIO-Write' )
# ***********************************************************************
# And in the following lines, just change the number
# if necessary
# At the moment we allow:
#   0 = not deep
#   1 = deeper
#   2 = deepest
# ***********************************************************************
Debug_How_Deep = {}
Debug_How_Deep [ 'TIO_Read' ] = 2
Debug_How_Deep [ 'Brick' ] = 2
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Debug_Dump ( *args ) :
  from inifile_support import inifile

  Pre   = '\n++ '
  After = ' '
  line = ''
  for item in args :
    if isinstance ( item, inifile ) :
      line += item.Filename
    else :
      line += item.__str__()
    line += After
  line = line.replace ( '\n','\n    ')

  line = Pre + line
  print(line)
# ***********************************************************************
# ***********************************************************************
def Debug_Dump_Trace ( *args ) :
  Debug_Dump ( *args )
  Debug_From ( 3 )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Debug_From ( Level = 2 ) :
  """
  Display information about the CALLER
  """
  NDeep = 10
  My_Dir = path_split ( Application.Dir ) [0]
  My_File = False
  #Level = 1 #4
  pre = '   '
  while not ( My_File ) and ( Level < 20 ):
    try:
      F = sys._getframe ( Level )
      path, filename = path_split ( F.f_code.co_filename )
      if path.startswith ( My_Dir ) :
        for i in range ( NDeep ) :
          #'%5d' %( int(value) )
          print(pre + 'Called from : %5d,' %(F.f_lineno), filename)

          # Stop when top level of the application found
          if filename == Application.FileName :
            break

          Level += 1
          #pre += '  '
          F = sys._getframe ( Level )
          filename = path_split ( F.f_code.co_filename )[1]
        return

      Level += 1
    except :
      return
  print("  **** Debug, can't find CALLER, level =", Level)
# ***********************************************************************




# ***********************************************************************
# ***********************************************************************
def exprint ( *args ) :
  """
  Print procedure with Traceback.
  """
  for arg in args :
    print(arg, end=' ')
  print()
  print ('____________ Print Traceback ____________')
  Debug_From ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Application_Object ( object ) :
  def __init__ ( self ) :
    Parameters_Help = """
    a parameter without a preceeding minus: application to launch
    otherwise;

    -cfg-xxxxxx    xxxx is the configfile to use
    -debug
    -debugfile
    -debugtable
    -demo
    -design
    -editflags,    Let the user edit the flags + clipboard copy,
                   Not yet implemented
    -original
    -TestRun
    -testall
    -testxxx,      where xxx is series of digits
    -user-xxx,     Alt_User, will replace the User in non-critical applications
    -userdir-xxx,  Alt User Directory (to store config file etc
    -afd-xxx,      Afdeling for RadQuest
    -vmdelayxxxx,  where xxxx is delay in msec
    -wx_inspect

    -os-xxxxxx     force the program to run in this mode (for testing only)
                   where xxxxxx = Windows / Linux / ...

    """
    self.Application = sys.argv[0]
    self.Dir = os.getcwd ()
    self.FileName = path_split    ( self.Application   ) [1]
    self.FileName_Only, ext = os.path.splitext ( self.FileName )
    self.Start_Config_File = None
    self.Start_Application = None
    self.Alt_User = None

    # Set some global debug vars
    global _pd, _pd_nr, _pd_pd_pre, _pd_FileName, _pd_flags, _pd_file, _pd_testall
    _pd_nr = 0
    ##print '************** ALARM *************'
    _pd_FileName = os.path.join ( self.Dir, self.FileName_Only + '_debug.txt')

    # determine the commandline flags
    _pd_pd_pre = '-- '
    _pd_flags = sys.argv
    _pd =         ( '-debug'     in sys.argv [ 1 : ] ) or \
                  ( '-debugfile' in sys.argv [ 1 : ] )
    _pd_file =    ( '-debugfile' in sys.argv [ 1 : ] )

    _pd_testall = ( '-testall'   in sys.argv [ 1 : ] )


    """
    # find strings ala "-test127"
    if ( '-test'      in sys.argv [ 1 : ] ) :
      for arg in sys.argv [ 1 : ] :
        if arg.startswith ( '-test' ) and ( arg [ 5 : ].isdigit ) :
          tests = []
          for digit in arg [ 5 : ] :
            tests.append ( int ( digit ) )
          Test_Defs ( tests )
    """

    # Find the numeric flags
    self.VM_Delay = 19 / 1000.0    #normally 50 fps
    self.Args = {}
    for xx, arg in enumerate ( sys.argv [ 1 : ] ) :
      # Store all arguments in a dictionair
      a = arg.split('-')

      # ignore empty space
      if not ( arg.strip () ) :
        continue

      print('Command Line arg %s: %s = %s' % ( xx+1, arg, a ))

      if len (a ) > 1 :
        self.Args [ a[1].lower() ] = '-'.join ( a[2:] )

      if arg.startswith ( '-cfg-' ) :
         self.Start_Config_File = arg [ 5 : ]

      elif arg.startswith ( '-apps-' ) :
         self.Start_Application = arg [ 6 : ]

      elif arg.startswith ( '-user-' ) :
         self.Alt_User = arg [ 6 : ]

      # IMPORTANT CHANGE FOR WP 2.0
      # The user directory can be set here
      elif arg.startswith ( '-userdir-' ) :
         self.Dir = arg [ 9 : ]

      # IMPORTANT CHANGE FOR WP 2.0
      # The user directory can be set here
      elif arg.startswith ( '-afd-' ) :
         self.Afdeling = arg [ 5 : ]

      elif arg.startswith ( '-os-' ) :
         Forced_System = arg [ 4 : ]
         global Platform_Windows
         if Forced_System.lower() == 'windows' :
           Platform_Windows = True
         elif Forced_System.lower() == 'linux' :
           Platform_Windows = False

      # find strings ala "-test127"
      elif arg.startswith ( '-test' ) and ( arg [ 5 : ].isdigit ) :
        tests = []
        for digit in arg [ 5 : ] :
          tests.append ( int ( digit ) )
        ##Test_Defs ( tests )

      elif arg.startswith ( '-vmdelay' ) and ( arg [ 8 : ].isdigit ) :
        self.VM_Delay = int ( arg [ 8: ] ) / 1000.0

      elif '?' in arg :
        print(Parameters_Help)
        sys.exit ()

    #if  '-VP3' in sys.argv [ 1 : ] :
    #  self._VPython_Version = 3
    #else :
    #  self._VPython_Version = 5

    # Get the config file
    for arg in sys.argv [ 1 : ] :
      # to prevent the filenurse flag |---------------|
      if ( arg[0] != '-' ) and        ( arg[1] != ':' ):
        self.Config_File = arg
        break
    else :
      self.Config_File = None

    self.Debug_Mode      = _pd
    self.Demo_Mode       = '-demo'       in sys.argv [ 1 : ]
    self.Debug_Table     = '-debugtable' in sys.argv [ 1 : ]
    self.Orgininal       = '-original'   in sys.argv [ 1 : ]
    self.WX_Inspect_Mode = '-wx_inspect' in sys.argv [ 1 : ]
    self.Design_Mode     = '-design'     in sys.argv [ 1 : ]

    # special: Uppercase characters !!
    # This parameter is intended for automatic test runs
    self.TestRun = '-TestRun' in sys.argv [ 1 : ]

    self.Restart = False
# ***********************************************************************



# ***********************************************************************
# Create the application Object
Application = Application_Object ()
# ***********************************************************************


Application._VPython_Version = 5
"""
# ***********************************************************************
# ***********************************************************************
def Get_Visual ( Version = 3 ) :
  import os, sys
  for path in sys.path :
    if path.endswith ( 'site-packages') :
      break
  vpath = os.path.join ( path, 'visual' )
  if ( Version == 3 ) and os.path.exists ( vpath + '3' ) :
    print 'Visual ==> 3', vpath
    os.rename ( vpath, vpath + '5' )
    os.rename ( vpath + '3', vpath )
  elif ( Version == 5 ) and os.path.exists ( vpath + '5' ) :
    print 'Visual ==> 5', vpath
    os.rename ( vpath, vpath + '3' )
    os.rename ( vpath + '5', vpath )
# ***********************************************************************


# ***********************************************************************
# BY DEFAULT WE WANT VPYTHON VERSION-3 !!
# So you must override it, when you want version 5
# ***********************************************************************
print 'VPython Version =', Application._VPython_Version
Get_Visual ( Application._VPython_Version )
# ***********************************************************************
"""



# ***********************************************************************
# ***********************************************************************
"""
class Null ( object ) :
  def __getattr__ ( self, attr ) :
    try:
      return super ( self.__class__, self ).__getattr__ ( attr )
    except AttributeError:
      if attr in ('__base__', '__bases__', '__basicsize__', '__cmp__',
                  '__dictoffset__', '__flags__', '__itemsize__',
                  '__members__', '__methods__', '__mro__', '__name__',
                  '__subclasses__', '__weakrefoffset__',
                  '_getAttributeNames', 'mro'):
        raise
      else:
        return self

  def next ( self ) :
    raise StopIteration

  def __str__(self):
    "Convert to a string and return it."
    return 'Null'

  __repr__ = __str__

  def __init__ ( self, *args, **kwargs ) :
    pass

  def __len__ ( self ) :
    "ensures that 'if myself:' works correctly"
    return 0

  def __eq__ ( self, other ) :
    return self is other

  def __hash__ ( self ) :
    return hash ( None )

  def __call__ ( self, *args, **kwargs ) :
    return self

  __sub__ = __div__ = __mul__ = __floordiv__ = __mod__ = __and__ = __or__ = \
  __xor__ = __rsub__ = __rdiv__ = __rmul__ = __rfloordiv__ = __rmod__ = \
  __rand__ = __rxor__ = __ror__ = __radd__ = __pow__ = __rpow__ = \
  __rshift__ = __lshift__ = __rrshift__ = __rlshift__ = __truediv__ = \
  __rtruediv__ = __add__ = __getitem__ = __neg__ = __pos__ = __abs__ = \
  __invert__ = __setattr__ = __delattr__ = __delitem__ = __setitem__ = \
  __iter__ = __call__

# Create the Null object
Null = Null ()
"""
# ***********************************************************************


# ***********************************************************************
"""
  # Set in code which tests should be performed
  # This doesn't affect the order in which the tests are performed
  Test_Defs ( 2, 7 )

  # In the code you can test which tests should be performed
  if Test ( 2 ) :
    .. do it

  # Commandline parameters can add settings
  -testall  :all tests will be performed
  -test239  :tests 2, 3, 9 will be added

"""

# ***********************************************************************
_GG_Test_Defs = []
_GG_Start_Time = None
# ***********************************************************************
def Test_Defs ( *args ) :
  global _GG_Test_Defs, _GG_Start_Time
  for arg in args :
    _GG_Test_Defs.append ( arg )
  _GG_Start_Time = time.time()
# ***********************************************************************
def Test ( *args ) :
  global _GG_Test_Defs, _pd_testall
  if _pd_testall :
    v3print ( '***** Test ', args, '*****' )
    return True
  for arg in args :
    if arg in _GG_Test_Defs :
      v3print ( '***** Test ', args, '*****' )
      return True
  else :
    return False
# ***********************************************************************
def Test_Time () :
  """
  Can be used to print the elapsed timer after all tests have run
  """
  v3print ( '==> Elapsed Time [s] =', int ( time.time() - _GG_Start_Time ) )
# ***********************************************************************


_PD_Start_Time = time.time ()

# ***********************************************************************
# ***********************************************************************
def _pd_pre () :
  global _pd_nr
  _pd_nr += 1
  return _pd_pd_pre + str ( _pd_nr ) + ': '
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def pd ( line_user )  :
  global _PD_Start_Time
  line_user = _pd_pre() + line_user
  if _pd:
    if _pd_file :
      if _pd_nr == 1 :
        from datetime import date
        import os
        print(sys.argv[0])
        print(os.path.basename(sys.argv[0]))

        line = '\n' + 80 * '*' + '\n'
        line += str ( date.today () )
        line += '  OS: ' + os.name + ' / ' + sys.platform
        line += '\nPython: ' + sys.version
        line += '\n' + 'Command Line: ' + str ( sys.argv [ 1 : ] )

        fh = open ( _pd_FileName, 'a' )
        fh.write ( line  + '\n')
        fh.close ()

      # now write the normal information
      fh = open ( _pd_FileName, 'a' )
      fh.write ( line_user + '\n')
      fh.close ()
    print(line_user.ljust(80), int ( 1000 * ( time.time() - _PD_Start_Time ) ))
    _PD_Start_Time = time.time ()


    """
    for Path in sys.path :
      if not ( Path.startswith ( 'P:') ) :
        print Path
    """
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def pd_Module ( line = None ):
  """
  This procedure will print the imported module, if debug mode is on.
  Usage, at the bottom of each module, place the following line:
    pd_Module ( __file__ )

  Or for standard library files, for which you're interested, e.g. numpy
    import numpy
    pd_Module ( 'Numpy' )

  For modules launched with execfile, "__file__" doesn't exist,
  so you'll get an error message when the program closes.
  Therefor it's also allowed to use the function without parameter
    pd_Module ()
  In which case the procedure will evaluate the filename.
  Unfortunately in the latter case you can't see if the 'py' file
  or the 'pyc'-file is loaded.
  """
  if not ( line ) :
    line = sys._getframe(1).f_code.co_filename
  pd ( 'Imported : ' + os.path.normpath ( line ) )
# ***********************************************************************


# ***********************************************************************
def test():
  "Perform some decent tests, or rather: demos."

  # constructing and calling

  n = Null()
  n = Null('value')
  n = Null('value', param='value')

  n()
  n('value')
  n('value', param='value')

  # attribute handling

  n.attr1
  n.attr1.attr2
  n.method1()
  n.method1().method2()
  n.method('value')
  n.method(param='value')
  n.method('value', param='value')
  n.attr1.method1()
  n.method1().attr1

  n.attr1 = 'value'
  n.attr1.attr2 = 'value'

  del n.attr1
  del n.attr1.attr2.attr3

  # representation and conversion to a string

  print('$$', repr(n), str(n))
  #assert repr(n) == '<Null>'
  #assert str(n) == '<Null>'
  print(dir(n))
  print(not(n))

  a = Null() ; d = Null() ; j = Null(3)
  j **= (d + 3) * (old_div(a, j))
  print(j is j('parameters', any='parameters').attribute.access.is_.allowed['and item']()())
  print((d < j, d > j, d == j))
  print(sorted([Null(n + d) for n in range(3)]), sorted(a))
  print('%d == %d == 0' % (len(a), len(list(a))))

  a = Null
  if a :
    print('not NUll')
  else :
    print('NULLLLLL')
  print(a)
  print(a == Null)
  print(a == None)
# ***********************************************************************



# ***********************************************************************
# At this moment we may call other libraries of our own
# so here we can extend our Application object
# ***********************************************************************
# Get the General Inifile
from inifile_support import inifile
#Path, File = path_split ( __file__ )
Path = sys._getframe().f_code.co_filename
Path = os.path.split ( Path ) [0]

filnam = os.path.join ( Path, 'General_Global_Settings.cfg' )
Application.General_Global_Settings = inifile ( filnam )

from system_support import Get_User
Application.User = Get_User ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == '__main__':
    test()
# ***********************************************************************

pd_Module ( __file__ )
