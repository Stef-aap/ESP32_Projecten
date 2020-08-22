

#ifndef SI4432_support_h
#define SI4432_support_h   0.1

// ***********************************************************************************
// ***********************************************************************************
// Twee belangrijke documenten betreffende de SI4432
//  file:///home/stef/CWin/D/_raspberry/Remote/Tranceivers/4432/Si4430-31-32-1.pdf
//  file:///home/stef/CWin/D/_raspberry/Remote/Tranceivers/4432/AN440_registers.pdf
//
// Onderstaande is eigenlijk geheel overgenomenvan het jal programma
//    file:///home/stef/CWin/D/JALcc/JAL/SI4432/si4432_support.jal
//    file:///home/stef/CWin/D/JALcc/JAL/SI4432/si4432_tools_main.jal
//
//
//    http://mientki.ruhosting.nl/data_www/raspberry/doc/si4432_support_package.html
//    http://mientki.ruhosting.nl/data_www/raspberry/doc/ws3000_hack.html
//    http://mientki.ruhosting.nl/data_www/raspberry/doc/si4432_register_viewer.html
//    http://mientki.ruhosting.nl/data_www/raspberry/doc/spectrum_analyzer.html
//    http://mientki.ruhosting.nl/data_www/raspberry/doc/klikaanklikuit.html
//
// ***********************************************************************************
// ***********************************************************************************


/*
data begint op index 31:
          if ( Data_Received[31] & 0xF0 ) == 0x50 :

            Temperature = 25.6 * ( Data_Received[32] & 0x07 ) + Data_Received[33]/10.0

            if Data_Received[32] & 0x08 :

              Temperature *= -1.0

            Humidity    = Data_Received[34]

            WindSpeed   = 20 * 1.22 * Data_Received[35]



            RainFall    = 256 * ( Data_Received[37] & 0x0F ) + Data_Received[38]

            if Last_RainFall < 0 :

              Last_RainFall = RainFall

            RainFall = 0.3 * ( RainFall - Last_RainFall )


we zien hier dus :
RH = Data[34] = 14       klopt
T = Data[33]/10 = 22.8   klopt
Wind = Data[35] 0        klopt


146=x5=x4=x212=x119=x87=x196=x0=2192  2  192  680.
680.
680.
680.
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
680.
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
x146=x5=x131=x106=x207=x170=x174=x32=0102  0  102  680.
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
680.
680.
680.
x91=x160=x228=x15=x0=x0=x15=x23=179179  179  179  255
x91=x160=x228=x14=x0=x0=x15=x23=9696  96  96  255
x91=x160=x228=x15=x0=x0=x15=x23=179179  179  179  255
680.
*/

//#define SI4432_Debug

byte _Serial_Start_Byte = 0xFA ;


// ***********************************************************************************
String Hex2b ( int Value ) {
  String Line ;
  if ( Value < 16 ) Line += "0" ;
  Line += String ( Value, HEX ) ;
  Line.toUpperCase() ;
  return Line ;
}
// ***********************************************************************************
void Serial_Hex ( int Value ) {
  String Line ;
  if ( Value < 16 ) Line += "0" ;
  Line += String ( Value, HEX ) ;
  Line.toUpperCase() ;
  Serial.print ( Line + "  " ) ;
}

// ***********************************************************************************
// like Serial.write, but then with a long as input
// The MSB is outputed first
// ***********************************************************************************
void Serial_Write_Byte ( byte Value ) {
  #ifndef SI4432_Debug
    Serial.write ( Value ) ;
  #else
    //Serial.print ( Value, HEX ) ;
    //Serial.print ( " " ) ;
    Serial_Hex ( Value ) ;
  #endif
}
void Serial_Write_Long ( unsigned long Value ) {
  #ifndef SI4432_Debug
    byte Temp ;
    Temp = (byte)((( Value & 0xFF000000 ) >> 24 ) & 0xFF ) ;
    Serial.write ( Temp ) ;
    Temp = (byte)((( Value & 0x00FF0000 ) >> 16 ) & 0xFF ) ;
    Serial.write ( Temp ) ;
    Temp = (byte)((( Value & 0x0000FF00 ) >> 8  ) & 0xFF ) ;
    Serial.write ( Temp ) ;
    Temp = (byte)((( Value & 0x000000FF )       ) & 0xFF ) ;
    Serial.write ( Temp ) ;
  #else
    Serial.print ( Value ) ;
    Serial.print ( " " ) ;
  #endif
}

//#include "si4432.h"


      const unsigned long IF_Bandwidth_1 [] = { 
        2600, 2800, 3100, 3200, 3700, 4900, 5400, 5900, 6100, 7200, 
        9500, 10600, 11500, 12100, 14200, 16200, 17500, 19400, 21400, 23900, 
        25700, 28200, 32200, 34700, 38600, 42700, 47700, 51200, 56200, 64099, 
        69200, 75200, 83200, 90000, 95300, 112100, 127900, 137900, 142800, 167800, 
        181100, 191500, 208400, 225100, 248800, 269300, 284900, 335500, 361800, 420200, 
        468400, 518799, 577000, 620700 } ;
        
      const byte IF_ndec_exp_1 [] = { 
        5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 
        3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
        3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 
        1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 
        1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0 } ;

      const byte IF_filset_1 [] = {
        1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 
        1, 2, 3, 4, 5, 6, 10, 11, 12, 13, 
        14, 5, 6, 7, 11, 12, 13, 14, 5, 6, 
        7, 1, 2, 3, 4, 5, 6, 7, 4, 5, 
        9, 6, 10, 1, 2, 3, 4, 8, 9, 10, 
        11, 12, 13, 14 } ;

      const byte IF_dwn3_bypass_1 [] = {
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
        1, 1, 1, 1 } ;


      const unsigned long IF_Bandwidth_2 [] = { 
        2600, 2800, 3100, 3200, 3700, 4900, 5400, 5900, 6100, 7200, 
        9500, 10600, 11500, 12100, 14200, 16200, 17500, 18900, 21600, 22700, 
        24000, 28200, 31900, 34700, 38600, 42700, 47700, 51200, 56200, 64099, 
        69200, 75200, 83200, 90000, 95300, 112100, 127900, 137900, 138700, 154200, 
        168000, 181100, 208400, 232000, 256000, 269300, 284900, 335500, 361800, 420200, 
        468400, 518799, 577000, 620700 } ;

      const byte IF_ndec_exp_2 [] = { 
        5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 
        3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 
        2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 
        0, 0, 0, 0 } ;

      const byte IF_filset_2 [] = {
        1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 
        1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 
        4, 10, 15, 7, 11, 12, 13, 14, 5, 6, 
        7, 1, 2, 3, 4, 5, 6, 7, 10, 11, 
        8, 9, 10, 11, 12, 3, 4, 8, 9, 10, 
        11, 12, 13, 14 } ;

      const byte IF_dwn3_bypass_2 [] = {
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
        1, 1, 1, 1 } ;


      const unsigned long IF_Bandwidth_3 [] = { 
        2600, 2800, 3100, 3200, 3700, 4900, 5400, 5900, 6100, 7200, 
        9500, 10600, 11500, 12100, 14200, 16200, 17500, 19400, 21400, 23900, 
        25700, 28200, 32200, 34700, 38600, 42700, 47700, 51200, 56200, 64099, 
        69400, 77100, 85100, 95300, 102200, 115600, 127700, 142800, 153300, 168000, 
        181100, 208400, 232000, 256000, 269300, 284900, 335500, 361800, 420200, 468400, 
        518799, 577000, 620700 } ;

      const byte IF_ndec_exp_3 [] = { 
        5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 
        3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
        3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 
        1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 
        1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 
        0, 0, 0 } ;

      const byte IF_filset_3 [] = {
        1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 
        1, 2, 3, 4, 5, 6, 10, 11, 12, 13, 
        14, 5, 6, 7, 11, 12, 13, 14, 5, 6, 
        10, 11, 12, 13, 14, 11, 12, 13, 14, 8, 
        9, 10, 11, 12, 3, 4, 8, 9, 10, 11, 
        12, 13, 14 } ;
        
      const byte IF_dwn3_bypass_3 [] = {
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
        1, 1, 1 } ;

      const unsigned long IF_Bandwidth_0 [] = { 
        2600,2800,3100,3200,3700,4200,4500,4900,5400,5900,
        6100,7200,8200,8800,9500,10600,11500,12100,14200,16200,
        17500,18900,21000,22700,24000,28200,32200,34700,37700,41700,
        45200,47900,56200,64100,69200,75200,83200,90000,95300,112100,
        127900,137900,142800,167800,181100,191500,225100,248800,269300,284900,
        335500,361800,420200,469400,518800,577000,620700 } ;
      const byte IF_ndec_exp_0 [] = { 
        5,5,5,5,5,5,5,4,4,4,
        4,4,4,4,3,3,3,3,3,3,
        3,2,2,2,2,2,2,2,1,1,
        1,1,1,1,1,0,0,0,0,0,
        0,0,1,1,1,0,0,0,0,0,
        0,0,0,0,0,0,0 } ;
      const byte IF_dwn3_bypass_0 [] = {
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1 } ;
      const byte IF_filset_0 [] = {
          1,2,3,4,5,6,7,1,2,3,
          4,5,6,7,1,2,3,4,5,6,
          7,1,2,3,4,5,6,7,1,2,
          3,4,5,6,7,1,2,3,4,5,
          6,7,4,5,9,15,1,2,3,4,
          8,9,10,11,12,13,14 } ;


// ***********************************************************************************
// ***********************************************************************************
#define    _OOK_Size     32
unsigned long _OOK_Start = 0 ;
int           _OOK_Other = 0 ;
int           _OOK_Buffer [_OOK_Size] ;  /// plaats voor 16 meetpunten
int           _OOK_WP    = 0 ;
int           _OOK_RP    = 0 ;


// ***********************************************************************************
// ***********************************************************************************
static void _OOK_Int () ICACHE_RAM_ATTR ;
static void _OOK_Int () {

  if ( digitalRead ( SI4432_GPIO2_Pin ) == HIGH ) {
    _OOK_Buffer [ _OOK_WP + 1 ] = micros() - _OOK_Start ;
    _OOK_Start = micros() ;
    _OOK_Buffer [ _OOK_WP     ] = _OOK_Other ;
    _OOK_WP += 2 ;
    _OOK_WP %= _OOK_Size ;
  } else {
    _OOK_Other = micros() - _OOK_Start ;
    _OOK_Start = micros() ;
  }
}

// ***********************************************************************************
// ***********************************************************************************
static void _QIA_OOK_Int () ICACHE_RAM_ATTR ;
static void _QIA_OOK_Int () {

  if ( digitalRead ( SI4432_QIA_Rec_Pin ) == LOW ) {
    _OOK_Buffer [ _OOK_WP + 1 ] = micros() - _OOK_Start ;
    _OOK_Start = micros() ;
    _OOK_Buffer [ _OOK_WP     ] = _OOK_Other ;
    _OOK_WP += 2 ;
    _OOK_WP %= _OOK_Size ;
//Serial.print ( _OOK_WP ) ;  
//Serial.print ( " ");  
//Serial.print ( _OOK_RP==_OOK_WP ) ;  
//Serial.print ( " ");  
  } else {
//Serial.print(":");    
    _OOK_Other  = micros() - _OOK_Start ;
    _OOK_Start = micros() ;
  }
}
     


// ***********************************************************************************
// ***********************************************************************************
//class _WS3000 {
class _SI4432  {
  public:
    byte WS3000_Data [8] ;

    // **************************************************************
    // **************************************************************
    _SI4432 ( int sdnPin, int InterruptPin = 0 ) {  
      this->_sdnPin      = sdnPin ;
      this->_intPin      = InterruptPin ;
      //this->_GPIO2_Pin   = GPIO2_Pin ;
      //this->_QIA_Rec_Pin = QIA_Rec_Pin ;
      this->_freqCarrier = 433000000 ;
      this->_freqChannel = 0 ;
      this->_kbps        = 100 ;
      this->_packageSign = 0xDEAD ; // default is 450 mhz
    }
    
    // **************************************************************
    // **************************************************************
    int Init () {
      if ( this->_intPin    > 0 ) pinMode ( this->_intPin   , INPUT ) ;
      //if ( this->_GPIO2_Pin > 0 ) pinMode ( this->_GPIO2_Pin, INPUT ) ;
      pinMode ( this->_sdnPin, OUTPUT ) ;

    	digitalWrite ( this->_sdnPin, HIGH ) ; // turn off
      delay ( 100 ) ;                         // datasheet: minimal 20 msec

      pinMode ( SS, OUTPUT ) ;
      digitalWrite ( SS, HIGH ) ; // set pin high, so chip would know we don't use it. - well, it's turned off anyway but...

      SPI.begin ( SCK, MISO, MOSI, SS ) ;
      SPI.setBitOrder     ( MSBFIRST        ) ;

      //SPI.setClockDivider ( SPI_CLOCK_DIV2 ) ;  
      SPI.setClockDivider ( SPI_CLOCK_DIV64 ) ;  

      SPI.setDataMode     ( SPI_MODE0       ) ;
      //SPI.setDataMode     ( SPI_MODE3       ) ;
      /*
      divider: Set one of the following:
  SPI_CLOCK_DIV2: 8MHz
  SPI_CLOCK_DIV4: 4MHz (default)
  SPI_CLOCK_DIV8: 2MHz
  SPI_CLOCK_DIV16: 1MHz
  SPI_CLOCK_DIV32: 500kHz
  SPI_CLOCK_DIV64: 250kHz
  SPI_CLOCK_DIV128: 125kHz
      */

      this->SI4432_Reset () ;

      return this->Wait_For_ID () ;
    }


 
   // **************************************************************
    // **************************************************************
    void SI4432_Reset () {
    	digitalWrite ( this->_sdnPin, HIGH ) ;
      delay ( 100 ) ;                          // datasheet: minimal 20 msec
    	digitalWrite ( this->_sdnPin, LOW ) ;
      delay ( 40 ) ;                           // datasheet: minimal 20 msec
    }  

    // **************************************************************
    // **************************************************************
    byte SI4432_Read ( byte Addr ) {
      byte regVal = Addr & 0x7F ; // clear MSB
      digitalWrite ( SS, LOW  ) ;
      SPI.transfer ( regVal   ) ;
      byte Value = SPI.transfer ( 0xFF ) ;
      digitalWrite ( SS, HIGH ) ;
      return Value ;
    }
 
    // **************************************************************
    // **************************************************************
    void SI4432_Write ( byte Addr, byte Value ) {
      byte regVal = Addr | 0x80 ; // set MSB
      digitalWrite ( SS, LOW  ) ;
      SPI.transfer ( regVal   ) ;
      SPI.transfer ( Value    ) ;
      digitalWrite ( SS, HIGH ) ;
    }
    
