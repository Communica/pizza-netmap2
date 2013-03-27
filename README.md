pizza-netmap2
=============

![A netmap in a pizzabox!](http://technocake.net/screenshots/pizzamap.jpg)

Pizza net map is a computer network monitoring device, inside a pizza box. 

We want to make a miniature model of The Gathering network. Participants access the network through switches and access points. We will monitor these and represent their status using LED lights on the model.

Our challenge is to make a modular system that is not limited to one application, but is flexible and can be applied to other networks, not necessarily computer networks.

We achieve this by using an Arduino and shift-registers to control an unlimited amount of LEDs and layouts. 

Our software communicates with an Arduino through a USB connection. A computer checks with the existing Network Management System to see which network access switches are online or not. Based on this data the computer turns a corresponding LED on or off.


#Installation Instructions

## Physical
Here is a video showing the instructions on how to set it up:

on Vimeo:
https://vimeo.com/62769705

For those with super interwebzspeed, here is a highresolution "raw" video:
http://www.komsys.org/pizza-netmap/instruction.mp4

This will run you through the physical setup, connections. 
Please note:
  - DO NOT connect the arduino BEFORE the PSU has been connected to the circuit.
  - Only one switch on the cores should be up,  to let the cores be configured correctly

So this means if you have 2 distros connected, only the switch labeled 2 should be up, and vice versa.


## The Code


Clone this repository, the working code is in the master branch. 

#Firmware --> Arduino
The Arduino given to the TG has already been preloaded with this firmware. But if you are to 
set this up from scratch, upload the pizzanetmap_firmware to the arduino. 
 
#Pizzadaemon
The pizzadaemon.py is responsible for fetching the state of the network and communicating with the pizzanetmap  (Arduino)  
it needs an config.py file in its folder. 
See config-example.py for reference

Circuit schematics and more docs will arrive fresh from the pizza owen (soon).






