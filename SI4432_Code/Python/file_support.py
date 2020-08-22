from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import range
from builtins import object
import __init__

"""
General purpose file / directory handling procedures
"""

from General_Globals  import *
from language_support import _

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
_Version_Text = [

[ 1.20, '10-07-2016', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Find_Files_Ext_Date, relative path sometimes started with backslash = root
""" ],


[ 1.19, '27-02-2012', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Nice_Path bug when first part was "D:/", slash was removed
""" ],

[ 1.18, '21-02-2012', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Find_Dirs_Special, Find_Dirs_1,
    don't crashes anymore when looking in locked system folders
""" ],

[ 1.17, '11-02-2012', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Find_Dirs_Special  added
- Find_Dirs and Find_Dirs_1 also returned .svn directories, Fixed
""" ],

[ 1.16, '12-07-2011', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Copy_Recursive, checks if file already exists and if the date is equal
""" ],

[ 1.15, '22-01-2011', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- File_Exists, normalizes filename, necessary to test UNC paths
""" ],

[ 1.14, '09-01-2011', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Change_FileExt, now handles also files with special characters, like accents
""" ],

[ 1.13, '24-11-2010', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Copy_Recursive  added
""" ],


[ 1.12, '23-11-2010', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Clear_Dir generated an exception when ReadOnly files encountered
  (ignore errors activated)
""" ],

[ 1.11, '23-10-2010', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Nice_Path removed the double forward slash in URLs
""" ],

[ 1.10, '17-10-2010', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Change_FileExt, now only inserst a "." is extension is specified (without a ".")
- Find_Files doesn't remove the extension anymore, if mask extension is ".*"
""" ],

[ 1.9, '02-06-2010', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Path_Add_Base added
""" ],



[ 1.8, '26-04-2010', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- File_Date crashed when file didn't exist
""" ],

[ 1.7, '20-12-2009', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Copy_File changed: File Attributes and timestamps are also copied
                     Destination may also be a directory without a filename.
""" ],

[ 1.6, '17-12-2009', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- File_Size added
""" ],

[ 1.5, '10-09-2009', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- File_Date added
""" ],

[ 1.4, '10-09-2009', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Delete_Dir, Clear_Dir added
""" ],

[ 1.3, '29-04-2009', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Get_Relative_Path and Get_Rel_Path required that the file existed, not anymore
""" ],

[ 1.2, '05-03-2009', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Find_Files now leaves svn directories untouched
""") ],

[ 1.1, '05-02-2009', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Find_Files now removes empty filenames
""") ],

[ 1.0, '17-01-2009', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Get_Rel_Path   added
  - Get_Abs_Path   added
""") ],

[ 0.9, '21-12-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Find_Files_1 extended with 'RootOnly'
""") ],

[ 0.8, '23-11-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Get_Windows_Filename renamed to Get_PDB_Windows_Filename
  - Get_PDB_Windows_Filename bugs solved
""") ],

[ 0.7, '19-10-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Get_Relative_Path, returns source, if on another drive (windows)
""") ],

[ 0.6, '07-10-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Find_Files and Find_Files_1, now returns a sorted result
  - Get_Relative_Path, didn't account for case-insensitivity on Windows systems
  - Get_Relative_Path, double backslashes translated to forward slash
  - Get_Absolute_Path_REMOVED_FOR_THE_MOMENT (Linux problems and not necessary for windows)
""") ],

[ 0.5, '31-09-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Change_FileExt, improved, so you can extend the filename
                    Change_FileExt ( Filename, '_extra.cfg' )
""") ],

[ 0.4, '31-09-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Get_Windows_Filename: Crashed when used with non-existing filename
""") ],

[ 0.3, '24-09-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Get_Windows_Filename added
""") ],

[ 0.2, '20-08-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Change_FileExt added
""") ],

[ 0.1, '27-02-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - orginal release
""") ],
]
# ***********************************************************************




import os
import sys
import fnmatch
import glob

"""
THIS DOESN'T WORK :
a = D:\data_to_test\JALsPy
b = \JAL\demo_test_eeprom.jal
c = join (a, b)
"""


# ***********************************************************************
# ***********************************************************************
def Nice_Path ( *args ) :
  """
  Joins (if more than 1 argument) strings to one path.
  Normalizes the path.
  Changes the path to all forward slashes.
  Each subpath string is allowed to be terminated with a (back-) slash.
  """
  args = list ( args )
  for i,arg in enumerate ( args ) :
    args [i] = args[i].replace ( '\\', '/' )
    while ( i != 0 ) and args[i].startswith ( '/' ) :
      args[i] = args[i][1:]
    while args[i].endswith ( '/' ) :
      args[i] = args[i][:-1]

  result = os.path.join ( *args )
  result = os.path.normpath ( result )
  result = result.replace ( '\\', '/' )
  # Double forward slashes are lost in normpath,
  # so correct this

  # correct if a forward slash after the drive ':' is missing
  x1 = result.find( ':' )
  if ( x1 > 0 ) and ( x1 != result.find ( ':/' ) ) :
    result = result.replace ( ':', ':/', 1)
  return result
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Change_FileExt ( filename, new_ext ) :
  if new_ext and new_ext.find ( '.' ) < 0 :
    new_ext = u'.' + new_ext
  try :
    return os.path.splitext ( filename )[0] + new_ext
  except :
    filename = str ( filename, 'windows-1252' )
    return os.path.splitext ( filename )[0] + new_ext
