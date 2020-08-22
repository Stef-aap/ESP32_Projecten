from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
from past.builtins import basestring
from builtins import object
import __init__

# ***********************************************************************
from language_support import _
from General_Globals  import *
# ***********************************************************************


# ***********************************************************************
_Version_Text = [

[ 1.1 , '31-09-2008', 'Stef Mientki',
'Test Conditions:', (2, ),
_(0, ' - Get_CallTip_Completion  added')],

[ 1.0 , '28-09-2008', 'Stef Mientki',
'Test Conditions:', (2, ),
_(0, ' - orginal release')]
]
# ***********************************************************************


# ***********************************************************************
#from visual import *
#import visual

import rlcompleter
import inspect
from inspect import *
from wx.py import introspect
import pickle
from  file_support import File_Exists, Force_Dir, Nice_Path
from utility_support import NoCase_Dict, NoCase_List

Special_Imports = {
  'DOM' : [ 'pyjamas' ],
  'pyjamas' : [ 'pyjamas', 'pyjamas.ui'],
  'wx'  : [ 'wx.gizmos', 'wx.grid', 'wx.lib', 'wx.stc' ],
  'stc' : [ 'wx.stc as stc' ]
}
# ***********************************************************************


# ***********************************************************************
# Determines the type of the partial string
# Returns     in caes of
#    int         56
#    str         'a string'
#    False       uncompleted string:  'a string
#    None        otherwise
# ***********************************************************************
def _Find_Type ( Part) :
  if ( Part.find ("'") >= 0 ) :
    start  = Part.find ( "'" )
    finish = Part.find ( "'", start + 1 )
    if finish < start :
      return False
    return str
  else :
    try :
      Typ = eval ( 'type ( '  + Part + ')' )
      # on integer, just return: "integer." will become a float
      if Typ == int :
        return int
    except :
      return None
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class my_Completer ( rlcompleter.Completer ) :
  def global_matches ( self, text ) :
    matches = []
    n = len ( text )
    text = text.lower ()

    # We only use self.namespace for autocompletion
    # And also ignore the case !!

    for word in self.namespace:
      if word[:n].lower() == text :
        matches.append(word)
    return matches
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def Get_Completions ( word, NameSpace = None ) :
  #print '********* start completion of :', word

  # *********************************************
  # parse the specified word
  # *********************************************
  Left_Part  = None
  Right_Part = word
  N_Parts    = 1
  if word.find('.') >= 0 :
    Word_Parts = word.split('.')
    N_Parts    = len ( Word_Parts )
    Left_Part  = '.'.join ( Word_Parts [ : -1 ] )
    Right_Part = Word_Parts [ -1 ]

  # *********************************************
  # Handle special type like integer / string
  # *********************************************
  Typ = None
  if not ( Left_Part ) :
    Typ = _Find_Type ( Right_Part )
    if Typ in ( False, int, str ) :
      return None
  else :
    Typ = _Find_Type ( Left_Part )
    if Typ in ( False, int ) :
      return None

    # if not a special type, import left_part
    if not ( Typ ) :

      # *********************************************
      # special import packages that can't be detected
      # *********************************************
      if Word_Parts [0] in Special_Imports :
        Imports = Special_Imports [ Word_Parts [0] ]
        for module in Imports :
          try :
            print('Special import :', module)
            exec ( 'import ' + module )
            Failed = False
          except :
            pass

      # *********************************************
      # import the necessary module
      # because we don't know how many parts on the left of the word
      # are module / path information ( instead of class information)
      # we start with the largest left part,
      # and each time we don't succeed we try one part less
      # *********************************************
      Failed = True
      N      = N_Parts
      while Failed and ( N > 1 ) :
        N -= 1
        module = '.'.join ( Word_Parts [ : N ] )
        try :
          exec ( 'import ' + module )
          Failed = False
        except :
          pass

  if Typ == str :
    Completion_Line = u'str.'
  else :
    Completion_Line = word
  RL = len ( Right_Part )
  #print 'CLine', Typ, RL, Completion_Line

  # *********************************************
  # Determine lenght of left part
  # *********************************************
  if Left_Part :
    LL = len ( Left_Part ) + 1
  else :
    LL = 0

  # *********************************************
  # get the completions
  # *********************************************
  if not ( NameSpace ) :
    NameSpace = locals ()
  Completer = my_Completer ( NameSpace )
  #rlcompleter.Completer ( NameSpace )
  State     = 0
  Result    = []
  #print 'UUU',Completion_Line, State
  try:
    Next      = Completer.complete ( Completion_Line, State )
    while Next :
      if Typ == str :
        if Next [ 4 ] != '_' :
          Result.append ( Next.replace ( 'str.', '' ) )
      else :
        # remove the part before the dot = left_part
        line = Next [ LL : ]
        # accept only items not starting with '_'  except '__init__'
        if line and ( ( line == '__init__' ) or ( line [ 0 ] != '_' ) ) :
          Result.append ( line )
      State  += 1
      Next = Completer.complete ( Completion_Line, State )
  except :
    pass

  # *********************************************
  # join the result and return
  # *********************************************
  if not ( Result ) :
    return None
  Result.sort()
  Result = ' '.join ( Result )
  return ( RL, Result )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_CallTip_Completion ( word, Arg_Index = 0 ) :
  #print '********* start CallTip of :', word
  pass

  """
  # *********************************************
  # get rid of everything starting at '(...'
  # and return if no left bracket
  # *********************************************
  i = word.find('(')
  if i < 0 :
    return
  word = word [ : i].strip()
  """

  # *********************************************
  # parse the specified word
  # *********************************************
  Word_Parts = word.split('.')
  N_Parts    = len ( Word_Parts )

  # *********************************************
  # special import packages that can't be detected
  # *********************************************
  if Word_Parts [0] in Special_Imports :
    Imports = Special_Imports [ Word_Parts [0] ]
    for module in Imports :
      try :
        #print 'Special import :', module
        exec ( 'import ' + module )
        Failed = False
      except :
        pass

  # *********************************************
  # import the necessary module
  # because we don't know how many parts on the left of the word
  # are module / path information ( instead of class information)
  # we start with the largest left part,
  # and each time we don't succeed we try one part less
  # *********************************************
  Failed = True
  N      = N_Parts
  while Failed and ( N > 0 ) :
    module = '.'.join ( Word_Parts [ : N ] )
    N -= 1
    try :
      exec ( 'import ' + module )
      Failed = False
    except :
      pass

  from wx.py import introspect
  import inspect

  # *********************************************
  # Get the object
  # *********************************************
  try:
    object = eval ( word, locals() )
  except:
    return None

  # *********************************************
  # get the objects name
  # *********************************************
  name = ''
  object, dropSelf = introspect.getBaseObject(object)
  try:
    name = object.__name__
  except AttributeError:
    pass

  # *********************************************
  # get arguments
  # *********************************************
  tip1 = ''
  argspec = ''
  if inspect.isbuiltin(object):
      # Builtin functions don't have an argspec that we can get.
      pass
  elif inspect.isfunction(object):
      # tip1 is a string like: "getCallTip(command='', locals=None)"
      argspec = inspect.formatargspec(*inspect.getargspec(object))
      if dropSelf:
          # The first parameter to a method is a reference to an
          # instance, usually coded as "self", and is usually passed
          # automatically by Python; therefore we want to drop it.
          temp = argspec.split(',')
          if len(temp) == 1:  # No other arguments.
              argspec = '()'
          elif temp[0][:2] == '(*': # first param is like *args, not self
              pass
          else:  # Drop the first argument.
              argspec = '(' + ','.join(temp[1:]).lstrip()
      tip1 = name + argspec


  # *********************************************
  # get doc
  # *********************************************
  doc = ''
  if callable(object):
    try:
      doc = inspect.getdoc(object)
    except:
      pass
  if doc:
      # tip2 is the first separated line of the docstring, like:
      # "Return call tip text for a command."
      # tip3 is the rest of the docstring, like:
      # "The call tip information will be based on ... <snip>
      firstline = doc.split('\n')[0].lstrip()
      if tip1 == firstline or firstline[:len(name)+1] == name+'(':
          tip1 = ''
      else:
          tip1 += '\n\n'
      docpieces = doc.split('\n\n')
      tip2 = docpieces[0]
      tip3 = '\n\n'.join(docpieces[1:])
      tip = '%s%s\n\n%s' % (tip1, tip2, tip3)
  else:
      tip = tip1

  #calltip = (name, argspec[1:-1], tip.strip())
  return tip.strip()

# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def Find_Classes ( my_module, my_path = None, prefix = '' ):
  import pyclbr
  if my_path != None:
    path = []
    path.append ( my_path )
    my_classes = pyclbr.readmodule_ex ( my_module, path )
  else:
    my_classes = pyclbr.readmodule_ex ( my_module )
    #my_classes = pyclbr.readmodule_ex ( my_module,
    #  [ 'D:/Data_Python_25/PyLab_Works/controls', 'D:/Data_Python_25/PyLab_Works'])

  # now order them by linenr
  ordered_list = []
  L = len ( prefix )
  for item in my_classes:
    if my_classes[item].module == my_module :
      name = my_classes [ item ].name
      if name [:L] == prefix :
        ordered_list.append ( ( my_classes[item].lineno,
                                my_classes[item].name [L:]  ) )
        """
        module -- the module name
        name -- the name of the class
        super -- a list of super classes (Class instances)
        methods -- a dictionary of methods
        file -- the file in which the class was defined
        lineno -- the line in the file on which the class statement occurred
        """

  # Sort the list
  ordered_list.sort()

  # now build a list with only brick names
  my_class_names = []
  for item in ordered_list:
    my_class_names.append ( item [1] )
  return my_class_names
# ***********************************************************************


# ***********************************************************************
# imports the module, instead of parsing like Find_Classes does.
# (No line_no support yet)
# See: PyLab_Works_search_bricks.py
# ***********************************************************************

