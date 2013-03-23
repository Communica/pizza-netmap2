// we need fundamental FILE definitions and printf declarations
#include <stdio.h>

int SER_Pin = 13;   //pin 14 on the 75HC595
int RCLK_Pin = 12;  //pin 12 on the 75HC595
int SRCLK_Pin = 11; //pin 11 on the 75HC595
int BKTRK_Pin = 10;  //last output in a shiftregister chain.
int MR_Pin = 9; // Master Reset


// create a FILE structure to reference our UART output function

static FILE uartout = {0} ;

// create a output function
// This works because Serial.write, although of
// type virtual, already exists.
static int uart_putchar (char c, FILE *stream)
{
    Serial.write(c) ;
    return 0 ;
}


//How many of the shift registers - change this
#define number_of_74hc595s 2
// Delay between node count. Visual fx only!
#define count_delay 100
//Repulse - timeslots between retransmitting pulse. 
#define RE_PULSE 8
#define MAX_NODE_COUNT 24 // if no BKTRK is connected.
//do not touch
#define numOfRegisterPins number_of_74hc595s * 8

boolean registers[numOfRegisterPins];

void setup(){
  pinMode(SER_Pin, OUTPUT);
  pinMode(RCLK_Pin, OUTPUT);
  pinMode(SRCLK_Pin, OUTPUT);
  pinMode(BKTRK_Pin, INPUT);
  pinMode(MR_Pin, OUTPUT);


  Serial.begin(9600);
  
  // fill in the UART file descriptor with pointer to writer.
   fdev_setup_stream (&uartout, uart_putchar, NULL, _FDEV_SETUP_WRITE);

   // The uart is the standard output device STDOUT.
   stdout = &uartout ;

  //reset all register pins
  clearRegisters();
  writeRegisters();
}               


//set all register pins to LOW
void clearRegisters(){
  for(int i = numOfRegisterPins - 1; i >=  0; i--){
     registers[i] = LOW;
  }
} 


//Set and display registers
//Only call AFTER all values are set how you would like (slow otherwise)
void writeRegisters(){

  digitalWrite(RCLK_Pin, LOW);

  for(int i = numOfRegisterPins - 1; i >=  0; i--){
    digitalWrite(SRCLK_Pin, LOW);

    int val = registers[i];
    val = i%2;

    digitalWrite(SER_Pin, val);
    digitalWrite(SRCLK_Pin, HIGH);

  }
  digitalWrite(RCLK_Pin, HIGH);
  

}

//set an individual pin HIGH or LOW
void setRegisterPin(int index, int value){
  registers[index] = value;
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
    digitalWrite(RCLK_Pin, LOW);
    digitalWrite(SRCLK_Pin, LOW);
    //Sending pulse in an interval (@see RE_PULSE)
    digitalWrite(SER_Pin, (*nodes)%RE_PULSE == 0);
    digitalWrite(SRCLK_Pin, HIGH);
    digitalWrite(RCLK_Pin, HIGH);
    (*nodes)++;
  } while ( int(bkval = digitalRead(BKTRK_Pin)) == 0 && *nodes < MAX_NODE_COUNT );
  
  if (*nodes >= MAX_NODE_COUNT) {
     *nodes = -1; 
  }
  
}


void loop(){
  int nodes = 0;
  countNodes(0, &nodes);
  if (Serial.available() > 0) {
    Serial.flush();
    printf("%i nodes counted\n", nodes);
  }
  }
