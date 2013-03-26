#include "stdio.h"
#include "stdlib.h"
#include "stdbool.h"
#define number_of_cores 2


/*  
 *  Struct to keep track on how many distro switches,
 *  and pins are connected to each core switch.
 */
 
typedef struct
{
  int n_distros;
  int n_pins;
  bool active;
} _core;
 
 _core * core_stat;



int main(int argc, char const *argv[])
{

	core_stat = (_core *) malloc(number_of_cores * sizeof(_core)); 
  if (core_stat != NULL) {
    core_stat[0].n_distros 	= 4;
    core_stat[0].n_pins 	= 32;
    core_stat[0].active 	= 1;
    core_stat[1].n_distros 	= 4;
    core_stat[1].n_pins 	= 32;
    core_stat[1].active 	= 1;
  }

	int c = 0;
	int rb = 0;
	
	bool registers[9] = {true, false,true,true,true,true,true,true,true};
	bool val;

	int bits = 0x92; 


	 for (int i = 0; i < 7; ++i)
      {
        if ( rb < core_stat[c].n_pins ) {// Filling up one core at a time.
           val = ((bits & (0x01 << i )) != 0);
          registers[rb++] = val;
          if (val)
          	printf("1" );
          else
          	printf("0");
        }
        else if (c < number_of_cores) 
        {
          c++;
          rb = 0;


        }

      }
	return 0;
}