from types import FunctionType, ModuleType, BuiltinFunctionType#, ClassType
from os.path import splitext
def Find_Classes_Fast ( my_module, my_path = None, prefix = '' ):

  import inspect
  try:
    A = __import__(my_module)
  except:
    #pass
    print('Find_Classes_Fast, __import__ failed from %s' % ( __module__ ))
    return
  ordered_list = []

  for i in dir(A):
    if i.startswith(prefix):
      Module = A.__dict__[i]
      if inspect.isclass(Module) or type(Module)==FunctionType or type(Module)==BuiltinFunctionType:
        try:
          #fil = inspect.getfile(Module)
          fil = inspect.getsourcefile(Module)
          if not fil:
            continue
        except:
          continue
        ## sourcefile      == sourcefile_of_module:
        ##print 'AAAAAA', A, fil
        if splitext(A.__file__)[0] == splitext(fil)[0]:
          #pass
          #print inspect.getsourcelines(Module)[-1]
          #print inspect.getmembers(Module)
          #meth = Module.Generate_Output_Signals
          # So, now we have the method.
          #func = meth.im_func
          # And the function from the method.
          #code = func.func_code
          # And the code from the function!
          #print code.co_firstlineno
          line_no = 0
          ordered_list.append( (line_no, i[len(prefix):] ) )

