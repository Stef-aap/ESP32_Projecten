from __future__ import print_function
from __future__ import absolute_import
from past.builtins import basestring
from builtins import object
# -*- coding: utf-8 -*-

import __init__

# ***********************************************************************
__doc__ = """
doc_support.py :

License: freeware, under the terms of the BSD-license
Copyright (C) 2011 Stef Mientki
"""

# ***********************************************************************


# ***********************************************************************
from General_Globals import *
from language_support import _
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
_Version_Text = [

[ 0.2, '31-07-2011', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
- Generate_Doc_File added
""" ) ],

[ 0.1, '28-07-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
    - orginal release
""" ) ]
]
# ***********************************************************************


import os
from   inspect import *
import inspect
import pyclbr
import re

# ***********************************************************************
# ***********************************************************************
def Get_Classes_And_Functions ( my_module, my_paths = [] ):
  """
  Creates a list with all classes and functions defined in my_module
  (Imported items are excluded)
  If the module is NOT on the Pythonpath, my_paths must be specified.
    my_paths is one of the following: empty / string / list of strings
  The returned result consist of
    List (Ordened by Name) :
      Name, LineNr, { '<method>' : linenr }
    Full filename (including full path) of the scanned module
  For functions there are no methods
  """

  # if paths is a string, make it a one-item list
  if isinstance ( my_paths, basestring ) :
    my_paths = [ my_paths ]

  My_Classes = pyclbr.readmodule_ex ( my_module, my_paths )
  """ Returns :
  module  -- the module name
  name    -- the name of the class
  super   -- a list of super classes (Class instances)
  methods -- a dictionary of methods: { '<method>' : linenr }
  file    -- the file in which the class was defined
  lineno  -- the line in the file on which the class statement occurred
  """

  # now order them by linenr
  #print my_classes
  Ordened_List = []
  My_File  = None
  for key in My_Classes:
    item = My_Classes [ key ]
    if item.module == my_module :
      # if the filename (including path) not yet read, do it here once
      if not ( My_File ) :
        My_File = item.file
      temp = [ item.name, item.lineno ]
      if isinstance ( item, pyclbr.Class ):
        temp.append ( item.methods )
      Ordened_List.append ( temp )

  Ordened_List.sort ()
  return Ordened_List, My_File
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Classes_And_Functions_Split2 ( my_module, my_paths = [] ):
  """
  Creates a list with all classes and functions defined in my_module
  (Imported items are excluded)
  If the module is NOT on the Pythonpath, my_paths must be specified.
    my_paths is one of the following: empty / string / list of strings
  The returned result consist of
    List (Ordened by Name) :
      Name, LineNr, { '<method>' : linenr }
    Full filename (including full path) of the scanned module
  For functions there are no methods
  """

  # if paths is a string, make it a one-item list
  if isinstance ( my_paths, basestring ) :
    my_paths = [ my_paths ]

  My_Classes = pyclbr.readmodule_ex ( my_module, my_paths )
  """ Returns :
  module  -- the module name
  name    -- the name of the class
  super   -- a list of super classes (Class instances)
  methods -- a dictionary of methods: { '<method>' : linenr }
  file    -- the file in which the class was defined
  lineno  -- the line in the file on which the class statement occurred
  """

  # now order them by linenr
  #print my_classes
  Function_List = []
  Class_List = []
  My_File  = None
  for key in My_Classes:
    item = My_Classes [ key ]
    if item.module == my_module :
      # if the filename (including path) not yet read, do it here once
      if not ( My_File ) :
        My_File = item.file
      if isinstance ( item, pyclbr.Class ):
        Class_List.append ( [ item.name, item.lineno, item.methods ] )
      else :
        Function_List.append ( [ item.name, item.lineno ] )

  Function_List.sort ()
  Class_List.sort ()
  return Function_List, Class_List, My_File
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def Get_Classes_And_Functions_Split ( my_module, underscore = '_' ):
  """
  Creates a list with all classes and functions defined in my_module
  Much faster than Get_Classes_And_Functions_Split2
  (Imported items are excluded)
  The returned result consist of
    Function List (Ordened by Name),
    Class List    (Ordened by Name)
  """
  Function_List = []
  try :
    #exec ( 'import ' + my_module +' as Mod' )
    Mod = __import__ ( my_module )
    List = getmembers ( Mod, isfunction )
    for item in List :
      if ( item[0][0] != underscore ) and \
         ( my_module in getfile ( item[1] ) ) :
        Function_List.append ( item[0] )
  except :
    pass

  Class_List = []
  try :
    #exec ( 'import ' + my_module +' as Mod' )
    Mod = __import__ ( my_module )
    List = getmembers ( Mod, isclass )
    for item in List :
      if ( item[0][0] != underscore ) and \
         ( my_module in getfile ( item[1] ) ) :
        Class_List.append ( item[0] )
  except :
    pass

  return Function_List, Class_List
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def _Get_My_Object ( my_module, my_class, my_method = None ) :
  try :
    # The 2 solutions below are identical
    #exec ( 'import '+ self.PyFile )
    #CL = eval ( self.PyFile + '.' + my_class )

    #exec ( 'from ' + my_module + ' import ' + my_class )
    MA = __import__ ( my_module )
    if my_method :
      #CL = eval ( my_class + '.' + my_method )
      CL = getattr ( MA, my_method )
    else :
      #CL = eval ( my_class )
      CL = MA
  except :
    return None

  # check if it's not an method imported from another module
  source_file = getfile ( CL )
  if not ( my_module in source_file ) :
    return None

  return CL
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Class_Methods ( my_module, my_class, underscore = '_' ) :
  CL = _Get_My_Object ( my_module, my_class )
  if CL:
    List = getmembers ( CL, ismethod )
    CM = []
    for C in List :
      """ getfile( object)
      Return the name of the (text or binary) file in which an object was defined.
      This will fail with a TypeError if the object is a built-in module, class, or function.
      """
      """
      if ( my_module in getfile ( C[1] ) ) and \
         ( C[0][0] != underscore ):
        CM.append ( C[0] )
      """
      if C[0][0] != underscore :
        try :
          if my_module in getfile ( C[1] ) :
            CM.append ( C[0] )
        except :
          CM.append ( C[0] )
    return CM
  else :
    return None