    // **************************************************************
    // **************************************************************
    void SI4432_Print_Registers () {

      Serial.print ( "\nAddr:  " ) ;
      for ( int i=0; i<16; ++i) {
        Serial.print ( i, HEX ) ;
        Serial.print ( "   " ) ; 
      }

      for ( int i=0; i<127; ++i) {
        if ( i % 16 == 0 ) {
          Serial.print ( "\n" ) ;
          Serial.print ( "0x" ) ;
          Serial.print ( Hex2b ( i ) ) ;
          Serial.print ( "  " ) ;
        }
        Serial.print ( Hex2b ( SI4432_Read ( i ) ) ) ;
        Serial.print ( "  " ) ;
      }
      Serial.println () ;
    }
    
    // **************************************************************
    // **************************************************************
    void SI4432_Dump_Registers () {
      Serial.write ( 0xAA ) ;
      Serial.write ( 0xBB ) ;
      Serial.write ( 0xCC ) ;
      for ( int i=0; i<127; ++i) {
        Serial.write ( this->SI4432_Read ( i ) ) ;
      }
      Serial.write ( 0xAA ) ;
      Serial.write ( 0xBB ) ;
      Serial.write ( 0xDD ) ;
    }
    
    // **************************************************************
    // **************************************************************
    void SI4432_Antenna_Rx () {
      this->SI4432_Write  ( 0x0B, 0x1F ) ; // GPIO-0: pin = 0
      this->SI4432_Write  ( 0x0C, 0x1D ) ; // GPIO-1: pin = 1
    }
    void SI4432_Antenna_Tx () {
      this->SI4432_Write  ( 0x0B, 0x1D ) ; // GPIO-0: pin = 1
      this->SI4432_Write  ( 0x0C, 0x1F ) ; // GPIO-1: pin = 0
    }

    // **************************************************************
    // Test is the communication with the SI4432 functions normally
    // otherwise the SI4432 is in hangup mode
    // Trying to read/write one of the reserved words is not allowed.
    // **************************************************************
    bool SI4432_Hangup_Test () {
      bool x =
         ( SI4432_Read ( 0x00 ) == 0x08 ) &&   // Device Type Code
         ( SI4432_Read ( 0x01 ) == 0x06 ) &&   // Version Code
         ( SI4432_Read ( 0x09 ) == 0x7F ) &&   // Crystal Load Capacitanceors
         ( SI4432_Read ( 0x13 ) == 0x00 ) ;    // temperature value offset
      return x ;
    }


    // **************************************************************
    // **************************************************************
    void SI4432_Hangup_Test_Serial () {
      if ( SI4432_Hangup_Test () ) Serial.write ( 0x44 ) ;   // runs  = "D"
      else                         Serial.write ( 0x33 ) ;   // hangs = "3"
    }

   // **************************************************************
    void SI4432_Set_Carrier ( word Carrier ) {
      byte Freq_Carrier_high = ( Carrier & 0xFF00 ) >> 8 ;
      byte Freq_Carrier_low  =   Carrier & 0xFF ;
      SI4432_Write ( 0x76, Freq_Carrier_high ) ;
      SI4432_Write ( 0x77, Freq_Carrier_low  ) ;
    }

    // **************************************************************
    //     RXosc = ( 500 * ( 1 + 2 * dwn3_bypass ) / 
    //             ( 2**ndec_exp * Rb * ( 1 + Manchester ))
    //
    // For using this formula with integer values instead of floats
    // we need to
    //    We need 3 decimal digits, so we need to multiply by 8
    //    We must Rb in bps (instead of kbps) so we need to multiply by 1000
    //    We need to round: round(X) in integer: (1+2*X)/2
    //    for enough accuracy we need to use dword
    //
    // This leads to the following formula, which consumes
    //     454 bytes of Code memory
    //      32 bytes of Data Memory
    //
    // Some test examples
    //    IF-Bandwidth     Rb       Manchester  ==>  RXosc         dwn3  ndec
    //    64_000           1_200     0          ==>  00_00_06_83    0     1
    // **************************************************************
    unsigned long SI4432_Calc_RxOsc ( unsigned long Rb_Hz,
                                      byte Manchester ) {
      return ( 1 + 
                ( 500 * 8 * 1000 * 2 * (1 + 2 * (unsigned long)(dwn3_bypass)) )
                   /
                ( (unsigned long)(1 << ndec_exp) * Rb_Hz * ( 1 + Manchester ) )
              ) / 2 ;
      }

    // **************************************************************
    // **************************************************************
    unsigned long SI4432_Calc_ncoff ( unsigned long Rb_Hz,
                                      byte Manchester ) {
      // next formula seems to be safe over the whole range 
      return ( Rb_Hz * ( 1 + Manchester ) * (unsigned long)((unsigned long)(1) << ( 15 + ndec_exp )) )
                 / 
              ( 125 * 125 * (1 + 2 * (unsigned long)(dwn3_bypass)) ) ;
    }
  

    // **************************************************************
    // **************************************************************
    void SI4432_Set_crgain ( unsigned long RB_Hz,
                             byte Manchester,
                             unsigned long f_Dev_Hz,
                             unsigned long rxosc ) {
      unsigned long crgain ;
      crgain = 2 + ( ( 1 << 16 ) * RB_Hz * ( 1 + Manchester ) ) / ( f_Dev_Hz * rxosc ) ;
      //crgain = int ( round ( crgain ))
      if ( crgain > 2047 ) crgain = 2047 ;

      byte Value = ( crgain & 0x0700 ) >> 8 ;
      Value = Value | 0x10 ;               // compensate for "max Rb error > 1%"
      SI4432_Write ( 0x24, Value ) ;
      Value = crgain & 0xFF ;
      SI4432_Write ( 0x25, Value ) ;

    }


    // **************************************************************
    // Sets the frequency (in Hz) of the transceiver.
    // The frequency resolution for this setting is 156.25 Hz
    // **************************************************************
    void SI4432_Set_Frequency ( unsigned long Freq ) {
      // determine the main divider by 2 flag
      byte hbsel ;
      if ( Freq >= 480000000 ) {
        hbsel = 1 ;
        Freq = Freq / 2 ;
      } else hbsel = 0 ;
      
      // register 75, "Frequency Band Select", 
      //   bit 6 = sbsel, "SideBand Select, default set
      //   no idea what it means, but let's keep it this way
      const byte sbsel = 1 ;
      
      unsigned long N = Freq / 10000000 ;
//Serial.print ( "N") ;
//Serial.print (  ( Freq - N * 10000000 ) ) ;
      
      // The next formula is optimized for the smallest error (using integers)
      Carrier = ( 4 * ( Freq - N * 10000000 )) / 625 ;
//Serial.print ( "M") ;
//Serial.print (  Carrier ) ;
      
      byte Freq_Band = ( N - 24 ) | ( hbsel << 5 ) | ( sbsel << 6 ) ;
//Serial.print ( "P") ;
//Serial.print (  Freq_Band ) ;

      SI4432_Write ( 0x75, Freq_Band ) ;

      word WCarrier = Carrier & 0xFFFF ;
      SI4432_Set_Carrier ( WCarrier ) ;

    //  // for test  
    //  delay_100ms ( 1 )
    //  serial_hw_write ( 0xBB )
    //  serial_hw_write ( Freq_Band )
    //  serial_hw_write ( Freq_Carrier_high )
    //  serial_hw_write ( Freq_Carrier_low  )
    //  delay_100ms ( 1 )
    }

    // **************************************************************
    // Sets the IF Bandwidth specified in kHz for FSK and GFSK modulation.
    // The values are picked from the application note AN440.
    // (this application note might be difficult to find, look for it under RFM22B)
    // This procedure looks for a bandwidth (in table IF_Bandwidth)
    // larger or equal to the desired bandwidth.
    // If the procedure can't find that value, the largest bandwidth is set.
    // Names used for the variables resembles the names used in the datasheet. 
    // **************************************************************
    void SI4432_Set_BW_FSK_0 ( byte Table_Nr, unsigned long BW_Hz ) {
      if ( Table_Nr == 0 ) {
        // set the largest bandwidth (used if no valid value is found)
        int Count = sizeof ( IF_Bandwidth_0 ) / sizeof ( long ) ;
        byte Index = Count  - 1 ;
        
        // loop until a bandwidth larger or equal to the desired bandwidth is found
        //for count ( IF_Bandwidth_0 ) using i loop
        for ( int i=0; i<Count; i++) {
          if ( IF_Bandwidth_0 [i] >= BW_Hz ) {
            // if found, remember the index and leave the loop
            Index = i ;
            break ;
          }
        }
       
        // get the parts from the different lookup tables
        ndec_exp    = IF_ndec_exp_0    [ Index ] ;
        dwn3_bypass = IF_dwn3_bypass_0 [ Index ] ;
        filset      = IF_filset_0      [ Index ] ;
      }
      else if ( Table_Nr == 1 ) {
        // set the largest bandwidth (used if no valid value is found)
        int Count = sizeof ( IF_Bandwidth_1 ) / sizeof ( long ) ;
        byte Index = Count - 1 ;
        
        // loop until a bandwidth larger or equal to the desired bandwidth is found
        //for count ( IF_Bandwidth_1 ) using i loop
        for ( int i=0; i<Count; i++) {
          if ( IF_Bandwidth_1 [i] >= BW_Hz ) {
            // if found, remember the index and leave the loop
            Index = i ;
            break ;
          }
        }
       
        // get the parts from the different lookup tables
        ndec_exp    = IF_ndec_exp_1    [ Index ] ;
        dwn3_bypass = IF_dwn3_bypass_1 [ Index ] ;
        filset      = IF_filset_1      [ Index ] ;
      }
      else if ( Table_Nr == 2 ) {
        // set the largest bandwidth (used if no valid value is found)
        int Count = sizeof ( IF_Bandwidth_2 ) / sizeof ( long ) ;
        byte Index = Count - 1 ;
        
        // loop until a bandwidth larger or equal to the desired bandwidth is found
        //for count ( IF_Bandwidth_2 ) using i loop
        for ( int i=0; i<Count; i++) {
          if ( IF_Bandwidth_2 [i] >= BW_Hz ) {
            // if found, remember the index and leave the loop
            Index = i ;
            break ;
          }
        }
       
        // get the parts from the different lookup tables
        ndec_exp    = IF_ndec_exp_2    [ Index ] ;
        dwn3_bypass = IF_dwn3_bypass_2 [ Index ] ;
        filset      = IF_filset_2      [ Index ] ;
      }
      else  { // Table_Nr == 3
        // set the largest bandwidth (used if no valid value is found)
        int Count = sizeof ( IF_Bandwidth_3 ) / sizeof ( long ) ;
        byte Index = Count - 1 ;
        
        // loop until a bandwidth larger or equal to the desired bandwidth is found
        //for count ( IF_Bandwidth_3 ) using i loop
        for ( int i=0; i<Count; i++) {
          if ( IF_Bandwidth_3 [i] >= BW_Hz ) {
            // if found, remember the index and leave the loop
            Index = i ;
            break ;
          }
        }
       
        // get the parts from the different lookup tables
        ndec_exp    = IF_ndec_exp_3    [ Index ] ;
        dwn3_bypass = IF_dwn3_bypass_3 [ Index ] ;
        filset      = IF_filset_3      [ Index ] ;
      }
      
      // merge the parts and write them to the bandwidth register
      byte Value = (dwn3_bypass << 7) | (ndec_exp << 4) | filset ;
      SI4432_Write ( 0x1C, Value ) ;
    }


    // **************************************************************
    // **************************************************************
    void SI4432_Set_BW_FSK ( byte Table_Nr,
                             unsigned long BW_Hz,
                             unsigned long Rb_Hz,
                             byte Manchester,
                             unsigned long f_Dev_Hz ) {
      byte Value ;
         
      SI4432_Set_BW_FSK_0 ( Table_Nr, BW_Hz ) ;
Serial.println ( "FSK_0 done" ) ;
       
      Serial_Write_Long ( f_Dev_Hz ) ;
      Serial_Write_Long ( Rb_Hz ) ;
      Serial_Write_Long ( BW_Hz ) ;
      Serial_Write_Byte ( Table_Nr ) ;
      Serial_Write_Byte ( ndec_exp ) ;
      Serial_Write_Byte ( dwn3_bypass ) ;
      Serial_Write_Byte ( filset ) ;
Serial.println ( "FSK_0 done bytes written" ) ;
      delay ( 100 ) ;
       
 
      // ***********************************
      // rxosc = Clock Recovery Oversampling
      // ***********************************
      unsigned long rxosc = SI4432_Calc_RxOsc ( Rb_Hz, Manchester ) ;
      Value = rxosc & 0xFF ;
      SI4432_Write ( 0x20, Value ) ;
 
      Value = ( rxosc & 0xFF00 ) >> 3 ;
      SI4432_Write ( 0x21, Value ) ;
 
      // ***********************************
      // ncoff = Clock Recovery Offset
      // ***********************************
      unsigned long ncoff = SI4432_Calc_ncoff ( Rb_Hz, Manchester ) ;
      byte Value2 = ( ncoff & 0xFF0000 ) >> 16 ;
      Value = Value | Value2 ;
      SI4432_Write ( 0x21, Value ) ;
      Value = ( ncoff & 0xFF00 ) >> 8 ;
      SI4432_Write ( 0x22, Value ) ;
      Value = ncoff & 0xFF ;
      SI4432_Write ( 0x23, Value ) ;
 
      // ***********************************
      // ***********************************
      SI4432_Set_crgain ( Rb_Hz, Manchester, f_Dev_Hz, rxosc ) ;
 
      const bool AFC_Enabled = true ;
      if ( AFC_Enabled ) Value = 0x40 ;
      else               Value = 0x3C ;
      SI4432_Write ( 0x1D, Value ) ;
 
      if ( AFC_Enabled ) {
        if ( ( Rb_Hz * ( 1 + Manchester )) / 1000 < 200 ) Value = 0x0A ;
        else                                               Value = 0x02 ;
      }
      else                                                 Value = 0x00 ;
      SI4432_Write ( 0x1E, Value ) ;
 
      SI4432_Write ( 0x1F, 0x00 ) ; // yields for "max Rb error > 1%"
      SI4432_Write ( 0x2A, 0x30 ) ; // ZEER MOEILIJK NOG UITZOEKEN
      SI4432_Write ( 0x69, 0x60 ) ; // constant
 
      // for Test only
      /* dus maareven weg
      SI4432_Print_Reg ( 0x1C ) ;
      SI4432_Print_Reg ( 0x20 ) ;
      SI4432_Print_Reg ( 0x21 ) ;
      SI4432_Print_Reg ( 0x22 ) ;
      SI4432_Print_Reg ( 0x23 ) ;
      SI4432_Print_Reg ( 0x24 ) ;
      SI4432_Print_Reg ( 0x25 ) ;
      SI4432_Print_Reg ( 0x1D ) ;
      SI4432_Print_Reg ( 0x1E ) ;
      SI4432_Print_Reg ( 0x2A ) ;
      SI4432_Print_Reg ( 0x1F ) ;
      SI4432_Print_Reg ( 0x69 ) ;
      */
    }