# ***********************************************************************


# ***********************************************************************
# returns the relative path (of a complete filename)
# doesn't work well !!
# ***********************************************************************
#def Get_Relative_FileName ( filename ):
#  common_path = os.path.commonprefix ( [ filename, os.getcwd() ] )
#  return filename [ len ( common_path ) :]
# ***********************************************************************

class test_class ( object ):
  def __init__ ( self ):
    """
    testclass docstring
    """
    pass

# ***********************************************************************
# ***********************************************************************
# generates a full path, from a path relative to the calling module
# example:
#   Image_Path = Get_Absolute_Path ( '../pictures' )
# ***********************************************************************
def Get_Absolute_Path_REMOVED_FOR_THE_MOMENT ( Relative_Path ) :
  # find from which file this function is called
  SourceFile = sys._getframe(1).f_code.co_filename
  Path, File = path_split ( SourceFile )
  Path = os.path.join ( Path, Relative_Path )
  # remove the intermediate /../
  return os.path.normpath ( Path )
# ***********************************************************************



# ***********************************************************************
# R.Barran 30/08/2004
# ***********************************************************************
def Get_Relative_Path ( target, base=os.getcwd()):  #os.curdir ) :
  """
  Return a relative path to the target from either the current dir or an optional base dir.
  Base can be a directory specified either as absolute or relative to current dir.
  """
  # in case of an empty string
  if not ( target ) :
    return ''

  #if not os.path.exists(target):
  #  raise OSError, 'Target does not exist: '+ target

  if not os.path.isdir(base):
      raise OSError('Base is not a directory or does not exist: '+base)

  base_list = (os.path.abspath(base)).split(os.sep)
  target_list = (os.path.abspath(target)).split(os.sep)

  # On the windows platform the target may be on a completely different drive from the base.
  if os.name in ['nt','dos','os2'] and (base_list[0].upper() != target_list[0].upper() ):
    #raise OSError, 'Target is on a different drive to base. Target: '+target_list[0].upper()+', base: '+base_list[0].upper()
    return target

  # Starting from the filepath root, work out how much of the filepath is
  # shared by base and target.
  for i in range(min(len(base_list), len(target_list))):
    if os.name in ['nt','dos','os2'] :
      if base_list[i].upper() != target_list[i].upper(): break
    else :
      if base_list[i] != target_list[i]: break
  else:
      # If we broke out of the loop, i is pointing to the first differing path elements.
      # If we didn't break out of the loop, i is pointing to identical path elements.
      # Increment i so that in all cases it points to the first differing path elements.
      i+=1

  rel_list = [os.pardir] * (len(base_list)-i) + target_list[i:]
  if rel_list :
    dir = os.path.join(*rel_list)
    dir = dir.replace ( '\\', '/' )
    return dir
  else :
    return ''
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Rel_Path ( target ) :
  """
  Creates a path, relative to the applications path
  """
  ##v3print ( 'Get_Rel_Path:', target, Application.Dir )
  return Get_Relative_Path ( target, Application.Dir )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Abs_Path ( target ) :
  """
  Creates a path, absolute to the applications path
  """
  return os.path.join ( Application.Dir, target )
# ***********************************************************************


#***************************************************
#***************************************************
def Path_Add_Base ( Base_Path, Path, File = None ) :
  """
  Adds a Base_Path to Path and joins the filename if avalaible,
  Only if Base_Path is available and Path is relative.
  """
  if Base_Path and Path and ( len(Path) > 2 ) and \
     not( Path[1] == ':' ) and not ( Path.startswith( r'\\' ) ) :
    Path = os.path.join ( Base_Path, Path )

  Full_Filename = Path
  if File :
    Full_Filename = os.path.join ( Full_Filename, File )
  return Full_Filename
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Main_Module_Filename () :
  return sys.argv[0]
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def File_Exists ( filename ) :
  if filename :
    filename = os.path.normpath ( filename )
    return os.path.exists ( filename)
  else :
    return None
# ***********************************************************************


# ***********************************************************************
# **********************************************************************
def File_Date ( filename ) :
  if not ( File_Exists ( filename ) ) :
    return None
  if filename :
    return os.path.getmtime ( filename )
  else :
    return None
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def File_Size ( filename ) :
  from stat import ST_SIZE

  if filename :
    file_mode = os.stat ( filename )
    return file_mode [ ST_SIZE ]
  else :
    return None
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_PDB_Windows_Filename ( FileName ) :
  """
On windows systems,
  Translates the Filename to the correct case
  the preceding absolute or relative path is converted to lower case !!
  Used to translate filenames coming from PDB and similar packages
On other OS, it just returns the unmodified string
  """
  if os.name == 'nt' :
    """
    # path will be translated to lowercase
    # and we want only forward slashes
    FileName = FileName.lower ().replace ( '\\', '/' )

    # Do a search with some degrees of freedom
    # otherwise glob.glob just returns the original string !!
    Result = glob.glob ( FileName [:-1] + '*')

    if Result:
      for R in Result :
        if R.lower().replace( '\\', '/' ) == FileName :
          return R.replace ( '\\', '/' )
    """
    import win32file
    filename = FileName.lower ().replace ( '\\', '/' )
    Path, File = path_split ( filename )
    try:
      File = win32file.FindFilesW ( FileName )
    except :
      return None #FileName
    if Path :
      Path += '/'
    #print 'PPDDBB',FileName, Path, File
    if File :
      return Path.lower() + File[0] [8]
    else :
      return FileName

  return FileName
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def File_Delete ( filename ):
  if File_Exists ( filename ) :
    os.remove ( filename )