# ***********************************************************************


# ***********************************************************************
class Analyze_PyFile ( object ) :
  """
  Analyzes the content of a Py file,
  with special support for the Bricks Libraries of PyLab_Works.
  The following items are determined :
    - self.Path
    - self.FileName
    - self.PyFile
    - self.Doc_String
    - self._Version_Text
    - self.Classes
    - self.Functions
    - Class_Doc_String ( my_class )
    - Class_Args ( my_class )
  """

  def __init__ ( self, filename, paths = [] ) :
    """
    - filename maybe specified in any way:
        - with or without extension
        - with or without absolute / relative path
    - paths is one of the following:
        - empty / string / list of strings
    """
    self.Path, self.FileName = path_split ( filename )
    self.PyFile = os.path.splitext ( self.FileName )[0]

    #exec ( 'import '+ self.PyFile )
    MA = __import__ ( self.PyFile )

    # In general a module/file contains a doc-string.
    #self.Doc_String = eval ( self.PyFile + '.__doc__')
    self.Doc_String = MA.__doc__
    if self.Doc_String:
      self.Doc_String = self.Doc_String.lstrip ('\n').rstrip('\n')

    try :
      #self.Version_Text = eval ( self.PyFile + '._Version_Text' )
      self.Version_Text = MA._Version_Text
    except :
      self.Version_Text = ''

    # Classes and Functions
    classes, self.Full_FileName = Get_Classes_And_Functions ( self.PyFile, paths )
    self.Classes   = []
    self.Functions = []
    for item in classes :
      if len ( item ) == 2 :
        self.Functions.append ( item )
      else :
        self.Classes.append ( item )

  """
  # *********************************************************
  # only called when not found with the normal mechanism
  # *********************************************************
  def __getattr__ ( self, attr ) :
    if   attr == 'x' :
      return self._XY_Org [0]
    elif attr == 'y' :
      return self._XY_Org [1]
    else :
      if not ( self.__dict__.has_key ( attr ) ) :
        self.__dict__[attr] = 0
      return self.__dict__[attr]
  """


  # *********************************************************
  # *********************************************************
  def Class_Doc_String ( self, my_class, my_method = None ) :
    # Get the object
    CL = _Get_My_Object ( self.PyFile, my_class, my_method )

    if CL :
      line = CL.__doc__
      line = getdoc ( CL )
      if line :
        return line + '\n'
      else :
        return ''
    return ''

  # *********************************************************
  # *********************************************************
  def Get_Init_Def ( self, my_class, my_method = None ) :
    # Get the object
    CL = _Get_My_Object ( self.PyFile, my_class, my_method )

    line = ''
    if CL :
      if isfunction ( CL ) or ismethod ( CL ) :
        source = getsourcelines ( CL )
      else :
        source = getsourcelines ( CL.__init__ )
      line = ''.join ( source [0] )
      line = line [ : line.find ( ':') + 1]
    return line

  # *********************************************************
  # *********************************************************
  def Get_Class_Methods ( self, my_class ) :
    # Get the object
    CL = _Get_My_Object ( self.PyFile, my_class )

    List = None
    if CL :
      List = getmembers ( CL, isfunction )
    return List

  # *********************************************************
  # *********************************************************
  def Class_Args ( self, my_class ) :
    #exec ( 'import '+ self.PyFile )
    #class_def = eval ( self.PyFile + '.' + my_class )
    MA = __import__ ( self.PyFile )
    class_def = getattr ( MA, my_class )

    #getargspec( func)
    #Get the names and default values of a function's arguments.
    #A tuple of four things is returned: (args, varargs, varkw, defaults).
    #args is a list of the argument names (it may contain nested lists).
    #varargs and varkw are the names of the * and ** arguments or None.
    #defaults is a tuple of default argument values or None
    #if there are no default arguments; if this tuple has n elements,
    #they correspond to the last n elements listed in args.

    return inspect.getargspec ( class_def )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Html_Doc ( object ) :
  def __init__ ( self, Module ) :
    self.Example_Count = 0
    self.Html_Start = """
<!DOCTYPE HTML><html class="Debug"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <title>CodeMirror 2: Autocomplete Demo</title>

<link rel="stylesheet" href="css/codemirror.css">
<script src="js/codemirror.js"></script>
<link rel="stylesheet" href="css/night.css">
<link rel="stylesheet" href="css/elegant.css">
<link rel="stylesheet" href="css/neat.css">
<link rel="stylesheet" href="css/default.css">
<link rel="stylesheet" href="css/robbie.css">
<script src="js/css.js"></script>
<script src="js/python.js"></script>
<link rel="stylesheet" href="css/docs.css">
<script src="js/ph_codemirror.js"></script>

<link rel="stylesheet" href="css/py_punthoofd.css">

  </head>
    <body>
      <!--<div class="body">-->
        <h1>Module %s</h1>
    """ % Module

    self.Html_Final= """
      <!--</div>-->
    </body>
</html>
    """
    self.Html = self.Html_Start
  def Write ( self, Filename ) :
    #fh = open ( '../WebKit/CodeMirror/aap.html', 'w' )
    fh = open ( Filename, 'w' )
    fh.write ( self.Html + self.Html_Final )
    fh.close ()

  def Add_Last_Version ( self, Version ) :
    self.Html += '<b>Last Version %s</b>,   %s<br><br>' % ( Version[0][0], Version[0][1] )

  def Add_Version_History ( self, Version ) :
    """
[ 2.3 , '02-07-2011', 'Stef Mientki',
'Test Conditions:', (2,),
    """
    ##self.Html += 'Version history<br>'
    for Vers in Version :
      line = '<br><b>Version: %s, Date: %s</b><br>' % ( Vers[0], Vers[1] )
      self.Html += line
      Lines = Vers[5].strip().splitlines()
      for Line in Lines :
        if Line.strip() :
          self.Html += '<tt>'+ Line + '</tt><br>'

  def Add_Class ( self, text ) :
    self.Html += '<tt class="klass">%s</tt>' % text

  def Add_Method ( self, text ) :
    self.Html += '<tt class="method">%s</tt>' % text

  def Add_Function ( self, text ) :
    self.Html += '<tt class="function">%s<br></tt>' % text

  def Add_Doc ( self, text ) :
    ST_DOC      = 1
    ST_ARGUMENT = 2
    ST_RETURN   = 3
    ST_NOTE     = 4
    ST_WARNING  = 5
    ST_EXAMPLE  = 6
    ST_ULLIST   = 7
    if text :
      Doc_ = re.sub ( "\s+", "", text )
      if Doc_ :
        text = text.lstrip ()
        ##print 'Doc :', text
        State         = ST_DOC
        self.Html     += '<p>'
        Old_Finish    = '</p>'
        for line in text.splitlines() :
          sline = line.strip()

          # unordered list
          if not ( State == ST_EXAMPLE ) and sline and ( sline[0] in '-#') :
            if State != ST_ULLIST :
              self.Html += '\n<ul><li>'
              State = ST_ULLIST
              Old_Finish = '  </li>\n  </ul>'
            else :
              self.Html += '  </li>\n  <li>'
          else :
            if ( State == ST_ULLIST ) and sline and not ( line.startswith ( ' ' )) :
              State = ST_DOC
              self.Html += '  </li></ul>\n<p>'
              Old_Finish = '</p>'

            Parts = line.lower().split (':')
            if len ( Parts ) > 1 :
              New_State = True
              First = Parts [0]
              """
              if     First.startswith ( 'argument' ) :
                State = ST_ARGUMENT
                Start = '<div> Arguments :'
                Finish = '</div>'
              elif   First.startswith ( 'return' ) :
                State = ST_RETURN
                Start = '<p> Arguments :'
                Finish = '</p>'
              """
              if   First.startswith ( 'plain' ) :
                State  = ST_DOC
                Start  = '<br><p>'
                Finish = '</p>'
              elif   First.startswith ( 'note' ) :
                State  = ST_NOTE
                Start  = '<br><div class="note-title"><b>NOTE</b></div>   <div class="note">'
                Finish = '</div>'
              elif   First.startswith ( 'warning' ) :
                State  = ST_WARNING
                Start  = '<br><div class="note-title"><b>WARNING</b></div>   <div class="note">'
                Finish = '</div>'
              elif   First.startswith ( 'example' ) :
                State = ST_EXAMPLE
                self.Example_Count += 1
                Prefix = -1
                Nr = self.Example_Count
                Start  = '<div class="example"> Example: <b>%s</b> </div>' % ( ':'.join ( Parts[1:]))
                Start  += '<br><samp id="CMS_%s">' % Nr
                Finish = """
  </samp>
  <script type="text/javascript">
  Something_2_CodeMirror( "CMS_%s", "CM_%s" );
  </script> <br>""" % ( Nr, Nr )
                Finish = '</samp>'
              else :
                New_State = False

              if New_State :
                self.Html += Old_Finish
                self.Html += Start
                Old_Finish = Finish
                # Dont proces the first line
                continue

          if State == ST_EXAMPLE :
            #line = line.replace ( r'\t', r'\\t' )
            if Prefix < 0 :
              # determine the leading spaces
              Prefix = len ( line ) - len ( line.lstrip() )
            line = line [ Prefix : ]

            # docstrings contains weird escaped characters
            line = line.replace ( '\x08', r'\b' )
            # if we don't have a '\n' in the text,
            # everything in CodeMirror is placed on 1 line !!
            if line and ( line [-1] != '\n' ) :
              line = line + '\n'

            self.Html += line
          else :
            ##if sline and sline[0] in '-#' :
            if State == ST_ULLIST :
              if sline and sline[0] in '-#' :
                while not ( line[0] in '-#' ) :
                  line = line [1:]
                line = line [1:]
                line = line.lstrip ()
                parts = line.split (':')
                if len ( parts ) > 1 :
                  line = '<b>' + parts[0] + '</b>' + ':'.join ( parts [1:] )
              else :
                line = ' ' + line.strip()
              while '  ' in line :
                line = line.replace ( '  ', ' &nbsp;' )
              ##self.Html += '<br><tt>' + line + '</tt>'
              self.Html += line
            elif not ( sline ) :
              self.Html += '<br>'
            else :
              self.Html += line + ' '

        # close the last part
        self.Html += Old_Finish