    // **************************************************************
    // **************************************************************
    void SI4432_Generate_FSK_Block () {
      //;;SI4432_Write ( 0x07, 0x0B )    -- Transmit <<<<<<<<<<<<<<<<<<<<<<
      //CSN    = Low
      //SSPBUF = 0x7F | 0x80
    	digitalWrite ( SS, LOW ) ;
      SPI.transfer ( 0x7F | 0x80 ) ;

      //for 5 loop
      //  while ! SSPIF loop end loop
      //    SSPBUF = 0x55
      //  SSPIF = false
      //end loop
      //while ! SSPIF loop end loop
      for ( int i=0; i<5; i++ ) {
        SPI.transfer ( 0x55 ) ;
      }
      
      //  SSPBUF = 0x2D
      //SSPIF = false
      //while ! SSPIF loop end loop
      SPI.transfer ( 0x2D ) ;
      

      //SSPBUF = 0xD4
      //SSPIF = false
      SPI.transfer ( 0xD4 ) ;

      //for 40 loop
      //  while ! SSPIF loop end loop
      //    SSPBUF = 0x00
      //  SSPIF = false
      //end loop
      //while ! SSPIF loop end loop
      for ( int i=0; i<40; i++ ) {
        SPI.transfer ( 0x00 ) ;
      }

      //CSN = high
    	digitalWrite ( SS, HIGH ) ;
      
      SI4432_Write ( 0x07, 0x0B ) ;   // Transmit <<<<<<<<<<<<<<<<<<<<<<
      // wait for transmission is ready, VERY IMPORTANT
      while ( SI4432_Read ( 0x07 ) != 0x03 ) ;


      
      delay ( 1000 ) ;
    	digitalWrite ( SS, LOW ) ;
      //SSPBUF = 0x7F | 0x80
      SPI.transfer ( 0x7F | 0x80 ) ;

      //for 5 loop
      //  while ! SSPIF loop end loop
      //    SSPBUF = 0x55
      //  SSPIF = false
      //end loop
      //while ! SSPIF loop end loop
      for ( int i=0; i<5; i++ ) {
        SPI.transfer ( 0x55 ) ;
      }


      //  SSPBUF = 0x2D
      //SSPIF = false
      //while ! SSPIF loop end loop
      SPI.transfer ( 0x2D ) ;

      //  SSPBUF = 0xD4
      //SSPIF = false
      SPI.transfer ( 0xD4 ) ;

      //for 40 loop
      //  while ! SSPIF loop end loop
      //    SSPBUF = 0xFF
      //  SSPIF = false
      //end loop
      //while ! SSPIF loop end loop
      for ( int i=0; i<40; i++ ) {
        SPI.transfer ( 0xFF ) ;
      }
    	digitalWrite ( SS, HIGH ) ;
      
      SI4432_Write ( 0x07, 0x0B ) ;   // Transmit <<<<<<<<<<<<<<<<<<<<<<
      // wait for transmission is ready, VERY IMPORTANT
      while ( SI4432_Read ( 0x07 ) != 0x03 );
    }
    
    
    // **************************************************************
    // **************************************************************
    void SI4432_Generate_FSK_Block_2 () {
      const byte Packet_Len = 9 ;
      
      // reset FIFO
      SI4432_Write ( 0x08, 0x03 ) ;
      SI4432_Write ( 0x08, 0x00 ) ;

      // packet length
      SI4432_Write ( 0x3E, Packet_Len ) ;   

      // fill the FIFO
      //for Packet_Len using i loop
      for ( int i=0; i< Packet_Len; i++) {
        SI4432_Write ( 0x7F, i+0x20 ) ;
        //SI4432_Write ( 0x7F, 0x55 ) ;   ;<<<<< tijdlijk to fetch preamble
      }

      // Start Transmission
      SI4432_Write ( 0x07, 0x0B ) ;
      
      // TEST: read EZMAC
      Serial_Write_Byte ( SI4432_Read ( 0x31 ) ) ;

      // wait for transmission is ready, VERY IMPORTANT
      while ( SI4432_Read ( 0x07 ) != 0x03 ) {
        Serial_Write_Byte ( SI4432_Read ( 0x31 ) ) ;
        delay ( 20 ) ;
      }

      // when the FIFO gets empty, while loop above,
      // the last byte has to be sent yet
      // so depending on the Baudrate we've to wait a little while
      delay ( 2 ) ; // needs to be at least 2 msec
      Serial_Write_Byte ( SI4432_Read ( 0x02 ) ) ;
      Serial_Write_Byte ( SI4432_Read ( 0x03 ) ) ;
      Serial_Write_Byte ( SI4432_Read ( 0x04 ) ) ;
      Serial_Write_Byte ( SI4432_Read ( 0x31 ) ) ;
      // response should be:  20 24 02 01
      //                       |  |  |  |__ package sent
      //                       |  |  |_____ Chip Ready
      //                       |  |________ ipksent, TX-FIFO almost empty
      //                       |___________ RX/TX Underflow
    }


    // **************************************************************
    // **************************************************************
    void SI4432_Read_Status () {
      byte Reg ;
      Serial.println ( "============== Status Registers  ==============" ) ;
      
      // **************************
      // R00 en R01 chip type and version
      // **************************
      Reg = SI4432_Read ( 0x00 ) ;
      Serial.print ( "00: " ) ;
      Serial_Hex ( Reg ) ;
      Serial.print ( " Device Type: " ) ;
      if ( ( Reg & 0x1F ) == 0x08 ) Serial.println ( "EZRadioPRO" ) ;
      
      Reg = SI4432_Read ( 0x01 ) ;
      Serial.print ( "01: " ) ;
      Serial_Hex ( Reg ) ;
      Serial.print ( " Version: " ) ;
      if ( ( Reg & 0x1F ) == 0x06 ) Serial.println ( "Rev B1" ) ;
      
      // **************************
      // R02 Status
      // **************************
      Reg = SI4432_Read ( 0x02 ) ;
      Serial.print ( "02: " ) ;
      Serial_Hex ( Reg ) ;
      Serial.print ( " Status: " ) ;
      if ( ( Reg & 0x80 ) != 0 ) Serial.print ( "FIFO RX/TX Overflow, " ) ;
      if ( ( Reg & 0x40 ) != 0 ) Serial.print ( "FIFO RX/TX Underflow, " ) ;
      if ( ( Reg & 0x20 ) != 0 ) Serial.print ( "RX empty, " ) ;
      if ( ( Reg & 0x10 ) != 0 ) Serial.print ( "Header Error " ) ;

      if ( ( Reg & 0x08 ) != 0 ) Serial.print ( "Frequency Error, " ) ;
      if       ( ( Reg & 0x03 ) == 0x00 ) Serial.print ( "STATE IDLE" ) ;
      else if ( ( Reg & 0x03 ) == 0x01 ) Serial.print ( "STATE RX" ) ;
      else if ( ( Reg & 0x03 ) == 0x10 ) Serial.print ( "STATE TX" ) ;
      else                                Serial.print ( "STATE ???" ) ; 
      Serial.println () ;
      
      // **************************
      // R03 and R04 are Interrupt or Status Flags
      // **************************
      Reg = SI4432_Read ( 0x03 ) ;
      Serial.print ( "03: " ) ;
      Serial_Hex ( Reg ) ;
      Serial.print ( " Interrupts: " ) ;
      if ( ( Reg & 0x80 ) != 0 ) Serial.print ( "FIFO under/overflow, " ) ;
      if ( ( Reg & 0x40 ) != 0 ) Serial.print ( "FIFO TX almost full, " ) ;
      if ( ( Reg & 0x20 ) != 0 ) Serial.print ( "FIFO TX almost empty, " ) ;
      if ( ( Reg & 0x10 ) != 0 ) Serial.print ( "FIFO RX almost full " ) ;

      if ( ( Reg & 0x08 ) != 0 ) Serial.print ( "External Interrupt, " ) ;
      if ( ( Reg & 0x04 ) != 0 ) Serial.print ( "Packet Sent, " ) ;
      if ( ( Reg & 0x02 ) != 0 ) Serial.print ( "Valid Packet Received, " ) ;
      if ( ( Reg & 0x01 ) != 0 ) Serial.print ( "CRC Error, " ) ;
      Serial.println () ;

      // **************************
      // R03 and R04 are Interrupt or Status Flags, so they must be listed twice
      // **************************
      Reg = SI4432_Read ( 0x04 ) ;
      Serial.print ( "04: " ) ;
      Serial_Hex ( Reg ) ;
      Serial.print ( " Interrupts: " ) ;
      if ( ( Reg & 0x80 ) != 0 ) Serial.print ( "Sync detected, " ) ;
      if ( ( Reg & 0x40 ) != 0 ) Serial.print ( "Valid Preamble Detected, " ) ;
      if ( ( Reg & 0x20 ) != 0 ) Serial.print ( "Invalid Preamble Detected, " ) ;
      if ( ( Reg & 0x10 ) != 0 ) Serial.print ( "RSSI above treshold " ) ;

      if ( ( Reg & 0x08 ) != 0 ) Serial.print ( "WakeUp Timer, " ) ;
      if ( ( Reg & 0x04 ) != 0 ) Serial.print ( "Low Batt detected, " ) ;
      if ( ( Reg & 0x02 ) != 0 ) Serial.print ( "ChipRdy, " ) ;
      if ( ( Reg & 0x01 ) != 0 ) Serial.print ( "Power On" ) ;
      Serial.println () ;
      
      // **************************
      // R05 and R06 are Interrupt Enable Flags 
      // **************************
      Reg = SI4432_Read ( 0x05 ) ;
      Serial.print ( "05: " ) ;
      Serial_Hex ( Reg ) ;
      Serial.print ( " IE on: " ) ;
      if ( ( Reg & 0x80 ) != 0 ) Serial.print ( "FIFO under/overflow, " ) ;
      if ( ( Reg & 0x40 ) != 0 ) Serial.print ( "FIFO TX almost full, " ) ;
      if ( ( Reg & 0x20 ) != 0 ) Serial.print ( "FIFO TX almost empty, " ) ;
      if ( ( Reg & 0x10 ) != 0 ) Serial.print ( "FIFO RX almost full " ) ;

      if ( ( Reg & 0x08 ) != 0 ) Serial.print ( "External Interrupt, " ) ;
      if ( ( Reg & 0x04 ) != 0 ) Serial.print ( "Packet Sense, " ) ;
      if ( ( Reg & 0x02 ) != 0 ) Serial.print ( "Valid Packet Received, " ) ;
      if ( ( Reg & 0x01 ) != 0 ) Serial.print ( "CRC Error, " ) ;
      Serial.println () ;
      
      Reg = SI4432_Read ( 0x06 ) ;
      Serial.print ( "06: " ) ;
      Serial_Hex ( Reg ) ;
      Serial.print ( " IE on: " ) ;
      if ( ( Reg & 0x80 ) != 0 ) Serial.print ( "SyncWord Detected, " ) ;
      if ( ( Reg & 0x40 ) != 0 ) Serial.print ( "Valid-Preamble, " ) ;
      if ( ( Reg & 0x20 ) != 0 ) Serial.print ( "Invalid-Preamble, " ) ;
      if ( ( Reg & 0x10 ) != 0 ) Serial.print ( "RSSI, " ) ;

      if ( ( Reg & 0x08 ) != 0 ) Serial.print ( "WakeUp Timer, " ) ;
      if ( ( Reg & 0x04 ) != 0 ) Serial.print ( "Low Battery, " ) ;
      if ( ( Reg & 0x02 ) != 0 ) Serial.print ( "XTAL Ready, " ) ;
      if ( ( Reg & 0x01 ) != 0 ) Serial.print ( "Power On Reset, " ) ;
      Serial.println () ;

      // **************************
      // **************************
      Reg = SI4432_Read ( 0x07 ) ;
      Serial.print ( "07: " ) ;
      Serial_Hex ( Reg ) ;
      Serial.print ( " Mode: " ) ;
      if ( ( Reg & 0x80 ) != 0 ) Serial.print ( "Software-Rest, " ) ;
      if ( ( Reg & 0x40 ) != 0 ) Serial.print ( "Enable detect Low_batt, " ) ;
      if ( ( Reg & 0x20 ) != 0 ) Serial.print ( "Enable WakeUp, " ) ;
      if ( ( Reg & 0x10 ) != 0 ) Serial.print ( "32kHz Xtal, " ) ;

      if ( ( Reg & 0x08 ) != 0 ) Serial.print ( "TX-on, " ) ;
      if ( ( Reg & 0x04 ) != 0 ) Serial.print ( "RX-on, " ) ;
      if ( ( Reg & 0x02 ) != 0 ) Serial.print ( "PLL-on, " ) ;
      if ( ( Reg & 0x01 ) != 0 ) Serial.print ( "XTAL-on, " ) ;
      Serial.println () ;

      // **************************
      // **************************
      Reg = SI4432_Read ( 0x27 ) ;
      Serial.print ( "27: " ) ;
      Serial_Hex ( Reg ) ;
      Serial.print ( " RSSI TReshold: " ) ;
      Serial_Hex ( Reg ) ;
      Serial.println () ;

      // **************************
      // Carrier Frequency
      // **************************
      unsigned long Fractie = this->SI4432_Read ( 0x76 ) ;
      Fractie = ( Fractie << 8 ) | SI4432_Read ( 0x77 ) ;
      Reg = SI4432_Read ( 0x75 ) ;
      double Fractie2 = ((double)Fractie) / 64000 ;
      double Freq = 10000000 * ( 1 + (( Reg & 0x20 ) >> 5 ) ) * (( Reg & 0x1F ) + 24 + Fractie2 ) ;
      Serial.print ( "27: " ) ;
      Serial_Hex ( Reg ) ;
      Serial.print ( " Carrier Frequency: " ) ;
      Serial.print ( Freq ) ;
      Serial.println () ;



    }

    
    // **************************************************************
    // **************************************************************
    void SI4432_Watch_Status () {
      unsigned long N = 0 ;
      byte R02, R03, R04, R07, R31, R02_Old, R03_Old, R04_Old, R07_Old, R31_Old ;
      byte RSSI ;
SI4432_Write ( 0x07, 0x07 ) ;    // Operating Mode and Function Control 1
SI4432_Antenna_Rx () ;
      
      //this -> Dump_All () ;
      String Header = "R02 R03 R04 R07 R31 RSSI N" ;
      while ( true ) {
        R02 = SI4432_Read ( 0x02 ) ;
        R03 = SI4432_Read ( 0x03 ) ;
        R04 = SI4432_Read ( 0x04 ) & 0x8F ; // ignore Valid-Preamble, Invalid-Preamble, RSSI
        //;R04 = SI4432_Read ( 0x04 ) & 0xCF   -- ignore Invalid Preamble, RSSI
        //;R04 = SI4432_Read ( 0x04 ) & 0xDF   -- ignore Invalid Preamble
        R07 = SI4432_Read ( 0x07 ) ;
        R31 = SI4432_Read ( 0x31 )  & 0xDF ; // ignore Package-Searching
        RSSI = SI4432_Read ( 0x26 ) ;
        if ( ( R02 != R02_Old ) |
             ( R03 != R03_Old ) |
             ( R04 != R04_Old ) |
             ( R07 != R07_Old ) |
             ( R31 != R31_Old ) ) { //|
             //( RSSI > 255    ) ) {
          if (( N % 20 ) == 0 ) Serial.println ( Header ) ;
          Serial_Hex ( R02 ) ;
          Serial_Hex ( R03 ) ;
          Serial_Hex ( R04 ) ;
          Serial_Hex ( R07 ) ;
          Serial_Hex ( R31 ) ;
          Serial_Hex ( RSSI ) ;
          Serial.print ( N ) ;
          
          String Line = "  " 
          ;
          byte Temp = R02 & 0x03 ;
          if      ( Temp == 0x01 )  Line += "RX-mode, " ;
          else if ( Temp == 0x02 ) Line += "TX-mode, " ;
               else                 Line += "Idle, ";
          
          if ( ( R02 & 0x20 ) != 0 ) Line += "RX-FIFO empty, " ;
          
          if ( ( R02 & 0xD8 ) != 0 ) Line += "R2-error, " ;
          
          Serial.println ( Line ) ;

          R02_Old = R02 ;
          R03_Old = R03 ;
          R04_Old = R04 ;
          R07_Old = R07 ;
          R31_Old = R31 ;
          //N = 0 ;
          //;delay_1ms ( 100 )
          delay ( 100 ) ;
          N = N + 1 ;
        } 
      
        // enter receive mode
        if ( ( R07 & 0x04 ) != 0x04 ) {
          SI4432_Write ( 0x07, 0x07 ) ; // Operating Mode and Function Control 1
        }
              
      }
    }

    

