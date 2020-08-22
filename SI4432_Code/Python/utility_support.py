from __future__ import print_function
from __future__ import absolute_import
from past.builtins import cmp
from builtins import str
from past.builtins import basestring
from builtins import object

_Version_Text = [

[ 0.14, '28-03-2013', 'Stef Mientki',
'Test Conditions:', (),
"""
- NoCase_Dict.__getitem__  improved for unicode/string
""" ],

[ 0.13, '02-08-2012', 'Stef Mientki',
'Test Conditions:', (),
"""
- flatten added
""" ],

[ 0.12, '12-06-2012', 'Stef Mientki',
'Test Conditions:', (),
"""
- NoCase_Dict.__repr__ will not print __builtins__ anymore
""" ],

[ 0.11, '24-03-2012', 'Stef Mientki',
'Test Conditions:', (),
"""
- NoCase_Dict.__getstate__ will raise an exception, needed for Pickle !!
""" ],

[ 0.10, '21-1-2012', 'Stef Mientki',
'Test Conditions:', (),
"""
- NoCase_Dict.__repr__  added (prints a readable list)
- NoCase_Dict.__str__  added  (otherwise __repr__ is used instead)
""" ],

[ 0.9, '26-12-2011', 'Stef Mientki',
'Test Conditions:', (),
"""
- NoCase_Dict.Get_CaseName   added, returns the Key in the exact case
""" ],

[ 0.8, '17-09-2011', 'Stef Mientki',
'Test Conditions:', (),
"""
- NoCase_Dict, keys integer <==> string improved
""" ],

[ 0.7, '26-6-2011', 'Stef Mientki',
'Test Conditions:', (),
"""
- NoCase_Dict made callable
""" ],

[ 0.6, '18-11-2010', 'Stef Mientki',
'Test Conditions:', (),
"""
- Sort_Dict   added
- NoCase_List  bug fixed in comapring non-string values
""" ],

[ 0.5, '29-10-2010', 'Stef Mientki',
'Test Conditions:', (),
"""
- Get_Dict_Col_Data   added
""" ],

[ 0.4, '26-09-2010', 'Stef Mientki',
'Test Conditions:', (),
"""
- NoCase_Dict.has_key, still didn't work correctly
- NoCase_Dict several methods improved for handling non string keya
""" ],

[ 0.3, '05-09-2010', 'Stef Mientki',
'Test Conditions:', (),
"""
- NoCase_Dict  delete element added
- NoCase_Dict.has_key, didn't work correctly
- NoCase_Dict, now keys may also be specified as attributes
- NoCase_Dict.Copy added
""" ],

[ 0.2, '25-06-2009', 'Stef Mientki',
'Test Conditions:', (),
"""
- super_object doens't give an error if a non-existing attribute is asked,
  but just returns None
""" ],

[ 0.1, '???', 'Stef Mientki',
'Test Conditions:', (),
"""
- orginal release
""" ]
]
# ***********************************************************************

import __init__
from   string_support  import _2U

#from General_Globals import *
#from General_Globals import pd_Module


"""
# ***********************************************************************
# ***********************************************************************
class s_list ( list ) :
  def Get ( self, Attrib, Default ) :
    try :
      return getattr ( self, Attrib )
    except :
      return Default
# ***********************************************************************
"""




# ***********************************************************************
# ***********************************************************************
class super_dict ( dict ) : #, object ) :
  pass

class super_object ( object ) :
  """Object with some features of a dictionair"""
  def Get ( self, arg, default ) :
    """Mimicks the "get" function of a dictionair."""
    try :
      return getattr ( self, arg )
    except :
      # If the property doesn't exist,
      # Create it now
      setattr ( self, arg, default )
      return default

  # *********************************************************
  # only called when not found with the normal mechanism
  # *********************************************************
  def __getattr__ ( self, attr ) :
    if not ( attr in self.__dict__ ) :
      self.__dict__[attr] = None
    return self.__dict__[attr]



# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get ( Base, Attrib, Default ) :
  try :
    return getattr ( Base, Attrib )
  except :
    return Default
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def  nice_number ( value ) :
  if   abs ( value ) >= 100 :
    line = '%5d' %( int(value) )
  elif abs ( value ) >= 10 :
    line = '%5.1f' %( value )
  else:
    line = '%5.2f' %( value )
  return line
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
_types = ['int   ', 'float ', 'string' ]
def _Type_Enumerate_weg ( value, pre, counters ) :
  pre += '--'
  if type ( value ) in [ list, tuple ] :
    counters.append ( [ 0, 0 ] )
    print(pre, type ( value ).__name__)
    for item in value :
      _Type_Enumerate ( item, pre, counters )
    count = counters.pop ()
    for i,c in enumerate ( count ) :
      if c > 0 :
        print(pre + '--', _types[i], '=', c)
  else :
    if type ( value ) == int :
      counters [-1][0] += 1
    if type ( value ) == float :
      counters [-1][1] += 1
    #print pre, type (value).__name__, counters[-1]