# ***********************************************************************

# ***********************************************************************
class Generate_Doc_File ( object ) :
  """
Generates a doc file, from the python source file.
The included items are in this order:
  - last version + date
  - doc string of the module
  - functions and classes, in the exact order in which the appear in the file
  - version history


The doc-string is parsed, and special parts, starting with a keyword and
followed by a colon, will be recognized and treated in a special manner,
these are :
  - Note, placed in a box with background colouring
  - Warning, placed in a box with background colouring
  - Example, placed in a ACTIVE code editor (below are some real examples)
    # in Punthoofd, these examples can really be modified and executed
  - plain, to go back to the normal document mode

For classes, the doc string of the class itself and the doc string
of the __init__ or __new__ will be combined.


Lines that starts with a "#" or "-" will be displayed in a fix font,
and with the correct number of spaces.
So the following lines will look exactly like
they are shown in a normal code editor.
  - line displayed in fixed font
      # more intendation
  - a second line


Example : Title of the example
  for i in range ( 5 ) :
    print i * i

Example : Another example, in a separate Code editor
  for i in range ( 5 ) :
    print i * i
    if i > 2 :
      break
  """

  def __init__ ( self, filename, Output_Filename, paths = [] ) :
    """
    - filename maybe specified in any way:
        - with or without extension
        - with or without absolute / relative path
    - paths is one of the following:
        - empty / string / list of strings
    """
    self.UnderScores = 0   ## <<== should come from a parameter
    self.Html = Html_Doc ( filename )
    self.Path, self.FileName = path_split ( filename )
    self.PyFile = os.path.splitext ( self.FileName )[0]

    import imp
    from os.path import split