    // **************************************************************
    // Continuously reads the RSSI (Receive Signal Strength Indicator) register
    // and if the value is above the desired treshold,
    // sends the data to the serial port.
    // **************************************************************
    void SI4432_Loop_Read_RSSI ( byte Treshold ) {
      //?alias Data is GPIO2 
      int N = 0 ;
      while ( true ) {
        byte RSSI = SI4432_Read ( 0x26 ) ;
        if ( RSSI > Treshold ) {
          Serial.print ( RSSI, HEX ) ;
          Serial.print ( " " ) ;
          delay ( 100 ) ;
          N += 1 ;
          if ( N > 100 ) {
            Serial.println () ;
            N = 0 ;
          }
        }
      }
    }

    // **************************************************************
    // bare minimal receive mode
    // **************************************************************
    void SI4432_Init_Rx () {
      this->SI4432_Reset () ;

      // clear FIFO
      this->SI4432_Write ( 0x08, 0x03 ) ;
      this->SI4432_Write ( 0x08, 0x00 ) ;


      // set RSSI Treshold
      this->SI4432_Write ( 0x27, 0x00 ) ;
      
      // set carrier frequency
      this->SI4432_Set_Frequency ( 434000000 ) ;


      // set the sytem in Ready mode. PLL on, RX manual receive
      this->SI4432_Write ( 0x07, 0x03 ) ;    
      delay ( 100 ) ;
      this->SI4432_Write ( 0x07, 0x07 ) ;    
      delay ( 100 ) ;

      this->SI4432_Antenna_Rx () ;
      delay ( 100 ) ;

      // disable all interrupts      
      this->SI4432_Write ( 0x05, 0x00 ) ;    
      this->SI4432_Write ( 0x06, 0x00 ) ;    

      // read (and thereby clear all pending interrupts
      this->SI4432_Read ( 0x03 ) ;    
      this->SI4432_Read ( 0x04 ) ;    

      
      
      this->SI4432_Print_Registers () ;
      this->SI4432_Read_Status    () ;
      
      unsigned int N = 0 ;
      byte         RSSI ;
      while ( true ) {
        RSSI = this->SI4432_Read ( 0x26 ) ;
        Serial_Hex ( RSSI ) ;
        delay ( 1000 ) ;
        N += 1 ;
        if ( N % 32 == 0 ) {
          Serial.println () ;
          this->SI4432_Read_Status () ;
        }
      }
    }

    // **************************************************************
    // some of the commands seem to have a critical position
    //                        // <<<< CRITICAL
    // **************************************************************
    void SI4432_Init () {
      SI4432_Reset () ;

      // the following registers needs a clean up !!!
      //;SI4432_Write(0x72, 0x50) ;
      SI4432_Write(0x75, 0x53) ;
      SI4432_Write(0x76, 0x62) ;
      SI4432_Write(0x77, 0x00) ;

      SI4432_Write(0x6E, 0x19) ;
      SI4432_Write(0x6F, 0x9A) ;
      SI4432_Write(0x70, 0x04) ;
      SI4432_Write(0x58, 0xC0) ;

      //;SI4432_Write(0x71, 0x29) ;

      SI4432_Write(0x1C, 0x81) ;
      SI4432_Write(0x20, 0x78) ;
      SI4432_Write(0x21, 0x01) ;
      SI4432_Write(0x22, 0x11) ;
      SI4432_Write(0x23, 0x11) ;
      SI4432_Write(0x24, 0x01) ;
      SI4432_Write(0x25, 0x13) ;
      SI4432_Write(0x2C, 0x28) ;
      SI4432_Write(0x2D, 0x0C) ;
      SI4432_Write(0x2E, 0x28) ;
      SI4432_Write(0x1F, 0x03) ;
      SI4432_Write(0x69, 0x60) ;

      // from RFM22.cpp
      // disable all interrupts
      SI4432_Write ( 0x06, 0x00 ) ;    // <<<< CRITICAL

      // set the sytem in Ready mode. PLL on, RX manual receive
      SI4432_Write ( 0x07, 0x07 ) ;     // <<<< CRITICAL
      
      // set crystal oscillator cap to 12.5pf (but I don't know what this means) ;
      //write(0x09, 0x7f);
      
      // GPIO setup - not using any, like the example from sfi
      // Set GPIO clock output to 2MHz - this is probably not needed, since I am ignoring GPIO...
      //write(0x0A, 0x05);--default is 1MHz
      
      // set antenna switch for RX 
      // GPIO power drive capability 00 seems to be enough
      SI4432_Antenna_Rx () ;
      SI4432_Write  ( 0x0D, 0x14 ) ;    // GPIO-2 = RX-data
      //;SI4432_Write  ( 0x0D, 0x0F ) ;    // GPIO-2 = RX-clock
      
      // GPIO 0-2 are ignored, leaving them at default
      //write(0x0D, 0x00);
      // no reading/writing to GPIO
      //write(0x0E, 0x00);

      
      // ADC and temp are off
      //write(0x0F, 0x70);
      //write(0x10, 0x00);
      //write(0x12, 0x00);
      //write(0x13, 0x00);
      
      // no whiting, no manchester encoding, data rate will be under 30kbps
      // subject to change - don't I want these features turned on?
      //write(0x70, 0x20);
      SI4432_Write ( 0x70, 0x00 ) ;
      
      // filset= 0b0100 or 0b1101
      // bit 7   = Bypass Decimator by 3 (if set) ;
      // bit 6:4 = IF Filter Decimation Rates
      // bit 3:0 = IF Filter Coefficient Sets
      //           Defaults are for Rb = 40 kbps and Fd = 20 kHz so Bw = 80 kHz
      SI4432_Write ( 0x1C, 0x04 ) ;  
      //;SI4432_Write ( 0x1C, 0x8E ) ;   630 kHz
      //;SI4432_Write ( 0x1C, 0x00 ) ;  

      // bit 7   = afcbd = If set, the tolerated AFC frequency error will be halved.
      // bit 6   = enafc = AFC Enable.
      // bit 5:3 = afcgearh[2:0] = AFC High Gear Setting.
      // bit 2:0 = afcgearl[2:0] = AFC Low Gear Setting.
      //write(0x1D, 0x40);--"battery voltage" my ass
      SI4432_Write ( 0x1D, 0x00 ) ;  // No AFC

      // RX Modem settings (not, apparently, IF Filter?)
      //write(0x1E, 0x08);--apparently my device's default
      
      // Clock recovery - straight from 3e-club.ru with no understanding
      //write(0x20, 0x41);
      //write(0x21, 0x60);
      //write(0x22, 0x27);
      //write(0x23, 0x52);
      // Clock recovery timing
      //write(0x24, 0x00);
      //write(0x25, 0x06);
      
      // Tx power to max
      //write(0x6D, 0x07);--or is it 0x03?
      
      // Tx data rate (1, 0) ; - these are the same in both examples
      //write(0x6E, 0x27);
      //write(0x6F, 0x52);
      
      // "Data Access Control"
      // Enable CRC
      // Enable "Packet TX Handling" (wrap up data in packets for bigger chunks, but more reliable delivery) ;
      // Enable "Packet RX Handling"
      //write(0x30, 0x8C);
      // Diasble all RX packet + CRC
      SI4432_Write ( 0x30, 0x00 ) ;
      
      // "Header Control" - appears to be a sort of 'Who did i mean this message for'
      // we are opting for broadcast
      //write(0x32, 0xFF);
      SI4432_Write ( 0x32, 0x00 ) ;
      
      // "Header 3, 2, 1, 0 used for head length, fixed packet length, synchronize word length 3, 2,"
      // Fixed packet length is off, meaning packet length is part of the data stream
      //SI4432_Write (0x33, 0x42);
      // 7 Reserved Reserved.
    //;6:4 hdlen[2:0] Header Length.
    //;Length of header used if packet handler is enabled for RX (enpacrx). Headers are
    //;received in descending order.
    //;000: No RX header
    //;001: Header 3
    //;010: Header 3 and 2
    //;011: Header 3 and 2 and 1
    //;100: Header 3 and 2 and 1 and 0
    //;3 fixpklen Fix Packet Length.
    //;When fixpklen = 1 the packet length (pklen[7:0]) is not included in the header. When fixpklen
    //;= 0 the packet length is included in the header.
    //;2:1 synclen[1:0] Synchronization Word Length.
    //;The value in this register corresponds to the number of bytes used in the Synchronization
    //;Word. The synchronization word bytes are transmitted/received in descending order.
    //;00: Synchronization Word 3
    //;01: Synchronization Word 3 followed by 2
    //;10: Synchronization Word 3 followed by 2 followed by 1
    //;11: Synchronization Word 3 followed by 2 followed by 1 followed by 0
    //;0 prealen[8] MSB of Preamble Length.
    //;See register Preamble Length.
      SI4432_Write ( 0x33, 0x80 ) ; 
      
      
      // "64 nibble = 32 byte preamble" - write this many sets of 1010 before starting real data. NOTE THE LACK OF '0x'
      //write(0x34, 64);
      // "0x35 need to detect 20bit preamble" - not sure why, but this needs to match the preceeding register
      //write(0x35, 0x20);
      SI4432_Write ( 0x34, 0x00 ) ;    // preamble length (min = 1,  0 ==> 1) ;
      SI4432_Write ( 0x35, 0x00 ) ;    //?????????????
      
      // synchronize word - apparently we only set this once?
      //write(0x36, 0x2D);
      //write(0x37, 0xD4);
      //write(0x38, 0x00);
      //write(0x39, 0x00);
      
      // 4 bytes in header to send (note that these appear to go out backward?)
      //write(0x3A, 's');
      //write(0x3B, 'o');
      //write(0x3C, 'n');
      //write(0x3D, 'g');
      
      // Packets will have 1 bytes of real data
      //write(0x3E, 1);
      
      // 4 bytes in header to recieve and check
      //write(0x3F, 's');
      //write(0x40, 'o');
      //write(0x41, 'n');
      //write(0x42, 'g');
      
      // Check all bits of all 4 bytes of the check header
      //write(0x43, 0xFF);
      //write(0x44, 0xFF);
      //write(0x45, 0xFF);
      //write(0x46, 0xFF);
      SI4432_Write ( 0x44, 0x00 ) ;    //?????????????
      SI4432_Write ( 0x45, 0x00 ) ;    //?????????????
      SI4432_Write ( 0x46, 0x00 ) ;    //?????????????

      
      //No channel hopping enabled
      //write(0x79, 0x00);
      //write(0x7A, 0x00);
      
      // Modulation Mode Control 2
      // 7:6 = trclk[1:0] = TX Data Clock Configuration.
      //       00: No TX Data CLK is available (asynchronous mode – Can only work with modulations FSK or OOK).
      //       01: TX Data CLK is available via the GPIO (one of the GPIO’s should be programmed as well).
      //       10: TX Data CLK is available via the SDO pin.
      //       11: TX Data CLK is available via the nIRQ pin
      // 5:4 = dtmod[1:0] = Modulation Source (TX Only).
      //       00: Direct Mode using TX_Data function via the GPIO pin (one of the GPIO’s should be programmed accordingly as well) ;
      //       01: Direct Mode using TX_Data function via the SDI pin (only when nSEL is high) ;
      //       10: FIFO Mode
      //       11: PN9 (internally generated) ;
      // 3 = eninv = Invert TX and RX Data
      // 2 fd[8] MSB of Frequency Deviation Setting, see "Register 72h. Frequency Deviation".
      // 1:0 = modtyp[1:0] = Modulation Type.
      //       00: Unmodulated carrier
      //       01: OOK
      //       10: FSK
      //       11: GFSK (enable TX Data CLK (trclk[1:0]) when direct mode is used) ;
      // RX/TX direct mode, not-invert, OOK
      SI4432_Write ( 0x71, 0x01);


      // frequency deviation from Excel sheet (30 kHz) ;
      //;SI4432_Write ( 0x72, 0x30 ) ;

      // No Frequency Offet is already set by default
      //SI4432_Write ( 0x73, 0x00 ) ;
      //SI4432_Write ( 0x74, 0x00 ) ;
      
      //SI4432_Set_Frequency ( 433920 ) ; ;<<<<<<<<<<<<<<<<
                    

      //resetFIFO();
    }  