# ***********************************************************************
# ***********************************************************************
def _Type_Enumerate ( value, pre, counters ) :
  pre += '--'
  typ = type ( value )
  last = counters [-1]

  if typ in [ list, tuple, array ] :
    if ( last [0] > 0):
      print(pre, last[1].__name__.ljust(6), '=', last[0])
      counters.pop()

    counters.append ( [ 0, None ] )
    print(pre, typ.__name__)
    for item in value :
      _Type_Enumerate ( item, pre, counters )

    last = counters.pop ()
    if last [0] > 0 :
      print(pre + '--', last[1].__name__.ljust(6),'=',last[0])

  else :
    if last [1] == typ :
      last [0] += 1
    else :
      if last[0] > 0:
        print(pre, last[1].__name__.ljust(6),'=',last[0])
      last[0] = 1
      last[1] = typ


# ***********************************************************************
# ***********************************************************************
def Type_Enumerate ( value ) :
  _Type_Enumerate ( value, '|', [0, [0,None]] )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class TIO_Dict ( dict ) :
  """
  Dictionary that can print or log debug info.
  The following methods will be logged:
  - Create
  - Read
  - Write
  """
  def _Log ( self, *args ) :
    #if 'TIO' in Debug_What :
    if self.Max_Log_Count > 0 :
      Debug_Dump_Trace ( 'TIO_Dict\n', *args )
      self.Max_Log_Count -= 1
      if self.Max_Log_Count == 0 :
         Debug_Dump ( 'TIO_Dict, ****** max limit exceeded ******')

  #def __init__ ( self, Parent = None, PIndex = -1 ):
  def __init__ ( self, Parent, PIndex ):
    self.Parent = Parent
    self.PIndex = PIndex
    self.Max_Log_Count = 100
    dict.__init__ ( self )
    ##self.Modified = False
    if ( 'TIO-Read' in Debug_What ) :
      self._Log ( 'Create' )

  def __setitem__ ( self, key, value ) :
    dict.__setitem__ ( self, key, value )
    ##self.Modified = True
    # Pass the modify flag to the parent
    self.Parent._Set_Modified ( self.PIndex, value, key )
    if ( 'TIO-Write' in Debug_What ) :
      self._Log ( 'Write:', key, '=', value )

  # Override, because we want to log during debug
  def __getitem__ ( self, key ) :
    value = dict.__getitem__ ( self, key )
    if ( 'TIO-Read' in Debug_What ) :
      self._Log ( 'Read: ', key, '=', value )
    return value
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class NoCase_List ( list ) :
  """
  Case Insensitive List :
  The methods "sort" and "index" are case insensitive.
  The "in" operator works also case insensitive.
  After the list is sorted once,
  appending a new item keeps the list sorted.
  """
  def __init__ ( self, *args, **kwargs ):
    self.Sorted = False
    list.__init__ ( self )
    if len ( args ) == 0 :
      return
    if isinstance ( args[0], list ) :
      for item in args [0] :
        self.append ( item )
    else :
      self.append ( args[0] )

  def append ( self, value ) :
    list.append ( self, value )
    if self.Sorted :
      self.sort ()

  def sort ( self, *args, **kwargs ) :
    self.Sorted = True
    def _sort ( a, b ) :
      if isinstance ( a, basestring ) :
        return cmp ( a.lower(), b.lower() )
      else :
        return cmp ( a, b )
    return list.sort ( self, _sort )

  def index ( self, value ) :
    if isinstance ( value, basestring ) :
      value = value.lower()
      for i, item in enumerate ( self ) :
        if item.lower() == value :
          return i
      else :
        return -1
    else :
      for i, item in enumerate ( self ) :
        if item == value :
          return i
      else :
        return -1


  def __contains__ ( self, value ) :
    return self.index ( value ) >= 0
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class NoCase_Dict ( dict ) :
  """
Dictionair with
  - Case Insensitive keys and attributes
    ( the case of the first use is stored )
  - Attributes and Keys are the same
So the following are all equal:
  My_Dict [ 'Beer' ] = 44
  My_Dict [ 'BEER' ] = 44
  My_Dict.Beer = 44
  My_Dict.BEER = 44

NOT COMPLETELEY FINISHED
  """
  # *********************************************************
  def __init__ ( self, *args, **kwargs ):
    dict.__init__ ( self, *args, **kwargs )
    ## The next statement is not allowed, because it Calls __setattr__ !!
    ##self.has_key = self.__contains__

  # *********************************************************
  def __call__ ( self, key ) :
    return self [ key ]

  # *********************************************************
  def __repr__ ( self ) :
    Keys = []
    for Key in list(self.keys()) :
      Keys.append ( Key.lower () )
    Keys.sort ()
    Line = ''
    for Key in Keys :
      if Key != '__builtins__':
        Key = self.Get_CaseName ( Key )
        Line += u'%-30s  = %s\n'% ( _2U ( Key ), _2U ( self [ Key ] ) )
    return Line

  # *********************************************************
  def __str__ ( self ) :
    try :
      Line = dict.__str__ ( self )
    except :
      Line = 'ERROR: str(NoCase_Dict )'
    return Line

  # *********************************************************
  def Copy ( self ) :
    from copy import copy
    return NoCase_Dict ( copy ( dict ( self ) ) )

  # *********************************************************
  def Compare ( self, Other ) :
    """
Compares two dictionaires (which should have equal keys)
Returns True if all key-value pairs are equal.
    """
    for key in list(self.keys ()) :
      if key.lower() != Other[key] :
        return False
    return True

  # *********************************************************
  def Compare_And_Equal ( self, Other ) :
    """
Compares two dictionaires (which should have equal keys)
Returns True if all key-value pairs are equal.
After the comparison, the Other dictionair is made equal.
This is very handy, in case you want to track modifications.
    """
    for key in list(self.keys ()) :
      if Other[key] != self.__getitem__ ( key ) :
        break
    else:
      return True

    # Make key-values of Other equal to myself
    for key in list(self.keys ()) :
      Other [ key ] = self.__getitem__ ( key )
    return False

  # *********************************************************
  def has_key ( self, Key ) :
    return self.__contains__ ( Key )

  # *********************************************************
  def Get_CaseName ( self, Key ) :
    if isinstance ( Key, basestring ) :
      Key = Key.lower ()
      for key in list(self.keys ()) :
        if key.lower() == Key :
          return key
      return False
    return Key

  # *********************************************************
  def __contains__ ( self, Key ) :
    if isinstance ( Key, basestring ) :
      Key = Key.lower ()
      for key in list(self.keys ()) :
        if isinstance(key, basestring):
          if key.lower() == Key :## Dit kunnen ook andere objecten zijn die geen 'lower' functie hebben
            return True
        else:
          if key == Key:
            return True
      return False
    return dict.has_key ( self, Key )

  # *********************************************************
  def __getitem__ ( self, Key ) :
    if isinstance ( Key, basestring ) :
      Key = Key.lower ()
      for key in list(self.keys ()) :
        ## it might be possible that Key is "123", so a string
        ## but that the key is an integer 123
        ## so always convert to string

        ## 28-3-2013 modified
        #if str(key).lower() == Key :
        #  return dict.__getitem__ ( self, key )

        if isinstance ( key, basestring ) :
          if key.lower() == Key :
            return dict.__getitem__ ( self, key )
        elif str(key) == Key :
          return dict.__getitem__ ( self, key )

      return None
    if dict.has_key ( self, Key ) :
      return dict.__getitem__ ( self, Key )
    else :
      return None

  # *********************************************************
  # always called instead of the normal mechanism
  # *********************************************************
  def __setattr__ ( self, attr, value ) :
    """
So here attributes are handled as keys
    """
    Key = attr.lower ()
    for key in list(self.keys ()) :
      if key.lower() == Key :
        dict.__setitem__ ( self, key, value )
        return
    else :
      dict.__setitem__ ( self, attr, value )

  # *********************************************************
  # only called when not found with the normal mechanism
  # *********************************************************
  def __getattr__ ( self, attr ) :
    """
So here attributes are handled as keys
    """
    if attr == '__getstate__' :
      raise AttributeError ( "otherwise problems with Pickle" )
    return self.__getitem__ ( attr )

  # *********************************************************
  # always called
  # *********************************************************
  def __delattr__ ( self, attr ) :
    #print 'DELETTTE', attr
    Key = attr.lower ()
    for key in list(self.keys ()) :
      #print '::::',Key, key
      if key.lower() == Key :
        dict.__delitem__ ( self, key )
        return
    else :
      dict.__delattr__ ( self, attr )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def flatten ( *args ) :
  for x in args :
    if hasattr ( x, '__iter__' ) :
      for y in flatten ( *x ) :
        yield y
    else:
      yield x
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Dict_Col_Data ( Data, Col_Name, Ignores = NoCase_List() ) :
  """
Fetches a column form a List of NoCase_Dict.

Data     = List of NoCase_Dict
Col_Name = the name of the column to fetch data from
Ignores  = values that will be ignored
           (Case-insensitive, if Ignores oa a NoCase_List)
  """
  Result = NoCase_List ()
  for Row in Data :
    Col_Data = eval ( 'Row.' + Col_Name )
    if not ( Col_Data in Ignores ) :
      Result.append ( Col_Data )
  Result.sort ()
  return Result
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def Sort_Dict ( Data, Col_Name, Reverse = False, Ignores = NoCase_List() ) :
  Org_Col_Data = Get_Dict_Col_Data ( Data, Col_Name, Ignores )

  # Er kunnen dubbel in voorkomen
  Col_Data = NoCase_List ()
  for ColName in Org_Col_Data :
    if not ( ColName in Col_Data ) :
      Col_Data.append ( ColName )

  if Reverse :
    Col_Data.reverse ()
  New = []
  for Name in Col_Data :
    New_Rows = Find_Dict_All_Row_Data ( Data, Col_Name, Name )
    #New.append ( New_Row )
    for Row in New_Rows :
      New.append ( Row )
  return New
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Find_Dict_All_Row_Data ( Data, Col_Name, Col_Value ) :
  """
Fetches all the ROWs form a List of NoCase_Dict,
always a list of Rows is returned
where the Value in column Col_Name equals Col_Value.

Data      = List of NoCase_Dict
Col_Name  = the name of the column where to search for the Col_Value
Col_Value = the text to search
  """
  Result = []
  for Row in Data :
    Col_Data = eval ( 'Row.' + Col_Name )
    if Col_Data == Col_Value :
      Result.append ( Row )
  return Result
