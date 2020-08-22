from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import range
from past.builtins import basestring
from builtins import object
from past.utils import old_div
import __init__
import sys


# ***********************************************************************
__doc__ = """
"""
# ***********************************************************************


# ***********************************************************************
_Version_Text = [

[ 2.12 , '9-8-2013', 'Stef Mientki',
'Test Conditions:', (2,),"""
- Delphi_Date.from_Browser added
"""],

[ 2.11 , '18-04-2013', 'Stef Mientki',
'Test Conditions:', (2,),"""
- Delphi_Date: Access time with micro-seconds added
"""],

[ 2.10 , '11-04-2013', 'Stef Mientki',
'Test Conditions:', (2,),"""
- Delphi_Date didn't detect time component in MS Access string
"""],

[ 2.9 , '23-02-2013', 'Stef Mientki',
'Test Conditions:', (2,),"""
- Delphi_Date extended to accept HL7 format "20111229171200"
"""],

[ 2.8 , '10-02-2013', 'Stef Mientki',
'Test Conditions:', (2,),"""
- SQL_Date ( = Delphi_Date.from_SQL ) added
- Delphi_Date.from_SQL                added
- Delphi_Date.to_SQL                  added
"""],

[ 2.7 , '04-04-2012', 'Stef Mientki',
'Test Conditions:', (2,),"""
- Delphi_Date can handle teveel voorloop nullen
"""],

[ 2.6 , '12-02-2012', 'Stef Mientki',
'Test Conditions:', (2,),"""
- Delphi_Date can handle RFC2822 datetime strings
- Some string inputs, were converted wrong, so that time became 00:00
"""],

[ 2.5 , '03-10-2011', 'Stef Mientki',
'Test Conditions:', (2,),"""
- Delphi_Date.to_Month  added
"""],

[ 2.4 , '02-09-2011', 'Stef Mientki',
'Test Conditions:', (2,),"""
- If input of datetime is a string, it's stripped before analyzing,
  so now also a date with an EOL will be processed correctly
"""],

[ 2.3 , '02-07-2011', 'Stef Mientki',
'Test Conditions:', (2,),"""
- to_datetime deed een onterechte rounding,
  waardoor 40600.6 in to_String een dag te ver kwam
"""],

[ 2.2 , '22-06-2011', 'Stef Mientki',
'Test Conditions:', (2,),"""
- to_datetime didn't account for the day fraction
"""],

[ 2.1 , '19-06-2011', 'Stef Mientki',
'Test Conditions:', (2,),"""
- Delphi_Date ( large integer / large integer string ) went wrong
"""],

[ 2.0 , '19-05-2011', 'Stef Mientki',
'Test Conditions:', (2,),"""
********************************************************
- Totally changed, including names !!!!!
- All use the class Delphi_Date
********************************************************
"""],

[ 1.3 , '02-05-2011', 'Stef Mientki',
'Test Conditions:', (2,),"""
- translating from float-date to int-date was done by truncation
  therefor some days were displayed as one-day-before
"""],

[ 1.2 , '09-09-2010', 'Stef Mientki',
'Test Conditions:', (2,),"""
- added Delphi_Now
"""],

[ 1.1 , '09-04-2010', 'Stef Mientki',
'Test Conditions:', (2,),"""
"""],

[ 1.0 , '17-06-2009', 'Stef Mientki',
'Test Conditions:', (2,),
' - orginal release' ]
]
# ***********************************************************************

from   General_Globals  import Test, Test_Defs
import time
import datetime
from   email.utils      import parsedate_tz, mktime_tz
try :
  import wx
except :
  pass
##from   track_support    import _Track_Methods, Track_Class

Month_Ends = {}
Month_Ends [ 'januari'   ] = '31-01-'
Month_Ends [ 'februari'  ] = '28-02-'
Month_Ends [ 'maart'     ] = '31-03-'
Month_Ends [ 'april'     ] = '30-04-'
Month_Ends [ 'mei'       ] = '31-05-'
Month_Ends [ 'juni'      ] = '30-06-'
Month_Ends [ 'juli'      ] = '31-07-'
Month_Ends [ 'augustus'  ] = '31-08-'
Month_Ends [ 'september' ] = '30-09-'
Month_Ends [ 'oktober'   ] = '31-10-'
Month_Ends [ 'november'  ] = '30-11-'
Month_Ends [ 'december'  ] = '31-12-'

# Delphi Date is defined as the number of days since 30-12-1899
# so we set Delphi_Date_0 to the ordinal value of the Python Date
#Delphi_Date_0 = date ( *strptime ( '30-12-1899', '%d-%m-%Y' )[0:3]).toordinal()
Delphi_Date_0_DT = datetime.date ( *time.strptime ( '30-12-1899', '%d-%m-%Y' )[0:3])
Delphi_Date_0    = Delphi_Date_0_DT.toordinal()
Date_Ord_Now  = datetime.datetime.now().toordinal()