##  #['MatPlot_2D', 'PyPlot_XT', 'Scene_2D', 'VPython_Controls', 'Geo_Tool_Buttons', 'VPython', 'PyPlot_Signal', 'Generator', 'ADC', 'BP_Analysis', 'Scope_Display', 'Scope_Plot', 'Code_Editor', 'Code_Editor_In_Out', 'Print_Inputs', 'PyJamas', 'Circuit_Plots', 'Signal_Workbench', 'Code_Slider', 'Select_File', 'Read_Sound', 'Input_Selector', '_Play_Sound', 'BTC']
##  #['MatPlot_2D', 'PyPlot_XT', 'Scene_2D', 'Play_Sound', '_Play_Sound', 'VPython_Controls', 'Geo_Tool_Buttons', 'VPython', 'PyPlot_Signal', 'Generator', 'ADC', 'BP_Analysis', 'Scope_Display', 'Scope_Plot', 'Code_Editor', 'Code_Editor_In_Out', 'Print_Inputs', 'PyJamas', 'Circuit_Plots', 'Signal_Workbench', 'Code_Slider', 'Select_File', 'Read_Sound', 'Input_Selector', 'BTC']
##  def sort(a):
##      return A.__dict__['t_'+ a].After_Init.im_func.func_code.co_firstlineno
##  my_classes2.sort(key = sort)
##  #print Module, inspect.getsourcelines(Module)[-1]
##  #inspect.getsourcelines(object)
##  return my_classes2
  # Sort the list (on line_no)
  ordered_list.sort()

  # now build a list with only brick names
  my_class_names = []
  for item in ordered_list:
    my_class_names.append ( item [1] )
  return my_class_names
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def _Get_Doc ( Object ) :

  # *********************************************
  # if object is a class, we add the class documentation
  # *********************************************
  if inspect.isclass ( Object ) :
    Class_Doc = Object.__doc__
  else :
    Class_Doc = None
  Class_Doc = None

  # *********************************************
  # get the objects name
  # *********************************************
  name = ''
  object, dropSelf = introspect.getBaseObject(Object)
  try:
    name = object.__name__
  except AttributeError:
    pass

  # *********************************************
  # get arguments
  # *********************************************
  tip1 = ''
  argspec = ''
  if inspect.isbuiltin(object):
      # Builtin functions don't have an argspec that we can get.
      pass
  elif inspect.isfunction(object):
      # tip1 is a string like: "getCallTip(command='', locals=None)"
      argspec = inspect.formatargspec(*inspect.getargspec(object))
      if dropSelf:
          # The first parameter to a method is a reference to an
          # instance, usually coded as "self", and is usually passed
          # automatically by Python; therefore we want to drop it.
          temp = argspec.split(',')
          if len(temp) == 1:  # No other arguments.
              argspec = '()'
          elif temp[0][:2] == '(*': # first param is like *args, not self
              pass
          else:  # Drop the first argument.
              argspec = '(' + ','.join(temp[1:]).lstrip()
      tip1 = name + argspec


  # *********************************************
  # get doc
  # *********************************************
  doc = ''
  if callable(object):
    try:
      doc = inspect.getdoc(object)
    except:
      pass
  if doc:
      # tip2 is the first separated line of the docstring, like:
      # "Return call tip text for a command."
      # tip3 is the rest of the docstring, like:
      # "The call tip information will be based on ... <snip>
      firstline = doc.split('\n')[0].lstrip()
      if tip1 == firstline or firstline[:len(name)+1] == name+'(':
          tip1 = ''
      else:
          tip1 += '\n\n'
      docpieces = doc.split('\n\n')
      tip2 = docpieces[0]
      tip3 = '\n\n'.join(docpieces[1:])
      tip = '%s%s\n\n%s' % (tip1, tip2, tip3)
  else:
      tip = tip1

  if Class_Doc :
    tip += Class_Doc

  # remove empty lines
  New = ''
  tip = tip.splitlines()
  for line in tip :
    if line :
      New += line + '\n'

  #calltip = (name, argspec[1:-1], tip.strip())
  return New.strip()

# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class Doc_Info ( object ) :
  def __init__ ( self, Specials = [] ) :
    """
Base class for documentation info, contains cashed versions of
  - Autocompletion Lists
  - Tooltips for methods
If Specials is specified, special imports will be done.
  - web2py : list of globals is added
Specials can be
  - a single string
  - a string, containing space separated items
  - a list of strings
    """
    self._Tool_Tips_0        = NoCase_Dict ()
    self._Tool_Tips_0 [ '' ] = {}
    self._Auto_Completions_0 = NoCase_List ()
    self._Tool_Tips_1        = {}
    self._Auto_Completions_1 = {}
    self._Tool_Tips_2        = {}
    self._Auto_Completions_2 = {}
    self._Tool_Tips_3        = {}
    self._Auto_Completions_3 = {}
    self._Done               = []


  # *********************************************
  def Build_Specials ( self, Specials ) :
    if isinstance ( Specials, basestring ) :
      Specials = Specials.split ()

    for Special in Specials :
      if Special.lower () == 'web2py' :
        self._Auto_Completions_0.append ( 'response')
        self._Auto_Completions_0.append ( 'request')
        self._Auto_Completions_0.append ( 'session')
        self._Done.append ( 'request')
        self._Done.append ( 'response')
        self._Done.append ( 'session')

        line = '_vars,body,cookies,download,files,flash,headers,meta,menu,'
        line += 'postprocessing,render,session_file,session_file_name,'
        line += 'session_id,session_id_name,status,stream,'
        line += 'subtitle,title,view,write,xmlrpc'
        self._Auto_Completions_1 [ 'response' ] = line.split(',')

        line = 'application,controller,function,env,extension,view,'
        line += 'folder,args,vars,get_vars,post_vars,wsgi'
        self._Auto_Completions_1 [ 'request' ] = line.split(',')

        line = 'content_length,content_type,http_accept,http_accept_encoding,'
        line += 'http_accept_language,http_cookie,http_host,http_max_forwards,'
        line += 'http_referer,http_user_agent,http_via,http_x_forwarded_for,'
        line += 'http_x_forwarded_host,http_x_forwarded_server,path_info,'
        line += 'query_string,request_method,script_name,server_name,server_port,'
        line += 'server_protocol,web2py_path,we2bpy_version,web2py_runtime_gae,'
        line += 'wsgi_errors,wsgi_input,wsgi_multiprocess,wsgi_multithread,'
        line += 'wsgi_run_once,wsgi_url_scheme,wsgi_version'
        self._Auto_Completions_2 [ 'request.env' ] = line.split(',')

        line = 'connect,forget'
        self._Auto_Completions_1 [ 'session' ] = line.split(',')

        #sys.path.append ( r'P:\Web2Py\web2py_src\web2py\gluon' )
        Path = Nice_Path ( Application.Dir, '..', '..', 'web2py', 'gluon' )
        sys.path.append ( Path )
        ##?from   gluon.utils        import md5_hash #, web2py_uuid
        Libs = ( 'dal,html,sqlhtml,validators' )
        Libs = Libs.split ( ',' )
        for Lib in Libs :
          self._Build_Doc_Web2Py ( Lib )

        self._Auto_Completions_0.sort ()
        #print 'XXX', self._Auto_Completions_0
        #print 'YYY', self._Auto_Completions_1

  # *********************************************
  def _Build_Doc_Web2Py ( self, module_name ) :
    """ special version for web2py, which defines everything global """
    if module_name in self._Done :
      return

    self._Done.append ( module_name )

    Path = Nice_Path ( os.path.split ( __file__ ) [0], 'Doc_Info' )
    Force_Dir ( Path )
    Filename = os.path.join  ( Path, module_name + '.txt' )
    _TT   = {}
    _Auto = []
    if File_Exists ( Filename ) :
      fh = open ( Filename, 'r' )
      _TT, _Auto = pickle.load ( fh )
      fh.close ()
    else :
      exec ( 'import ' + module_name  + ' as _O_N_Z_I_N')

      Names = dir ( _O_N_Z_I_N )
      for Name in Names :
        if not ( Name.startswith ( '_' ) ) :
          try :
            Object = eval ( '_O_N_Z_I_N.'+ Name )
            _TT [ Name ] = _Get_Doc ( Object )
            _Auto.append ( Name )
          except :
            pass

      if len ( _Auto ) > 0 :
        fh = open ( Filename, 'wb' )
        pickle.dump ( ( _TT, _Auto ), fh, 0 )
        fh.close ()

    #self._Auto_Completions_0 [ module_name ] = _Auto
    for item in _Auto :
      if not ( item in self._Auto_Completions_0 ) :
        self._Auto_Completions_0.append ( item )
    self._Auto_Completions_0.sort ()
    #self._Tool_Tips_0 [ module_name ] = _TT
    #self._Tool_Tips_0 [ '' ]
    for key, value in list(_TT.items ()) :
      if not ( key in self._Tool_Tips_0 [ '' ]) :
        self._Tool_Tips_0 [ '' ] [ key ] = value


  # *********************************************
  def Build_Doc ( self, module_name ) :
    """
Gets all the Documentation and Objects from a library
with the name "module_name"
and adds them to the Autocompletion list and Tooltips dictionair.
This method is only executed once for each module_name.
The library must be findable.
The found doc-info is stored in a file.
If the file exists, the library is not analyzed,
but the information is fetched from the file.
    """
    if module_name in self._Done :
      return

    # *********************************************
    # parse the specified word
    # *********************************************
    Parts   = module_name.split('.')
    N_Parts = len ( Parts )

    # If just one word, add also to single word autocompletion list
    if N_Parts == 1 :
      if not ( module_name in self._Auto_Completions_0 ) :
        self._Auto_Completions_0.append ( module_name )
        self._Auto_Completions_0.sort ()

    self._Done.append ( module_name )
    Path = os.path.split ( __file__ ) [0]
    Filename = os.path.join  ( Path, 'Doc_Info', module_name + '.txt' )
    _TT   = {}
    _Auto = []
    if File_Exists ( Filename ) :
      fh = open ( Filename, 'r' )
      _TT, _Auto = pickle.load ( fh )
      fh.close ()
    else :
      # *********************************************
      # import the necessary module
      # because we don't know how many parts on the left of the word
      # are module / path information ( instead of class information)
      # we start with the largest left part,
      # and each time we don't succeed we try one part less
      # *********************************************
      Failed = True
      N      = N_Parts
      while Failed and ( N > 0 ) :
        module = '.'.join ( Parts [ : N ] )
        N -= 1
        try :
          exec ( 'import ' + module  + ' as _O_N_Z_I_N')
          Failed = False
        except :
          pass

      print('completer_support', N, Failed, module)
      Names = dir ( _O_N_Z_I_N )
      for Name in Names :
        if not ( Name.startswith ( '_' ) ) :
          try :
            Object = eval ( '_O_N_Z_I_N.'+ Name )
            _TT [ Name ] = _Get_Doc ( Object )
            _Auto.append ( Name )
          except :
            pass

      if len ( _Auto ) > 0 :
        fh = open ( Filename, 'wb' )
        pickle.dump ( ( _TT, _Auto ), fh, 0 )
        fh.close ()

    Tool_Tips = eval ( 'self._Tool_Tips_' + str ( N_Parts ) )
    Auto_Completions = eval ( 'self._Auto_Completions_' + str ( N_Parts ) )

    # Add the information to the internal lists and sort the list
    #for i, item in enumerate ( _TT ) :
    #  Tool_Tips [ item ] = _TT [ item ]
    #  Auto_Completions.append ( _Auto [i] )
    Auto_Completions [ module_name ] = _Auto
    Tool_Tips [ module_name ] = _TT

  # *********************************************
  def Get_Call_Tip ( self, word ) :
    Parts = word.split ( '.' )
    N_Dot = len ( Parts ) - 1

    if N_Dot == 0 :
      List = self._Tool_Tips_0['']
    else :
      Tool_Tips = eval ( 'self._Tool_Tips_' + str ( N_Dot ) )
      Key = '.'.join ( Parts [ : -1 ] )

      # If the left parts are not yet in the library lists,
      # try to import them
      if not Key in self._Done :
        self.Build_Doc ( Key )

      #print Key, N_Dot, Auto_Completions.keys ()
      if not ( Key in Tool_Tips ) :
        return []
      List = Tool_Tips [ Key ]

    Last = Parts [ -1 ] #.lower ()
    if Last in List :
      return List [ Last ]
    else :
      #return Get_CallTip_Completion ( word, Arg_Index = 0 )
      return ''

  # *********************************************
  def Get_Completions ( self, word ) :
    Parts = word.split ( '.' )
    N_Dot = len ( Parts ) - 1

    if N_Dot == 0 :
      List = self._Auto_Completions_0
    else :
      Auto_Completions = eval ( 'self._Auto_Completions_' + str ( N_Dot ) )
      Key = '.'.join ( Parts [ : -1 ] )

      # If the left parts are not yet in the library lists,
      # try to import them
      if not Key in self._Done :
        self.Build_Doc ( Key )

      #print Key, N_Dot, Auto_Completions.keys ()
      if not ( Key in Auto_Completions ) :
        return []
      List = Auto_Completions [ Key ]

    New = []
    Line = ''
    Last = Parts [ -1 ].lower ()
    #print Last, List
    for item in List :
      if item.lower().startswith ( Last ) :
        New.append ( item )
        Line += item + ' '
    New.sort ()
    return len ( Parts[-1] ), Line

    """
    Parts = word.split ( '.' )
    N_Dot = len ( Parts ) - 1

    if N_Dot == 0 :
      List = self._Auto_Completions_0
    else :
      Auto_Completions = eval ( 'self._Auto_Completions_' + str ( N_Dot ) )
      Key = '.'.join ( Parts [ : -1 ] )

      # If the left parts are not yet in the library lists,
      # try to import them
      if not Key in self._Done :
        self.Build_Doc ( Key )

      #print Key, N_Dot, Auto_Completions.keys ()
      if not ( Key in Auto_Completions ) :
        return []
      List = Auto_Completions [ Key ]

    New = []
    Line = ''
    Last = Parts [ -1 ].lower ()
    #print Last, List
    for item in List :
      if item.lower().startswith ( Last ) :
        New.append ( item )
        Line += item + ' '
    New.sort ()
    return len ( Parts[-1] ), Line
    """

# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
if __name__ == "__main__":

  Test_Defs ( 5 )

  if Test ( 1 ) :
    #print Get_Completions ( 'wx.' )
    words = []
    words.append ( 'wx.s' )
    words.append ( 'wx.g' )
    words.append ( 'wx.stc.wx' )
    words.append ( 'wx.stc.StyledTextCtrl.' )
    words.append ( 'wx.stc.StyledTextCtrl.Is' )
    words.append ( "'Aapje"  )
    words.append ( "'Aapje'." )
    words.append ( '68'  )
    words.append ( '68.' )
    words.append ( '68.4' )
    words.append ( 'stc.' )
    words.append ( 'w' )
    for word in words :
       v3print ( word, Get_Completions ( word ) )

  if Test ( 2 ) :
    NameSpace = {}
    NameSpace [ 'T1' ] = 'Therapie 1 template'
    NameSpace [ 'T2' ] = 'Therapie 2 template'
    NameSpace [ 'p'  ] = 'patient'
    NameSpace [ 'pr' ] = 'partner'
    words = []
    words.append ( 'T' )
    words.append ( 'T2' )
    words.append ( 'p' )
    words.append ( 'pr' )
    for word in words :
       v3print ( word, Get_Completions ( word, NameSpace ) )

  if Test ( 3 ) :
    print(Get_CallTip_Completion ( 'os.path.join', 1 ))
    #print Get_CallTip_Completion ( 'sys.')
    #print Get_CallTip_Completion ( 'sys.path.isdir(')

  if Test ( 4 ) :
    module = r'D:\Data_Python_25\PyLab_Works\bricks\brick_Plotting.py'
    import brick_Plotting
    module = 'brick_Plotting'
    print(Find_Classes ( module ))

  # **************************************************
  # Test Web2Py
  # **************************************************
  if Test ( 5 ) :
    """
    TT = Doc_Info ()

    words = []
    words.append ( 'os.pa' )
    words.append ( 'os.path.' )
    words.append ( 'os.path.j' )
    for word in words :
      print word, ':', TT.Get_Completions ( word )
    #sys.exit()

    words = []
    words.append ( 'os.path.join' )
    words.append ( 'os.path.jo' )
    for word in words :
      print word, '==>\n', TT.Get_Call_Tip ( word )

    #print  Get_CallTip_Completion ( word, Arg_Index = 0 )
    #print  Get_CallTip_Completion ( word, Arg_Index = 1 )
    sys.exit()
    """

    TT = Doc_Info ()
    TT.Build_Specials ( 'web2py' )

    words = []
    words.append ( 'os.' )
    words.append ( 'o' )
    words.append ( 'os' )
    words.append ( 'os.pa' )
    words.append ( 'os.path.' )
    words.append ( 'h' )
    words.append ( 'ht' )
    words.append ( 're' )
    words.append ( 'response.' )
    #for word in words :
    #  print word, ':', TT.Get_Completions ( word )

    """
    words = []
    words.append ( 'htm' )
    words.append ( 'html' )
    words.append ( 'os.path.jo' )
    words.append ( 'os.path.' )
    words.append ( 'os.path' )
    for word in words :
      print word, ':'#, TT.Get_Call_Tip ( word )
      print '=====', TT.Get_Completions ( word )
    """

    words = []
    #words.append ( 'os.path.join' )
    #words.append ( 'os.path.jo' )
    #words.append ( 'htm' )
    words.append ( 'HTML' )
    for word in words :
      print(word, '==>\n', TT.Get_Call_Tip ( word ))

    #print TT._Tool_Tips_0
    #for key, value in TT._Tool_Tips_0[''].iteritems () :
    #  print key
    print(TT._Tool_Tips_0['']['HTML'])
    sys.exit()


    class Request ( object ) :
      def __init__ ( self ) :
        self.aap = 3
        self.aap2 = 'beer'

    words = []
    words.append ( 'Request.' )
    words.append ( 'R.' )
    for word in words :
       v3print ( word, Get_Completions ( word ) )

    R = Request ()
    for word in words :
       v3print ( word, Get_CallTip_Completion ( word ) )

    print('RRRRRRR', dir(R))
    print(type(R))

    #import globals
    """
    from globals import Request
    print dir(Response)
    print Request.__dict__
    R = Request ()
    print dir ( R )
    print R.vars
    """

# ***********************************************************************
pd_Module ( __file__ )