# ***********************************************************************



# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':

  from General_Globals import Test, Test_Defs

  Test_Defs ( 7 )

  # **********************************
  # **********************************
  if Test ( 1 ) :
    a = [2,3,(3,4,'strif','sdas',50.,4.5),[45.,89,'stri'],(5)]
    Type_Enumerate ( a  )

  # **********************************
  # TIO_Dictionary test
  # **********************************
  if Test ( 2 ) :
    class tParent ( object ):
      def __init__ ( self ) :
        pass
      def _Set_Modified ( self, PIndex, value, key ) :
        pass
    TIO_Parent = tParent ()

    Application.Debug_Mode = True
    TIO = TIO_Dict ( TIO_Parent, 1 ) ;
    TIO [ 'aap'] = 'beer'
    TIO [ 'aap'] = 'beer'
    TIO [ 33 ]   = 44
    for item in TIO :
      a = TIO [ item ]

  # **********************************
  # **********************************
  if Test ( 3 ) :
    SD = super_dict ()
    SD [ 'aap' ] = 44
    SD [ 44    ] = 33
    SD.type = 'aap'
    print(SD, dir ( SD ), SD.type)

    SD = super_object ()
    SD.aap = 44
    SD.type = 'aap'
    print(SD, dir ( SD ), SD.type)
    print(SD.Get ( 'aap', 684 ), SD.Get ( 'beer', 685))

  # **********************************
  # t_signal_attr
  # **********************************
  if Test ( 4 ) :
    signal_attr = t_signal_attr ()
    signal_attr.Color = 'Color'
    v3print ( signal_attr.Color )
    v3print ( signal_attr.Not_Existing )

    for item in dir() :
      if item[0].isupper () :
        print(item, type ( eval ( item ) ),eval(item))
    print(type(WRAP))

  # **********************************
  # NoCase List
  # **********************************
  if Test ( 5 ) :
    #My_List = NoCase_List ( 'coala', 'donky' )
    My_List = NoCase_List ( 'coala' )
    #My_List = [ 'coala', 'donky' ]
    #My_List = NoCase_List ( My_List )
    My_List.append ( 'Aap' )
    My_List.append ( 'aapje' )
    My_List.append ( 'beerthe' )
    My_List.append ( 'BEER' )
    print(My_List)
    My_List.sort ()
    print(My_List)
    My_List.append ( 'aapJ' )
    print(My_List)
    print(My_List.index ( 'beer' ))
    print('beer' in My_List)
    print('beert' in My_List)

  # **********************************
  # NoCase Dict
  # **********************************
  if Test ( 6 ) :
    My_Dict = NoCase_Dict ( { 'Coala':33, 'BEEr': 44 } )
    print(list(My_Dict.keys()))
    print('beer' in My_Dict)
    print(My_Dict [ 'BEEr' ])
    print(My_Dict [ 'beer' ])
    print(My_Dict [ 'beser' ])

    aap = My_Dict.Copy ()
    My_Dict.bEEr= 5678
    print(My_Dict)
    print(aap)
    print(My_Dict.bEEr)
    print(aap.bEeR)

    My_Dict.Aap= 'beer'
    print(My_Dict)

    My_Dict [2] = 'aap'
    print(2 in My_Dict, 3 in My_Dict)
    print(2 in My_Dict, 3 in My_Dict)

  # **********************************
  # **********************************
  if Test ( 7 ) :
    a = [2,3,(3,[4,5],'strif','sdas',50.,4.5),[45.,89,'stri'],(5)]
    for item in flatten ( a ) :
      print(item)

# ***********************************************************************
#pd_Module ( __file__ )

