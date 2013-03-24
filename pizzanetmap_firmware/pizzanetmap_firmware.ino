

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
#define n_74hc595_per_distro 2 // Shift registers per distro
#define n_shiftregister_pins 8 // Number of output pins on shiftreg.

/*____________________________________________________________
 *    END OF CONFIGURATION  
 */
 
typedef struct
{
  int n_distros;
  int n_pins;
  boolean active;
} _core;

 
 _core * core_stat;
 
 



/* helper arrays */
int CLK[number_of_cores] = {CLK1_Pin, CLK2_Pin};
int RX[number_of_cores]  = {RX1_Pin, RX2_Pin};
int TX[number_of_cores]  = {TX1_Pin, TX2_Pin};

int active_cores, bits_shifted, tot_nodes = 0;
int nodes = 0;

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
  
  // For the API to work :).
  Serial.begin(9600);
  
  // Keeping track of core-statistics. i.e numbers.
  core_stat = (_core *) malloc(number_of_cores * sizeof(_core)); 
  
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
  
  Serial.print(core_stat[0].n_distros);
  Serial.print(active_cores);

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



void loop(){


}
