# -*- coding: windows-1252 -*-
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from builtins import chr
from builtins import str
from past.builtins import basestring
import __init__
import sys

import _io
file = _io.TextIOWrapper

"""
import sys
sys.setdefaultencoding ( 'windows-1252' )
print sys.getdefaultencoding()

import sys, locale
print 'piep'
reload(sys)
print 'piep'
print 'Locale', locale.getdefaultlocale(),locale.getlocale(),locale.getpreferredencoding()
sys.setdefaultencoding(locale.getdefaultlocale()[1])

#sys.setdefaultencoding ( 'windows-1252' )
aap = unicode
def unicode ( line , encoding = 'windows-1252') :
  return aap ( line, encoding )
"""


# ***********************************************************************
# ***********************************************************************
My_Codec = 'Windows-1252'
def Win_Unicode ( line ) :
  """
  Translates a windows string with coding windows-1252,
  to a unicode string.
  If the input is already a unicode, it's returned without translation.
  """
  if isinstance ( line, str ) :
    return line
  '''
  print 'GGGG',type(line), line
  for kar in line :
    print ord(kar),
  print
  '''
  return str ( line, My_Codec )
# ***********************************************************************
def Win_String ( line ) :
  if isinstance ( line, str ) :
    return line
  return line.encode ( My_Codec )





# ************************************************************************
# ************************************************************************
def remove_diacritic ( input ) :
  '''
Accept a unicode string, and return a normal string (bytes in Python 3)
without any diacritical marks.
Remove diacritical marks from strings containing characters from any
latin alphabets.

Tested on both Python 2.x and Python 3.x
## {{{ http://code.activestate.com/recipes/576648/ (r7)
  '''
  import unicodedata
  return unicodedata.normalize('NFKD', input).encode('ASCII', 'ignore')
# ************************************************************************


# ************************************************************************
# ************************************************************************
#def Remove_Accents ( input ) :
#  if isinstance ( input, str) or sys.hexversion >= 0x3000000:
#    # On Python >= 3.0.0
#    return remove_diacritic ( input ).decode()
#  else:
#    # On Python < 3.0.0
#    return remove_diacritic ( str ( input, 'ISO-8859-1' ))
import unicodedata
def Remove_Accents(txt):
    """This method removes all diacritic marks from the given string"""
    #txt = 'aap'
    #print ( type(txt), txt[:5])
    #if not isinstance ( txt, unicode ) :
#    if not isinstance ( txt, unicode ) :
#      #print ('convert')
#      try :
#        #print ( '1252')
#        txt = unicode ( txt, 'windows-1252' )
#      except :
#        try:
#          #print ( 'utf-8' )
#          txt = unicode ( txt, 'utf-8' )
#        except :
#          #print ( 'kaal')
#          txt = unicode ( txt )
    #txt = unicode ( txt )
    ##print (type(txt),txt)
    norm_txt = unicodedata.normalize ( 'NFD', txt )
    #print
    shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))
    return unicodedata.normalize('NFC', shaved)
# ************************************************************************



# ************************************************************************
# ************************************************************************
def Sanitize_Filename ( Filename ) :
  Filename = Filename.replace ( ' ', '_' )
  Filename = Filename.replace ( '-', '_' )
  Filename = Filename.replace ( '+', '_plus' )
  Filename = Remove_Accents ( Filename )
  return Filename
# ************************************************************************



# ***********************************************************************
# ***********************************************************************
def str2u ( line ) :
  if isinstance ( line, str ) :
    return line
  return str ( line, My_Codec )
"""
def u2str ( line ) :
  if isinstance ( line, unicode ) :
    return line.encode ( My_Codec )
  else :
    return line
"""


# ***********************************************************************
# ****************************************************************
def _2U ( Value ) :
  """
Make an unicode string of everything.
If the input is a string, codes in the following order are applied
  - Windows-1252
  - utf-8
  """
  """  FOR PYTHON # ALL IS UNICODE
  if isinstance ( Value, str ) :
    try :
      Value = str ( Value, 'Windows-1252' )
    except :
      Value = str ( Value, 'utf-8' )
  elif not ( isinstance ( Value, basestring ) ) :
    Value = str ( Value)
  """
  return Value
