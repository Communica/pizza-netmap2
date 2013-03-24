#!/usr/bin/python
import pnmp
import sys
import time
import random


#		 _______________________
#		| INPUT
#		| serial-device (port)
#		| switch-status-source (url)
#		|_______________________
#		| OUTPUT
#		| 
#		|
#		|_______________________
#
#
#		setup / init:
#			Test lines and count nodes:
#		
#			Map switches sysname to hw addr.  
#				e73-1  --> 2.2.4.1
#			Push the maping to the arduino. 
#				api.push_map({'e73-1' : "2.2.4.1", ...})
#
#
#		loop:
#		
#
##




watch = {
	"10.13.37.6": '7', 
	"10.13.37.1": '5',  
	"10.13.37.2": '6', 
	"10.13.37.3": '2', 
	"10.13.37.4": '3',
	"10.13.37.5": '4'
	}

lost = {}

count = 3

################################
#	MONITORING
################################





def tellThePizza(switch):
	"""	Flipping the switch-status. """
	if not switch in lost:
		print "Switch %s is down :(" % switch
		lost[switch] = watch[switch]
		n = watch[switch]
		ser.write( n )

def weGotMorePizzaAgain(switch):
	"""	A switch has come back up to life """
	if switch in lost:
			del lost[switch]
			ser.write(watch[switch])





if __name__ == '__main__':
	print ("Init")
	COM_PORT = '/dev/tty.usbmodemfd121'
	api = pnmp.api(COM_PORT)

	print ( api.getNodeCount() )
	api.clean_the_mess_up_after_you()