    // **************************************************************
    // can be used for both transmitting and receiving
    // **************************************************************
    void SI4432_Init_WS3000_TxRx () {
    /*  
      -- Modulation Type     : FSK
      -- Frequency Deviation : 67.0 [kHz]
      -- Manchester          : OFF
      -- Carrier Frequency   : 868.33 [MHz]
      -- Data Rate           : 17.24 [kb/s]
      -- AFC                 : Enable
      -- Rb Error            : > 1%

      -- ******  FIFO MODE  *****************
      -- Select LSB/MSB First, MSB, Each byte of the Header, Packet Length and Data will be sent MSB first
      -- Select Modulation type:, FSK, This value is set at the Modem Registers Calculations sheet
      -- Select DATA INVERSION, OFF, Operates on the entire data
      -- Select Manchester Enable, OFF, This value is set at the Modem Registers Calculations sheet
      -- Select Manchester Data Inversion, Invert, Manchester is Disabled
      -- TX Clock configuration, 00, No TX Data CLK is available outside the chip
      -- RX Specific Configurations:, DROP Down Menu, Comment
      -- Select Sync Word Length, Sync word 3 & 2, No Need to configure sync Word, default values are available
      -- Configure sync Word 3, 2D, Relevant ONLY for RX side
      -- Configure sync Word 2, D4, Relevant ONLY for RX side
      -- Configure sync Word 1, 00, Relevant ONLY for RX side
      -- Configure sync Word 0, 00, Relevant ONLY for RX side
      -- Select Preamble Detection Threshold (in nibble resolution), 0.0, This means we will evaluate the preamble for 0 bits.
      -- Select Preamble Length (in nibbles resolution) -  (Decimal value between 0 to 511), 4.0, 0.0
      -- Irrelevant Configurations for Direct FIFO Mode, 0.0, 0.0
      -- (no need to configure these), 0.0, 0.0
      -- Enable CRC, NO, Irrelevant in Direct FIFO mode
      -- CRC Over Data Only , YES, CRC is not Enabled
      -- Select CRC TYPE, CRC16-IBM, CRC is not Enabled
      -- Select Manchester Preamble Polarity, 0101 …., Irrelevant in Direct FIFO mode
      -- Select Data Whitening, OFF, Cannot be used in Direct FIFO mode
      -- Select Headers in Packet, NO Header, Irrelevant in direct FIFO mode
      -- Select Variable Packet Length, NO, Irrelevant in direct FIFO mode
    */

      const byte Preamble_Len = 6 ;
      const byte Manchester   = 0 ;
      const unsigned long Rb_Hz       = 17240 ;
      const unsigned long f_dev_Hz    = 67000 ;
      const unsigned long BW_Hz       = 2 * f_dev_Hz + Rb_Hz * ( 1 + Manchester ) ;
      //BW_Mod = 2 * f_Dev + Rb * ( 1 + M )      # more realistic + Excel sheet
      const byte Packet_Len   = 9 ;

      SI4432_Reset () ;

      SI4432_Write ( 0x06, 0x00 ) ;  // Interrupt Enable 2
      SI4432_Write ( 0x07, 0x03 ) ;  // Operating Mode and Function Control 1
                                     // XTal + PLL on
      SI4432_Antenna_Rx () ;
      SI4432_Write ( 0x0D, 0x14 ) ; // GPIO Configuration 2

      // ********************************************************
      // SI4432_Set_BW_FSK ( 2, BW_Hz, Rb_Hz, Manchester, f_dev_Hz )
      // Use Table 2 form the Excel file 
      //    (due to errors table 2 will never be choosen in the Excel sheet) 
      // results in
      // ********************************************************
      SI4432_Write ( 0x1C, 0x0B ) ; // IF Bandwidth
                                     // 7   = dwn3_bypass, Bypass Decimator by 3 (if set)
                                     // 6:4 = ndec_exp = IF Filter Decimation Rates
                                     // 3:0 = filset
      SI4432_Write ( 0x20, 0xE8 ) ; // Clock Recovery Oversampling Rate
      SI4432_Write ( 0x21, 0x00 ) ; // Clock Recovery Offset 2
      SI4432_Write ( 0x22, 0x8D ) ; // Clock Recovery Offset 1
      SI4432_Write ( 0x23, 0x3A ) ; // Clock Recovery Offset 0
      SI4432_Write ( 0x24, 0x10 ) ; // Clock Recovery Timing Loop Gain 1
      SI4432_Write ( 0x25, 0x4A ) ; // Clock Recovery Timing Loop Gain 0

      // wordt even later 0x2A gezet SI4432_Write ( 0x2E, 0x2B ) ; // Slicer Peak Holder


      SI4432_Write ( 0x1D, 0x40 ) ; // AFC Loop Gearshift Override 00xx xxxx?
      SI4432_Write ( 0x1E, 0x0A ) ;
      SI4432_Write ( 0x2A, 0x30 ) ; // AFC Limiter
      // not according to the AN440, but from the Excel sheet
      // D21 = IF(H7=0,"03","00"),  where H7 = Rb Error > 1 %
      SI4432_Write ( 0x1F, 0x00 ) ; //  
      SI4432_Write ( 0x69, 0x60 ) ; //
      // ********************************************************
      // ********************************************************

      SI4432_Write ( 0x2C, 0x28 ) ; // OOK Counter Value 1
      SI4432_Write ( 0x2D, 0x48 ) ; // OOK Counter Value 2
      SI4432_Write ( 0x2E, 0x2A ) ; // Slicer Peak Holder

      SI4432_Write ( 0x30, 0xA8 ) ;  // Data Access Control (Packet handling)
                                     // 7  = 1  = Enable Rx Packet handling
                                     // 6  = 0  = LSB first
                                     // 5  = 1  = CRC Data Only
                                     // 4  = 0  = skip2ph
                                     // 3  = 1  = Enable Tx Packet handling
                                     // 2  = 0  = CRC Enable
                                     // 10 = 00 = CRC Polynome 
      
      SI4432_Write ( 0x32, 0x00 ) ;  // Header Control 1
                                     // 7654 = Broadcast address
                                     // 3210 = Received header check
      
      SI4432_Write ( 0x33, 0x0A ) ;  // 0000_0110   Header Control 2
                                     // 7   = 0   = skipsyn
                                     // 654 = 000 = hdlen
                                     // 3   = 1   = fxpklen
                                     // 21  = 01  = synclen = 2 bytes
                                     // 0   = 0   = MSB of preamble length
      
      SI4432_Write ( 0x34, 64 ) ;   // Preamble Length
      
      SI4432_Write ( 0x35, ( Preamble_Len << 3 ) ) ; // Preamble Detection Control
                                     // 76543 = 4 = preamble detection treshold
                                     // 210   = 0 = RSSI offset = 0*4dB
                                     //   RSSI Offset probably only visual effect
      
      SI4432_Write ( 0x3E, Packet_Len ) ;  // Packet length 
      
      SI4432_Write ( 0x6E, 0x9D )  ; // TX Data Rate 1    19.2 kHz
      SI4432_Write ( 0x6F, 0x49 )  ; // TX Data Rate 0    19.2 kHz

      
      SI4432_Write ( 0x70, 0x20 ) ;  // Modulation Mode Control 1 (Manchester/whitening)
                                     // 5  = 1 = Set this if Datarate < 30 kbps
                                     // 3  = x = manchester inversion
                                     
      SI4432_Write ( 0x71, 0x22 ) ;  // Modulation Mode Control 2
                                     // 76 = 00 = No Tx clock on pins
                                     // 54 = 10 = FIFO mode
                                     // 3  = 0  = Invert Tx, Rx data
                                     // 2  = 0  = MSB of reg 0x72
                                     // 10 = 10 = FSK
      
      SI4432_Write ( 0x72, 0x6B ) ; // Frequency deviation  67 kHz
      
      SI4432_Write ( 0x75, 0x73 ) ; // Frequency Band Select
      SI4432_Write ( 0x76, 0x68 ) ; // Nominal Carrier Frequency
      SI4432_Write ( 0x77, 0x20 ) ; // Nominal Carrier Frequency  868.33

      SI4432_Write ( 0x79, 0x00 ) ; // No hop channel select
      SI4432_Write ( 0x7A, 0x00 ) ; // hop stepsize
      SI4432_Write ( 0x73, 0x00 ) ; // No Frequency Offset
      SI4432_Write ( 0x74, 0x00 ) ; // No Frequency Offset

      SI4432_Write ( 0x58, 0x80 ) ; // this is a reserved word ???   !!!!
    }


    // **************************************************************
    void SI4432_Spectrum_Analyzer () {
      unsigned long Freq  = 421120000 ; // at 100kHz step, center freq = 433920
      Serial_Write_Byte ( 0xBB ) ;
      Serial_Write_Byte ( 0xBB ) ;
      Serial_Write_Long ( Freq ) ;
      
      unsigned long FStep_kHz  = 100 ;
      word  NSamp      = 10;
      unsigned long BW         = 100 * FStep_kHz ;
      byte Temp_Delay  = 90 ;
      const  int  NStep       = 256 ;
      byte Mode        = 2 ;
      byte Time_Sweep  = 0 ;
      byte Measurement = 0 ;
      word WCarrier ;
      byte Smart_Treshold ;
      byte Data ;
      byte RS232 ;
      unsigned long Value ;
      byte RSSI_Reg = 0x26 ;
      
byte Test = 0 ;

      this->SI4432_Init () ;

      
      while ( true ) {
        if ( Time_Sweep == 0 ) {
          SI4432_Set_Frequency ( Freq ) ;           // Start Frequemcy

          SI4432_Set_BW_FSK_0 ( 0, BW ) ;           // IF Bandwidth in Hz
          SI4432_Write  ( 0x7A, FStep_kHz / 10 ) ;  // step size in 10 kHz units
        
          Smart_Treshold = 3 * NSamp / 2 ;
          
          WCarrier = Carrier & 0xFFFF ;
          if ( FStep_kHz <= 5 ) {
            SI4432_Write ( 0x79, 0 ) ;
          }
        }  
        else if ( Time_Sweep < 10 ){
          SI4432_Set_Frequency ( Freq ) ;      // Start Frequemcy
          SI4432_Write ( 0x79, 0 ) ;           // Step Number
          Time_Sweep = Time_Sweep + 10 ;
        }
        
        Serial.write ( 0xAA ) ;
        Serial.write ( 0xBB ) ;
        Serial.write ( 0xCC ) ;
      
        for ( int i=0; i<NStep; i++ ) {
          if ( Time_Sweep == 0 ) {
            if ( FStep_kHz > 5 ) SI4432_Write ( 0x79, i ) ;
            else {
              SI4432_Set_Carrier ( WCarrier ) ;
              if      ( FStep_kHz == 0 ) WCarrier = WCarrier + 1 ;
              else if ( FStep_kHz == 1 ) WCarrier = WCarrier + 2 ;
              else if ( FStep_kHz == 2 ) WCarrier = WCarrier + 4 ;
              else if ( FStep_kHz == 3 ) WCarrier = WCarrier + 8 ;
              else if ( FStep_kHz == 4 ) WCarrier = WCarrier + 16 ;
              else                        WCarrier = WCarrier + 32 ;
            }
          }

          byte min = 255 ;
          byte max = 0 ;
          unsigned int  avg = 0 ;
          byte Nmax = 0 ;
          byte RSSI ;
      
          // after setting another channel, it's necessary to wait about 
          // 1.5 to 2 msec to stabilize the oscillator
          // This delay was derived from some tests with the py-spectrum-analyzer.
          if ( Time_Sweep == 0 ) {
            delayMicroseconds ( 2*10*Temp_Delay ) ;
          }
      
          // the next loop takes about 75 msec for NSamp=10  and NStep=256
          for ( int ii=0; ii<NSamp; ii++ ) {
            RSSI = SI4432_Read ( RSSI_Reg ) ; //0x26 ) ;
            //delayMicroseconds ( 10 ) ;    //doesn't improve averaging
//RSSI = 20 + 10 * _Serial_State ;
//RSSI = 10*Test ; //Serial.available () ;
            if ( RSSI > max ) {
              max  = RSSI ;
              Nmax = Nmax + 1 ;
            }
            if ( RSSI < min ) min = RSSI ;
            avg = avg + RSSI ;
          }
      
          avg = avg / NSamp ;
          if      ( Mode == 0 ) Measurement = RSSI ; // last sample
          else if ( Mode == 1 ) Measurement = avg ;
          else if ( Mode == 2 ) Measurement = max ;
          else if ( Mode == 3 ) Measurement = min ;
          else {
            if ( Nmax >= Smart_Treshold ) Measurement = max ;
            else {
              if ( i % 2 == 0 ) Measurement = max ;
              else              Measurement = min ;
            }      
          }  
          Serial.write ( Measurement ) ;
        }
      
      
        // **************************************************************************** 
        // **************************************************************************** 
        if ( this->Serial_Poll () > 0 ) {
        // **************************************************************************** 
          RS232 = _Serial_Commands [0] ;
          //RS232 = 0 ; // ALL SERIAL COMMANDS WILL BE IGNORED FOR THE MOMENT
          
          // ******************************
          // Set Frequency
          // ******************************
          if ( RS232 == 0xB0 ) { 
            if ( _Serial_State > 4 ) {
//Test +=1 ;//= Data ;
              Value = _Serial_Commands [1]  ;
              Value = Value << 8 |  _Serial_Commands [2]  ;
              Value = Value << 8 |  _Serial_Commands [3]  ;
              Value = Value << 8 |  _Serial_Commands [4]  ;
              Freq  = Value ;
              if ( Time_Sweep > 10 ) Time_Sweep -= 10 ; // so Frequency will be recalculated
              _Serial_State = -1 ;
              #ifdef SI4432_Debug 
                Serial.printf ( "CMD: Set Frequency = %i\n", Freq ) ;
              #endif
            }
          }
          // ******************************
          // Set Frequency Stepsize
          // ******************************
          else if (  RS232 == 0xAF ) { 
//Test +=1 ;//= Data ;
            if ( _Serial_State > 1 ) {
              Data = _Serial_Commands[1] ;
              if       ( Data == 0x00 ) FStep_kHz =  0 ;
              else if ( Data == 0x01 ) FStep_kHz =  1 ;
              else if ( Data == 0x02 ) FStep_kHz =  2 ;
              else if ( Data == 0x03 ) FStep_kHz =  3 ;
              else if ( Data == 0x04 ) FStep_kHz =  4 ;
              else if ( Data == 0x05 ) FStep_kHz =  5 ;
              else if ( Data == 0x06 ) FStep_kHz =  10 ;
              else if ( Data == 0x07 ) FStep_kHz =  20 ;
              else if ( Data == 0x08 ) FStep_kHz =  50 ;
              else if ( Data == 0x09 ) FStep_kHz =  100 ;
              else if ( Data == 0x0A ) FStep_kHz =  200 ;
              else if ( Data == 0x0B ) FStep_kHz =  500 ;
              else if ( Data == 0x0C ) FStep_kHz =  1000 ;
              else if ( Data == 0x0D ) FStep_kHz =  2000 ;
              _Serial_State = -1 ;
              #ifdef SI4432_Debug 
                Serial.printf ( "CMD: Set Step = %i\n", FStep_kHz ) ;
              #endif
            }
          }
          // **************************************************
          // here are starting all the one byte commands
          // **************************************************
          else {
            // ******************************
            // reset + init
            // ******************************
            if (  RS232 == 0xF0 ) { 
              this->SI4432_Reset () ;
              this->SI4432_Init () ;
            }
            // ******************************
            // return OK-Test
            // ******************************
            else if (  RS232 == 0xF2 ) SI4432_Hangup_Test_Serial () ;
              
            // ******************************
            // Set the IF-Bandwidth
            //;  2600,2800,3100,3200,3700,4200,4500,4900,5400,5900,
            //; Datas below 5000 don't seems to work
            // ******************************
            else if ( RS232 == 0x10 ) { BW = 2000   ; Temp_Delay = 250 ; } 
            else if ( RS232 == 0x11 ) { BW = 5000   ; Temp_Delay = 175 ; }
            else if ( RS232 == 0x12 ) { BW = 10000  ; Temp_Delay = 90  ; }
            else if ( RS232 == 0x13 ) { BW = 20000  ; Temp_Delay = 65  ; }
            else if ( RS232 == 0x14 ) { BW = 50000  ; Temp_Delay = 35  ; }
            else if ( RS232 == 0x15 ) { BW = 100000 ; Temp_Delay = 25  ; }
            else if ( RS232 == 0x16 ) { BW = 200000 ; Temp_Delay = 15  ; }
            else if ( RS232 == 0x17 ) { BW = 500000 ; Temp_Delay = 15  ; }
      
            // ******************************
            // Set the number of samples for each bin
            // ******************************
            else if ( RS232 == 0x20 ) { NSamp = 10  ; Time_Sweep = 0 ; }
            else if ( RS232 == 0x21 ) { NSamp = 20  ; Time_Sweep = 0 ; }
            else if ( RS232 == 0x22 ) { NSamp = 50  ; Time_Sweep = 0 ; }
            else if ( RS232 == 0x23 ) { NSamp = 100 ; Time_Sweep = 0 ; }
            else if ( RS232 == 0x24 ) { NSamp = 10  ; Time_Sweep = 1 ; }
            else if ( RS232 == 0x25 ) { NSamp = 50  ; Time_Sweep = 1 ; }
            else if ( RS232 == 0x26 ) { NSamp = 250 ; Time_Sweep = 1 ; }
      
            // ******************************
            // Set the display mode
            // ******************************
            else if ( RS232 == 0x80 ) Mode = 0 ;
            else if ( RS232 == 0x81 ) Mode = 1 ;
            else if ( RS232 == 0x82 ) Mode = 2 ;
            else if ( RS232 == 0x83 ) Mode = 3 ;
            else if ( RS232 == 0x84 ) Mode = 4 ;
      
      
            // ******************************
            // The desktop program has some extra buttons
            // X90 .. x94 which can be used for test purposes
            // ******************************
            else if ( RS232 == 0x90 ) SI4432_Antenna_Tx () ; 
            else if ( RS232 == 0x91 ) SI4432_Antenna_Rx () ;
            else if ( RS232 == 0x92 ) RSSI_Reg = 0x26 ;
            else if ( RS232 == 0x93 ) RSSI_Reg = 0x27 ;
            else if ( RS232 == 0x94 ) RSSI_Reg = 0x28 ;
            
            // *********************
            // clear serial buffer
            // *********************
            _Serial_State = -1 ;
          }
        }
        // ********************************************************************
        // end serial poll
        // ********************************************************************
      }
    }