# ************************************************************************
# ************************************************************************
##__start_time = time_orginal.time ()
__start_time = time.time ()
def ptime ( line = '' ) :
  global __start_time
  old = __start_time
  __start_time = time.time()
  print('TIME (ms): ',int ( 1000 * ( __start_time - old )), line)
# ************************************************************************


def _datetime_2_Delphi ( Something ) :
  Value = Something.toordinal() - Delphi_Date_0
  try :
    Fraction = Something.time()
    h = Fraction.hour
    m = Fraction.minute
    s = Fraction.second
    Day_Fraction = old_div(( s + 60 * ( m + ( 60 * h ) ) ), 86400.0)
    Value += Day_Fraction
  except :
    pass
  return Value


# ************************************************************************
# ************************************************************************
"""
class Delphi_Date ( Track_Class, float ) :
  def __init__ ( self, Something = -2 ) :
    self.aap = 'aapje',Something
    print '===', Something
    Track_Class.__init__( self, __file__ )
  def __new__ ( self, Something = -2 ) : ##None ) :
    self.___Args = ( Something )
"""

class Delphi_Date ( float ) :
  def __new__ ( self, Something = -2 ) : ##None ) :

    """
Class meant to handle any datetime type, and converts it basically to
a Delphi DateTime (float: number of days since 1-1-1900).

The input can be one of the following types :
  - empty                  : the current date-time is used
  - 30000.9                : float,   Delphi datetime
  - 30000                  : integer, Delphi datetime
  - "30000.9"              : string,  Delphi datetime
  - "30000,9"              : string,  Delphi datetime (Dutch string)
  - "20-5-11"              : string,  short year notation
  - "20-05-2011"           : string,  long year notation
  - "2009-09-24 10:12:24"  : string,  MS Access string
  - "20111229171200"       : string,  as used in HL7
  - datetime.datetime ( 2011, 1, 15 )
  - time.time ()           : large float
  - time.struct_time       :
  - wx.DateTime            :
  - "Mon, 20 Nov 1995 19:12:08 -0500" : RFC2822 datetime as used in emails

The following output methods are available
  - to_time ()
  - to_datetime ()
  - to_String ( self , Format = "%d-%m-%Y" )
  - to_String_Short ()
  - to_String_Date_Time_Short ()
  - to_String_Time_Short ()
  - to_String_Date_Time ()
  - to_wxTime ()
  - to_Iso ()
    """
    if Something == None :
      return float.__new__ ( self, -2 )


    # The current date-time is used, if no parameter is specified
    ##if Something is None :
    if Something is -2 :
      Something = datetime.datetime.now ()

    # floating point is assumed to be a Delphi datetime
    # if it's too large, a time.time() is assumed
    if isinstance ( Something, float ) :
      # if input is coming from time.time, it's very large
      if Something < 73000 :
        Value = Something
      else :
        #Value = datetime.datetime.fromtimestamp (
        #          Something).toordinal() - Delphi_Date_0
        Value = datetime.datetime.fromtimestamp ( Something )
        Value = _datetime_2_Delphi ( Value )


    # sometimes a Delphi datetime is stored as an integer
    elif isinstance ( Something, int ) :
      # if input is coming from int ( time.time ) or PHP,
      # it's very large
      if Something < 73000 :
        Value = Something
      else :
        #Value = datetime.datetime.fromtimestamp (
        #          Something).toordinal() - Delphi_Date_0
        Value = datetime.datetime.fromtimestamp ( Something )
        Value = _datetime_2_Delphi ( Value )

    # A string can represent a lot of things
    elif isinstance ( Something, basestring ) :
      Something = Something.strip ()
      ##if Something.strip () == '' :
      if Something == '' :
        #return ''
        return float.__new__ ( self, -1 )

      # string used in HL7
      # this must be tested before trying to convert to a float/int
      try :
        # HL7-string: '20111229171200'
        Value = datetime.datetime.strptime( Something,'%Y%m%d%H%M%S')
        Value = _datetime_2_Delphi ( Value )
      except :
        # HL7-string: '20111231122529.363'
        try :
          Value = datetime.datetime.strptime( Something,'%Y%m%d%H%M%S.%f')
          Value = _datetime_2_Delphi ( Value )
        except :

          ##print '+++++', Something, type(Something) ##, Value

          # a float or integer,
          # also the Dutch notation where decimal separator is a comma
          try :
            Something = float ( Something.replace(',','.') )
            # if input is coming from int ( time.time ) or PHP,
            # it's very large
            if Something < 73000 :
              Value = Something
            else :
              #Value = datetime.datetime.fromtimestamp (
              #          Something).toordinal() - Delphi_Date_0
              Value = datetime.datetime.fromtimestamp ( Something )
              Value = _datetime_2_Delphi ( Value )
          except :

            # a string as a short year notation
            try :
              Value = datetime.datetime.strptime ( Something, '%d-%m-%y' )
            except ValueError :

              # a string as a long year notation
              try:
                Value = datetime.datetime.strptime ( Something, '%d-%m-%Y' )
              except :

                try :  # string   YEAR  MONTH
                  Value = datetime.datetime.strptime ( Something, '%Y %m' )
                except :
                  #try : # string   YEAR
                  #  Value = datetime.datetime.strptime ( Something, '%Y' )
                  #except :

                  # a string as a (Dutch) Access notation
                  try :
                    # Access string : "2009-09-24 00:00:00"
                    Value =  datetime.datetime.strptime ( Something, "%Y-%m-%d %H:%M:%S" )
                    ##Value =  datetime.datetime.strptime ( Something.split(' ')[0], "%Y-%m-%d" )
                  except :
                   try:
                    # Access string with microseconds : "2009-09-24 00:00:00.454"
                    Value =  datetime.datetime.strptime ( Something, "%Y-%m-%d %H:%M:%S.%f" )
                   except:

                    try :
                      # remove all spaces
                      Something2 = Something.replace ( ' ', '' )
                      Value = datetime.datetime.strptime ( Something2, '%d-%m-%Y' )
                    except :

                      # Datum (zonder tijd) met teveel voorloop nullen
                      try :
                        Something2 = Something.replace ( ' ', '' )
                        Val = Something2.split ( '-' )
                        if len ( Val ) != 3                   : raise error ('voorloopnul')
                        Dag = int ( Val [0] )
                        if ( Dag < 1 ) or ( Dag > 31 )        : raise error ('voorloopnul')
                        Maand = int ( Val [1] )
                        if ( Maand < 1 ) or ( Maand > 12 )    : raise error ('voorloopnul')
                        Jaar = int ( Val [2] )
                        if ( Jaar < 1900 ) or ( Jaar > 2050 ) : raise error ('voorloopnul')
                        Something2 = '%s-%s-%s' % ( Dag, Maand, Jaar )
                        Value = datetime.datetime.strptime ( Something2, '%d-%m-%Y' )
                      except :

                        try :
                          Value = datetime.datetime.utcfromtimestamp (
                                    mktime_tz ( parsedate_tz ( Something )))
                          #print 'XDXDXD', Value  #, self.to_String_Date_Time_Short()
                        except :

                          print('=====  impossible date  =====', Something)
                          Value = Delphi_Date_0_DT
                          import traceback
                          traceback.print_exc ()

            ## DIT WAS FOUT
            ##Value = Value.toordinal() - Delphi_Date_0
            Value = _datetime_2_Delphi ( Value )

    # datetime.datetime ()
    elif isinstance ( Something, datetime.datetime ) :
      # with toordinal, day fraction is lost
      """
      Value = Something.toordinal() - Delphi_Date_0
      Fraction = Something.time()
      h = Fraction.hour
      m = Fraction.minute
      s = Fraction.second
      Day_Fraction = ( s + 60 * ( m + ( 60 * h ) ) ) / 86400.0
      Value += Day_Fraction
      """
      Value = _datetime_2_Delphi ( Something )

    # time.struct_time
    elif isinstance ( Something, time.struct_time ) :
      Value = time.mktime ( Something )
      DT = datetime.datetime.fromtimestamp ( Value )
      Value = DT.toordinal() - Delphi_Date_0

    else :
      try :
        # wx.DateTime
        if isinstance ( Something, wx.DateTime ) :
          DT = datetime.date ( Something.GetYear (),
                               Something.GetMonth () + 1,
                               Something.GetDay () )
          Value = DT.toordinal() - Delphi_Date_0
      except :
        print(type(Something), Something)
        raise error ( 'aap' )

    return float.__new__ ( self, Value )

  @classmethod
  def from_Browser ( cls, Something = -2 ) :
    return cls ( datetime.datetime.fromtimestamp ( int(Something )))

  # SQL server dates start 2 days later !!!
  # SQL Server = 40871.431264506
  # Delphi     = 40873.4333729861
  @classmethod
  def from_SQL ( cls, Something = -2 ) :
    return cls ( Something + 2 )

  def to_SQL ( self ) :
    return float ( self ) - 2

  def to_time ( self ):
    return time.mktime ( self.to_datetime().timetuple() )

  def to_datetime ( self ) :
    #return datetime.datetime.fromordinal ( int ( round ( self + Delphi_Date_0 )))
    #DT = datetime.datetime.fromordinal ( self + Delphi_Date_0 )
    ##DT = datetime.datetime.fromordinal ( int (round ( self + Delphi_Date_0 )))
    DT = datetime.datetime.fromordinal ( int ( self + Delphi_Date_0 ))
    Fraction = self % 1
    Fraction = datetime.timedelta ( Fraction )
    DT = DT + Fraction
    return DT
    ##return datetime.datetime.fromordinal ( self + Delphi_Date_0 )
    #return datetime.datetime.fromordinal ( int ( self + 0.001 )  + Delphi_Date_0 )

  """
  def WEG__str__ ( self, Format = "%d-%m-%Y"  ) :
    if self < 0 :
      return ''
    DT = self.to_datetime()
    try :
      return DT.strftime ( Format )
    except :
      return '01-01-1900'
  """

  def __bool__ ( self ) :
    """
Used in boolean evaluations,
return False for negative numbers,
so only valid dates will return True.
    """
    if self < 0 :
      return False
    else :
      return True

  def __str__ ( self ) :
    if self < 0 :
      return ''
    else :
      return float.__str__ ( self )

  def __repr__ ( self ) :
    return self.__str__()

  def __unicode__ ( self ) :
    return self.__str__()

  def to_String ( self , Format = "%d-%m-%Y" ) :
    if self < 0 :
      return ''
    DT = self.to_datetime()
    #Fraction = self % 1
    #Fraction = datetime.timedelta ( Fraction )
    #DT = DT + Fraction
    try :
      return DT.strftime ( Format )
    except :
      return '01-01-1900'

  def to_String_Short ( self ) :
    DT = self.to_datetime()
    return DT.strftime ( "%d-%m-%y" )

  def to_Filename ( self ) :
    return self.to_String ( "%d-%m-%Y %H-%M" )

  def to_String_Date_Time_Short ( self ) :
    return self.to_String ( "%d-%m-%Y %H:%M" )

  def to_String_Time_Short ( self ) :
    return self.to_String ( "%H:%M" )

  def to_String_Date_Time ( self ) :
    return self.to_String ( "%d-%m-%Y %H:%M:%S" )

  def to_wxTime( self ) :
   DT = self.to_datetime()
   WX = wx.DateTime()
   WX.Set ( DT.day, DT.month-1, DT.year )
   return WX

  def to_int ( self ) :
    # prevent that a float just below an integer,
    # will result in the previous day
    return int ( self + 0.001 )

  def to_Iso ( self ) :
    """
Transforms a Delphi Datetime into an ISO tuple: ( year, week, day-of-week )
    """
    return self.to_datetime().isocalendar ()

  def to_Month ( self ) :
    """
like to_ISO, but return ( year, month, day )
    """
    DT = self.to_datetime ()
    return DT.year, DT.month, DT.day

  def Get_First_Week_In_Month ( self ) :
    DT = self.to_datetime ()
    First_Day = datetime.date ( DT.year, DT.month, 1 )
    return First_Day.isocalendar () [1]
