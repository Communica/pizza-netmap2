// we need fundamental FILE definitions and printf declarations
#include <stdio.h>

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


#define count_delay 50     // Delay between node count. Visual fx only!
#define RE_PULSE 8          // Repulse - timeslots between retransmitting pulse. 
#define MAX_NODE_COUNT 512  // if no BKTRK is connected.
#define number_of_cores 2    // Core switches in use 
/*____________________________________________________________
 *    END OF CONFIGURATION  
 */
 

/* helper arrays */
int CLK[number_of_cores] = {CLK1_Pin, CLK2_Pin};
int RX[number_of_cores]  = {RX1_Pin, RX2_Pin};
int TX[number_of_cores]  = {TX1_Pin, TX2_Pin};

  // To have printf
static FILE uartout = {0} ;
static int uart_putchar (char c, FILE *stream)
{
    Serial.write(c) ;
    return 0 ;
}

void setup(){
  //Core #1
  pinMode(TX1_Pin, OUTPUT);
  pinMode(CLK1_Pin, OUTPUT);
  pinMode(RX1_Pin, INPUT);
  //Core #2
  pinMode(TX2_Pin, OUTPUT);
  pinMode(CLK2_Pin, OUTPUT);
  pinMode(RX2_Pin, INPUT);

  pinMode(MR_Pin, OUTPUT);


  Serial.begin(9600);
  
  // fill in the UART file descriptor with pointer to writer.
   fdev_setup_stream (&uartout, uart_putchar, NULL, _FDEV_SETUP_WRITE);

   // The uart is the standard output device STDOUT.
   stdout = &uartout ;

}               




void reset(int dt) {
  digitalWrite(MR_Pin, LOW);
  delay(dt);
  digitalWrite(MR_Pin, HIGH);
}

// Dynamically count the number of nodes on one line. 

void countNodes (int line, int * nodes) {
 
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
    (*nodes)++;
  } while ( int(bkval = digitalRead(RX[line])) == 0 && *nodes < MAX_NODE_COUNT );
  
  if (*nodes >= MAX_NODE_COUNT) {
     *nodes = -1; 
  }
  
}

int nodes;

void loop(){
  nodes=0;

  //CORE 1
  countNodes(0, &nodes);
  if (Serial.available() > 0) {
    Serial.flush();
    printf("Core 1::\t %i nodes counted\n", nodes);
  }

  // CORE 2
  countNodes(1, &nodes);
  if (Serial.available() > 0) {
    Serial.flush();
    printf("Core 2::\t %i nodes counted\n", nodes);
  }
}
