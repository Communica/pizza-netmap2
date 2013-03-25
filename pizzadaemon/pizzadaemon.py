#!/usr/bin/python
import pnmp
import sys
import time
import random
import urllib2
import re
import string


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



def list_com_ports():
	from serial.tools import list_ports
	
	return "Choose serial device / COM port: \n %s" % '\n'.join(list("\t[%u] : %s" % (i, u[0]) for i,u in enumerate( list_ports.comports() )))
	



if __name__ == '__main__':
	print ("Init")

	print ( list_com_ports())


	COM_PORT = '/dev/tty.usbmodemfa131'


	api = pnmp.api(COM_PORT)

	URL  = "http://www.komsys.org/pizza-netmap/src/pizza-netmap2/nms-simulator/switchlist.txt"

	statusmap = [ re.split("\s", string.rstrip(u)) for u in urllib2.urlopen(URL).readlines() ]

	print ("Pushing state")
	print (statusmap)
	api.pushState(statusmap)
	
	api.clean_the_mess_up_after_you()