# ************************************************************************
SQL_Date = Delphi_Date.from_SQL


# ************************************************************************
# ************************************************************************
def NWeek_Year ( Year ) :
  """
Determines the number of weeks in the Year
  """
  Day = 31
  Lastweek = 1
  while Lastweek == 1 :
    Lastweek = datetime.date ( Year, 12, Day ).isocalendar()[1]
    Day -= 1
  return Lastweek
# ************************************************************************



# ************************************************************************
# ************************************************************************
class Week_List ( object ) :
  def __init__ ( self, Delphi_Start, NWeeks ) :
    self.Delphi_Start = Delphi_Date ( Delphi_Start )
    NYear        = old_div(NWeeks, 52)

    Start_Iso = self.Delphi_Start.to_Iso ()
    Year, Week, DayofWeek = Start_Iso
    #print 'DOW',DayofWeek, self.Delphi_Start.to_String ()

    ## Set Delphi_start to Wednesday
    self.Delphi_Start = Delphi_Date ( self.Delphi_Start - ( DayofWeek - 3 ) )

    self.Weeks = list ( range ( Week, NWeek_Year ( Year )+1 ) )
    self.Weeks_Years = []
    Year_Str = str ( Year ) [ -2: ]
    for Week in self.Weeks:
      self.Weeks_Years.append ( str ( Week ) + '\n.' + Year_Str )

    Year += 1
    while len ( self.Weeks ) <  ( NYear - 1 )* 52 :
      self.Weeks += list ( range ( 1, NWeek_Year ( Year )+1 ) )
      Year_Str = str ( Year ) [ -2: ]
      for Week in self.Weeks [ -NWeek_Year ( Year ): ]:
        self.Weeks_Years.append ( str ( Week ) + '\n.' + Year_Str )
      Year += 1

    # als er te weinig zijn, resterende weken toevoegen
    N = NWeeks - len ( self.Weeks )
    self.Weeks += list ( range ( 1, N + 1 ) )
    Year_Str = str ( Year ) [ -2: ]
    for Week in self.Weeks [ -N: ]:
      self.Weeks_Years.append ( str ( Week ) + '\n.' + Year_Str )

  def Delphi_Index ( self, Date ) :
    Index = old_div(( int ( Date + 0.001 ) - self.Delphi_Start.to_int() + 3 ), 7)
    if 0 <= Index < len ( self.Weeks ) :
      return Index

  def Date_from_Index ( self, Index ) :
    Date = self.Delphi_Start + 7 * Index
    return Date
