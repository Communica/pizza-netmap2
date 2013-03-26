#include "stdlib.h"

/*

LOGO = """
  ______                              _            
 / _____)                            (_)           
| /      ___  ____  ____  _   _ ____  _  ____ ____ 
| |     / _ \|    \|    \| | | |  _ \| |/ ___) _  |
| \____| |_| | | | | | | | |_| | | | | ( (__( ( | |
 \______)___/|_|_|_|_|_|_|\____|_| |_|_|\____)_||_|



_____________PRESENTS______________________________
                                                   

       _                                                     
      (_)                             _                      
 ____  _ _____ _____ ____ ____   ____| |_  ____   ____ ____  
|  _ \| (___  |___  ) _  |  _ \ / _  )  _)|    \ / _  |  _ \ 
| | | | |/ __/ / __( ( | | | | ( (/ /| |__| | | ( ( | | | | |
| ||_/|_(_____|_____)_||_|_| |_|\____)\___)_|_|_|\_||_| ||_/ 
|_|                                                   |_|    
      ______    ______       
     (_____ \  / __   |      
 _   _ ____) )| | //| | ____ 
| | | /_____/ | |// | |/ _  |
 \ V /_______ |  /__| ( ( | |
  \_/(_______|_)_____/ \_||_|




  Copyright 2013      Robin G. Aaberg  (technocake)
              Erik S. Haugstad (isamun)
              Lars Thorsen (larsyboy)
              Joaquin Alejandro Correas Pernigotti (jacp)
              Andras Csernai (Mr.Sunshine)
              Jan Gunnar Ludvigsen (MrLudde)
              Christer Larsen (awelan) 
              Martin Bergo (minroz)                              

              Collaborators:
              Steinar H. Gunderson (Sesse)
              Tristan Straub ()
              Chad Toprak (MrCh4d)
              Tom Penney  (Asgasasdasdafsa)

  All hardware, schematics, code, software and 
  other creative derivatives are freely distributed 
  and made available to the public under one constraint: 
    Share your knowledge.

  By which we mean all derivative works based on pizzanetmap 
  must be made available as libre-source. 
  Non-commercial or commercial alike.


  Licenced under a multi-license:
  MIT, GPLv2 and Beer Share and
  Creative Commons Share-alike
"""
 */


/* Core #1  */
int TX1_Pin   = 13;                //SER (pin 14 on the 75HC595)
int RX1_Pin   = 12;                //last output in a shiftregister chain.
int CLK1_Pin  = 11;                //SRCLCK and RCLK

/* Core #2 */
int TX2_Pin   = 10;                //SER (pin 14 on the 75HC595)
int RX2_Pin   = 9;                 //last output in a shiftregister chain.
int CLK2_Pin  = 8;                 //SRCLCK and RCLK

int MR_Pin    = 7;                 // Master Reset


#define count_delay           0    // Delay between node count. Visual fx only!
#define RE_PULSE              8    // Repulse - timeslots between retransmitting 
#                                  //   pulse. @see countNodes 
#define MAX_NODE_COUNT        512  // If no RX is connected, prevents infinity loop, 
#                                  //but also limits supported nodes per core.
#define number_of_cores       2    // Core switches in use 
#define n_74hc595_per_distro  4    // Shift registers per distro
#define n_shiftregister_pins  8    // Number of output pins on shiftreg.

/*____________________________________________________________
 *    END OF CONFIGURATION  
 */

/*
 *  BEGIN Protocol
 */
 
#define   PUSHSTATE           0xF0      // Start byte for stream of bits 
                                        //   transmission 
#define   ENDPUSHSTATE        0xF1      // Stop byte. 
#define   WRITE_LED           0xF2      //
#define   GET_NETWORK_GRAPH   0xF3      // Getting stats from this pizzanetmap.
 
 
/*  
 *  Struct to keep track on how many distro switches,
 *  and pins are connected to each core switch.
 */
 
typedef struct
{
  int n_distros;
  int n_pins;
  boolean active;
} _core;
 
 _core * core_stat; // Array of core stats structs.  
 

boolean * registers; // Array of the bits that is shifted out to the leds :).

/* helper arrays */
int CLK[number_of_cores] = {CLK1_Pin, CLK2_Pin};
int RX[number_of_cores]  = {RX1_Pin, RX2_Pin};
int TX[number_of_cores]  = {TX1_Pin, TX2_Pin};

int active_cores, bits_shifted, tot_nodes, nodes = 0;
char cb; //buffer


/* functions */
void writeRegisters();
void reset(int dt);
void countNodes (int line, int * nodes);



