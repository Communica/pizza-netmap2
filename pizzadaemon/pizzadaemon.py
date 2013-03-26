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


LOGO = """
  ______                              _            
 / _____)                            (_)           
| /      ___  ____  ____  _   _ ____  _  ____ ____ 
| |     / _ \|    \|    \| | | |  _ \| |/ ___) _  |
| \____| |_| | | | | | | | |_| | | | | ( (__( ( | |
 \______)___/|_|_|_|_|_|_|\____|_| |_|_|\____)_||_|



_____________PRESENTS______________________________
                                                   

       _                                                     
      (_)                             _                      
 ____  _ _____ _____ ____ ____   ____| |_  ____   ____ ____  
|  _ \| (___  |___  ) _  |  _ \ / _  )  _)|    \ / _  |  _ \ 
| | | | |/ __/ / __( ( | | | | ( (/ /| |__| | | ( ( | | | | |
| ||_/|_(_____|_____)_||_|_| |_|\____)\___)_|_|_|\_||_| ||_/ 
|_|                                                   |_|    
      ______    ______       
     (_____ \  / __   |      
 _   _ ____) )| | //| | ____ 
| | | /_____/ | |// | |/ _  |
 \ V /_______ |  /__| ( ( | |
  \_/(_______|_)_____/ \_||_|




	Copyright 2013			Robin G. Aaberg  (technocake)
							Erik S. Haugstad (isamun)
							Lars Thorsen (larsyboy)
							Joaquin Alejandro Correas Pernigotti (jacp)
							Andras Csernai (Mr.Sunshine)
							Jan Gunnar Ludvigsen (MrLudde)
							Christer Larsen (awelan) 
							Martin Bergo (minroz)                              

							Collaborators:
							Steinar H. Gunderson (Sesse)
							Tristan Straub ()
							Chad Toprak (MrCh4d)
							Tom Penney  (Asgasasdasdafsa)

	All hardware, schematics, code, software and 
	other creative derivatives are freely distributed 
	and made available to the public under one constraint: 
		Share your knowledge.

	By which we mean all derivative works based on pizzanetmap 
	must be made available as libre-source. 
	Non-commercial or commercial alike.


	Licenced under a multi-license:
	MIT, GPLv2 and Beer Share and
	Creative Commons Share-alike
"""


def list_com_ports():
	from serial.tools import list_ports
	return "Choose serial device / COM port: \n %s" % '\n'.join(list("\t[%u] : %s" % (i, u[0]) for i,u in enumerate( list_ports.comports() )))
	



if __name__ == '__main__':
	print ( LOGO )
	time.sleep(2)

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

		""" % (2, str([3,2])) # Yes, hardcoded.



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