# ************************************************************************


# ************************************************************************
# ************************************************************************
def Year_Week_List ( Year = None ) :
  # use the current year, if not specified
  if not ( Year ) :
    Year = Delphi_Date ().to_Iso()[0]

  ## determine the start of the first week in the selected year
  Begin_First_Week = Delphi_Date ( datetime.datetime ( Year, 1, 1 ) )
  while Begin_First_Week.to_Iso()[0] < Year :
    Begin_First_Week = Delphi_Date ( Begin_First_Week + 1 )

  Result = []
  Current_Year, Current_Week, Current_Day = Delphi_Date().to_Iso ()
  if Year == Current_Year :
    ## WL geeft een lijst van WOENSDAGEN
    WL = Week_List ( Begin_First_Week, Current_Week )
    for i in range ( Current_Week + 1 ) :
      Result.append ( Delphi_Date ( Delphi_Date ( WL.Date_from_Index(i))-2))

  else :
    Current_Week = NWeek_Year ( Year )
    WL = Week_List ( Begin_First_Week, Current_Week )
    for i in range ( Current_Week + 1 ) :
      Result.append ( Delphi_Date ( Delphi_Date ( WL.Date_from_Index(i))-2))

  return Result
# ************************************************************************


# ************************************************************************
# ************************************************************************
class Kal ( object ) :
  """
first day of the week = Monday
first week = contains 4 January
           = 1st Thursday in that week
           = 4?7 days of year in that week
Most of Europe ISO 8601(1988) except UK, European Norm EN 28601 (1992)
  """
  def __init__ ( self, Date_Tuple = None ) :
    if Date_Tuple :
      self.Date = date ( *Date_Tuple )
    else :
      self.Date = date.today ()
    self.Year = self.Date.year
    self.Agenda = Calendar ()

    ##self.Now  = self.now ()
    ##self.Week = self.week ()

  def Now ( self ) :
    return date.today ()

  def Week ( self ) :
    First_Day = date ( self.Year, 1, 1 )
    NDays = (self.Date - First_Day).days
    NDays += First_Day.weekday()
    NWeek = 1 + old_div(NDays, 7)
    return NWeek

  # *************************************************
  # *************************************************
  def Days_of_Week ( self, week, year = None ) :
    """
    Returns a list with the day numbers of the week.
    If "year" is not specified, the current year is used.
    """
    if not ( year ) :
      year = self.Year

    First_Day = date ( year, 1, 1 )
    Delta = timedelta ( (week-1) * 7 )
    DiW = First_Day + Delta
    This_Month = DiW.month

    DayNr = DiW.day
    Month = self.Agenda.monthdayscalendar ( year, This_Month )
    for Row in Month :
      if DayNr in Row :
        break

    # if first week of the year
    if ( DiW.month == 1 ) and ( Row[0] == 0 ) :
      This_Month = 12
      Month = self.Agenda.monthdayscalendar ( year-1, 12 )
      Prev_Month = Month [-1]
      i = 0
      while Row[i] == 0 :
        Row[i] = Prev_Month[i]
        i+= 1

    # if beginning of month and week has days of previous month
    elif Row[0] == 0 :
      This_Month -= 1
      Month = self.Agenda.monthdayscalendar ( year, This_Month )
      Prev_Month = Month [-1]
      i = 0
      while Row[i] == 0 :
        Row[i] = Prev_Month[i]
        i+= 1

    # if end of month and week has days of next month
    elif Row[-1] == 0 :
      #This_Month += 1
      Month = self.Agenda.monthdayscalendar ( year, This_Month +1)
      Next_Month = Month [0]
      i = 6
      while Row[i] == 0 :
        Row[i] = Next_Month[i]
        i-= 1

    Month_Name = [ 'Unknown',
                   'Januari', 'Februari', 'Maart',
                   'April', 'Mei', 'Juni',
                   'Juli', 'Augustus', 'September',
                   'Oktober', 'November', 'December' ]
    Row.insert ( 0, Month_Name [ This_Month ] )
    return Row
  # *************************************************

  # *************************************************
  # *************************************************
  def Get_Days_of_Week_Range ( self, week_before, week_after ) :
    Grid = []
    for week in range ( self.Week - week_before,
                        self.Week + week_after + 1 ) :
      Grid.append ( self.Days_of_Week ( week ) )

    # Just use each month name once
    Month = ''
    for i, Row in enumerate ( Grid ) :
      if Row[0] == Month :
        Row[0] = ''
      else :
        Month = Row[0]
      # remove saterday / sunday
      Grid[i] = Row [:-2]

    return Grid


