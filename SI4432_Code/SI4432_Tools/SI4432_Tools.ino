// ****************************************************************************
// ESP31 dev module
// 240 MHz
// default 4MB, (1.2 MB / 1,5 MB)
// Debug level none
// PSRam disabled
// ****************************************************************************
#define _Main_Name     "Test_SI4432"
#define _Main_Version  0.1

// ****************************************************************************
#include <SPI.h>

#define SCK   18
#define MISO  19
#define MOSI  23
#define SS     5

// ****************************************************************************
#define SI4432_Shutdown_Pin  16
#define SI4432_Int_Pin       17
#define SI4432_GPIO2_Pin     22
#define SI4432_QIA_Rec_Pin   12

//#define SI4432_Debug  true
#include "SI4432_support.h"


// ****************************************************************************
_SI4432 Transceiver ( SI4432_Shutdown_Pin , SI4432_Int_Pin ) ;

// ****************************************************************************
// ****************************************************************************

void setup() {
  Serial.begin ( 115200 ) ;
  
  int Device ;  
  Device = Transceiver.Init() ;
//Serial.print ( "Reset ") ;
//Serial.println ( Device ) ;

  // *******************************************
  // SpectrumAnalyzer
  // *******************************************
  if ( Device == 0 ) {
    Transceiver.SI4432_Spectrum_Analyzer () ;
  }

  // *******************************************
  // UHF Generator, werkt behoorlijk
  // *******************************************
  else if ( Device == 1 ) {
    Transceiver.SI4432_UHF_Generator () ;
  }

  // *******************************************
  // Interactive Register Viewer
  // *******************************************
  else if ( Device == 2 ) {
    Transceiver.SI4432_Interactive_Viewer      () ;
  }

  // *******************************************
  // Stream Viewer
  // *******************************************
  else if ( Device == 3 ) {
    Transceiver.QIA_OOK_Stream_Viewer () ;
  }
  else if ( Device == 4 ) {
    Transceiver.SI4432_OOK_Stream_Viewer () ;
  }

  // *******************************************
  // Future Devices
  // *******************************************
  else {
    Transceiver.SI4432_Print_Registers () ;
    Transceiver.SI4432_Read_Status () ;

    Serial.print   ( "Future Device = 0xAA 0xBB 0x" ) ;
    Serial.println ( Device, HEX ) ;
    while ( true ) {};
  }

  //Transceiver.SI4432_Init_Rx () ;

  Transceiver.SI4432_Init_WS3000_TxRx () ;
  Transceiver.SI4432_Print_Registers () ;
  Transceiver.SI4432_Read_Status () ;

  //Transceiver.SI4432_Init_KAKU () ;
  //Transceiver.SI4432_Init () ;
}

// ****************************************************************************
// ****************************************************************************
bool First_Time = true ;
void loop() {
  //Transceiver.SI4432_Loop_Read_RSSI ( 0x05 ) ;
  //Transceiver.SI4432_Watch_Status () ;
  
  if ( First_Time ) {
    First_Time = false ;
    //Transceiver.readAll () ;
  }

  if ( Transceiver.SI4432_WS3000_Loop () ) {
    //for ( int i=0; i<9; i++ ) {
    //    Serial.print ( WS3000_Data [i], HEX ) ;
    //    //Soladin_Data [31+i] = WS3000_Data [i]
   // }
    //Serial.println ( 0xFF ) ;
  }
  else Serial.println ( '.' ) ;

//delay (1000 );

}