# ***********************************************************************


# ***********************************************************************
# removes a tree (path), even if it contains files
# ***********************************************************************
def Delete_Dir ( Dir, NoQuery = False ) :
  if not ( os.path.exists ( Dir ) ) :
    print('*** ERR *** File_Support, Delete_Dir, DIR doesn''t exists : ', Dir)
    return
  if NoQuery :
    if len ( Dir ) < 10 :
      print('Clear not allowed on such small paths')
      return
    else :
      import shutil
      shutil.rmtree ( Dir )
  else :
    from   dialog_support import AskYesNo
    if AskYesNo ( Question = 'Delete Directory: ' + Dir,
                  Title    = 'Please read carefully ' ) :
      import shutil
      shutil.rmtree ( Dir )
# ***********************************************************************


# ***********************************************************************
# Clears a directory, but leaves the directory itself
# ***********************************************************************
def Clear_Dir ( Dir, Condensed_Display = False ) :
  #print 'Clear_Dir', Dir
  #print os.listdir ( Dir )
  #Condensed_Display = False

  if not ( os.path.exists ( Dir ) ) :
    #print '*** ERR *** File_Support, Delete_Dir, doesn''t exists : ', Dir
    return

  if len ( Dir ) < 10 :
    print('Clear not allowed on such small paths')
    return

  import shutil
  for File in os.listdir ( Dir ) :
    Filename = os.path.join ( Dir, File )
    #print 'trying to delete', Filename
    if Condensed_Display :
      print('CD', end=' ')
    else :
      v3print ( 'Clear_Dir', Filename )
    if os.path.isfile ( Filename ) :
      os.remove ( Filename )
    else :
      shutil.rmtree ( Filename, True )  # Ignore Errors !!
# ***********************************************************************



# ***********************************************************************
def Force_Dir ( path, init = False ) :
  """
Forces a directory and
can create a default __init__.py file if not exists and init = True
Returns True if the directory did not exist yet.
  """
  Created = False
  if not ( path ) :
    return Created
  if not( File_Exists ( path ) ) :
    os.makedirs ( path )
    Created = True
  if init :
    initfile = os.path.join ( path, '__init__.py')
    if not ( File_Exists ( initfile ) ) :
      file = open ( initfile, 'w' )
      file.write ( '# This is a Python package.' )
      file.close ()
  return Created
# ***********************************************************************


# ***********************************************************************
def Copy_File ( Source, Destination ) :
  """
Destination may be a directory or a full qualified filename.
Attributes, including dates are also copied.
"""
  if not( File_Exists ( Source ) ) :
    return

  # Because Destination is path+filename,
  # we can safely get the destination path
  Force_Dir ( os.path.split ( Destination ) [0] )

  from shutil import copy2
  copy2 ( Source, Destination )
  return True
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Copy_Recursive ( Source, Dest, Exclude_Dirs = [], Exclude_Files = [] ) :
  Files = Find_Files ( Source, '*.*', RootOnly = False )

  for File in Files :
    for Ex in Exclude_Dirs :
      if Ex in File[0] :
        break
    else :
      for Ex in Exclude_Files :
        if Ex in File[1] :
          break
      else :
        Filename = Nice_Path ( Source, File[0], File[1] )
        Dest_File = Nice_Path ( Dest, File[0], File[1] )
        if File_Exists ( Dest_File ) :
          if round ( File_Date ( Filename )) == round ( File_Date ( Dest_File )) :
            continue
        try :
          Copy_File ( Filename, Dest_File )
          ##print 'Copied from : ', Filename
          ##print '         To : ', Dest_File
          ##print File_Date ( Filename ), File_Date ( Dest_File ), round(File_Date ( Filename )) == round (File_Date ( Dest_File ))
        except :
          pass
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Find_Files_1 ( path , Py_Files, mask = '*.py', RootOnly = False ) :
  """
# Searches for all (Python) files, starting at path
# Returns a list of tuples,
# whereas each tuple contains
#   - the path
#   - the filename
'''
['../PyLab_Works/save temp', 'float_slider.py']
['..PyLab_Works', 'setup.py']
'''
"""
  if File_Exists ( path ) :
    try :
      files = os.listdir ( path )
    except :
      files = []
      print('>>>> Access Denied ???', path)
    for file in files :
      if os.path.isfile ( os.path.join ( path, file ) ) :
        #if os.path.splitext ( file ) [1] == mask :
        if fnmatch.fnmatch ( file, mask ) :
          #print file
          Py_Files.append ( [ path, file ] )
      elif not ( RootOnly ) :
        # Dont touch SVN directories !!
        if file != '.svn' :
          new_path = os.path.join ( path, file )
          Find_Files_1 ( new_path, Py_Files, mask )
    Py_Files.sort()
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def Find_Files ( dir, mask = '*.py', RootOnly = False  ) :
  """
  # Searches for all (Python) files, starting at path
# Returns a list of tuples,
# whereas each tuple contains
#   - the path
#   - the filename
'''
['', 'control_matplot']
['', 'control_ogl']
['/lang', 'PyLab_Works_search_bricks_NL']
['/lang', '__init__']
['/pylab_works_programs/Signal_WorkBench', 'Akto_Raw']
'''
"""
  Py_Files = []
  Find_Files_1 ( dir, Py_Files, mask, RootOnly )

  # ********************************************
  # Sort the filelist and
  #   remove the basepath
  #   remove file extension ( if extension is not ".*" )
  # ********************************************
  Py_Files.sort()
  Ext = os.path.splitext ( mask )[1] != '.*'
  N = len (dir)
  for i,item in enumerate ( Py_Files ) :
    Py_Files [i][0] = Py_Files [i][0][N:]
    if Ext :
      Py_Files [i][1] = os.path.splitext ( Py_Files[i][1] )[0]

  # remove empty
  empty = [ '', '' ]
  if empty in Py_Files :
    Py_Files.remove ( empty )

  return Py_Files