# ************************************************************************


# ************************************************************************
# ************************************************************************
if __name__ == '__main__':

  Test_Defs ( 1,2,3,4,5 )

  # **************************************************************
  # **************************************************************
  if Test ( 1 ) :
    #_Track_Methods [ '*' ]
    print(Delphi_Date ())
    print(Delphi_Date ( 41500 ).to_String_Date_Time())
    Browser_Date = '1376054534'
    print(Browser_Date)
    print(4,Delphi_Date ( Browser_Date ))
    print(5,Delphi_Date.from_Browser ( Browser_Date ))
    print(5,Delphi_Date.from_Browser ( Browser_Date ).to_String_Date_Time ())
    sys.exit()
    print(1,Delphi_Date ( 1375874993 ))
    print(2,Delphi_Date ( '00193877' ).to_String_Date_Time ())
    print(3,Delphi_Date ( '1375874993' ).to_String_Date_Time ())

    print('DD',Delphi_Date ('2011-04-18 16:00:00'))
    #print 'DD',Delphi_Date ('15-4-2013')
    print(Delphi_Date ())
    print(Delphi_Date ( None ))
    print(Delphi_Date ( 'None000000' ))
    exit()
    print('DD',Delphi_Date ( '1-1-1980' ))
    exit()
    HL7 = '20111229171200'
    Date = Delphi_Date ( HL7 )
    print('HL7:', HL7, Date.to_String_Date_Time ())
    HL7 = '20111231122529.363'
    ##HL7 = '20111231142242'
    Date = Delphi_Date ( HL7 )
    print('HL7:', HL7, Date.to_String_Date_Time ())

    print(Delphi_Date ( '2009' ))
    print(Delphi_Date ( '2009 04' ))
    sys.exit()


    Nu = Delphi_Date ( 40786.0 )
    print(Nu)
    print(Delphi_Date ().to_time(), Nu.to_String())

    print(Delphi_Date ( '02-04-1982' ).to_String())
    print(Delphi_Date ( '3-4-1982' ).to_String())
    print(Delphi_Date ( '005-4-1982' ).to_String())
    print(Delphi_Date ( '6-4-01982' ).to_String())

    print(Delphi_Date ( '1-1-1900'))
    print(str(Delphi_Date ( None )),'##')
    print(str(Delphi_Date ( '' )),'$$')
    print(Delphi_Date ( 0 ))
    sys.exit ()

    # 23-05-2005  17:43:44 ==>  Delphi_Time = 38495.7387037
    Delphi_Time = 38495.7387037
    Delphi_Time = 39848

    pytime = Delphi_Date ( Delphi_Time ).to_time()
    print('pytime =', pytime)
    print('Format_Date     ', Delphi_Date( pytime ).to_String ())

    print(Delphi_Time)
    print(Delphi_Date ( pytime ))

    DT = Delphi_Date ( '30-11-2005' )
    print('Format_Date_Time 30-11-2005', DT.to_String_Date_Time ())


    import mx.DateTime
    DT = Delphi_Date ( '01-02-1950' )
    print('Format_Date_Time 01-02-1950', DT.to_String_Date_Time ())

    Line = '30-09-2009'
    print('\nConvert to Delphi DateTime of :', Line)
    DDT = Delphi_Date ( Line )
    print('Results in Delphi Format :', DDT)
    Line = DDT.to_String ()
    print('Back to string :', Line)


    print('Convert ACCESS to Python')
    AT1 = Delphi_Date().from_Access (  '2009-09-24 00:00:00' )
    AT2 = Delphi_Date().from_Access (  '2009-09-25 00:00:00' )
    print(AT1,AT2,(AT2-AT1)/60/60/24)

  # **************************************************************
  # **************************************************************
  if Test ( 2 ) :
    # Delphi_DateTime = number of days since 30-12-1899
    DateStrings = [ '01-01-1980', '01-01-1900', '01-01-2008',
                    '01-01-1940', '1-1-40', '23-05-2005' ]

    v3print ( '\n===== String_2_Delphi_Date =====' )
    Delphi_Dates = []
    for Date in DateStrings :
      Delphi_Dates.append ( Delphi_Date ( Date ) )
      v3print ( Date, Delphi_Dates[-1] )

    v3print ( '\n===== Delphi_Date =====' )
    for i, Date in enumerate ( Delphi_Dates ) :
      v3print ( DateStrings[i], Delphi_Date ( Date ) ).to_String ()

  # **************************************************************
  # **************************************************************
  if Test ( 3 ) :
    import time
    DDate = Delphi_Date ()
    print(DDate)
    print(Delphi_Date ( DDate ).to_String ())
    print(Delphi_Date ( '11-02-2010'))
    print(Delphi_Date ( '34-02-2010'))
    print(Delphi_Date ( '11-2-2010'))
    print(Delphi_Date ( '11-02-10'))
    print(Delphi_Date ( '11-02-10'))
    print(Delphi_Date ( '11 02-10'))
    print(Delphi_Date ( '11 feb 10'))
    exit()

    print(DDate.to_String_Date_Time_Short())

    print(Delphi_Date ().to_String ())
    print(Delphi_Date().to_String_Date_Time_Short())

  # **************************************************************
  # **************************************************************
  if Test ( 4 ) :
    import datetime
    print(dir(datetime.date))
    DT = datetime.date

    X  = datetime.datetime(2006, 7, 1, 4, 0)
    print('datetime.datetime 2 Delphi :', Delphi_Date ( X ))



    print(DT.day, DT.today())
    Now=DT.today()
    print(Now.month, Now.isocalendar())
    """[
    'ctime', 'day', 'fromordinal', 'fromtimestamp', 'isocalendar', 'isoformat',
    'isoweekday', 'max', 'min', 'month', 'replace', 'resolution', 'strftime',
    'timetuple', 'today', 'toordinal', 'weekday', 'year']
    """

    from calendar import Calendar
    #from calendar import *
    Agenda = Calendar ()
    print(dir(Agenda))
    """
'_firstweekday', 'firstweekday', 'getfirstweekday',
'itermonthdates', 'itermonthdays', 'itermonthdays2',
'iterweekdays',
'monthdatescalendar','monthdays2calendar', 'monthdayscalendar',
'setfirstweekday',
'yeardatescalendar', 'yeardays2calendar', 'yeardayscalendar']
    """
    year = 2010
    for month in range ( 1, 6 ) :
      print(Agenda.monthdatescalendar ( year, month ))

    for day in Agenda.itermonthdays ( year, 1 ) :
      print(day)

    print('AAA',Agenda.monthdays2calendar ( year, 1 ))
    print('BBB',Agenda.monthdayscalendar ( year, 3 ))
    print('CCC',Agenda.monthdayscalendar ( year, 4 ))

  # **************************************************************
  # **************************************************************
  if Test ( 5 ) :


    Date = Kal()
    Now = Date.Now
    aap = Date.Week
    print('Now=',Now, aap)

    for week in range ( 1, 20 ) :
      print('Week =', week, Date.Days_of_Week ( week, 2010 ))

    Grid = Date.Get_Days_of_Week_Range ( 4, 5 )
    print('=====')
    for Row in Grid :
      print(Row)

    Grid = Date.Get_Days_of_Week_Range ( 0, 0 )
    print('=====')
    print(Grid)

    Test_Dates = [ (2010,1,1), (2010,1,2),(2010,1,3),(2010,1,4),(2010,5,2), (2010,5,3) ]
    for Test_Date in Test_Dates :
      Date = Kal ( Test_Date )
      WeekNr = Date.Week
      print('Date =', Date.Date, WeekNr)

    '''
    Agenda = Calendar ()
    print Now, Agenda.firstweekday, type(Now), dir(Now)
    '''

    #year = 2010
    #print 'CCC',Agenda.monthdayscalendar ( year, 4 )

  # **************************************************************
  # **************************************************************
  if Test ( 6 ) :

    NYear = 3
    Delphi_Start = Delphi_Date () -  NYear * 365 + 10 * 7
    print(Delphi_Date ( Delphi_Start ).to_String ())

    Delphi_Start = Delphi_Date ( '1-1-2011')
    WL = Week_List ( Delphi_Start, NYear*52 )
    print('WL', WL)
    for i in range(5) :
      print(Delphi_Date ( WL.Date_from_Index(i)).to_String())
    print(Delphi_Date ( '1-1-2011'))
    print(Delphi_Date ( '1-1-2011').to_Iso ())
    print(Delphi_Date ( ).to_Iso ())
    print(Delphi_Date ( '3-1-2011'))


    for Year in range ( 2000, 2014 ) :
      Weeks = Year_Week_List ( Year )
      print(Year, Weeks[0].to_String(), Weeks[-1].to_String())

    print(Delphi_Date ( 40681.1 ).to_String ())
    print(Delphi_Date ( 40681.6 ).to_String ())
    exit ()

    WL = Week_List ( Delphi_Start, This_Week_Nr )
    print('WL', WL, dir(WL))
    for i in range(5) :
      print(Delphi_Date ( WL.Date_from_Index(i)).to_String())


    #print 'week 1 loopt van - tot ',
    exit()

    Dates = [ '01-01-2008', '9-11-2008', '9-5-2011', '30-10-2011',
              '24-4-2011',
              '30-4-2011','1-5-2011',
              '2-5-2011',
              '15-5-2011','16-5-2011','17-5-2011','18-5-2011','19-5-2011',
              '20-5-2011','21-5-2011']

    Dates = [ '15-5-2011','16-5-2011','17-5-2011','18-5-2011','19-5-2011',
              '20-5-2011','21-5-2011']
    for Date in Dates :
      DD = Delphi_Date ( Date )
      Index = WL.Delphi_Index ( DD )
      print(Date, DD, Index, end=' ')
      if Index :
        print(WL.Weeks [ WL.Delphi_Index ( DD )])
      else :
        print()

  # **************************************************************
  # **************************************************************
  if Test ( 7 ) :
    """
    Dates = '1-1-2011,20-5-2011,31-12-2011,1-1-1954,13-3-1954,31-12-1954'.split(',')
    #import time
    #import datetime
    #import wx

    print '\n======   String ==> Delphi ==> String'
    for SD in Dates :
      print '%12s'% SD,
      DD = Delphi_Date ( SD )
      print '%12s'% DD,
      print '%12s'% DD.to_String ()

    print '\n======   Delphi ==> time.time  ==> Delphi'
    for SD in Dates :
      print '%12s'% SD,
      DD = Delphi_Date ( SD )
      try:
        DT = DD.to_time ()
      except:
        DT = 0
      print DT,
      D = Delphi_Date ( DT )
      print '%12s'% D.to_String ()

    print '\n======   Delphi ==> datetime.date  ==> Delphi'
    for SD in Dates :
      print '%12s'% SD,
      DD = Delphi_Date ( SD )
      DT = DD.to_datetime()
      print DT.date(),
      D = Delphi_Date(DT)
      print '%12s'% D.to_String()

    print '\n======   Delphi ==> wx.time  ==> Delphi'
    for SD in Dates :
      print '%12s'% SD,
      DD = Delphi_Date ( SD )
      WX = DD.to_wxTime()
      print WX,
      print '%12s'% Delphi_Date(WX).to_String()

    print '\n======   Delphi ==> ISO'
    for SD in Dates :
      DD = Delphi_Date ( SD )
      print '%12s'% SD,
      Iso = DD.to_Iso()
      print Iso

    print 'NOW :', Delphi_Date ().to_String_Short ()

    print 'Access :', Delphi_Date ( '2009-09-24 00:30:00' ).to_String_Short ()

    print Delphi_Date ( Delphi_Date () ).to_String ()
    print Delphi_Date ().to_String ()
    print Delphi_Date ()
    """

    Test_Dates = []
    Test_Dates.append ( 30000 )
    Test_Dates.append ( 30000.9 )
    Test_Dates.append ( '30000' )
    Test_Dates.append ( '30000.9' )
    Test_Dates.append ( '30000,9' )
    Test_Dates.append ( time.time() )
    Test_Dates.append ( '1-1-2011' )
    Test_Dates.append ( ' 1-  1-2011' )
    Test_Dates.append ( '01-01-11' )
    Test_Dates.append ( '2011-09-24 00:00:00' )
    Test_Dates.append ( 'aap' )
    Test_Dates.append ( '' )
    Test_Dates.append ( None )
    for Date in Test_Dates :
      DD = Delphi_Date ( Date )
      print(DD, DD.to_String (), str ( DD ), type(Date), Date, type(DD))
    DD = Delphi_Date ()
    print(DD, DD.to_String (), str ( DD ), type(Date), Date, type(DD))
    DD = Delphi_Date ('')
    print(DD, DD.to_String (), str ( DD ), type(Date), Date, type(DD))
    DD = Delphi_Date (None)
    print(DD, DD.to_String (), str ( DD ), type(Date), Date, type(DD))

    DD = Delphi_Date ('')
    if DD :
      print(True)
    else :
      print(False)

  # **************************************************************
  # **************************************************************
  if Test ( 8 ) :
    for i in range ( 1950, 2020 ) :
      a = NWeek_Year ( i )
      if a > 52 :
        print(i)

    Result = [40724, 40694, 40663, 40633, 40602, 40574]
    Delphi_Dates = '31-12-10,1-1-11,31-1-11,28-2-11,31-3-11,30-4-11,31-5-11,30-6-11'.split(',')
    for DD in Delphi_Dates :
      print(Delphi_Date( DD ).to_int(), Delphi_Date( DD ))


    print('=============')
    a = Delphi_Date ( 1308346136.0 )
    print(a)
    a = Delphi_Date ( 1308346136 )
    print(a)
    a = Delphi_Date ( '1308346136.0' )
    print(a)
    a = Delphi_Date ( '1308346136' )
    print(a.to_String_Date_Time_Short())
    a = Delphi_Date ( a + 0.5 )
    print(a.to_String_Date_Time_Short())

  # **************************************************************
  # **************************************************************
  if Test ( 9 ) :
    WL = Year_Week_List ( Year = None )
    for week in WL [:6] :
      print(Delphi_Date ( week ).to_String ())

    """
def first_monday(year, week):
    d = date(year, 1, 4)  # The Jan 4th must be in week 1  according to ISO
    return d + timedelta(weeks=(week-1), days=-d.weekday())
"""
# ************************************************************************
