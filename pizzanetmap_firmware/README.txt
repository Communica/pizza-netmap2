This is the firmware to be running on the arduino of Pizzanetmap. 
It features auto-discovery of attached outputs through the shiftregisters (number of leds possible to control),
and a binary-"api" for a computer to speak with (through the USB). 

For now, it only supports updating the map in full-bunk. That is, all the led's status at once.

If the computer gives it more information (number of nodes) than it currently has attached, it 
silently ignores that information. It will only light / light off the number of leds it actually has
attached. 


                         / Distros  4 x --- 8 ---- Leds
  Arduino  ---->  Core /        |
  ^                 |   \_______|
  |_________________|



Pinout: 

Await the fritzing sketch.

