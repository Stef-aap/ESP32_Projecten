from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from past.builtins import basestring
from builtins import object
import __init__

# ***********************************************************************
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007..2008 Stef Mientki
# ***********************************************************************

# ***********************************************************************
__doc__ = """
"""
# ***********************************************************************


# ***********************************************************************
_Version_Text = [

[ 1.21 , '10-06-2020', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Get_User, werkte niet goed onder Fedora/Py27
""" ],

[ 1.20 , '09-08-2014', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Get_Process_PID, made win-7 compatible
""" ],


[ 1.11 , '03-12-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Run_My_Python_and_Capture, __init__ is extended with parameter "Python_Exe"
  which allows to use a specific python.exe
- Run_My_Python_and_Capture, Get_Data2 added,
  this is a much simpler full replacement for Get_Data,
  and should replace Get_Data in the future.
""" ],

[ 1.10 , '07-11-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Get_hwnds_from_PID added
- Get_hwnds_from_PID added
""" ],

[ 1.9 , '03-10-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- added Run_My_Python_and_Capture
""" ],


[ 1.8 , '28-09-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- added Get_PID_and_CommandLine
- added Get_PID_from_CommandLine
""" ],

[ 1.7 , '02-08-2010', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- # VERY IMPORTANT CHANGE
  # a number of procedures are replaced by AutoIt functions: much faster
  # NO NO NO, we use psutils now, almost as fast as AutoIt,
  #   but working on every OS !!
  # Disadvantage: you've to register AutoIt, see also:
  #    http://sebsauvage.net/python/snyppets/#autoit
- Get_Process_PID and Kill_Process, Kill_Process_pid_Name were static,
  they are changed to dynamic now,
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  but therefor they require Filename + Extension
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
""" ] ,

[ 1.6 , '02-12-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Get_Shares function added
- extra try/except and several bugs
""" ] ,

[ 1.5 , '24-09-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Get_User function added
""" ] ,

[ 1.4 , '09-01-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Beep function added
""" ] ,

[ 1.3 , '07-10-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Run_Python added (much simpeler than Run )
- Run_Python_NoWait, set shell different for Windows and Linux
""" ] ,

[ 1.2 , '20-08-2008', 'Stef Mientki',
'Test Conditions:', (1,),
"""
- GetProcessID didn't always return a value
- Kill_Process now return True if succeeded
""" ] ,

[ 1.1 , '15-02-2008', 'Stef Mientki',
'Test Conditions:', (1,),
"""
- GetAllProcesses was static, now made dynamic
""" ] ,

[ 1.0 , '28-12-2007', 'Stef Mientki',
'Test Conditions:', (1,),
' - orginal release' ]
]
# ***********************************************************************




from General_Globals import *
import os
import time

# VERY IMPORTANT CHANGE
# a number of procedures are replaced by AutoIt functions: much faster
# Disadvantage: you've to register AutoIt, see also:
#    http://sebsauvage.net/python/snyppets/#autoit
_AutoIt = None
if sys.platform == 'win32' :
  try :
    import win32com.client
    _AutoIt = win32com.client.Dispatch ( "AutoItX3.Control" )
  except :
    _AutoIt = None


import psutil

import subprocess
from   stat         import ST_SIZE
import tempfile

import hashlib

"""
#import base64
import ezPyCrypto
# Create a key object
# print "Generating 512-bit keypair - could take a while..."
encryption_key_1 = ezPyCrypto.key ( 512 )
#print 'Private_Key =', encryption_key_1.exportKeyPrivate ()
#print 'Public_Key  =', encryption_key_1.exportKey ()

# ***********************************************************************
# EnCryption / DeCryption, Working in SQLite
# ***********************************************************************
import pysqlite2.dbapi2 as sqlite3
def EnCrypt_1 ( line ) :
  return sqlite3.Binary ( encryption_key_1.encString ( line ) )
def DeCrypt_1 ( line ) :
  return str ( encryption_key_1.decString ( line ) )
"""

"""
# ***********************************************************************
# Working in SQLite
# ***********************************************************************
def EnCrypt_1b ( line ) :
  return base64.encodestring ( encryption_key_1.encString ( line ) )
def DeCrypt_1b ( line ) :
  return encryption_key_1.decString ( base64.decodestring ( line +'\n') )

# ***********************************************************************
# EnCryption / DeCryption, not working in SQLite
# ***********************************************************************
def EnCrypt_1c ( line ) :
  return encryption_key_1.encString ( line )
def DeCrypt_1c ( line ) :
  return encryption_key_1.decString ( line )
"""
# ***********************************************************************



"""
import win32api, win32pdhutil, win32con
import win32pdh, string
"""


# ***********************************************************************
# ***********************************************************************
def Get_User () :
  if sys.platform == 'win32' :
    import win32api
    return win32api.GetUserName ()
  else :
    #return os.environ.get( "USERNAME" )  # werkt niet goed onder Fedora Py27
    Username = os.environ.get( "USER" )
    
  if Username is None :
    Username = "Default"
  return Username
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Beep ( ID = None ) :
  import pygame
  """
generates an independant message beep,
by playing a wave file.
  """
  # DONT CHANGE THE ORDER, JUST APPEND SOUND FILES
  Sounds = [
    'Windows XP Error.wav',        # 0
  ]

  if not ( ID ) or ( ID >= len ( Sounds ) ) :
    ID = 0

  filename = os.path.join ( os.path.split(__file__)[0], '..', 'Sounds', Sounds [ID] )
  ##print 'SOUND', filename

  #v3print ( 'Beep:', filename )
  pygame.mixer.init ()
  soundfile = pygame.mixer.Sound ( filename )
  soundfile.play ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Shares ():
  import wmi
  c = wmi.WMI ()
  return c.Win32_Share ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_StartUps () :
  """
  instance of Win32_StartupCommand
{
	Caption = "CTFMON.EXE";
	Command = "C:\\WINDOWS\\system32\\ctfmon.exe";
	Description = "CTFMON.EXE";
	Location = "HKU\\S-1-5-21-682003330-616249376-2147280231-500\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run";
	Name = "CTFMON.EXE";
	User = "AMD64\\Administrator";
};
"""
  import wmi
  c = wmi.WMI ()
  return c.Win32_StartupCommand ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_MAC_IP () :
  import wmi
  c = wmi.WMI ()

  Result = {}
  for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1):
    #print interface.Description, interface.MACAddress
    Result [ interface.MACAddress ] = [ interface.Description ]
    for ip_address in interface.IPAddress:
      Result [ interface.MACAddress ].append ( ip_address )
      #print ip_address
    #print
  return Result
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def Get_ipconfig_all ():
  """
  Returns all the information from ipconfig/all"
  """
  import subprocess
  p = subprocess.Popen('ipconfig/all', shell = True, stdout = subprocess.PIPE)
  p.wait()
  Lines = p.stdout.read()
  Result = []
  for line in Lines.split('\n') :
    if line.strip() :
      Result.append ( line.rstrip() )
  return Result
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_MAC_Addresses () :
  """
  Returns a list of  tuples ( Description, MAC-address ) of all MAC addresses.
  """
  IpConfig = Get_ipconfig_all ()
  Result = []
  for line in IpConfig :
    regel = line.lstrip()
    if regel.startswith ( 'Description' ) :
      Description = line.split ( ':' ) [1].strip ()
    elif regel.startswith ( 'Physical Address' ) :
      MAC = line.split( ':' )[1].strip().replace ( '-', ':' )
      Result.append ( ( Description, MAC ))
  return Result
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def Get_Stopped_Services () :
  """
  instance of Win32_Service
{
	AcceptPause = FALSE;
	AcceptStop = FALSE;
	Caption = "Computer Browser";
	CheckPoint = 0;
	CreationClassName = "Win32_Service";
	Description = "Maintains an updated list of computers on the network and supplies this list to computers designated as browsers. If this service is stopped, this list will not be updated or maintained. If this service is disabled, any services that explicitly depend on it will fail to start.";
	DesktopInteract = FALSE;
	DisplayName = "Computer Browser";
	ErrorControl = "Normal";
	ExitCode = 1460;
	Name = "Browser";
	PathName = "C:\\WINDOWS\\System32\\svchost.exe -k netsvcs";
	ProcessId = 0;
	ServiceSpecificExitCode = 1460;
	ServiceType = "Share Process";
	Started = FALSE;
	StartMode = "Auto";
	StartName = "LocalSystem";
	State = "Stopped";
	Status = "OK";
	SystemCreationClassName = "Win32_ComputerSystem";
	SystemName = "AMD64";
	TagId = 0;
	WaitHint = 0;
};
"""
  import wmi
  c = wmi.WMI ()

  Result = []
  stopped_services = c.Win32_Service (StartMode="Auto", State="Stopped")
  if stopped_services:
    for s in stopped_services:
      Result.append ( s.Caption + ' / ' + s.PathName )
  return Result
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Process_CommandLine () :
  """
Returns a dictionair of all running classes,
  Key   = Exectuable
  Value = Commandline
WMI, so function is slow ( may take several seconds)
  """

  """
instance of Win32_Process
{
	Caption = "python.exe";
	CommandLine = "\"P:\\Python\\python.exe\"  \"D:\\Data_Python_25\\TO_aggregatie\\TO_aggregatie.py\" ";
	CreationClassName = "Win32_Process";
	CreationDate = "20091202205400.406250+060";
	CSCreationClassName = "Win32_ComputerSystem";
	CSName = "AMD64";
	Description = "python.exe";
	ExecutablePath = "P:\\Python\\python.exe";
	Handle = "3772";
	HandleCount = 83;
	KernelModeTime = "23437500";
	MaximumWorkingSetSize = 1413120;
	MinimumWorkingSetSize = 204800;
	Name = "python.exe";
	OSCreationClassName = "Win32_OperatingSystem";
	OSName = "Microsoft Windows XP Professional|C:\\WINDOWS|";
	OtherOperationCount = "74304";
	OtherTransferCount = "2270876";
	PageFaults = 80349;
	PageFileUsage = 36081664;
	ParentProcessId = 3336;
	PeakPageFileUsage = 37765120;
	PeakVirtualSize = "102940672";
	PeakWorkingSetSize = 45211648;
	Priority = 8;
	PrivatePageCount = "36081664";
	ProcessId = 3772;
	QuotaNonPagedPoolUsage = 7200;
	QuotaPagedPoolUsage = 115332;
	QuotaPeakNonPagedPoolUsage = 7360;
	QuotaPeakPagedPoolUsage = 116284;
	ReadOperationCount = "25694";
	ReadTransferCount = "16927575";
	SessionId = 0;
	ThreadCount = 3;
	UserModeTime = "57656250";
	VirtualSize = "101756928";
	WindowsVersion = "5.1.2600";
	WorkingSetSize = "43692032";
	WriteOperationCount = "2";
	WriteTransferCount = "140";
};
  """
  import wmi
  c = wmi.WMI ()
  Result = {}
  for process in c.Win32_Process ():
    Result [ process.Caption ] = process.CommandLine
    print(process.Caption, process.ProcessId)
  return Result
# ***********************************************************************


# ***********************************************************************
def Get_PID_and_CommandLine () :
  """
Returns a dictionair of all running classes,
  Key   = Executable
  Value = [ PID, Commandline ]
WMI, so function is slow ( may take several seconds)
  """
  import wmi
  c = wmi.WMI ()
  Result = {}
  for process in c.Win32_Process ():
    Result [ process.Caption ] = ( process.ProcessId, process.CommandLine )
  return Result
# ***********************************************************************


# ***********************************************************************
def Get_PID_from_CommandLine ( Executable, Commandline ) :
  """
Returns the PID of the process = Executable and
where the commandline contains Commandline
WMI, so function is slow ( may take several seconds)
  """
  import wmi
  c = wmi.WMI ()
  Result = {}
  for process in c.Win32_Process ():
    if ( process.Caption == Executable ) and \
       ( Commandline in process.CommandLine ) :
      return process.ProcessId
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def GetAllProcesses():
  if os.name != 'nt' :
    pass
  else:
    # THIS IS STATIC !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #import win32pdh
    #object = "Process"
    #items, instances = win32pdh.EnumObjectItems(None,None,object, win32pdh.PERF_DETAIL_WIZARD)

    import wmi
    w = wmi.WMI()
    processes = w.instances('Win32_Process')
    instances = []
    for process in processes :
      instances.append ( str(process.name) )

    return instances
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_hwnds_from_PID ( pid ) :
  """
Get the windows handles (hwnd) from the pid.
  """
  import win32con
  import win32gui
  import win32process
  def callback ( hwnd, hwnds ) :
    if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled ( hwnd ) :
      A, found_pid = win32process.GetWindowThreadProcessId (hwnd)
      ##print hwnd, "=>", win32gui.GetWindowText (hwnd)
      if found_pid == pid:
        hwnds.append (hwnd)
    return True

  hwnds = []
  win32gui.EnumWindows ( callback, hwnds )
  return hwnds
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_PID_from_hwnd ( hwnd ) :
  """
Get the windows handles (hwnd) from the pid.
  """
  import win32con
  import win32gui
  import win32process
  A, found_pid = win32process.GetWindowThreadProcessId (hwnd)
  return found_pid
  def callback ( hwnd, PIDs ) :
    if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled ( hwnd ) :
      if hwnd == hwnd_to_find :
        A, found_pid = win32process.GetWindowThreadProcessId (hwnd)
        ##print hwnd, "=>", win32gui.GetWindowText (hwnd)
        PIDs.append (hwnd)
    return True

  hwnds = []
  win32gui.EnumWindows ( callback, hwnds )
  return hwnds
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_hwnds_from_Title ( Title ) :
  """
Get the windows handle (hwnd) from the Title.
Finds all windows with the given title.
For each of these windows a tupple,
consisting of hwnd, pid is returned.
  """
  import win32con
  import win32gui
  import win32process
  def callback ( hwnd, hwnds ) :
    if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled ( hwnd ) :
      A, pid = win32process.GetWindowThreadProcessId (hwnd)
      if win32gui.GetWindowText (hwnd) == Title :
        hwnds.append ( ( hwnd, pid ) )
    return True

  hwnds = []
  win32gui.EnumWindows ( callback, hwnds )
  return hwnds
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Process_PID ( process ) :
  """
name must be the full filename, name + extension
the search is done case-insensitive.
  """
  process = process.lower ()
  """
  for p in psutil.process_iter ():
    if p.name.lower() == process :
      return p.pid
  """
  for p in psutil.process_iter ():
    try:
      if p.name.lower() == process :
        return p.pid
    except:
      pass



  return -1
  """
  # even faster, but only working under windows
  if os.name == 'nt' :
    return _AutoIt.ProcessExists ( process )
  """
# ***********************************************************************


"""
#THIS IS SLOW !!
def Kill_Process2 ( process ) :
  #get process id's for the given process name
  pids = win32pdhutil.FindPerformanceAttributesByName ( process )
  for p in pids:
    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, p) #get process handle
    win32api.TerminateProcess(handle,0) #kill by handle
    win32api.CloseHandle(handle)        #close api
"""


# ***********************************************************************
# ***********************************************************************
def Kill_Process_pid ( pid ) :
  if os.name != 'nt' :
    pass
  else:
    import win32api
    import win32con
    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, pid) #get process handle
    try:
      win32api.TerminateProcess(handle,0) #kill by handle
      win32api.CloseHandle(handle)        #close api
    except:   #the process might already be closed by the user
      pass
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Kill_Process_and_Children_pid ( PID ) :
  if os.name != 'nt' :
    return

  Children = []
  import win32com.client
  WMI = win32com.client.GetObject ( 'winmgmts:' )
  processes = WMI.InstancesOf ( 'Win32_Process' )
  for process in processes:
    pid    = process.Properties_ ( 'ProcessID' ).Value
    parent = process.Properties_ ( 'ParentProcessId' ).Value
    if parent == PID :
      Children.append ( pid )
    #print pid, parent, Children, PID, a, type(a)

  #Insert the parent at the top
  Children.insert ( 0, PID )
  print('KILLING',Children)

  import win32api
  import win32con
  for PID in Children :
    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, PID) #get process handle
    try:
      win32api.TerminateProcess(handle,0) #kill by handle
      win32api.CloseHandle(handle)        #close api
    except:   #the process might already be closed by the user
      pass
# ***********************************************************************



# ***********************************************************************
# A short wait might be necessary to prevent
#getting the pid of the just killed process
##    while Kill_Process ( 'cmd' ) :
##      time.sleep ( 0.1 )
# ***********************************************************************
def Kill_Process ( name ) :
  if os.name != 'nt' :
    return False
  else:
    try:
      pid = Get_Process_PID ( name )
      ##print 'pid',pid
      if pid:
        Kill_Process_pid ( pid )
        return True
      else :
        return False
    except:  #the process might already be closed by the user
      return False
# ***********************************************************************


# ***********************************************************************
# if Name is given try to kill process by pid
# afterwards always try to kill by name
# ***********************************************************************
def Kill_Process_pid_Name ( pid, name ) :
  if os.name != 'nt' :
    pass
  else:
    if pid :
      Kill_Process_pid ( pid )
    # now if the process is started outside this program
    # we kill it this way
    #   which doesn't always succeed !!
    #   especially in the following case
    #     - launched by this program
    #     - killed by user
    #     - launched by user
    print('piep')
    Kill_Process ( name )
    print('pop')
# ***********************************************************************



# ***********************************************************************
# Convert Relative path/url to Absolute path/url
# all the os/urllib/urlparse procedures seems a bit clumsy
# The following recipy seems to work for file and url
# ***********************************************************************
def Make_Absolute_Path ( path, file ) :
  import  urllib.parse
  # be sure all forward slashes to het urlparse work correctly
  path = path.replace('\\','/')
  file = file.replace('\\','/')
  # if a path on local disk, add "file:///" to let urljoin work ok
  if ( len ( path ) > 2 ) and ( path[1] == ':' ) :
    abs_path = urllib.parse.urljoin( 'file:///' + path, file)
  else :
    abs_path = urllib.parse.urljoin( path, file )
  # if file, remove the "file:///" again
  if abs_path.find ('file:///') == 0 :
    abs_path = abs_path [8:]
    #abs_path = abs_path.replace('/','\\')
  return abs_path
# ***********************************************************************


# ***********************************************************************
# Example:
#   line = Make_Links_Absolute ( line, 'href=', prim_path )
# where:
#   line = html string with possible relative paths on the tag 'href='
#   tag = 'href=', 'src=' or whatever you like
#   prim_path = 'D:\data\test.html', yes it should contain a filename
#               or last backslash ?
# ***********************************************************************
def Make_Links_Absolute ( line, tag, prim_path ) :
  # find all the reference links
  i = 0
  links = []
  N = len(tag) + 1
  while i >= 0 :
    i = line.find ( tag, i+1 )
    if i >= 0 :
      links.append ( i + N )

  # now replace them in reversed order (to keep the indexes correct
  N = len ( links )
  for i in range ( N ) :
    ii = N-i-1
    w = line.find ( '"', links[ii] )
    file = line [ links[ii] : w ]
    abs_path = Make_Absolute_Path ( prim_path, file)
    line = line.replace ( file, abs_path )
    #print prim_path, '|', file, '|', abs_path
    #print 'HREF',line

  return line
# ***********************************************************************



import subprocess
# requires Python 2.4 or higher


# ***********************************************************************
# ***********************************************************************
def _PreProcess_Run_Python ( arguments, cwd = None ) :
  """
  INTERNAL: Runs a Python script.
  "Arguments" starts with the script, followed by the commandline arguments.
  "Arguments" maybe of type string, tuple, list.
  The Python executable should NOT be in the argument list.
  If the script is started from another directory,
  cwd is automatically calculated.
  Examples:
    Run_Python ( [ 'PyLab_Works.py', 'aap' ] )
    Run_Python ( '../support/multi_language.py' )
  """
  # be sure arguments is of type list
  if not ( isinstance ( arguments, list ) ) :
    if isinstance ( arguments, tuple ) :
      arguments = list ( arguments )
    else :
      arguments = [ arguments ]

  # add "Python" to the beginning of the list
  arguments.insert ( 0, 'python' )

  # if the Current Working Directory cwd is not specified
  # try to set cwd to the path of the first argument
  if not ( cwd ) :
    cwd = path_split ( arguments [1] )[0]
    # if path is an empty string, we must make it None !!
    if not ( cwd ) :
      cwd = None

  return arguments, cwd
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class Run_My_Python_and_Capture ( object ) :
  """
Lauches the Python script,
and captures the output of that process.
The input Command, may be one of the following:
  - name of a python file (including the py-extension )
  - list, containing the python file and zero or more parameters
  NONONO:- comma separated list of python file and parameters
  """
  def __init__ ( self, Command, Python_Exe = '..\My_python.exe' ) :
    # make an empty file that captures the output of the process
    fh = tempfile.NamedTemporaryFile ( suffix = '.txt', delete = False )
    self.Filename = fh.name

    # prepare variables
    self.Done        = 0
    self.fh          = open ( self.Filename, 'r' )
    self.IsRunning   = True
    self.Status      = 0
    self.Time_Finish = 1

    # Make the commandline, we do this ourself,
    # because subprocess Popen sometimes gives problems with quotes
    if not ( isinstance ( Command, basestring ) ) :
      Command = ' '.join ( Command )
    ##Command = 'python -u %s >>%s 2>&1' %(  Command, self.Filename )
    ##print 'WE ARE NOW HERE', os.getcwd()
    #Command = '..\My_python.exe -u %s >>%s 2>&1' %(  Command, self.Filename )
    Command = Python_Exe + ' -u %s >>%s 2>&1' %(  Command, self.Filename )

    # write the commandline to the log file
    ##fh.write ( 'Command = ' + Command + '\n' )
    fh.close ()

    # Launch the process
    #print 'Current Directory =', os.getcwd ()
    #print 'Command =', Command
    self.Process = subprocess.Popen ( Command, shell = True )

  # *********************************************
  # *********************************************
  def Get_Data2 ( self ) :
    """
Returns the data produced by the launched process.
If the process is stopped, the tempfile will be closed.
Is this possible, just read from an open file
    """
    line = ''
    if self.Process.poll() is None :
      line = self.fh.read ()

    # if the process is stopped
    else :
      line = self.fh.read ()
      self.fh.close ()
      self.IsRunning = False
    return line

  # *********************************************
  # *********************************************
  def Get_Data ( self ) :
    """
Returns the data produced by the launched process.
If the process is stopped, the tempfile will be closed.
    """
    line = ''
    if self.Process.poll() is None :
      File_Mode = os.stat ( self.Filename )
      File_Size = File_Mode [ ST_SIZE ]
      if File_Size > self.Done :
        line = self.fh.read ( File_Size - self.Done )
        #print File_Size - self.Done, line
        self.Done = File_Size
        return line

    # if the process is stopped
    else :
      if self.Status  == 0 :
        self.Status = 1
        self.StopTime= time.time ()
      elif self.Status == 1 :
        if time.time () - self.StopTime > self.Time_Finish:
          # Read the last part of the file (if any)
          File_Mode = os.stat ( self.Filename )
          File_Size = File_Mode [ ST_SIZE ]
          if File_Size > self.Done :
            line = self.fh.read ( File_Size - self.Done )
          self.fh.close ()
          self.Status = 2
          self.IsRunning = False
    return line

  # *********************************************
  # *********************************************
  def Kill ( self ) :
    if self.Process.poll() is None :
      Kill_Process_and_Children_pid ( self.Process.pid )

# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def Run_Python ( arguments, cwd = None ) :
  """
  Runs a Python script and doesn't wait.
  "Arguments" starts with the script, followed by the commandline arguments.
  "Arguments" maybe of type string, tuple, list.
  The Python executable should NOT be in the argument list.
  If the script is started from another directory,
  cwd is automatically calcuated.
  Examples:
    Run_Python ( [ 'PyLab_Works.py', 'aap' ] )
    Run_Python ( '../support/multi_language.py' )
  """
  arguments, cwd = _PreProcess_Run_Python ( arguments, cwd )
  v3print ( '[[[]]]', arguments, cwd )
  return subprocess.Popen ( arguments,
                            cwd   = cwd ,
                            shell =  ( os.name == 'nt') )

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Run_Python_NoWait ( arguments, cwd = None, stdOUT = None ) :
  """
  Runs a Python script and doesn't wait.
  "Arguments" starts with the script, followed by the commandline arguments.
  "Arguments" maybe of type string, tuple, list.
  The Python executable should NOT be in the argument list.
  If the script is started from another directory,
  cwd is automatically calcuated.
  Examples:
    Run_Python_NoWait ( [ 'PyLab_Works.py', 'aap' ] )
    Run_Python_NoWait ( '../support/multi_language.py' )
  """
  arguments, cwd = _PreProcess_Run_Python ( arguments, cwd )

  # For Windows shell must be True,
  # For Ubuntu, shell must be False
  try :
    print('==== Run_Python_NoWait')
    print('    cwd =', cwd)
    print('   args =', arguments)
    Process = subprocess.Popen( arguments,
                                cwd    = cwd,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell  =  ( os.name == 'nt') )
  except :
    print('***** ERROR in Run_Python_NoWait ******')
    print('      arguments  = ', arguments)
  return Process

# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def Run(filename, cwd=None, show='normal', priority=2, bufsize=0, \
        executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None,\
        close_fds=False, shell=False, env=None, universal_newlines=False, \
        startupinfo=None, creationflags=0):
  #IDLE_PRIORITY         0x00000040 ok
  #BELOW_NORMAL_PRIORITY 0x00004000 ok
  #NORMAL_PRIORITY       0x00000020 ok
  #ABOVE_NORMAL_PRIORITY 0x00008000 ok
  #HIGH_PRIORITY         0x00000080 ok
  #REALTIME_PRIORITY     0x00000100 ok
  #Global Const SW_HIDE = 0
  #Global Const SW_SHOWNORMAL = 1
  #Global Const SW_SHOWMINIMIZED = 2
  #lobal Const SW_SHOWMAXIMIZED = 3
  if isinstance ( show, basestring ) :
    window_state = {"hide":0, "normal":1, "minimized":2,"maximized":3,\
                    "hidden":0,"minimize":2,"maximize":3}
    show = window_state[show]
  if show!=1:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= 1#subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = show
  if cwd == "":
    cwd = None
  process_priority =[ 0x40,0x00004000,0x00000020,0x00008000,0x00000080,0x00000100]
  #Run ( "filename" [, "workingdir" [, flag[, standard_i/o_flag]]] )
  return subprocess.Popen(filename, bufsize, executable, stdin, stdout, stderr,\
                          preexec_fn, close_fds, shell, cwd, env,\
                          universal_newlines, startupinfo, \
                          creationflags=(process_priority[priority]|creationflags))
  #subprocess.Popen( filename, shell=shell, cwd=workingdir, creationflags=process_priority[priority], startupinfo=startupinfo)
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def RunWait(*args, **kwargs):
  return Run(*args, **kwargs).wait()
##def RunWait(filename, cwd=None, show='normal', priority=2, bufsize=0, \
##        executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None,\
##        close_fds=False, shell=False, env=None, universal_newlines=False, \
##        startupinfo=None, creationflags=0):
##  #if type(show) == basestring:
##  if isinstance ( show, basestring ) :
##    window_state = {"hide":0, "normal":1, "minimized":2,"maximized":3,\
##                    "hidden":0,"minimize":2,"maximize":3}
##    show = window_state[show]
##  if show<>1:
##    startupinfo = subprocess.STARTUPINFO()
##    startupinfo.dwFlags |= 1 #subprocess.STARTF_USESHOWWINDOW
##    startupinfo.wShowWindow = show
##  if cwd == "":
##    cwd = None
##  process_priority =[ 0x40,0x00004000,0x00000020,0x00008000,0x00000080,0x00000100]
##  return subprocess.call(filename, bufsize, executable, stdin, stdout, stderr,\
##                          preexec_fn, close_fds, shell, cwd, env,\
##                          universal_newlines, startupinfo, \
##                          creationflags=(process_priority[priority]|creationflags))

runwait = Runwait = RunWait
run = Run

# ***********************************************************************
##def run(filename, workingdir=None,show="normal", priority=2, shell=False, env=None, startupinfo=None, creationflags=None ):
##  print "use Run, you are using a badly named routine",filename
##  Run(filename, workingdir,show, priority, shell, env, startupinfo, creationflags )
##def runwait(filename, workingdir=None,show="normal", priority=2, shell=False, env=None, startupinfo=None, creationflags=None ):
##  print "use RunWait, you are using a badly named routine",filename
##  RunWait(filename, workingdir,show, priority, shell, env, startupinfo, creationflags )
##def Runwait(filename, workingdir=None,show="normal", priority=2, shell=False, env=None, startupinfo=None, creationflags=None ):
##  print "use RunWait, you are using a badly named routine",filename
##  RunWait(filename, workingdir,show, priority, shell, env, startupinfo, creationflags )
# ***********************************************************************
def setpriority(pid=None,priority=1):
    """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process but can take any valid process ID. """

    import win32api,win32process,win32con

    priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                       win32process.BELOW_NORMAL_PRIORITY_CLASS,
                       win32process.NORMAL_PRIORITY_CLASS,
                       win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                       win32process.HIGH_PRIORITY_CLASS,
                       win32process.REALTIME_PRIORITY_CLASS]
    if pid == None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priorityclasses[priority])


#run(["notepad.exe"],"","minimized",priority=5)
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def test_back () :
  Source_File = sys._getframe(1).f_code.co_filename

  # PROBABLY BETTER
  Frame = 1
  while Source_File == '<string>' :
    print('FRAME UP +++', text)
    Frame += 1
    Source_File = sys._getframe( Frame ).f_code.co_filename

  print('Source_File', Source_File)

  Source_Path, Source_File = path_split ( Source_File )
  Source_File = os.path.splitext ( Source_File )[0]
  print('Source_Path', Source_Path)
  print('Source_File', Source_File)
  Language_File = os.path.join ( Source_Path, 'lang', Source_File + '_NL.py' )
  print('Language_File', Language_File)
  from file_support import File_Exists
  print(File_Exists ( Language_File ))
  sys.path.append ( os.path.join ( Source_Path, 'lang' ))
  print('sys.path:')
  import test_syspath_NL
  for item in sys.path :
    print('  ', item)

  if File_Exists ( Language_File ) :
    Language_File = os.path.splitext ( Language_File ) [0]
    line = 'from ' + Source_File + '_NL' + ' import LT'
    print('exec:', line)
    try :
      exec ( line )
      print('LT',LT)
    except :
      print('Error importing Language File', Language_File)
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Hash_Encrypt_MD5 ( line ) :
  encrypt = hashlib.md5 ( line )
  return encrypt.hexdigest ()

def Hash_Encrypt_SHA1 ( line ) :
  encrypt = hashlib.sha1 ( line )
  return encrypt.hexdigest ()

def Hash_Encrypt_SHA224 ( line ) :
  encrypt = hashlib.sha224 ( line )
  return encrypt.hexdigest ()

def Hash_Encrypt_SHA256 ( line ) :
  encrypt = hashlib.sha256 ( line )
  return encrypt.hexdigest ()

def Hash_Encrypt_SHA384 ( line ) :
  encrypt = hashlib.sha384 ( line )
  return encrypt.hexdigest ()

def Hash_Encrypt_SHA512 ( line ) :
  encrypt = hashlib.sha512 ( line )
  return encrypt.hexdigest ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == "__main__":

  Test_Defs ( 18)

  if Test ( 1 ) :
    # ************************************
    # test of Process
    # ************************************
    import subprocess
    pipe = subprocess.Popen('D:/Data_Lego/D7_uploader_programmer/UPD.exe')
    #time.sleep(5)
    print('PID',pipe.pid)

    a = GetAllProcesses()
    print(a)

    process = 'UPD'
    Kill_Process ( process )

  if Test ( 2 ) :
    for i in range ( 1 ) :
      time.sleep(2)
      a = GetAllProcesses()
      print(a)

  if Test ( 3 ) :
    # ************************************
    # test of Make_Absolute_path
    # ************************************
    file = '../aap.html'
    path = 'http://stef/het/new/oud/pylab_works_demo_graph_calculator.html'
    print(Make_Absolute_Path ( path, file ))
    path = 'file:///d:/stef/het/new/oud/pylab_works_demo_graph_calculator.html'
    print(Make_Absolute_Path ( path, file ))
    path = 'd:/stef/het/new/oud/pylab_works_demo_graph_calculator.html'
    print(Make_Absolute_Path ( path, file ))

    file = 'd:/beer/aap.html'
    path = 'http://stef/het/new/oud/pylab_works_demo_graph_calculator.html'
    print(Make_Absolute_Path ( path, file ))
    path = 'file:///d:/stef/het/new/oud/pylab_works_demo_graph_calculator.html'
    print(Make_Absolute_Path ( path, file ))
    path = 'd:/stef/het/new/oud/pylab_works_demo_graph_calculator.html'
    print(Make_Absolute_Path ( path, file ))

    path = 'D:\DATA_actueel\Stef'
    file = 'test_wxp_img1.gif'
    print(Make_Absolute_Path ( path, file ))
    # | file:///test_wxp_img1.gif

    path = 'D:\data_www\pylab_works'
    file = 'pw_animations_screenshots_img5.png'
    print(Make_Absolute_Path ( path, file ))
    # | D:\data_www\pw_animations_screenshots_img5.png

  if Test ( 4 ) :
    import subprocess
    subprocess.Popen ( [ 'python', 'file_support.py' ] )
    #run( ["tree_support.py"], shell =  ( os.name == 'nt') )

    #run( ["notepad.exe", "test.txt"] )

    Run_Python ( '../support/file_support.py' )

    """
    run ( [ 'Python', '../PyLab_Works/PyLab_Works.py',
            'aap' ],
          cwd = '../PyLab_Works/',
          shell =  ( os.name == 'nt') )
    """

  if Test ( 5 )  :
    import wmi
    w = wmi.WMI ()
    for process in w.Win32_Process ( caption = "cmd.exe" ) : #caption="notepad.exe"):
      print(process)

  if Test ( 6 ) :
     print(RunWait ( "cmd.exe", cwd=None, show='normal', priority=2, bufsize=0, \
        executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None,\
        close_fds=False, shell =  ( os.name == 'nt'), env=None, universal_newlines=False, \
        startupinfo=None, creationflags=0))

  # ************************************************************************
  # Test of Starting external winpdb
  # ************************************************************************
  if Test ( 7  ) :
    Main_File = r'D:/Data_Python_25/PyLab_Works/test_IDE.py'
    Main_Path = os.path.split( Main_File ) [0]
    import winpdb
    External_Debugger = winpdb.__file__
    subprocess.Popen (
        [ 'Python', External_Debugger, Main_File ],
        cwd   = Main_Path,
        shell = ( os.name == 'nt') )

  # ************************************************************************
  # ************************************************************************
  if Test ( 9 ) :
    print('sys.path:')
    for item in sys.path :
      print('  ', item)
    print('sys.path[0] = path of the main application file ', sys.path[0])
    print('os.getcwd()', os.getcwd ())
    print('__file__', __file__)

    #sys.path.append ( '../PyLab_Works' )
    from test_syspath import test
    test ()

  # *******************************************************
  # Beep and MAC addresses
  # *******************************************************
  if Test ( 10 ) :
    Beep ()
    print('\n=== Output of ipconfig/all ===')
    for line in Get_ipconfig_all () :
      print(line)

    print('\n=== MAC Addresses ===')
    for MAC in Get_MAC_Addresses () :
      print(MAC[1], '=', MAC[0])

  # *******************************************************
  # Encryption testing
  # *******************************************************
  if Test ( 11 ) :
    lines = [ 'z571117', 'Administrator' ]
    for line in lines :
      v3print ( '***** Encryption of :', line )
      v3print ( 'MD5    :', Hash_Encrypt_MD5    ( line ) )
      v3print ( 'SHA1   :', Hash_Encrypt_SHA1   ( line ) )
      v3print ( 'SHA224 :', Hash_Encrypt_SHA224 ( line ) )
      v3print ( 'SHA256 :', Hash_Encrypt_SHA256 ( line ) )
      v3print ( 'SHA384 :', Hash_Encrypt_SHA384 ( line ) )
      v3print ( 'SHA512 :', Hash_Encrypt_SHA512 ( line ) )


    for line in lines :
      # Encrypt a string
      enc = encryption_key_1.encString ( line )
      print("Encrypted", type ( enc ), enc)

      # Now decrypt it
      dec =  encryption_key_1.decString ( enc )
      print("Decrypted string: '%s'" % dec)

      enc = EnCrypt_1 ( line )
      print('EnCrypt_1', enc)
      print('DeCrypt_1', DeCrypt_1 ( enc ))


  # *******************************************************
  # *******************************************************
  if Test ( 12 ) :
    v3print ( 'Current logged in user =', Get_User () )
    import active_directory
    my_root = active_directory.root ()
    print(my_root)
    """
    for master in my_root.masteredBy:
      print master.Parent.dNSHostName


    all_users = set ()
    for group, groups, users in active_directory.find_group ("Domain Admins").walk ():
      all_users.update (users)

    for u in all_users:
      print u.displayName
    """

    i = 0
    for person in active_directory.search ("objectCategory='Person'") :
      #print person.displayName, person.properties
      Name = person.displayName
      if Name and 'mientki' in Name.lower() :
        print(Name,person.sAMAccountName)
        break
        #print dir(person)
        #print person.dump()
        props =  person.properties
        for prop in props :
          print(prop, end=' ')
          try :
            print(eval ( 'person.' + prop ))
          except :
            pass
        person.employeeNumber,
      """
Beheerder Jansen ['AD_iterator', '__class__', '__delattr__', '__dict__', '__doc__', '__eq__',
'__getattr__', '__getattribute__', '__getitem__', '__hash__', '__init__', '__iter__', '__module__',
 '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__str__',
 '__weakref__', '_delegate_map', '_property_map', 'as_string', 'child', 'com_object', 'dump',
 'find_computer', 'find_group', 'find_ou', 'find_public_folder', 'find_user', 'is_container',
 'parent', 'path', 'properties', 'search', 'set', 'walk']
"""
      """
Beheerder Jansen (u'cn', u'instanceType', u'nTSecurityDescriptor', u'objectCategory',
u'objectClass', u'objectSid', u'sAMAccountName', u'accountExpires', u'accountNameHistory',
u'aCSPolicyName', u'adminCount', u'adminDescription', u'adminDisplayName', u'allowedAttributes',
u'allowedAttributesEffective', u'allowedChildClasses', u'allowedChildClassesEffective',
u'altRecipient', u'altRecipientBL', u'altSecurityIdentities', u'assistant', u'attributeCertificate',
u'attributeCertificateAttribute', u'audio', u'authOrig', u'authOrigBL', u'autoReply',
u'autoReplyMessage', u'badPasswordTime', u'badPwdCount', u'bridgeheadServerListBL',
u'businessCategory', u'businessRoles', u'c', u'canonicalName', u'carLicense', u'co',
u'codePage', u'comment', u'company', u'controlAccessRights', u'countryCode', u'createTimeStamp',
u'dBCSPwd', u'defaultClassStore', u'deletedItemFlags', u'delivContLength', u'deliverAndRedirect',
u'deliveryMechanism', u'delivExtContTypes', u'department', u'departmentNumber', u'description',
u'desktopProfile', u'destinationIndicator', u'directReports', u'displayName',
u'displayNamePrintable', u'distinguishedName', u'division', u'dLMemDefault', u'dLMemRejectPerms',
u'dLMemRejectPermsBL', u'dLMemSubmitPerms', u'dLMemSubmitPermsBL', u'dnQualifier',
u'dSASignature', u'dSCorePropagationData', u'dynamicLDAPServer', u'employeeID', u'employeeNumber',
u'employeeType', u'enabledProtocols', u'expirationTime', u'extensionAttribute1',
u'extensionAttribute10', u'extensionAttribute11', u'extensionAttribute12', u'extensionAttribute13',
u'extensionAttribute14', u'extensionAttribute15', u'extensionAttribute2', u'extensionAttribute3',
u'extensionAttribute4', u'extensionAttribute5', u'extensionAttribute6', u'extensionAttribute7',
u'extensionAttribute8', u'extensionAttribute9', u'extensionData', u'extensionName',
u'facsimileTelephoneNumber', u'flags', u'folderPathname', u'formData', u'forwardingAddress',
u'fromEntry', u'frsComputerReferenceBL', u'fRSMemberReferenceBL', u'fSMORoleOwner',
u'garbageCollPeriod', u'gecos', u'generationQualifier', u'gidNumber', u'givenName',
u'groupMembershipSAM', u'groupPriority', u'groupsToIgnore', u'heuristics', u'homeDirectory',
u'homeDrive', u'homeMDB', u'homeMTA', u'homePhone', u'homePostalAddress', u'houseIdentifier',
u'importedFrom', u'info', u'initials', u'internationalISDNNumber', u'internetEncoding',
u'ipPhone', u'isCriticalSystemObject', u'isDeleted', u'isPrivilegeHolder', u'jpegPhoto',
u'kMServer', u'l', u'labeledURI', u'language', u'languageCode', u'lastKnownParent',
u'lastLogoff', u'lastLogon', u'lastLogonTimestamp', u'legacyExchangeDN', u'lmPwdHistory',
u'localeID', u'lockoutTime', u'loginShell', u'logonCount', u'logonHours', u'logonWorkstation',
u'mail', u'mailNickname', u'managedObjects', u'manager', u'mAPIRecipient', u'masteredBy',
u'maxStorage', u'mDBOverHardQuotaLimit', u'mDBOverQuotaLimit', u'mDBStorageQuota',
u'mDBUseDefaults', u'memberOf', u'mhsORAddress', u'middleName', u'mobile', u'modifyTimeStamp',
u'mS-DS-ConsistencyChildCount', u'mS-DS-ConsistencyGuid', u'mS-DS-CreatorSID',
u'msCOM-PartitionSetLink', u'msCOM-UserLink', u'msCOM-UserPartitionSetLink',
u'msDFSR-ComputerReferenceBL', u'msDFSR-MemberReferenceBL', u'msDRM-IdentityCertificate',
u'msDS-AllowedToDelegateTo', u'msDS-Approx-Immed-Subordinates', u'msDS-Cached-Membership',
u'msDS-Cached-Membership-Time-Stamp', u'msDS-KeyVersionNumber', u'msDs-masteredBy',
u'msDS-MembersForAzRoleBL', u'msDS-NCReplCursors', u'msDS-NCReplInboundNeighbors',
u'msDS-NCReplOutboundNeighbors', u'msDS-NonMembersBL', u'msDS-ObjectReferenceBL',
u'msDS-OperationsForAzRoleBL', u'msDS-OperationsForAzTaskBL', u'msDS-ReplAttributeMetaData',
u'msDS-ReplValueMetaData', u'msDS-Site-Affinity', u'msDS-SourceObjectDN', u'msDS-TasksForAzRoleBL',
u'msDS-TasksForAzTaskBL', u'msDS-User-Account-Control-Computed', u'msExchADCGlobalNames',
u'msExchALObjectVersion', u'msExchAssistantName', u'msExchConferenceMailboxBL',
u'msExchControllingZone', u'msExchCustomProxyAddresses', u'msExchExpansionServerName',
u'msExchFBURL', u'msExchHideFromAddressLists', u'msExchHomeServerName', u'msExchHouseIdentifier',
u'msExchIMACL', u'msExchIMAddress', u'msExchIMAPOWAURLPrefixOverride', u'msExchIMMetaPhysicalURL',
u'msExchIMPhysicalURL', u'msExchIMVirtualServer', u'msExchInconsistentState', u'msExchLabeledURI',
u'msExchMailboxFolderSet', u'msExchMailboxGuid', u'msExchMailboxSecurityDescriptor',
u'msExchMailboxUrl', u'msExchMasterAccountSid', u'msExchOmaAdminExtendedSettings',
u'msExchOmaAdminWirelessEnable', u'msExchOriginatingForest', u'msExchPfRootUrl',
u'msExchPoliciesExcluded', u'msExchPoliciesIncluded', u'msExchPolicyEnabled',
u'msExchPolicyOptionList', u'msExchPreviousAccountSid', u'msExchProxyCustomProxy',
u'msExchQueryBaseDN', u'msExchRecipLimit', u'msExchRequireAuthToSendTo', u'msExchResourceGUID',
u'msExchResourceProperties', u'msExchTUIPassword', u'msExchTUISpeed', u'msExchTUIVolume',
u'msExchUnmergedAttsPt', u'msExchUseOAB', u'msExchUserAccountControl', u'msExchVoiceMailboxID',
u'msIIS-FTPDir', u'msIIS-FTPRoot', u'mSMQDigests', u'mSMQDigestsMig', u'mSMQSignCertificates',
u'mSMQSignCertificatesMig', u'msNPAllowDialin', u'msNPCallingStationID',
u'msNPSavedCallingStationID', u'msRADIUSCallbackNumber', u'msRADIUSFramedIPAddress',
u'msRADIUSFramedRoute', u'msRADIUSServiceType', u'msRASSavedCallbackNumber',
u'msRASSavedFramedIPAddress', u'msRASSavedFramedRoute', u'msSFU30Name', u'msSFU30NisDomain',
u'msSFU30PosixMemberOf', u'name', u'netbootSCPBL', u'networkAddress', u'nonSecurityMemberBL',
u'ntPwdHistory', u'o', u'objectGUID', u'objectVersion', u'operatorCount',
u'otherFacsimileTelephoneNumber', u'otherHomePhone', u'otherIpPhone', u'otherLoginWorkstations',
u'otherMailbox', u'otherMobile', u'otherPager', u'otherTelephone', u'otherWellKnownObjects',
u'ou', u'ownerBL', u'pager', u'partialAttributeDeletionList', u'partialAttributeSet',
u'personalPager', u'personalTitle', u'photo', u'physicalDeliveryOfficeName', u'pOPCharacterSet',
u'pOPContentFormat', u'possibleInferiors', u'postalAddress', u'postalCode', u'postOfficeBox',
u'preferredDeliveryMethod', u'preferredLanguage', u'preferredOU', u'primaryGroupID',
u'primaryInternationalISDNNumber', u'primaryTelexNumber', u'profilePath', u'protocolSettings',
u'proxiedObjectName', u'proxyAddresses', u'publicDelegates', u'publicDelegatesBL', u'pwdLastSet',
u'queryPolicyBL', u'registeredAddress', u'replicatedObjectVersion', u'replicationSensitivity',
u'replicationSignature', u'replPropertyMetaData', u'replUpToDateVector', u'repsFrom', u'repsTo',
u'revision', u'rid', u'roomNumber', u'sAMAccountType', u'scriptPath', u'sDRightsEffective',
u'secretary', u'securityIdentifier', u'securityProtocol', u'seeAlso', u'serialNumber',
u'serverReferenceBL', u'servicePrincipalName', u'shadowExpire', u'shadowFlag', u'shadowInactive',
u'shadowLastChange', u'shadowMax', u'shadowMin', u'shadowWarning', u'showInAddressBook',
u'showInAdvancedViewOnly', u'sIDHistory', u'siteObjectBL', u'sn', u'st', u'street',
u'streetAddress', u'structuralObjectClass', u'submissionContLength', u'subRefs',
u'subSchemaSubEntry', u'supplementalCredentials', u'supportedAlgorithms', u'systemFlags',
u'targetAddress', u'telephoneAssistant', u'telephoneNumber', u'teletexTerminalIdentifier',
u'telexNumber', u'terminalServer', u'textEncodedORAddress', u'thumbnailLogo', u'thumbnailPhoto',
u'title', u'tokenGroups', u'tokenGroupsGlobalAndUniversal', u'tokenGroupsNoGCAcceptable', u'uid',
u'uidNumber', u'unauthOrig', u'unauthOrigBL', u'unicodePwd', u'unixHomeDirectory',
'unixUserPassword', u'unmergedAtts', u'url', u'userAccountControl', u'userCert',
u'userCertificate', u'userParameters', u'userPassword', u'userPKCS12', u'userPrincipalName',
u'userSharedFolder', u'userSharedFolderOther', u'userSMIMECertificate', u'userWorkstations',
u'uSNChanged', u'uSNCreated', u'uSNDSALastObjRemoved', u'USNIntersite', u'uSNLastObjRem',
u'uSNSource', u'versionNumber', u'wbemPath', u'wellKnownObjects', u'whenChanged', u'whenCreated',
u'wWWHomePage', u'x121Address', u'x500uniqueIdentifier')
"""
      i += 1
      if i >300000 :
        break

    domain_admins = active_directory.find_group ("Domain Admins")
    all_users = set ()
    #for group, groups, users in domain_admins.walk ():
    #  all_users.update (users)

  """
Explorer [/n] [/e] [(,)/root,<object>] [/select,<object>]

/n                Opens a new single-pane window for the default
                  selection. This is usually the root of the drive Windows
                   is installed on. If the window is already open, a
                  duplicate opens.

/e                Opens Windows Explorer in its default view.

/root,<object>    Opens a window view of the specified object.


/select,<object>  Opens a window view with the specified folder, file or
                  application selected.

Examples:

   Example 1:     Explorer /select,C:\TestDir\TestApp.exe

      Opens a window view with TestApp selected.

   Example 2:  Explorer /e,/root,C:\TestDir\TestApp.exe

      This opens Explorer with C: expanded and TestApp selected.

   Example 3:  Explorer /root,\\TestSvr\TestShare

      Opens a window view of the specified share.

   Example 4:  Explorer /root,\\TestSvr\TestShare,select,TestApp.exe

      Opens a window view of the specified share with TestApp selected.
"""
  # *******************************************************
  # *******************************************************
  if Test ( 13 ) :
    #subprocess.Popen ( ['Explorer.exe','/e' ], shell=False)
    #subprocess.Popen ( ['Explorer.exe','/root,D:\Data_Python_25' ], shell=False)
    subprocess.Popen ( ['Explorer.exe','/e,','D:\Data_Python_25' ], shell=False)

  # *******************************************************
  # *******************************************************
  if Test ( 14 ) :
    for Share in Get_Shares () :
      print(Share)

    '''
    print '\n*****  StartUp Programs  *****'
    for StartUp in Get_StartUps () :
      print ' ', StartUp.Command

    print '\n*****  MAC / IP  *****'
    MAC_IPs = Get_MAC_IP ()
    for K, V in MAC_IPs.iteritems() :
      print K
      print ' ', V

    print '\n*****  Stopped Services  *****'
    for Service in Get_Stopped_Services () :
      print ' ', Service
    '''

    print('\n*****  Process CommandLines  *****')
    '''
    for K, V in Get_Process_CommandLine().iteritems() :
      if ( K == 'cmd.exe') and ( 'rpdb2.py" --debugee' in V ) :
        print 'VCCCC ', K
        print '   ', V

      if ( K == 'python.exe') and ( 'rpdb2.py" --debugee' in V ) :
        print 'PPPP ', K
        print '   ', V
    '''
    start = time.time()
    print('CMD', Get_PID_from_CommandLine ( 'cmd.exe', 'rpdb2.py" --debugee' ))
    print('PYT', Get_PID_from_CommandLine ( 'python.exe', 'rpdb2.py" --debugee' ))
    print(int(1000*(time.time()-start)))

    start = time.time()
    Get_PID_and_CommandLine ()
    print(int(1000*(time.time()-start)))

    start = time.time()
    Get_PID_and_CommandLine ()
    print(int(1000*(time.time()-start)))

    for K, V in list(Get_PID_and_CommandLine ().items()) :
      if ( K == 'cmd.exe') and ( 'rpdb2.py" --debugee' in V[1] ) :
        print('VCCCC ', K)
        print('   ', V)

      if ( K == 'python.exe') and ( 'rpdb2.py" --debugee' in V[1] ) :
        print('PPPP ', K)
        print('   ', V)



    sys.exit()
    from file_support import File_Exists
    filename = 'D:/PIC-tools/D7_uploader_programmer/UPD.exe'
    if File_Exists ( filename ) :
      #pipe = subprocess.Popen( filename )
      #print 'PID',pipe.pid

      All_Processes = GetAllProcesses()
      for process in All_Processes :
        print(process)
      sys.exit()

      process = 'UPD'
      process = 'TO_aggregatie.exe'
      if process in All_Processes :
        process = 'TO_aggregatie.exe'
        PID = Get_Process_PID ( process )
        print('PID', process, PID)
        if PID :
          #Kill_Process_pid ( PID )
          #Kill_Process_pid_Name ( PID, process )
          ## Kill_Process ( process )
          Kill_Process_pid ( PID )
          PID = Get_Process_PID ( process )
          print('PID', process, PID)
      else :
        print('Proces not found', process)

      #Kill_Process ( process )
      print()

  # *******************************************************
  # speed of ProcessExists
  # *******************************************************
  if Test ( 15 ) :
    process = 'web2py_no_console.exe'

    start = time.time ()
    print('time', int ( 1000* ( time.time() - start ) ))

    start = time.time ()
    print('Get_Process_PID, PID', Get_Process_PID ( process ))
    print('time', int ( 1000* ( time.time() - start ) ))
    sys.exit()

    start = time.time ()
    print(_AutoIt.ProcessExists ( process ))
    print('time', int ( 1000* ( time.time() - start ) ))

    start = time.time ()
    print('Get_Process_PID, PID', Get_Process_PID ( process ))
    print('time', int ( 1000* ( time.time() - start ) ))

    #print dir(psutil)
    #print psutil.get_process_list ()
    """ print dir(psutil)
['AccessDenied', 'CPUTimes', 'ERROR_ACCESS_DENIED', 'ERROR_INVALID_PARAMETER',
'Impl', 'NUM_CPUS', 'NoSuchProcess', 'Process', 'ProcessInfo', 'TOTAL_PHYMEM',
'__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__',
'__path__', '__version__', '_last_idle_time', '_last_time', '_platform_impl',
'_psmswindows', 'avail_phymem', 'avail_virtmem', 'cpu_percent', 'cpu_times',
'errno', 'error', 'get_pid_list', 'get_process_list', 'get_system_cpu_times',
'grp', 'os', 'pid_exists', 'process_iter', 'pwd', 'sys', 'test', 'time',
'total_virtmem', 'used_phymem', 'used_virtmem', 'wmi', 'wrap_privileges']
"""

    start = time.time ()
    for p in psutil.process_iter ():
      #print p
      if p.name == process :
        print('Z',p.pid)
        break
    else:
      print("Not found")
    print('time', int ( 1000* ( time.time() - start ) ))

  # *******************************************************
  # Run_My_Python_and_Capture
  # Launch a python program and capture it's output
  # *******************************************************
  if Test ( 16 ) :
    Process = Run_My_Python_and_Capture ( 'stdout_redirect_test_run.py' )
    #Process = Run_My_Python_and_Capture ( ['stdout_redirect_test_run.py', 'piep' ] )
    #Process = Run_My_Python_and_Capture ( 'stdout_redirect_test_run.py, piep' )
    start = time.time ()
    while Process.IsRunning :
      print('XXX', Process.Get_Data ())
      time.sleep ( 0.3)
      if time.time() - start > 5 :
        Process.Kill ()

  # *******************************************************
  if Test ( 17 ) :
    # Kill all running IEs
    while Get_Process_PID ( 'iexplore.exe' ) >= 0 :
      Kill_Process ( 'iexplore.exe' )
      time.sleep ( 1 )

    # Start new IE with no SHELL !! and wait until it's finished
    Process = subprocess.Popen( [ 'C:/Program Files/Internet Explorer/iexplore.exe',
                                  'http://pic.flappie.nl' ],
                                shell=False)
    Process.wait()

    '''
    URL = 'http://pic.flappie.nl'
    import webbrowser
    print dir(webbrowser.get())
    wb=webbrowser.get()
    print wb.name,wb.basename,wb
    webbrowser.open ( URL )
    '''
    print('klaar', Process.poll())
  if Test(18):
    print(Get_hwnds_from_Title())


# ***********************************************************************
pd_Module ( __file__ )

