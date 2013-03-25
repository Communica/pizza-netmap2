#!/usr/bin/python
#coding: utf-8
import pnmp
import sys
import time
import random
import urllib2
import re
import string

#CONFIG

COM_PORT 		= 	'/dev/tty.usbmodemfa131'
URL  			= 	"http://www.komsys.org/pizza-netmap/src/pizza-netmap2/nms-simulator/switchlist.txt"
POLL_INTERVAL 	= 	5 #Seconds between update

# END CONFIG


################################
#	MONITORING
################################



def list_com_ports():
	from serial.tools import list_ports
	
	return "Choose serial device / COM port: \n %s" % '\n'.join(list("\t[%u] : %s" % (i, u[0]) for i,u in enumerate( list_ports.comports() )))
	



if __name__ == '__main__':
	print ("Init")

	#print ( list_com_ports())

	api = pnmp.api(COM_PORT)

	try:
		while 1:	
			statusmap = [ re.split("\s", string.rstrip(u)) for u in urllib2.urlopen(URL).readlines() ]
			print ("Pushing state")
			print (statusmap)
			api.pushState(statusmap)
			time.sleep(POLL_INTERVAL)

	except KeyboardInterrupt:
		api.clean_the_mess_up_after_you()
	finally:
		print ( "No more pizza!")