    // **************************************************************
    // This is a special procedure for the WS3000 weather station
    // it can not be achieved by the normal packet handler routines,
    // because the packet is sent a numerous times
    // **************************************************************
    bool SI4432_WS3000_Loop_OLD () {

SI4432_Init_WS3000_TxRx () ;

      const byte Packet_Len   = 9 ; 

      byte R02, R02_Old ;
      byte R03, R03_Old ;
      byte R04, R04_Old ;
      byte RSSI, RSSI_Old ;
      unsigned long N = 0 ;
      byte NN = 0 ;
      byte Table = 0 ;
      byte State     = 0 ;
      byte State_Old = 0 ;
      byte NPacket   = 0 ;

      // start Receiving
      delayMicroseconds ( 20 ) ;     // <<<<<<<<< Necessary !!!!
      SI4432_Write ( 0x07, 0x07 ) ;  // Operating Mode and Function Control 1

      R03_Old = 0x02 ;
      RSSI_Old = 0 ;
      while ( true ) {
        RSSI = SI4432_Read ( 0x26 ) ;
        if ( RSSI > RSSI_Old ) RSSI_Old = RSSI ;
        
        R03 = SI4432_Read ( 0x03 ) ;
        
        // wait till Valid Package GOES high
        //if ( R03 & 0x02 ) & ( ! ( R03_Old & 0x02 ) ) then
        //if (( R03 & 0x02 ) != 0 ) & ( ( R03_Old & 0x02 ) == 0 ) then
        // sometnih different wait till idle    
        R02 = SI4432_Read ( 0x02 ) ;
        if ( ( R02 & 0x03 ) == 0 ) {  
          ///Serial.print ( SI4432_Read ( 0x3E ) ) ;
          ///Serial.print ( " " ) ;
          Serial.print ( R02, HEX ) ;
          Serial.print ( " " ) ;
          delay ( 100 ) ;


          // reenter Receive mode
    //      SI4432_Write ( 0x07, 0x07 )    -- Operating Mode and Function Control 1

          //serial_hw_write ( 0xBB )
          //serial_hw_write ( RSSI_Old )
          //RSSI_Old = 0

          // write RS232 sync pulse
          //if ! Once then
          //  --serial_hw_write ( 0xCC )
          //  --serial_hw_write ( 0xBB )
          //  --serial_hw_write ( 0xAA )
          //end if
          
          // read until RX-FIFO empty (will always be equal to Packet_Len)
          byte CRC  = 0 ;
          //var bit  CB7  at CRC:7
          byte Data ;
          //var bit  B7   at Data:7
          bool  Mix ;
          //for Packet_Len - 1 using i loop
          for ( int i=0; i<Packet_Len-1; i++ ) {
            Data = SI4432_Read ( 0x7F ) ;
            WS3000_Data [i] = Data ;
            #ifdef SI4432_Debug
              Serial.print ( Data ) ;
            #endif
            for ( int ii=0; ii<8; ii++ ) {
              //Mix = ( CB7 ^ B7 ) != 0 ;
              Mix = ( ( CRC & 0x80 ) ^ ( Data & 0x80 ) ) != 0 ;
              CRC = CRC << 1 ;
              if ( Mix ) CRC = CRC ^ 0x31 ;
              Data = Data << 1 ;
            }
            //serial_hw_write ( SI4432_Read ( 0x7F ) )
          }
          
          Data = SI4432_Read ( 0x7F ) ;
          #ifdef SI4432_Debug
            Serial.print ( Data ) ;
            Serial.print ( CRC  ) ;
            Serial.print ( RSSI_Old ) ;
          #endif
          
          // reenter Receive mode
          //SI4432_Write ( 0x07, 0x07 )    -- Operating Mode and Function Control 1
          delay ( 100 ) ;

          // break if good record
          //if ( Data == CRC ) & Once then
          if ( Data == CRC ) return true ;
          
          
          RSSI_Old = 0 ;

          N = 0 ;
          NPacket = NPacket + 1 ;

        }
        R03_Old = R03 ;

        // ************************************************************
        // timeout
        //    0x00130000 is too short
        //    0x00140000 is long enough
        //    0x00150000 will be safe enough
        // ************************************************************
        N = N + 1 ;
        if ( N > 0x00150000 ) {
          N = 0 ;
Serial.println ( "Timeout ..." ) ;
          return false ;
        }

      }
    }


    // ********************************************************
    // Try to read Packet_Len bytes from SI4432
    // IF not enough bytes, stop reading and return False
    // TODO::: IF too many bytes, empty buffer
    // IF exactly the right amount of bytes then
    //     IF CRC ok, return True
    // ********************************************************
    bool Read_Packet () {
      const byte Packet_Len   = 9 ;
      // read until RX-FIFO empty (will always be equal to Packet_Len)
      byte CRC  = 0 ;
      byte Data ;
      bool  Mix ;                       
      for ( int i=0; i<Packet_Len-1; i++ ) {
      //for Packet_Len - 1 using i loop
        
        if (( SI4432_Read ( 0x02 ) & 0x20 ) != 0 ) {     // FIFO empty
//Serial.println ( " empty1 " ) ;
//Serial.print ( "1" ) ;
          return false ;
        }
//Serial.println ( "FIFO >>>" ) ;
        Data = SI4432_Read ( 0x7F ) ;
        WS3000_Data [i] = Data ;
#ifdef DEBUG
  Serial_Write_Byte ( Data ) ;
#endif
        for ( int b=0; b<8; b++ ) {
          //Mix = CB7 ^ B7 ;
          //Mix = ( CRC & 0x80 ) ^ ( Data & 0x80 ) != 0 ;
          Mix = (( CRC ^ Data ) & 0x80 ) != 0 ;
  
          CRC = CRC << 1 ;
          if ( Mix ) {
            CRC = CRC ^ 0x31 ;
          }
          Data = Data << 1 ;
        }
      }
      
      if ( ( SI4432_Read ( 0x02 ) & 0x20 ) != 0 ) {     // FIFO empty
        Serial.println ( " empty2 " ) ;
        return false ;
      }
      Data = SI4432_Read ( 0x7F ) ;
#ifdef DEBUG
  Serial.print ( Data ) ;
  Serial.print ( " CRC " ) ;
  Serial.println ( CRC  ) ;
  if ( Data != CRC ) {
    for ( int i=0; i<Packet_Len-1; i++ ) {
      Serial.print ( " " ) ;
      Serial.print ( WS3000_Data[i] ) ;
    }
  }
#endif

      // ********************************      
      // toegevoegd flush buffer
      // ********************************  
      /*
      byte Temp ;      
      while (( SI4432_Read ( 0x02 ) & 0x20 ) == 0 ) {     // FIFO not empty
        Serial.print ( ":" ) ;
        Temp = SI4432_Read ( 0x7F ) ;
        Serial.print ( Temp ) ;
      }
      */
      
      //if ( Data == CRC ) return true ;
      //else               return false ;
      return Data == CRC ;
    }

    // **************************************************************
    // This is a special procedure for the WS3000 weather station
    // it can not be achieved by the normal packet handler routines,
    // because the packet is sent a numerous times
    // **************************************************************
    bool SI4432_WS3000_Loop () {

      byte R02, R02_Old ;
      byte R03, R03_Old ;
      byte R04, R04_Old ;
      byte RSSI ;
      unsigned long N = 0 ;
      byte NN = 0 ;
      byte Table = 0 ;
      byte State     = 0 ;
      byte State_Old = 0 ;
      byte NPacket   = 0 ;

      // ********************************************************
      // ********************************************************
      const byte N_Retries_Seconds = 55 ;  
      const byte N_Restarts_Start  = 1  ;
      // ********************************************************
      // ********************************************************
SI4432_Init_WS3000_TxRx () ;

      byte N_Restarts = N_Restarts_Start ;
      while ( N_Restarts > 0 ) {
        // start Receiving
        delayMicroseconds ( 20 ) ;             // <<<<<<<<< Necessary !!!!
        SI4432_Write ( 0x07, 0x07 ) ;    // Operating Mode and Function Control 1
        // wait till receiver idle (packet received)
        //var byte N_ReTries = 100
        byte N_ReTries = N_Retries_Seconds ;
        while ( N_ReTries > 0 ) {
          delay ( 1000 ) ;
          R02 = SI4432_Read ( 0x02 ) ;
          if ( ( R02 & 0x03 ) == 0 ) {      // Receiver status is Idle
            if ( Read_Packet () ) {
//Serial.print ( "P" ) ;            
              return true ;
            }
 //??           N_ReTries = 0 ;               // be sure Receiver will be restarted
 N_ReTries = N_ReTries - 1 ;
          }
          else {
            N_ReTries = N_ReTries - 1 ;
            // Serial.print ( 0x33 ) ;;
            // Serial.print ( N_Retries ) ;
          }
        }
        
        N_Restarts = N_Restarts - 1 ;
        Serial.print ( "No Package" ) ; 
      } 

      return false ;
    }

