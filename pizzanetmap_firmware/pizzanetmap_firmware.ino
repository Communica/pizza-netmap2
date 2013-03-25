#include "stdlib.h"

/*
 *  Core #1
 *
 */

int TX1_Pin = 13;   //SER (pin 14 on the 75HC595)
int RX1_Pin = 12;   //last output in a shiftregister chain.
int CLK1_Pin = 11;  //SRCLCK and RCLK

/*
 *  Core #2
 * 
 */
int TX2_Pin = 10;   //SER (pin 14 on the 75HC595)
int RX2_Pin = 9;    //last output in a shiftregister chain.
int CLK2_Pin = 8;   //SRCLCK and RCLK

int MR_Pin = 7;     // Master Reset


#define count_delay 0     // Delay between node count. Visual fx only!
#define RE_PULSE 8          // Repulse - timeslots between retransmitting pulse. 
#define MAX_NODE_COUNT 512  // if no BKTRK is connected.
#define number_of_cores 2    // Core switches in use 
#define n_74hc595_per_distro 4 // Shift registers per distro
#define n_shiftregister_pins 8 // Number of output pins on shiftreg.

/*____________________________________________________________
 *    END OF CONFIGURATION  
 */
 
 
 
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

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete




/*###################################################################################
 *    
 *    SETUP
 *
 *##################################################################################*/

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
  
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
  
  // For the API to work :).
  Serial.begin(9600);
  
  // Keeping track of core-statistics. i.e numbers.
  core_stat = (_core *) malloc(number_of_cores * sizeof(_core)); 
  if (core_stat == NULL) {
     // No Memory! 
  }
  //Determine how many nodes connected to each core:
  tot_nodes = 0;
  active_cores = 0;

  // 1, 2,3,4,5,6,7,8,9,10,11,12
  for (int c=0; c < number_of_cores; c++) {
    nodes=0;
    countNodes( c, &nodes);
    
    if (nodes > 0) {
       core_stat[c].n_distros = nodes / (n_shiftregister_pins * n_74hc595_per_distro);
       core_stat[c].n_pins    = nodes;  
       core_stat[c].active    = true;
       tot_nodes += nodes;
       active_cores += 1;   
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
    memset( registers, LOW, sizeof(boolean) * tot_nodes );
  }


  
  /*
   * Debug
   */   
  Serial.print(core_stat[0].n_distros);
  Serial.print(active_cores);
  Serial.print("\nTotalt:"); 
  Serial.print(tot_nodes);
  Serial.print(" random-pick led: ");
  Serial.print(registers[5]);
  
  registers[7] = 1;
  registers[3] = 1;
  registers[15] = 1;


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
  int c = 0;

  
  /* drunken Ninja tricks to get the first active core */
  int i = 0;
  int b = 0;
  int ninja = 0;
  
  for (i = tot_nodes-1; i>=0; i--) {
    
     if ( b > core_stat[c].n_pins ){
        c++;
        b=0;
     }
     
      
     
      delay (count_delay);
      digitalWrite(CLK[c], LOW);
      //Sending pulse in an interval (@see RE_PULSE)
      digitalWrite(TX[c], int(registers[i]));
      digitalWrite(CLK[c], HIGH);
      b++;
     
  }  
  
  Serial.print("ninja: ");
  Serial.print(ninja);
  Serial.print("\n");
  Serial.print(core_stat[0].n_pins);
  Serial.print("\n");

}




char buffer[50];
void writeRegisters(char * data, int len) {
  boolean  ninja[sizeof(char)];
  
  for (int i=0; i<len && i < tot_nodes; i++) {
      ninja = (boolean*) data;
      for (int k=0; k<sizeof(boolean); k++ ) {
        registers[i++] = ninja[k]; 
      }
      
    
//     if (data[i] == (char) '1') {
//        registers[i] = HIGH;
//     }
//     else 
//       registers[i] = LOW;
  }
}


void loop(){
delay(100);
// print the string when a newline arrives:
  if (stringComplete) {
   
    // clear the string:
    
    writeRegisters(inputString.toCharArray(), inputstring.length());
    inputString = "";
    stringComplete = false;
  }
  
  
}

#define WRITE_LED 13
#define PUSHSTATE 13

void serialEvent() {
  int cmd, bits = 0;
  while ( Serial.available() ) {
     cmd = Serial.parseInt(); 
     
     if (cmd == PUSHSTATE) {
       
       while (Serial.available() ) {
            inputString += (char)Serial.read();
            if( inputString.length() >= tot_nodes ) {
                stringComplete  = true;
                break;
            }
        }
     }
  }
}