# ***********************************************************************
def Find_Files_List ( dir, mask ='*.py', RootOnly = False ) :
  Files = Find_Files ( dir, mask, RootOnly )
  Result = []
  for File in Files :
    Result.append ( File[1] )
  Result.sort ()
  return Result
# ***********************************************************************
def Find_Files_Ext ( dir, mask = '*.py', RootOnly = False  ) :
  """
  Returns a list of found files.
  """
  Py_Files = []
  Find_Files_1 ( dir, Py_Files, mask, RootOnly )

  # ********************************************
  # Sort the filelist and
  #   remove the basepath
  #   remove file extension
  # ********************************************
  Py_Files.sort()
  N = len (dir)
  for i,item in enumerate ( Py_Files ) :
    Py_Files [i][0] = Py_Files [i][0][N:]
    Py_Files [i][1] = Py_Files[i][1]        ## diff with Find_Files

  # remove empty
  empty = [ '', '' ]
  if empty in Py_Files :
    Py_Files.remove ( empty )

  return Py_Files
# ***********************************************************************
def Find_Files_Ext_Exclude ( dir, mask = '*.py', RootOnly = False, Excludes = ''  ) :
  """
Returns a list of found files. But not the extensions in excludes.
Excludes ia a comma separated string, caseinsenstive.
  """
  Py_Files = []
  Find_Files_1 ( dir, Py_Files, mask, RootOnly )

  # ********************************************
  # Sort the filelist and
  #   remove the basepath
  #   remove file extension
  # ********************************************
  Py_Files.sort()
  N = len (dir)
  for i,item in enumerate ( Py_Files ) :
    Py_Files [i][0] = Py_Files [i][0][N:]
    Py_Files [i][1] = Py_Files[i][1]        ## diff with Find_Files

  # remove empty
  empty = [ '', '' ]
  if empty in Py_Files :
    Py_Files.remove ( empty )

  Excludes = Excludes.lower().split(',')

  New = []
  for item in Py_Files :
    ext = item[1].split('.')[-1].lower()
    if not ( ext in Excludes ) :
      New.append ( item )

  return New
# ***********************************************************************


# ***********************************************************************
def Find_Files_Ext_Date ( dir, mask = '*.py', RootOnly = False  ) :
  """
  Returns a list of found files and their timestamp
  """
  Py_Files = []
  Find_Files_1 ( dir, Py_Files, mask, RootOnly )

  # ********************************************
  # Sort the filelist and
  #   remove the basepath
  # ********************************************
  Py_Files.sort()

  # we've to garantee that the relative filepath never starts with a backslash
  if dir.endswith ( '/' ) or dir.endswith ( '\\' ) :
    N = len (dir)
  else :
    N = len (dir) + 1

  for i,item in enumerate ( Py_Files ) :
    filename = os.path.join ( item[0], item [1] )
    TimeStamp = File_Date ( filename )
    Py_Files [i][0] = Py_Files [i][0][N:]
    Py_Files [i][1] = Py_Files[i][1]
    Py_Files [i].append ( TimeStamp )

  # remove empty
  empty = [ '', '' ]
  if empty in Py_Files :
    Py_Files.remove ( empty )

  return Py_Files
# ***********************************************************************

# ***********************************************************************
def Dict_Find_Files_Ext_Date ( *args, **kwargs ) : #dir, mask = '*.py', RootOnly = False  ) :
  """
  Returns a dictionair, where
    key   = filename, including relative path
    value = timestamp of the file
  """
  List = Find_Files_Ext_Date ( *args, **kwargs )
  Result = {}
  for item in List :
    filename = os.path.join ( item[0], item[1] )
    #print 'ZZ', filename, 'YY', item[1], item[0]
    Result [ filename ] = item[2]
  return Result
# ***********************************************************************