    // ********************************************************
    // Can be used for both Transmit and Receive
    // all registers are hand-optimized
    // ********************************************************
    void SI4432_Init_KAKU () {
      // Modulation Type    : OOK
      // Manchester         : OFF
      // Carrier Frequency  : 433.92 [MHz]
      // Data Rate          : 3.85 [kb/s]
      // Receiver Bandwidth : 600.0 [kHz]
      const byte Packet_Len = 35 ;

      SI4432_Reset () ;

      SI4432_Write ( 0x06, 0x00 ) ;    // Interrupt Enable 2
      SI4432_Write ( 0x07, 0x07 ) ;    // Operating Mode and Function Control 1
      SI4432_Antenna_Rx () ;
      SI4432_Write ( 0x0D, 0x14 ) ;    // GPIO Configuration 2

      SI4432_Write ( 0x1C, 0xAE ) ;    // IF Filter Bandwidth
      SI4432_Write ( 0x1D, 0x40 ) ;    // AFC Loop Gearshift Override 00xx xxxx?
      SI4432_Write ( 0x1F, 0x00 ) ;    // Clock Recovery Gearshift Override
      SI4432_Write ( 0x20, 0x0B ) ;    // Clock Recovery Oversampling Rate
      SI4432_Write ( 0x21, 0x60 ) ;    // Clock Recovery Offset 2
      SI4432_Write ( 0x22, 0x2A ) ;    // Clock Recovery Offset 1
      SI4432_Write ( 0x23, 0x0D ) ;    // Clock Recovery Offset 0
      SI4432_Write ( 0x24, 0x10 ) ;    // Clock Recovery Timing Loop Gain 1
      SI4432_Write ( 0x25, 0x2C ) ;    // Clock Recovery Timing Loop Gain 0

      SI4432_Write ( 0x2A, 0x2C ) ;    // AFC Limiter
      ;SI4432_Write ( 0x2C, 0x29 ) ;    // OOK Counter Value 1
      SI4432_Write ( 0x2C, 0x1A ) ;    // OOK Counter Value 1
      SI4432_Write ( 0x2D, 0x44 ) ;    // OOK Counter Value 2
      ;SI4432_Write ( 0x2E, 0x2B ) ;    // Slicer Peak Holder
      SI4432_Write ( 0x2E, 0x0F ) ;    // OOK Peak detector attack = 000
                                     // OOK Peak detector decay  = 1111 

      SI4432_Write ( 0x30, 0x21 ) ;    // Data Access Control (Packet handling) ;
      SI4432_Write ( 0x33, 0x0A ) ;    // Header Control 2
      ;SI4432_Write ( 0x33, 0x80 ) ;    // no effect
      SI4432_Write ( 0x34, 0x00 ) ;    // Preamble Length
      SI4432_Write ( 0x35, 0x02 ) ;    // Preamble Detection Control
      ;SI4432_Write ( 0x35, 0x00 ) ;    // probably ony effect because treshold used in detection
      SI4432_Write ( 0x3E, Packet_Len ) ;   // Packet length 

      SI4432_Write ( 0x69, 0x60 ) ;    // AGC Override 1 (if bit5=1: reads LNA Gain) ;
      SI4432_Write ( 0x6E, 0x1F ) ;    // TX Data Rate 1
      SI4432_Write ( 0x6F, 0x8A ) ;    // TX Data Rate 0
      SI4432_Write ( 0x70, 0x24 ) ;    // Modulation Mode Control 1
      SI4432_Write ( 0x71, 0x21 ) ;    // Modulation Mode Control 2

    ;
    ;  SI4432_Write ( 0x72, 0x30 ) ;    // 
              

      SI4432_Write ( 0x75, 0x53 ) ;    // Frequency Band Select
      SI4432_Write ( 0x76, 0x62 ) ;    // Nominal Carrier Frequency
      SI4432_Write ( 0x77, 0x00 ) ;    // Nominal Carrier Frequency

      SI4432_Write ( 0x6D, 0x0F ) ;    // Maximum transmit power
    }


    // **************************************************************
    // Address - the full 32 bit (so including Unit, On/Off and Group)
    // **************************************************************
    void SI4432_KAKU_Write ( byte Address [4], 
                             bool On_Off, 
                             bool Group,
                             byte Repeat_Count ) {
      // ******************************************
      // because Address is passed by reference
      // and we change the On/Off bit here, 
      // we must change it for both On and Off
      // ******************************************
      if ( On_Off ) Address[3] = Address[3] | 0x10 ;
      else          Address[3] = Address[3] & 0xEF ;

      // ******************************************
      // the same as above yields for the Group bit
      // ******************************************
      if ( Group ) Address[3] = Address[3] | 0x20 ;
      else         Address[3] = Address[3] & 0xDF ;

      // ******************************************
      // ******************************************
      for ( int ii=0; ii<Repeat_Count; ii++ ) {
        //CSN    = Low ;
        //SSPBUF = 0x7F | 0x80 ;       // write to Tx-Stack
        //SSPIF  = false ;
        //while ( ! SSPIF ) ;

      	digitalWrite ( SS, LOW ) ;
        SPI.transfer ( 0x7F | 0x80 ) ;
      
        // ************************
        // start bit
        // ************************
        //SSPBUF = 0x04 ;
        //SSPIF  = false ;
        //while ( ! SSPIF ) ;
        SPI.transfer ( 0x04 ) ;
        
        
        //SSPBUF = 0x00 ;
        //SSPIF  = false ;
        SPI.transfer ( 0x00 ) ;

        // ************************
        // Data bits
        // ************************
        for ( int i=0; i<4; i++) {
          byte Data = Address [i] ;
          for ( int iii=0; iii<8; iii++) {
            //while ( ! SSPIF ) ;
            //if ( Data & 0x80 ) SSPBUF = 0x82 ;
            //else               SSPBUF = 0xA0 ;
            if ( Data & 0x80 ) SPI.transfer ( 0x82 ) ;
            else               SPI.transfer ( 0xA0 ) ;
            //SSPIF = false ;
            Data = Data << 1 ;
          }
        }
        //while ( ! SSPIF ) ;

        // ************************
        // stop bit
        // ************************
        //SSPBUF = 0x80 ; 
        //SSPIF  = false ;
        //while ( ! SSPIF ) ; 
        SPI.transfer ( 0x80 ) ;
        
        //CSN = high ;
      	digitalWrite ( SS, HIGH ) ;
        
        SI4432_Write ( 0x07, 0x0B ) ;   // Transmit <<<<<<<<<<<<<<<<<<<<<<

        // wait for transmission is ready, VERY IMPORTANT
        while ( SI4432_Read ( 0x07 ) != 0x03 ) ;
       

        // ***************************************************
        // now extend the sync bit, 7 ==> 11 msec
        // ***************************************************
        delay ( 7 ) ;
      }
    }


    // **************************************************************
/* OPBOUW VAN DE OVER TE ZENDEN DATA
we've 2 unsigned words (16 bit), the high period and the low period
To create a trigger signal we use only 7 bits of each byte for the data 
and in one of the 5 bytes we place a "1" at the remaining bit


Data Masks

LSB: 0000 0000 0111 1111  
MSB: 0011 1111 1000 0000

LSB_Data =   Word << 1 
MSB_Data = ( Word & 0x3F80 ) >> 6

*/
    // **************************************************************
    // Generate some test patterns
    // The testpattern can be changed through the serial port
    // **************************************************************
    void SI4432_Generate_KAKU () {
      byte Mode = 4 ;
      byte RS232 ;
 
      // The address is  00_1110_0001_1100_0101_0000_0010  = 0x0_E1_C5_02
      // Group = 0
      // On / Off
      // And the Units value
      // A = 1010
      // B = 1011
      // combining the above gives 4 bytes 
 
      // AAAA AAAA AAAA AAAA AAAA AAAA AAGO UUUU
      // 0011_1000_0111_0001_0100_0000_100x_1010  where x=On/Off
 
      byte KAKU_1 [] = { 0x38, 0x71, 0x40, 0x8A } ;
      byte KAKU_2 [] = { 0x38, 0x71, 0x40, 0x8B } ;
      byte KAKU_4 [] = { 0xAA, 0x00, 0xFF, 0x55 } ;
      bool Group     = false  ;
 
      while ( true ) {
 
        // test: continuous A1-On ;
        if ( Mode == 0 ) SI4432_KAKU_Write ( KAKU_1, true, Group, 250 ) ;
 
        // test: continuous A1-Off ;
        else if ( Mode == 1 ) SI4432_KAKU_Write ( KAKU_1, false, Group, 250 ) ;
 
        // toggle A1 On/Off   ;
        else if ( Mode == 2 ) {
          SI4432_KAKU_Write ( KAKU_1, true, Group, 20 ) ;
          delay ( 2000 ) ;
          SI4432_KAKU_Write ( KAKU_1, false, Group, 20 ) ;
          delay ( 2000 ) ;
        }
        // sweep A1, A2     ;
        else if ( Mode == 3 ) {
          SI4432_KAKU_Write ( KAKU_1, true, Group, 20 ) ;
          delay ( 500 ) ;
          SI4432_KAKU_Write ( KAKU_2, true, Group, 20 ) ;
          delay ( 500 ) ;
 
          SI4432_KAKU_Write ( KAKU_1, false, Group, 20 ) ;
          delay ( 500 ) ;
          SI4432_KAKU_Write ( KAKU_2, false, Group, 20 ) ;
          delay ( 500 ) ;
        }
        else if ( Mode == 4 ) {
          SI4432_KAKU_Write ( KAKU_4, true, Group, 20 ) ;
          delay ( 100 ) ;
        }

       /*
        if serial_hw_read ( RS232 ) then ;
          if RS232 == 0xFA then ;
            -- wait until the real databyte is received ;
            RS232 = serial_hw_data ;
 
            if    RS232 == 0x90 then Mode = 0 ;
            elsif RS232 == 0x91 then Mode = 1 ;
            elsif RS232 == 0x92 then Mode = 2 ;
            elsif RS232 == 0x93 then Mode = 3 ;
            end if ;
          end if ;
        end if ;
        */
        // ********************************** 
        // ********************************** 
        if ( this->Serial_Poll () > 0 ) {
          RS232 = _Serial_Commands [0] ;
          if      (  RS232 == 0x90 )  Mode = 0 ;
          else if (  RS232 == 0x91 )  Mode = 1 ;
          else if (  RS232 == 0x92 )  Mode = 2 ;
          else if (  RS232 == 0x93 )  Mode = 3 ;
          _Serial_State = -1 ;
        }
      }
    }
 

    // **************************************************************
    void SI4432_OOK_Stream_Viewer () {
      const int uS_Delay = 8 ; //was 8
      word  N ;
      byte  RS232 ;

      this->SI4432_Init_KAKU () ;
      //this->SI4432_Init () ;

      this->SI4432_Write ( 0x0D, 0x14 ) ;    // GPIO-2 = RX-data
      //this->SI4432_Write ( 0x1C, 0x81 ) ;    // IF Bandwidth
      
      this->SI4432_Read_Status () ;
      
      //*
      pinMode ( SI4432_GPIO2_Pin, INPUT_PULLUP  ) ;
      attachInterrupt ( SI4432_GPIO2_Pin, _OOK_Int , CHANGE  ) ;
      
      // moet netter via een circular buffer
      while ( true ) {
        while ( _OOK_RP != _OOK_WP ) {
          N = _OOK_Buffer [ _OOK_RP ] / 10 ;
          Serial.write ( ( ( N & 0x3F80 ) >> 6 ) | 1 ) ;
          Serial.write ( N << 1 ) ;
          
          N = _OOK_Buffer [ _OOK_RP + 1 ] / 10 ;
          Serial.write ( ( ( N & 0x3F80 ) >> 6 )     ) ;
          Serial.write ( N << 1 ) ;
          
          _OOK_RP += 2  ;
          _OOK_RP %= 32 ;
        }  
        /*
        if ( _OOK_Count > 0 ) {
          N = _OOK_High / 10 ;
          Serial.write ( ( ( N & 0x3F80 ) >> 6 ) | 1 ) ;
          Serial.write ( N << 1 ) ;
          N = _OOK_Low / 10 ;
          Serial.write ( ( ( N & 0x3F80 ) >> 6 )     ) ;
          Serial.write ( N << 1 ) ;
          _OOK_Count = 0 ;
        } 
        */        
      
      //*/      
          

      /*
      while ( true ) {
        N = 0 ;
        while ( digitalRead ( _GPIO2_Pin ) ) {
          N += 1 ;
          delayMicroseconds ( uS_Delay ) ;
        } 
        Serial.write ( ( ( N & 0x3F80 ) >> 6 ) | 1 ) ;
        Serial.write ( N << 1 ) ;

        N = 0 ;
        while ( not digitalRead ( _GPIO2_Pin ) ) {
          N += 1 ;
          delayMicroseconds ( uS_Delay ) ;
        } 
        Serial.write ( ( ( N & 0x3F80 ) >> 6 )     ) ;
        Serial.write ( N << 1 ) ;
      //*/
        
      /*
      while ( true ) {
        N = 0 ;
        while ( digitalRead ( _GPIO2_Pin ) ) {
          N += 1 ;
          delayMicroseconds ( uS_Delay ) ;
        } 
        Serial.write ( ( ( N & 0x3F80 ) >> 6 ) | 1 ) ;
        Serial.write ( N << 1 ) ;

        N = 0 ;
        while ( not digitalRead ( _GPIO2_Pin ) ) {
          N += 1 ;
          delayMicroseconds ( uS_Delay ) ;
        } 
        Serial.write ( ( ( N & 0x3F80 ) >> 6 )     ) ;
        Serial.write ( N << 1 ) ;
      //*/
      
      /*
      unsigned long Last_Time = micros() ;
      while ( true ) {
        if ( micros() > Last_Time + 2000 ) {
          Last_Time = micros() ;
          N = 100 ;
          Serial.write ( ( ( N & 0x3F80 ) >> 6 ) | 1 ) ;
          Serial.write ( N << 1 ) ;
//MSB_Data = ( Word & 0x3F80 ) >> 6
//LSB_Data =   Word << 1 

          N = 50 ;
          Serial.write ( ( ( N & 0x3F80 ) >> 6 )     ) ;
          Serial.write ( N << 1 ) ;

        }  

      //*/


      
        // **************************************************************************** 
        // **************************************************************************** 
        if ( this->Serial_Poll () > 0 ) {
        // **************************************************************************** 
          RS232 = _Serial_Commands [0] ;

          // ******************************
          // The desktop program has some extra buttons
          // X90 .. x94 which can be used for test prurposes
          // These buttons sends code 0xFA + 0x90 ... 0x94
          // ******************************
          uint8_t Address = 0x1C ;
          if       ( RS232 == 0x90 ) SI4432_Write ( Address, 0x32 ) ;
          else if ( RS232 == 0x91 ) SI4432_Write ( Address, 0x22 ) ;
          else if ( RS232 == 0x92 ) SI4432_Write ( Address, 0x12 ) ;
          else if ( RS232 == 0x93 ) SI4432_Write ( Address, 0x05 ) ;
          else if ( RS232 == 0x94 ) SI4432_Write ( Address, 0x8E ) ;

          //if       ( RS232 == 0x90 ) SI4432_Write ( 0x70, 0x20 ) ;
          //else if ( RS232 == 0x91 ) SI4432_Write ( 0x70, 0x00 ) ;
          //else if ( RS232 == 0x92 ) SI4432_Write ( 0x69, 0x70 ) ;
          //else if ( RS232 == 0x93 ) SI4432_Write ( 0x69, 0x4C ) ;
          //else if ( RS232 == 0x94 ) SI4432_Write ( 0x69, 0x4F ) ;

          // *********************
          // clear serial buffer
          // *********************
          _Serial_State = -1 ;
        } 
      }
    }
 
    // **************************************************************
    void QIA_OOK_Stream_Viewer () {
      word  N ;

      pinMode ( SI4432_QIA_Rec_Pin, INPUT  ) ;
      attachInterrupt ( SI4432_QIA_Rec_Pin, _QIA_OOK_Int , CHANGE  ) ;
/*
_OOK_RP = 2 ;      
Serial.print ( "Connected " ) ;
Serial.print ( SI4432_QIA_Rec_Pin ) ;
Serial.print ( " ");
Serial.print ( _OOK_WP ) ;
Serial.print ( " ");
Serial.println ( _OOK_RP ) ;
//*/
      while ( true ) {
        while ( _OOK_RP != _OOK_WP ) {
          N = _OOK_Buffer [ _OOK_RP ] / 10 ;
          Serial.write ( ( ( N & 0x3F80 ) >> 6 ) | 1 ) ;
          Serial.write ( N << 1 ) ;

          N = _OOK_Buffer [ _OOK_RP + 1 ] / 10 ;
          Serial.write ( ( ( N & 0x3F80 ) >> 6 )     ) ;
          Serial.write ( N << 1 ) ;

          _OOK_RP += 2  ;
          _OOK_RP %= _OOK_Size ;
        }  
        yield () ;   // absolutely necessary !!!
      }
    }

