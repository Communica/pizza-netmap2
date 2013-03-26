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
#	
#	Config is in config.py. Edit that file.
##


# END CONFIG


################################
#	MONITORING
################################



def list_com_ports():
	from serial.tools import list_ports
	return "Choose serial device / COM port: \n %s" % '\n'.join(list("\t[%u] : %s" % (i, u[0]) for i,u in enumerate( list_ports.comports() )))
	



if __name__ == '__main__':
	print ("Init")

	print ( list_com_ports())
	
	from config import *

	api = pnmp.api(COM_PORT)

	#todo, implement..
	#n_cores, distros_in_cores = api.getNetworkGraph()

	print ( 
		"""
			Pizzadaemon

			________________________________________________

			Cores: %d\t Distros, per core: %s\t

		""" % (2, str([3,2]))



		)

	try:
		while 1:	
			statusmap = [ re.split(SWITCH_DELIM, string.rstrip(u)) for u in urllib2.urlopen(URL).readlines() ]
			print ("Pushing state")
			print (statusmap)
			api.pushState(statusmap)
			time.sleep(POLL_INTERVAL)

	except KeyboardInterrupt:
		api.clean_the_mess_up_after_you()
	finally:
		print ( "No more pizza!")