# ***********************************************************************
# Searches for all (Python) files, starting at path
# Returns a list of tuples,
# ***********************************************************************
def Find_Dirs_1 ( path , Py_Dirs, RootOnly = False ) :
  if File_Exists ( path ) and  os.path.isdir ( path ) and  ( path !='.svn' ) :
    try:
      ##print 'Find_Dirs_1', path
      files = os.listdir ( path )
      ##print 'Find_Dirs_1',files
      for file in files :
        if os.path.isdir ( os.path.join ( path, file ) ) and  (file != '.svn' ) :
          Py_Dirs.append ( [ path, file ] )
          if not ( RootOnly ) :
            # Dont touch SVN directories !!
            if file != '.svn' :
              new_path = os.path.join ( path, file )
              Find_Dirs_1 ( new_path, Py_Dirs )
        """
        elif not ( RootOnly ) :
          # Dont touch SVN directories !!
          if file != '.svn' :
            new_path = os.path.join ( path, file )
            Find_Dirs_1 ( new_path, Py_Dirs )
        """
      Py_Dirs.sort()
    except :
      print('Directory not allowed', path)
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Find_Dirs_Special ( path , Dirs ) :
  """
Special find dirs, for help extracting
  """
  if File_Exists ( path ) and  os.path.isdir ( path ) and  ( path !='.svn' ) :
    ##print 'DO', path
    text = ''
    SubDirs = []
    try:
      files = os.listdir ( path )
      for file in files :
        Filename = os.path.join ( path, file )
        if os.path.isfile ( Filename ) :
          text += ' ' + os.path.splitext ( file )[0]
        elif os.path.isdir ( Filename ) and  (file != '.svn' ) :
          text += ' ' + file
          SubDirs.append ( file )

      if text.strip() :
        Dirs.append ( ( path, text ) )

      for SubDir in SubDirs :
        if SubDir != '.svn' :
          new_path = os.path.join ( path, SubDir )
          Find_Dirs_Special ( new_path, Dirs )
    except :
      print('Directory not allowed', path)
  Dirs.sort()
# ***********************************************************************

