from __future__ import division
from __future__ import print_function
from builtins import str
from builtins import range
from past.builtins import basestring
from past.utils import old_div
from builtins import object
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Robbert Mientki
#
# Created:     29-12-2010
# Copyright:   (c) Robbert Mientki 2010
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import os
from os.path import isfile,split,splitext,join
import subprocess

def iterable(a):
  try:
    iter(a)
    return True
  except:
    return False


def Make_Iterable(a):
  if isinstance(a,basestring):
    return [a]
  if not iterable(a):
    return [a]
  return a


def SearchFiles_Exp(Regex, FilePaths):
  FilePaths = Make_Iterable(Make_Iterable)
  result = []
  for Path in FilePaths:
    files = win32api.FindFiles(Path+'\\*')
    for file in files :
      if file[0] & win32file.FILE_ATTRIBUTE_DIRECTORY:
        if file[8] not in ('.','..','.svn'):              # don't touch svn paths
          #new_path = join ( path, file[8] )
          new_path = path + '\\'+file[8]
          #Py_Paths.append ( new_path )
          result += SearchFiles_Exp (Regex, new_path)
      else:
        result.append(path + '\\'+file[8])


def Search(FilePattern='*.*',FilePaths = []):
  pass

def SearchFile(Text, Pattern_or_Files = [],FilePaths =[]):
  pass

def _Find_Paths(path, Py_Paths):
  files = win32api.FindFiles(path+'\\*')
  for file in files :
    if file[0] & win32file.FILE_ATTRIBUTE_DIRECTORY:
      if file[8] not in ('.','..','.svn'):              # don't touch svn paths
        #new_path = join ( path, file[8] )
        new_path = path + '\\'+file[8]
        Py_Paths.append ( new_path )
        _Find_Paths (new_path, Py_Paths)

def Find_Paths ( path, Py_Paths ) :
  if os.name == 'nt':
    _Find_Paths ( abspath( path ) , Py_Paths )
    Py_Paths.sort()
  else:
    Find_Paths_Slow (path , Py_Paths)

  pass

class PreCall(object):
  """
  Creates a function, with the arguments embedded.
  No parameters are required (But it accepts any argument)
  See also: functools.partial (a standard python, almost, equivalent)
  """
  def __init__(self,Func,*args,**kwargs):
    self.Func   = Func
    self.args   = args
    self.kwargs = kwargs
  def __call__(self,*args,**kwargs):
    return self.Func(*self.args,**self.kwargs)

def BinCmp(File1,File2):
  FileSize1 = os.path.getsize(File1)
  FileSize2 = os.path.getsize(File2)
  if FileSize1!=FileSize2:
    return False
  fh1 = open(File1,'rb')
  fh2 = open(File2,'rb')
  ChunkSize = 1024
  for i in range(old_div(FileSize1,ChunkSize) + 1):
    Data1 = fh1.read(ChunkSize)
    Data2 = fh2.read(ChunkSize)
    if Data1 != Data2:
      fh1.close()
      fh2.close()
      return False
  fh1.close()
  fh2.close()
  return True

def VirusScan(Filenames):
  """
  Uses Avira's antivir to scan ONE file
  """
  #if not isinstance(Filenames,list): Filenames = Filenames

  subprocess.Popen([join(split(__file__)[0],'VirusScan.exe'),Filenames]).wait()
  if isfile(Filenames):
    return False
  return True # File isn't among us anymore, it's placed in quarantine

isvirus = isVirus = VirusScan

def NicePrint(a,b=60,Marker='*'):
  a = ' '+a+' '
  d = b - len(a)
  print(d/2 * '*' + a + (b-len(a)-old_div(d,2))*'*')
_Print_Indent = 0
def Print_Indent(level,*args):

  global _Print_Indent
  _Print_Indent += level
  for i in args:
    for line in str(i).splitlines():
      print(_Print_Indent*' ',line)
  _Print_Indent -= level

# ############################################################################

def _WatchDir(path_to_watch,CallBack,*args,**kwargs):

  path_to_watch = os.path.normcase(path_to_watch)

  # Since this is a thread the imports can go here.
  # This way import are only done once in the nescessary thread
  import win32file
  import win32con

  ACTIONS = {
    1 : "Created",
    2 : "Deleted",
    3 : "Updated",
    4 : "Renamed from something",
    5 : "Renamed to something"
  }
  # Thanks to Claudio Grondi for the correct set of numbers
  FILE_LIST_DIRECTORY = 0x0001

  hDir = win32file.CreateFile (
    path_to_watch,
    FILE_LIST_DIRECTORY,
    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
    None,
    win32con.OPEN_EXISTING,
    win32con.FILE_FLAG_BACKUP_SEMANTICS,
    None
  )

  l = {}
  import time
  while 1:
    #
    # ReadDirectoryChangesW takes a previously-created
    #  handle to a directory, a buffer size for results,
    #  a flag to indicate whether to watch subtrees and
    #  a filter of what changes to notify.
    #
    # NB Tim Juchcinski reports that he needed to up
    #  the buffer size to be sure of picking up all
    #  events when a large number of files were
    #  deleted at once.
    #
    results = win32file.ReadDirectoryChangesW (
      hDir,
      1024,
      True,
      win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
       win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
       win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
       win32con.FILE_NOTIFY_CHANGE_SIZE |
       win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
       win32con.FILE_NOTIFY_CHANGE_SECURITY,
      None,
      None
    )
    for action, file in results:
      full_filename = os.path.join (path_to_watch, file)
      action_string = ACTIONS.get (action, "Unknown")
      ##print full_filename, action_string
      if action_string in ['Created','Updated']:
        # To filter out the temp-files

        if full_filename in l:
          if l[full_filename]+1.0 > time.time():
            #ignore
            continue
        try:
          args = list(args) + [full_filename]
          ##print args,kwargs
          CallBack(*args,**kwargs)
        except:
          import traceback
          traceback.print_exc ()
        #subprocess.Popen(['python','Monitor.py',full_filename],shell=True)
        l[full_filename] = time.time()

#from multiprocessing import Process
import threading
def WatchDir(*args,**kwargs):
  '''
  Watch for new downloaded files
  You are responsible for a thread-safe callback!!!!
  The filename is appended (at the end) to args
  self.Monitor = WatchDir(Location,wx.CallAfter,self.OnFile)

  This will call: wx.CallAfter(self.OnFile,Found_Filename)

  '''
  p = threading.Thread(target=_WatchDir, args=args)
  p.start()
  return p


def Aap ( *args ):
  print(args)

if __name__ == '__main__' :
  PID = WatchDir ( r'D:\temp', Aap )