# ****************************************************************


# ***********************************************************************
# ***********************************************************************
class Read_Text_File ( file ) :
  """
  Wraps the standard file input, like open / file.
  """
  def __init__ ( self, filename ) :
    file.__init__ ( self, filename, 'r' )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Write_Text_File ( file ) :
  """
  Wraps the standard file output, like open / file.
  Improvements :
    - if unicode string is specified, automatic encoding
  Extensions :
    - writeln (adds an '\n' to each write statement )
  """
  def __init__ ( self, filename ) :
    file.__init__ ( self, filename, 'w' )

  def write ( self, line ) :
    if isinstance ( line, str ) :
      line = line.encode ( 'windows-1252' )
    file.write ( self, line )

  def writeln ( self, line ) :
    if isinstance ( line, str ) :
      line = line.encode ( 'windows-1252' )
    file.write ( self, line + '\n' )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == '__main__':
  #input = str ( 'wav_cliënt-kort', 'windows-1252' )
  #input = str ( 'wav_client-kort', 'windows-1252' )
  #input = str ( 'wav_client-kort', 'utf-8' )
  input = unicode ( 'wav_cliënt-kort', 'utf-8' )
  print(input)

  print ( remove_diacritic ( input ))

  Text = 'bbe�r'
  print ( '1a-', type (Text), Text )
  Tokens = Remove_Accents ( Text )
  print ( '2a-', type ( Tokens ), Tokens )
  exit()


  print(Santinize_Filename ( input ))
  exit()

  print('===== in the first or second line of the file, we need')
  print('      # -*- coding: windows-1252 -*-')
  print('===== to be able to use special characters like é, ö')
  print()


  def PCs ( line ) :
    print(line, type(line), '    ', end=' ')
    for kar in line :
      print(ord ( kar ), end=' ')
    print()

  my_s = 'my_string'
  my_u = u'my_unicode'
  my_S = 'my_string+asc>127 ' + chr ( 243 ) + 'óö'
  print('===== Create some different string types')
  print('      my_s :', type(my_s), my_s)
  print('      my_u :', type(my_u), my_u)
  print('      my_S :', type(my_S), my_S, str(my_S,'windows-1252'))
  print()

  print('===== UNICODE can''t contain byte values > 127')
  print('      my_u = my_u + chr (246)')
  print('===== So we have to encode the special character')
  print("      my_u = my_u + unicode ( ' ö', 'windows-1252' )")
  my_u = my_u + str ( ' ö', 'windows-1252' )
  print('      my_u :', type(my_u), my_u)
  print()

  #fh = open ( 'test_write_strings.py', 'w' )
  fh = Write_Text_File ( 'test_write_strings.py' )
  print('===== writing to a file, unicode must ALWAYS be encoded !!')
  fh.writeln ( my_s )
  fh.writeln ( my_S )
  print("      fh.write ( my_u.encode('windows-1252') )")
  #fh.write ( my_u.encode('windows-1252') + '\n' )
  fh.writeln ( my_u )
  fh.close ()

  print('===== read file back')
  fh = open ( 'test_write_strings.py', 'r' )
  lines = fh.readlines ()
  fh.close ()
  for line in lines :
    print('      file:', line[:-1])


  fh = Read_Text_File ( 'test_write_strings.py' )
  lines = fh.readlines ()
  fh.close ()
  for line in lines :
    print('      file:', line[:-1])


  my_u = my_u + str('ó','windows-1252')
  print('      my_u :', type(my_u), my_u)

  """
  PCs ( my_s )
  PCs ( my_u )
  PCs ( my_S )

  print my_s, my_u, my_w

  s_u = my_s + my_u
  s_w = my_s + my_w
  print s_u, s_w

  # String + Unicode ==> Unicode
  x = my_s + my_u
  print type(x), x

  # FOUT:
  u_w = my_u + my_w
  print u_w

  # OK, translate everything to string
  u_W = str ( my_u ) + my_w
  print u_W

  # OK, translate everything to unicode with correct encoding
  U_w = my_u + unicode ( my_w, 'windows-1252' )
  print U_w
  """