# ***********************************************************************
def Find_Dirs ( dir, RootOnly = False  ) :
  """
If RootOnly = True, not a list of tuples is returned,
but a single list of subdirs.
  """
  Py_Dirs = []
  Find_Dirs_1 ( dir, Py_Dirs, RootOnly )

  # ********************************************
  # Sort the filelist and
  #   remove the basepath
  #   remove file extension
  # ********************************************
  Py_Dirs.sort()
  N = len (dir)
  for i,item in enumerate ( Py_Dirs ) :
    Py_Dirs [i][0] = Py_Dirs [i][0][N:]

  # remove empty
  empty = [ '', '' ]
  if empty in Py_Dirs :
    Py_Dirs.remove ( empty )

  if RootOnly :
    Result = []
    for item in Py_Dirs :
      Result.append ( item[1] )
    return Result
  else :
    return Py_Dirs
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Abs_Filename_Case ( Filename, RootOnly = True ) :
  """
  Find the right case of the filename,
  (the absolute or relative path must be in the correct case)
  and returns the filename in the correct case,
  with the absolute path.
  """
  # Test if absolute or relative path
  if Platform_Windows :
    Relative = ( len ( Filename ) < 2 ) or ( Filename[1] != ':' )
  else :
    Relative = not ( os.path.isabs ( Filename ) )

  # If relative path, make it absolute
  if Relative :
    # get path of file, from which this function was called
    SourceFile = sys._getframe(1).f_code.co_filename
    SourcePath, SourceFile = path_split ( SourceFile )
    v3print ( ' SourcePath', SourcePath )

    Filename = os.path.join ( SourcePath, Filename )
    v3print ( ' Filename', Filename)
    Filename = os.path.normpath ( Filename )
    v3print ( ' Filename', Filename)

  Filename = os.path.normpath ( Filename )
  v3print ( ' Filename', Filename)
  Filename = Filename.replace ( '\\', '/' )
  v3print ( ' Filename', Filename)

  Path, Filename = os.path.split ( Filename )
  Filename = Filename.lower ()
  v3print ( 'Path, Filename', Path, Filename)
  Files = Find_Files_Ext ( Path, mask = '*.*', RootOnly = True  )
  for File in Files :
    #v3print ( File )
    if File[1].lower () == Filename :
      #v3print ( 'Found:', File[1] )
      return os.path.join ( Path, File[1] ).replace ( '\\', '/' )
  else :
    return
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_LockFile ( Path, Silent = False, Retries = 5 ) :
  """
Creates a Lock File in the specified directory.
If, after creation of the Lock-File, there's more than one Lock-File,
the Lock-File is removed and nothing is returned.
If this was the only Lock-File, the name of the Lock-File is returned.

Example of use:

    Lock_File = Get_LockFile ( self.UpLoad_Dir )
    if Lock_File :

      ... do actions that require a lock

      os.remove ( Lock_File )

  """
  Filename = Get_User () + '_' + os.getenv('COMPUTERNAME') + '.lock'
  Force_Dir ( Path )
  Lock_File = Nice_Path ( Path, Filename )

  while Retries > 0 :
    fh = open ( Lock_File, 'w' )
    fh.write ( 'locked' )
    fh.close ()

    Locks = Find_Files_List ( Path, '*.lock' )
    if len ( Locks ) > 1 :
      import random
      os.remove ( Lock_File )
      Retries -=1
      time.sleep ( 0.5 + random.random () )
      print('Get_LockFile, locked = %s'% ( Locks ))
    else :
      break
  else :
    if not ( Silent ) :
      from dialog_support import Show_Message
      Show_Message ( 'Deze directory is gelocked\n%s' %Path )
    return

  return Lock_File
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == "__main__":

  Test_Defs ( 16 )

  #filnam = 'D:/data_to_test/JALsPy/JAL/test33.jal'
  #print os.getcwd()
  #print path_split ( filnam )
  #WINDOWS ONLY !! print os.path.splitunc ( filnam )
  #print os.path.basename ( filnam )
  #os.chdir()
  #print os.path.commonprefix ([filnam,os.getcwd()])

  # test of paths join / normalize
  if Test ( 1 ) :
    Open =u'P:\\Web2PY\\web2py_win\\web2py\\applications\\huisarts1/controllers\\..\\views\\default\\user.html'
    print(type(str(Nice_Path ( Open ))))

    print(Nice_Path ( 'D:\\', 'beer', 'aap.txt' ))
    print(Nice_Path ( 'D:/', 'beer', 'aap.txt' ))
    print(Nice_Path ( 'D:', 'beer', 'aap.txt' ))
    print(os.path.join('D:\\', 'beer', 'aap.txt' ))
    exit()

    print(Nice_Path ( 'D:\\Data_Python_25' ))
    print(Nice_Path ( 'D:\\Data_Python_25\\' ))
    print(Nice_Path ( 'D:/Data_Python_25' ))
    print(Nice_Path ( 'D:/Data_Python_25/' ))

    print(Nice_Path ( 'D:/Data_Python_25' , 'support', 'plot' ))
    print(Nice_Path ( 'D:/Data_Python_25/' , 'support', 'plot' ))
    print(Nice_Path ( 'D:/Data_Python_25/' , 'support/', 'plot\\' ))
    print(Nice_Path ( 'D:\\Data_Python_25/' , 'support/', 'plot\\' ))
    print(Nice_Path ( 'D:/Data_Python_25\\' , 'support/', 'plot\\' ))
    print(Nice_Path ( 'D:/Data_Python_25/' , 'support\\', 'plot\\' ))

    print(Nice_Path ( '/Data_Python_25/' , 'support/', 'plot\\' ))
    print(Nice_Path ( '\\Data_Python_25\\' , 'support/', 'plot\\' ))

    print(Nice_Path ( 'D:/Data_Python_25/support/plot' , '..', '..' ))
    print(Nice_Path ( 'D:/Data_Python_25/support/plot' , '../..', '..' ))
    print(Nice_Path ( 'D:/Data_Python_25\\support/plot' , '..\\', '..' ))

    print(Nice_Path ( 'http://127.0.0.1:8000/welcome/default/index' ))
    print(Nice_Path ( 'http://127.0.0.1:8000/','welcome', 'default', 'index' ))
    print(Nice_Path ( 'http://127.0.0.1:8000','welcome', 'default', 'index' ))

  if Test (2 ) :
    """
    #Force_Dir ('../PyLab_Works/land/duits/nl/aap', True )
    file   = r'\\umcradquest02.umcn.nl\RadQuest\Dekkerswald\LVPK\VLs'
    file   = os.path.join ( file, 'ncsi_2010.html' )
    ext1   = '.oldmoz.cache.html'
    ext2   = '.ie6.cache.html'
    Dest   = Change_FileExt ( file, ext1 )
    Source = Change_FileExt ( file, ext2 )
    print Dest
    print Source
    """

    Source   = r'\\umcradquest02.umcn.nl\RadQuest\NKCV\Beheer\VLs'
    Dest   = r'\\umcradquest01.extern.umcn.nl\RadQuest\NKCV\Beheer\VLs'
    Copy_Recursive ( Source, Dest )


  if Test ( 3 ) :
    print("****** files = glob.glob ( '../*.py' )")
    files = glob.glob ( '../*.py' )
    for file in files :
      print(os.path.isfile(file),file)

    print("******* os.listdir ( '../' )")
    print(os.listdir ( '../' ))

    print("****** files = os.listdir ( '../' )")
    files = os.listdir ( '../' )
    #for file in files :
    #  print file

  if Test ( 4 ) :
    """
    print "****** Find_Files ( '../PyLab_Works' )"
    dir = '../PyLab_Works'
    Py_Files = Find_Files ( dir )
    for item in Py_Files :
      print item

    print "****** Find_Files_1 ( '../PyLab_Works' )"
    dir = '../PyLab_Works'
    Py_Files = []
    Find_Files_1 ( dir, Py_Files )
    for item in Py_Files :
      print item
    """

    print("****** Find_Dirs ( '../NKCV Patienten dirs' )")
    dir = r'D:\__NKCV_aggregatie\Dagelijkse_DataBase\Patienten'
    Py_Dirs = Find_Dirs ( dir )
    for item in Py_Dirs :
      print(item)

    Brieven_Path = r'D:\Data_Python_25\data_TO\Word Sjablonen'
    Path = os.path.join ( Brieven_Path, 'Brieven_Huisarts')
    Files = Find_Files_List ( Path, '*.doc' )
    print(Files)

    """
['', 'CGT']
['', 'CZ']
['', 'VNK']
['', 'VNK-Screening']
"""

  if Test ( 5 ) :
    print(Get_Relative_Path ( '../pictures/pict.png', Application.Dir ))
    print(Get_Relative_Path ( 'D:/Data_Python_25/pictures/pict.png', Application.Dir ))
    print(Get_Relative_Path ( 'P:/portable/aap.txt', Application.Dir ))

    aap = Get_Relative_Path ( 'D:/Data_Python_25/pictures/pict.png', Application.Dir )
    aap = Get_Relative_Path ( aap )
    print(Get_Relative_Path ( aap ))

  # test of search text in file
  if Test ( 6 ) :
    import time
    dir = '../PyLab_Works'
    dir = 'P:\Python'

    start = time.time ()
    Py_Files = Find_Files ( dir )
    for item in Py_Files :
      #print '****', item
      if item [0].find('\\') == 0 :
        item[0] = item[0][1:]
        #print '****', item
      filename = os.path.join ( dir, item[0], item[1]) + '.py'
      file = open ( filename, 'r' )
      line = file.read()
      file.close ()
      if line.find ('SetValue') >= 0 :
        print(filename)
    print (time.time()-start)
    """ OUTPUT OF FINDSTR:  findstr /n /s /I  strsearched  *.py
    Lib\test\test_sundry.py:53:import rlcompleter
    Lib\test\test___all__.py:132:        self.check_all("rlcompleter")
    Lib\test\test___all__.py:168:        # rlcompleter needs special consideration;
    it import readline which
    Lib\test\test___all__.py:171:            self.check_all("rlcompleter")

    P:\Python>
    """

  # test of wrong case of filename
  if Test ( 7 ) :
    FileName = '../PyLab_Works/PyLab_Works_Globals.py'
    print('1', Get_PDB_Windows_Filename ( FileName ))
    print('2', Get_PDB_Windows_Filename ( FileName.lower () ))
    print('3', Get_PDB_Windows_Filename ( FileName.upper () ))
    FileName = 'D:/Data_Python_25/PyLab_Works/pylab_sworks_programs/VPython_Code/new.pcmd'
    print('1', Get_PDB_Windows_Filename ( FileName ))
    print('2', Get_PDB_Windows_Filename ( FileName.lower () ))
    print('3', Get_PDB_Windows_Filename ( FileName.upper () ))

  # test completer
  if Test ( 8 ) :
    import rlcompleter
    import wx
    import wx.stc as stc


    a = rlcompleter.Completer ( globals () )
    #print 'k',a.global_matches( 'a' )
    #print 'k',a.global_matches( 'test_class.' )
    #print a.complete( 'wx.',0)

    line = 'wx.A'
    result = ''
    State = 0
    while  a.complete ( line, State ) :
      result += ' ' + a.complete ( line, State )
      #print a.complete ( line, State )
      State += 1
    print(result)


  # speed test string vs list
  if Test ( 9 ) :
    import time
    start = time.time ()
    line = ''
    for i in range ( 10000000 ) :
      line += ' ' + 'aap'
    print(time.time () - start)

    start = time.time ()
    line = []
    for i in range ( 10000000 ) :
      line.append ( 'aap' )
    line = ' '.join ( line )
    print(time.time () - start)

  if Test ( 10 ) :
    filename = '../PyLab_Works/pylab_works_programs/2D_Scene_Ball1/ball1_save.py'
    filename = Get_Abs_Filename_Case ( filename )
    v3print ( 'Found:', filename )

    filename = '../pyLab_Works/pylab_works_programs/2D_Scene_Ball1/ball1_save.py'
    filename = Get_Abs_Filename_Case ( filename )
    v3print ( 'Found:', filename )

  # test of copy function
  if Test ( 11 ) :
    Source = 'D:/Data_Python_25/Lib_Extensions/inifile_debugger_test.ini'
    Destination = 'D:/Data_Python_25/TO_aggregatie/html_out/inifile_debugger_test.ini'
    v3print ( Copy_File ( Source, Destination ) )

  # *******************************************
  # Clear_Dir
  # *******************************************
  if Test ( 12 ) :
    #Clear_Dir ( 'D:/Data_Python25_Dist/matplotlib' )
    Clear_Dir ( 'D:/Data_Python25_Dist' )

  # *******************************************
  #
  # *******************************************
  if Test ( 13 ) :
    Dir = r'D:\Data_Python_25\TO_aggregatie\html_out'
    Mask = r'_Test_VAS_1*.*'
    Py_Files = []
    Find_Files_1 ( Dir, Py_Files, Mask, RootOnly = True )
    for file in Py_Files :
      Filename = os.path.join ( file[0], file[1] )
      print(File_Size ( Filename ), '\t\t', Filename)

  # *******************************************
  #
  # *******************************************
  if Test ( 14 ) :
    Path = r'P:/Web2PY/web2py_src/web2py/applications/examples/sessions'
    Path = r'P:/Web2PY/web2py_src/web2py/applications/My_ClientTools/errors'
    Files = Find_Files ( Path, '*', RootOnly = True )
    #Files = os.listdir ( Path )
    for File in Files :
      Filename = Nice_Path ( Path, File[1] )
      print(Filename)
      #print fnmatch.fnmatch ( File, '*.*' ), File

  # *******************************************
  # *******************************************
  if Test ( 15 ) :
    Dir = r'D:\Data_Python25_Dist\html_out'
    #Clear_Dir ( Dir )

    '''
    Source = r'D:\Data_Python_25\Map00'
    Dest   = r'D:\Data_Python25_Dist'
    Exclude_Dirs  = [ 'Map10' ]
    Exclude_Files = [ '__init__.py' ]
    Copy_Recursive ( Source, Dest, Exclude_Dirs, Exclude_Files )
    '''

    Source = r'D:\Data_Python_25__PyJamas_07'
    Dest   = r'D:\Data_Python25_Dist\PyJamas_07'
    Exclude_Dirs  = [ 'examples', 'pyjs' ]
    Exclude_Files = []
    Copy_Recursive ( Source, Dest, Exclude_Dirs, Exclude_Files )


  # *******************************************
  # *******************************************
  '''
  if Test ( 16 ) :
    #Dir = r'D:\d_midorg\PROTOCOL\VRAAGLST'
    Dir = r'\\Umcnkcv01\nkcv$\Commondata\Protocol\vraaglst'
    Files = Find_Files_List ( Dir, '*.vli' )
    from utility_support import NoCase_List
    Files = NoCase_List ( Files )
    Files.sort()
    for File in Files :
      print File
  '''

  # *******************************************
  # *******************************************
  if Test ( 16 ) :
    Dir = r'D:\Afdelingen'
    Excludes = 'one,onetoc2'
    Files = Find_Files_Ext_Exclude ( Dir, '*.*', RootOnly = False, Excludes = Excludes )

    EOL       = '\r\n<br>'
    Body      = '<b><a href="file://%s">%s</a></b>' % ( Dir, Dir ) + EOL
    Last_Path = ''
    Nest      = 1
    Spaces    = 2 * '&nbsp;'
    for Path, File in Files :
      if Path != Last_Path :
        Body += EOL
        P2 = Path.split ( '\\' )
        N2 = len ( P2 )

        Nest = N2 - 1
        Full = Dir + Path
        Body += Nest*Spaces + '<b><a href="file://%s">%s</a></b>' % ( Full, Path ) + EOL
        Nest += 1
        Last_Path = Path

      Full = Dir + Path + '/' + File
      Body += Nest * Spaces  + '<a href="file://%s">%s</a>' % ( Full, File ) + EOL
  print(Body)

  # *******************************************
  # *******************************************
  if Test (17 ) :
    Filename = r'D:\__aap\test_ph\aap33.html'
    Test_Dir = r'D:\Data_Python_25\WebKit'

    Dest, Filename = os.path.split ( Filename )
    if not ( File_Exists ( Nice_Path ( Dest, 'js' ))) :
      #User = self.User
      #User_Source = Nice_Path ( Application.Dir, '%s_static_html' %(User))
      #if not ( File_Exists ( User_Source ) ) :
      User = ''
      From = Nice_Path ( Test_Dir, '%s_static_html' %(User) )
      To   = Nice_Path ( Dest )
      Excludes = ['.svn']
      Copy_Recursive ( From, Dest, Exclude_Dirs = Excludes )

    exit ()

  # *******************************************
  # *******************************************
  if Test (18 ) :
    Test_Dir = r'H:\ID-Advies'
    """
    Files = Dict_Find_Files_Ext_Date ( Test_Dir, mask='*.*', RootOnly = False )
    for K,V in Files.iteritems () :
      print K, V
    """
    Files = Find_Files_Ext_Date ( Test_Dir, mask='*.*', RootOnly = False )
    #for Row in Files :
    #  print Row

    import xlwt
    wb = xlwt.Workbook()
    wsheet = wb.add_sheet ( 'H-schijf' )

    Row = 0
    wsheet.write ( Row,  0, 'Naam' )
    wsheet.write ( Row,  1, 'Afdeling' )
    wsheet.write ( Row,  2, 'HoofdOnderwerp' )
    wsheet.write ( Row,  3, 'Status' )
    wsheet.write ( Row,  4, 'Eigenaar' )
    wsheet.write ( Row,  5, 'Project' )
    wsheet.write ( Row,  6, 'Z_Stef' )
    wsheet.write ( Row,  7, 'Itemtype' )
    wsheet.write ( Row,  8, 'Pad' )

    from hl7_support import U2U
    for Line in Files :
      Row += 1
      wsheet.write ( Row, 0, U2U (Line[1]) )
      wsheet.write ( Row, 1, 'Z_Algemeen' )
      wsheet.write ( Row, 7, 'Item' )
      wsheet.write ( Row, 8, Line[0].replace ( '\\', '/' ))

    Filename_Dest = 'H:/ID-Temp/Stef/H-Schijf.xls'
    wb.save ( Filename_Dest )


# ***********************************************************************
pd_Module ( __file__ )