##    with open(filename,'r') as fh:
##      module = imp.load_source(self.PyFile,filename,fh)
##    self.module = module
##    #self.PyFile = 'self.module'
##    globals()[self.PyFile] = module
    paths.insert(0,split(filename)[0])
    #imp.load_module()
    sys.path.insert(0,split(filename)[0])

    #exec ( 'import '+ self.PyFile )
    MA = __import__ ( self.PyFile )

    # Version Text
    try :
      #self.Version = eval ( self.PyFile + '._Version_Text' )
      self.Version = MA._Version_Text
    except :
      self.Version = None
    if self.Version :
      self.Html.Add_Last_Version ( self.Version )

    # In general a module/file contains a doc-string.
    #self.Doc_String = eval ( self.PyFile + '.__doc__')
    self.Doc_String = MA.__doc__

    if self.Doc_String:
      #self.Doc_String = self.Doc_String.lstrip ('\n').rstrip('\n')
      self.Html.Add_Doc ( self.Doc_String.strip() )

    # Classes and Functions (we also get imported objects!!)
    Objects = pyclbr.readmodule_ex ( self.PyFile, paths  )
    My_Objects = {}
    PyFile = os.path.splitext ( os.path.split ( self.PyFile )[1])[0]
    for Name, Object in list(Objects.items ()) :
      OFile = os.path.splitext ( os.path.split ( Object.file )[1])[0]
      if OFile == PyFile :
        My_Objects [ Name ] = Object

    # derive the full filename, from one of the objects
    for key in My_Objects :
      self.Full_Filename = My_Objects [ key ].file
      break

    # and read the complete file
    fh = open ( self.Full_Filename, 'r' )
    self.PyLines = fh.readlines ()
    fh.close ()

    # make a list of linenumbers, to create the correct sorting
    LineNrs = {}
    for key in My_Objects :
      Object = My_Objects [ key ]
      #print Object.name, Object.lineno
      LineNrs [ Object.lineno ] = Object.name
    Line_Nrs = list(LineNrs.keys ())
    Line_Nrs.sort()

    Classes_Functions = []
    for Nr in Line_Nrs :
      Name = LineNrs [ Nr ]
      Classes_Functions.append ( My_Objects [ Name ] )

    for item in Classes_Functions :

      # test if the number of preceeding underscores is not too large
      UnderScores = len ( item.name ) - len ( item.name.lstrip('_') )
      if UnderScores > self.UnderScores:
        continue

      IsClass = isinstance ( item, pyclbr.Class )
      if IsClass :
        # if we found a class,
        # we've to search for the arguments in __init__ or __new__
        if '__new__' in item.methods :
          def_nr = item.methods [ '__new__' ]
          Def = self._Get_Def ( def_nr ).replace ( 'def', '' ).lstrip()
          Def = Def.replace ( '__new__', '' )
        elif '__init__' in item.methods :
          def_nr = item.methods [ '__init__' ]
          Def = self._Get_Def ( def_nr ).replace ( 'def', '' ).lstrip()
          Def = Def.replace ( '__init__', '' )
        else :
          def_nr = None
          Def = self._Get_Def ( item.lineno ).replace ( 'class', '' ).strip()

        Selfs = [ 'self,', 'self ,', 'self' ]
        for Self in Selfs :
          if Self in Def :
            Def = Def.replace ( Self, '' )
            break

        self.Html.Add_Class ( 'class <b>' + item.name + Def + '</b>')
        self.Html.Add_Doc ( self._Get_Doc_String ( item.name ) )

        # make a sorted list of methods
        lineno_methods = {}
        for method, lineno in list(item.methods.items ()) :
          lineno_methods [ lineno ] = method
        ordered_lineno = list(lineno_methods.keys())
        ordered_lineno.sort()

        #for method in item.methods :
        for lineno in ordered_lineno :
          method = lineno_methods [ lineno ]

          # test if the number of preceeding underscores is not too large
          UnderScores = len ( method ) - len ( method.lstrip('_') )
          if UnderScores > self.UnderScores:
            continue

          Def = self._Get_Def ( item.methods[method] ).replace ( 'def', '' ).lstrip()
          Selfs = [ 'self,', 'self ,', 'self' ]
          for Self in Selfs :
            if Self in Def :
              Def = Def.replace ( Self, '' )
              break
          self.Html.Add_Method ( item.name + '.<b>' + Def + '</b>' )
          self.Html.Add_Doc ( self._Get_Doc_String ( item.name, method ) )
      else :
        #print 'AAAA', self.PyLines [ item.lineno - 1 ]
        #self.Html.Add_Function ( '<b>' + item.name + '</b>' )
        Def = self._Get_Def ( item.lineno ).replace ( 'def', '' ).strip()
        self.Html.Add_Function ( 'def <b>' + Def + '</b>' )
        self.Html.Add_Doc ( self._Get_Doc_String ( item.name ) )

    if self.Version :
      self.Html.Add_Version_History ( self.Version )

    print('pop8')
    print ( "Tuple??" )
    print ( Output_Filename )
    self.Html.Write ( Output_Filename )
    return

  # *********************************************************
  # *********************************************************
  def _Get_Def ( self, lineno ) :
    lineno -= 1
    Result = self.PyLines [ lineno ]
    while not ( ':' in self.PyLines [ lineno ] ) :
      lineno += 1
      line = self.PyLines [ lineno ]
      line = line.replace ( ' ', '&nbsp;' )
      Result += '<br>' + line
    return Result

  # *********************************************************
  # *********************************************************
  def _Get_Doc_String ( self, Class, Method = None ) :
    CL = _Get_My_Object ( self.PyFile, Class, Method )
    line = None
    if CL :
      line = getdoc ( CL )
    #else :
    #  line = '<br>'

    if not ( line ) :
      line = '<br>'

    # if it was class, with Method = None,
    # and the docstring is empty,
    # search for __init__ or __new__,
    # to get the docstring
    """
    if CL and not ( line ) and not ( Method ) and inspect.isclass ( CL ) :
      line = getdoc ( CL.__new__ )
      if not ( line ) :
        line = getdoc ( CL.__init__ )
    """
    if CL and not ( Method ) and inspect.isclass ( CL ) :
      extra_line = getdoc ( CL.__new__ )
      if not ( extra_line ) or extra_line.startswith ( 'T.__new__') :
        extra_line = getdoc ( CL.__init__ )
      if extra_line :
        if line == '<br>' :
          line = extra_line.strip()
        else :
          line += '\nplain:\n' + extra_line.strip()

    if not ( line ) or not ( line.strip () ) :
      line = '&nbsp;'
    return line

# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':

  test = [  1 ]

  if 1 in test :
    PyFile = 'file_support.py'
    PyFile = 'file_support'
    #PyFile = 'date_time_support'
    PyFile = 'testfile_for_doc_support'
    PyFile = 'doc_support'
    PyPath = ''

    #PF = Analyze_PyFile ( PyFile, PyPath )
    #Output_Filename = '../WebKit/CodeMirror/aap.html', 'w'
    Output_Filename = '../WebKit/CodeMirror/aap.html'
    PF = Generate_Doc_File ( PyFile, Output_Filename )
    sys.exit()

    #print 'Tech_Description:', PF.__doc__
    #print 'Version_Text:',     PF.Version_Text

    #print 'Get_Relative_Path DOC:', PF.Class_Doc_String ( 'Get_Relative_Path' )
    #print 'Get_Absolute_Path DOC:', PF.Class_Doc_String ( 'Get_Absolute_Path' )

    #print 'Filename', PF.FileName
    print('Full Filename', PF.Full_FileName)
    #print 'Functions', PF.Functions
    #print 'Classes', PF.Classes

    print('=============  Classes  ================')
    for Class in PF.Classes :
      Klass = Class [0]
      print('======  %s  ======' % Klass)
      print(PF.Class_Doc_String ( Klass ))
      for Funk in Class [2] :
        if not ( Funk.startswith ( '_' )) or Funk in ( '__init__', '__new__' ):
          print('--', Funk)
          print(PF.Class_Doc_String ( Klass, Funk ))

    print('=============  Functions  ================')
    List = getmembers ( Analyze_PyFile, isfunction )
    for item in PF.Functions :
      Funk = item [ 0 ]
      print('======  %s  ======' % Funk)
      print(PF.Class_Doc_String ( Funk ))

    #print 'Args',PF.Class_Args ( 'Get_Relative_Path' )

  if 2 in test :
    from db_support import Find_ODBC
    # import db_support   <== not enough !!
    print(getsourcelines ( Find_ODBC ))

    #sys.path.append ( '../PyLab_Works' )
    from brick import tLWB_Brick
    source = getsourcelines ( tLWB_Brick )
    #text = ''.join ( source [0] )
    #print source
    #source[0] = source[0] [ : source[0].find (':')]
    #print source
    print(tLWB_Brick.__doc__)
    print(getdoc(tLWB_Brick))
    print(getfile (tLWB_Brick))
    List = getmembers (tLWB_Brick, ismethod)
    for item in List :
      print(item[0], type(item[1]))

    source = getsourcelines ( tLWB_Brick.__init__ )
    text = ''.join ( source [0] )
    text = text [ : text.find ( ':') + 1]

    print(text)
    print('done')

  if 3 in test :
    PyFile = 'db_support'
    PyFile = 'doc_support'
    PyPath = 'D:/Data_Python_25/support'

    #PF = Analyze_PyFile ( PyFile, PyPath )
    PF = Analyze_PyFile ( PyFile )

    print('Get_Relative_Path DOC:', PF.Class_Doc_String ( 'Get_Relative_Path' ))
    print('Get_Absolute_Path DOC:', PF.Class_Doc_String ( 'Get_Absolute_Path' ))
    print('Find_ODBC:',             PF.Class_Doc_String ( 'Find_ODBC' ))
    print('Not_existing:',          PF.Class_Doc_String ( 'Not_Existing' ))

    print('Init', PF.Get_Init_Def ('_DataBase'))
    print('Init', PF.Get_Init_Def ('Find_ODBC'))

    print(PF.FileName)
    print(PF.Full_FileName)
    print(PF.Functions)
    print(PF.Classes)

    for Class in PF.Classes :
      for Funk in Class [2] :
        print(Funk)

    List = getmembers ( Analyze_PyFile, isfunction )
    for item in List :
      print(item)


# ***********************************************************************
pd_Module ( __file__ )