/*#############################################################################
 *    
 *    SETUP
 *
 *###########################################################################*/

void setup(){
  //Core #1
  pinMode(TX1_Pin, OUTPUT);
  pinMode(CLK1_Pin, OUTPUT);
  pinMode(RX1_Pin, INPUT);
  //Core #2
  pinMode(TX2_Pin, OUTPUT);
  pinMode(CLK2_Pin, OUTPUT);
  pinMode(RX2_Pin, INPUT);
  //Reset
  pinMode(MR_Pin, OUTPUT);
  
  
  // For the API to work :).
  Serial.begin(9600);
  
  
  // Keeping track of core-statistics. i.e numbers.
  core_stat = (_core *) malloc(number_of_cores * sizeof(_core)); 
  if (core_stat == NULL) { /* No Memory! */ }

  //Determine how many nodes connected to each core:
  tot_nodes = 0;
  active_cores = 0;


  // 1,2,3,4,5,6,7,8,9,10,11,12
  for (int c=0; c < number_of_cores; c++) {
    
    nodes=0;
    countNodes( c, &nodes);
    
    if (nodes > 0) {
       core_stat[c].n_distros   = nodes / (n_shiftregister_pins * n_74hc595_per_distro);
       core_stat[c].n_pins      = nodes;  
       core_stat[c].active      = true;
       tot_nodes               += nodes;
       active_cores            += 1;   
    } 
    else { // Error occured
       core_stat[c].n_distros   = 0; 
       core_stat[c].n_pins      = 0;
       core_stat[c].active      = false;
    }
  }
  

  // Dynamically allocating the address space of all leds.
  registers = (boolean *) malloc( tot_nodes * sizeof(boolean) );
  if (registers != NULL) {
    // Setting default value on all leds.
    memset( registers, 0, sizeof(boolean) * tot_nodes );
  }


  writeRegisters();
}               


void reset(int dt) {
  digitalWrite(MR_Pin, LOW);
  delay(dt);
  digitalWrite(MR_Pin, HIGH);
}


// Dynamically count the number of nodes on a core (one ser-line). 
void countNodes (int line, int * nodes) {
  *nodes = 0;
   int bkval = 0;
  //reset
  reset(count_delay);
  
  do {
    delay (count_delay);
    digitalWrite(CLK[line], LOW);
    //Sending pulse in an interval (@see RE_PULSE)
    digitalWrite(TX[line], (*nodes)%RE_PULSE == 0);
    digitalWrite(CLK[line], HIGH);
    //Counting
    
  } while (  ((*nodes)++) < MAX_NODE_COUNT && int(bkval = digitalRead(RX[line])) == 0 );
  
  
  if (*nodes >= MAX_NODE_COUNT) {
     *nodes = -1; 
  }
  
 
}//end countNodes


void writeRegisters() {
  reset(count_delay);
  int c = 0;  // Core index
  int i = 0;  // bits index on a total basis
  int b = 0;  // bits index on a per core basis
  
  for (i = tot_nodes-1; i>=0; i--) 
  {

    if ( b > core_stat[c].n_pins ){
      c++;
      b=0;
    } 

    // Shifting one bit: Setting Clk low, write data, Clk High
    digitalWrite(CLK[c], LOW);
    delay (count_delay);
    digitalWrite(TX[c], int(registers[i]));
    digitalWrite(CLK[c], HIGH);
    b++; 
  }  

}



/*#############################################################################
 *    
 *   L
 *    O  
 *     O
 *      P
 *###########################################################################*/


boolean RECV_BITS  = false;  // RECV_BITS state flag
unsigned int rb   = 0;      // Received bits

void loop(){
  int cmd;                  //  cmd/data) buffer.
  int bits;                 //  CNAME --> cmd
  int c;                    //  Core index


  if (Serial.available() > 0) {
    cmd = Serial.read();
   
     if         (cmd == PUSHSTATE) {     
       RECV_BITS    = true;
       rb           = 0; 
       c            = 0;
       bits_shifted = 0;
     }else if  (cmd == ENDPUSHSTATE) {
       RECV_BITS = false;
       writeRegisters();  
     }else if  (RECV_BITS)  {   // Receiving chunk after chunk.

       bits = cmd;

       for (int i = 0; i < 7; ++i) {
         // Filling up one core at a time, bit for bit.
        if ( rb < core_stat[c].n_pins )  {
           registers[rb++] = ((bits & (0x01 << i )) != 0);
          bits_shifted++;
        }
        else if (c < number_of_cores) {
         c++;
         rb = 0;
       }//end else if
     }//end for

    } //end if
  } // end serial if
} //end loop