    // **************************************************************
    // **************************************************************
    void SI4432_Init_UHF_Generator () {
      this->SI4432_Reset () ;
      this->SI4432_Antenna_Tx () ;
    }

    // **************************************************************
    // **************************************************************
    void SI4432_UHF_Generator () {
      unsigned long Freq      = 434000000 ;
      unsigned long FStep_kHz = 100       ;
      const byte    NStep     = 256       ;
      byte          Step                  ;
      byte          RS232                 ;
      //byte          Mode      = 0         ;
      //byte          Old_Mode  = Mode - 1  ;  // to get started
      int           Mode      = 0         ;
      int           Old_Mode  = Mode - 1  ;  // to get started
      int           Delay     = 100       ;
      bool          OOK_On    = true     ;  
      unsigned long Value                 ;
/*
Old_Mode = 4 ;      
Serial.println ( Old_Mode ) ;
Serial.println ( Mode ) ;
Serial.println ( Delay ) ;
Serial.println ( Step ) ;
Serial.println ( "UHF started2");  
Serial.println ( Old_Mode ) ;
Serial.println ( Mode ) ;
*/     
  
      SI4432_Reset () ;
      SI4432_Init_UHF_Generator () ;
      while ( true ) {
        if ( Mode != Old_Mode ) { 
          // Turn off FSk mode ;
          if ( Old_Mode == 4 ) SI4432_Init_UHF_Generator () ;
          //SI4432_Reset () ;
          //SI4432_Init_UHF_Generator () ;
          
          SI4432_Write ( 0x07, 0x03 ) ;         // Set Tx Mode, Tx = OFF ;
          delay ( 100 ) ;
          
          //if ( Mode == 0 ) SI4432_Write ( 0x07, 0x03 ) ;         // Set Tx Mode, Tx = OFF ;
          //else {  
          if ( Mode != 0 ) {
            SI4432_Set_Frequency ( Freq ) ;         // Start Frequemcy ;
            SI4432_Write ( 0x79, 0 ) ;              // Step Number ;
            SI4432_Write ( 0x7A, (byte)(FStep_kHz/10) ) ; // step size in 10 kHz units ;
            SI4432_Write ( 0x07, 0x0B )           ; // Set Tx Mode, Tx = On ;
Serial.println ( "TX turned ON" ) ;            
          }
          Old_Mode = Mode ;
        }
        
        
         ;
        // ******************************
        //  Sweep Mode ;
        // ******************************
        if ( Mode == 2 ) { 
          delay ( Delay ) ;
          Step = Step + 1 ;
//Serial.print   ( "Sweep Mode ") ;
//Serial.println ( Step ) ; 
          SI4432_Write ( 0x79, Step ) ;
        }
        
        // ******************************
        // OOK Mode   ;
        // ******************************
        else if (  Mode == 3 ) { 
          delay ( Delay ) ;
          if ( OOK_On ) SI4432_Write ( 0x07, 0x03 ) ;   // Set Tx Mode, Tx = OFF 
          else          SI4432_Write ( 0x07, 0x0B ) ;   // Set Tx Mode, Tx = On 
          OOK_On = ! OOK_On ;
          #ifdef SI4432_Debug 
            Serial.printf ( "OOK = %d\n", OOK_On ) ;
          #endif
        }

        // ******************************
        // FSK Mode   ;
        // ******************************
        else if (  ( Mode == 4 ) | ( Mode == 5 ) ) { 
          
          delay ( 1050 ) ;
Serial.println ( "$$" ) ;          
SI4432_Generate_FSK_Block () ;
//          SI4432_Generate_FSK_Block_2 () ;
        }
         
         
        // **************************************************************************** 
        // **************************************************************************** 
        if ( this->Serial_Poll () > 0 ) {
        // **************************************************************************** 
//Serial.print ( ".x");
          RS232 = _Serial_Commands [0] ;
          
          // ******************************
          // Set Frequency
          // ******************************
          if ( RS232 == 0xB0 ) { 
            if ( _Serial_State > 4 ) {
              Value = _Serial_Commands [1]  ;
              Value = Value << 8 |  _Serial_Commands [2]  ;
              Value = Value << 8 |  _Serial_Commands [3]  ;
              Value = Value << 8 |  _Serial_Commands [4]  ;
              Freq  = Value ;
              SI4432_Set_Frequency ( Freq ) ;
              #ifdef SI4432_Debug 
                Serial.printf ( "CMD: Set Frequency = %i\n", Freq ) ;
              #endif
              _Serial_State = -1 ;
            }
          }
          // ******************************
          // Set Frequency Stepsize
          // ******************************
          else if (  RS232 == 0xAF ) { 
            if ( _Serial_State > 1 ) {
              FStep_kHz = 10 * _Serial_Commands[1] ;
              SI4432_Write  ( 0x7A, _Serial_Commands[1] ) ; // step size in 10 kHz units
              #ifdef SI4432_Debug 
                Serial.printf ( "CMD: Set Step = %i\n", FStep_kHz ) ;
              #endif
              _Serial_State = -1 ;
            }
          }
          // ******************************
          // reset + init
          // return all Registers + Ok + JAL-version + AA_BB_CC
          // ******************************
          else if (  RS232 == 0xF0 ) { 
            this->SI4432_Reset () ;
            this->SI4432_Init_UHF_Generator () ;
            this->SI4432_Print_Registers () ;
            Old_Mode = - 1 ;
          }
          // ******************************
          // return OK-Test
          // ******************************
          else if (  RS232 == 0xF2 ) SI4432_Hangup_Test_Serial () ;
            
          // ******************************
          // Tx Power, uses bit3=1, LNA switches closed, 
          // isn't really needed but can not harm
          // ******************************
          else if ( ( RS232 >= 0x80 ) && ( RS232 <= 0x87 ) ) {
            SI4432_Write ( 0x6D, RS232 - 0x80 + 0x08 )   ;
            #ifdef SI4432_Debug 
              Serial.printf ( "CMD: Set Power = %i\n", ( RS232 - 0x80 ) ) ; 
            #endif
          }

          // ******************************
          // Set Mode
          // ******************************
          else if ( ( RS232 >= 0xB1 ) && ( RS232 <= 0xB9 ) ) {
//delay ( 100 ) ;            
            // ******************************
            // On (fixed frequency) / Off
            // ******************************
            if      (  RS232 == 0xB1 ) Mode = 0 ;
            else if (  RS232 == 0xB2 ) Mode = 1 ;

            // ******************************
            // sweep 2 sec / 10 sec
            // ******************************
            else if (  RS232 == 0xB3 ) { 
              Mode  = 2 ;
              Delay = 5  ;
            }
            else if (  RS232 == 0xB4 ) {  
              Mode  = 2 ;
              Delay = 25 ;
            }
            // ******************************
            // OOK 0.5, 5 Hz   
            // ******************************
            else if (  RS232 == 0xB5 ) {  
              Mode = 3  ;
              Delay = 1000 ;
            }
            else if (  RS232 == 0xB6 ) {  
              Mode = 3 ;
              Delay = 100 ;
            }
            // ******************************
            // FSK
            // ******************************
            else if (  RS232 == 0xB7 ) {
Serial.println ( "FSK-1, blijft mogelijk hangen") ;               
              Mode = 4  ;
              SI4432_Init_WS3000_TxRx () ;
Serial.println ( "er door gevallen" ) ;               
            }
            else if (  RS232 == 0xB8 ) { 
Serial.println ( "FSK-1, blijft mogelijk hangen") ;               
              Mode = 5  ;
              SI4432_Init_WS3000_TxRx () ;
//Serial.println ( "FSK-1, blijft mogelijk hangen 2") ;               
              const byte Manchester = 0 ;
              const unsigned long Rb_Hz     = 17240 ;
              const unsigned long f_dev_Hz  = 67000 ;
              const unsigned long BW_Hz     = 2 * f_dev_Hz + Rb_Hz * ( 1 + Manchester )    ;
              //BW_Mod = 2 * f_Dev + Rb * ( 1 + M )   ;   // more realistic + Excel sheet ;
              SI4432_Set_BW_FSK ( 0, BW_Hz, Rb_Hz, Manchester, f_dev_Hz )  ;
Serial.println ( "er door gevallen" ) ;               
            }
            // ******************************
            // KAKU signal, once set it will hang here until reset
            // ******************************
            else if (  RS232 == 0xB9 ) {  
              #ifdef SI4432_Debug 
                Serial.println ( "CMD: KAKU (hangs until reset) " ) ; 
              #endif
              SI4432_Init_KAKU () ;
              SI4432_Generate_KAKU () ;
Serial.println ( "er door gevallen" ) ;               
            }
            #ifdef SI4432_Debug 
              Serial.printf ( "CMD: Set Mode = %i\n", ( RS232 - 0xB1 ) ) ; 
            #endif
          }

          // ******************************
          // The desktop program has some extra buttons
          // X90 .. x94 which can be used for test prurposes
          // These buttons sends code 0xFA + 0x90 ... 0x94
          // ******************************
          else if (  RS232 == 0x90 )  Serial.println ( "CMD: CMD = 0x90" ) ;
          else if (  RS232 == 0x91 )  Serial.println ( "CMD: CMD = 0x91" ) ;
          else if (  RS232 == 0x92 )  Serial.println ( "CMD: CMD = 0x92" ) ;
          else if (  RS232 == 0x93 )  Serial.println ( "CMD: CMD = 0x93" ) ;
          else if (  RS232 == 0x94 )  Serial.println ( "CMD: CMD = 0x94" ) ;

          // *********************
          // clear serial buffer
          // *********************
          //if ( ( RS232 != 0xB0 ) and ( RS232 != 0xAF ) )  _Serial_State = -1 ;
          if ( ( RS232 != 0xB0 ) && ( RS232 != 0xAF ) )  _Serial_State = -1 ;
        } 
      }
    }


    // **************************************************************
    // **************************************************************
    void SI4432_Init_Interactive_Viewer () {
      this->SI4432_Reset () ;

      // 434 MHz ( or 433.92 ???
      this->SI4432_Write ( 0x75, 0x53 ) ;   // Frequency Band Select
      this->SI4432_Write ( 0x76, 0x62 ) ;   // Nominal Carrier Frequency
      this->SI4432_Write ( 0x77, 0x00 ) ;   // Nominal Carrier Frequency
    }

    // **************************************************************
    // **************************************************************
    void SI4432_Interactive_Viewer () {
      byte RS232 ;
      byte Value ;

      this->SI4432_Init_Interactive_Viewer () ;
     
      while ( true ) {
        if ( this->Serial_Poll () > 0 ) {
          RS232 = _Serial_Commands [0] ;

          // ******************************
          // program one of the registers of the SI4432
          // ******************************
          if ( RS232 <= 0x7F ) {
            if ( _Serial_State > 1 ) {
              Value = _Serial_Commands[1] ;
              this->SI4432_Write ( RS232, Value ) ;
              this->_Serial_State = -1 ;
            }
          } 
          else {
            // ******************************
            // reset + init
            // return all Registers + Ok + JAL-version + AA_BB_CC
            // ******************************
            if ( RS232 == 0xF0 ) {
              this->SI4432_Reset                   () ;
              this->SI4432_Init_Interactive_Viewer () ;
              this->SI4432_Dump_Registers          ();
            }
            // ******************************
            // return all Registers + Ok + JAL-version + AA_BB_CC
            // ******************************
            else if ( RS232 == 0xF1 ) {
              this->SI4432_Dump_Registers () ;
            }
            // ******************************
            // return OK-Test
            // ******************************
            else if ( RS232 == 0xF2 ) {
              this->SI4432_Hangup_Test_Serial () ;
            } 
            this->_Serial_State = -1 ;
          }
        }
      }
    }


    // **************************************************************
    // **************************************************************
    private :
      uint8_t _sdnPin, _intPin;
      //uint8_t _GPIO2_Pin ;
      //uint8_t _QIA_Rec_Pin ;

      uint64_t _freqCarrier;
      uint8_t _freqChannel;
      uint16_t _kbps;
      uint16_t _packageSign;
      unsigned long Carrier ;

      byte ndec_exp ; 
      byte dwn3_bypass ;
      byte filset ;

      //bool Serial_Command_Ready = false ;
      int  _Serial_State  = -1  ;
      byte _Serial_Commands [8] ;
      //byte Serial_Data                   ;


    // ***************************************************************      
    // ***************************************************************      
    int Wait_For_ID () {    
      byte Data ;
      int  State = 0 ;
     
      while ( State < 5 ) {      
        if ( Serial.available () ) {
          Data = Serial.read () ;
          if       ( State == 0 ) {
            if ( Data == 0xAA ) State = 1 ;
          }
          else if ( State == 1 )  {
            if ( Data == 0xBB ) State = 2 ;
            else               State = 0 ;
          } 
          else if ( State == 2 )  {
            if ( ( Data >= 0xC0 ) & ( Data <= 0xCF ) ) State = Data ;
          }
        }
      }      
      // Bow echo the ID_String
      Serial.write   ( 0xAA ) ;        
      Serial.write   ( 0xBB ) ;        
      Serial.write   ( State ) ;        
      //Serial.println () ;       
      return State - 0xC0 ;    
    }



    // **************************************************************
    // ********************************************************
    int Serial_Poll () {
      byte Data ;
      if ( Serial.available () ) {
        Data = Serial.read () ;
/*
Serial.print ( "%" ) ; 
Serial.print (_Serial_State,HEX ) ;      
Serial.print ( " " ) ; 
Serial.print ( Serial.available());       
Serial.print ( " " ) ; 
Serial.print ( Data, HEX ) ;        
Serial.print ( " " ) ; 
//*/
        if ( _Serial_State == -1 ) {
          if ( Data == _Serial_Start_Byte ) {
            _Serial_State = 0 ;
          }
        } 
        else if ( _Serial_State < 8 ) {
          _Serial_Commands [ _Serial_State ] = Data ;
          _Serial_State += 1 ;
        }
        
        if ( _Serial_State >= 0 ) {
          while ( Serial.available () ) {
            Data = Serial.read () ; 
            if ( _Serial_State < 8 ) {
              _Serial_Commands [ _Serial_State ] = Data ;
              _Serial_State += 1 ;
            }
          }
        }
//Serial.println (_Serial_State,HEX ) ;      
      } 
      return _Serial_State ; // > 0 ;
    }


};
#endif