#!/usr/bin/env python
#coding: utf-8

#
#	Code to create patchlist for the pizzanetmap :)
#

import pnmp
import urllib2
import string
import re

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

from config import *
#URL  = "http://www.komsys.org/pizza-netmap/src/pizza-netmap2/nms-simulator/switchlist.txt"

statusmap = [ re.split(SWITCH_DELIM, string.rstrip(u)) for u in urllib2.urlopen(URL).readlines() ]

BOLD = '\033[1m'
ENDC = '\033[0m'
def color(i ,binary=False):
	if binary and not COLOR_SUPPORT:
		return ''
	elif binary:
		return ['\033[91m' 	 , '\033[93m',    '\033[92m',	'\033[82m',		'\033[94m',	  '\033[096m', '\033[090m', 	'\033[097m' ][i]
	try:
		return ["dark orange", "light orange", "dark green", "light green", "dark blue", "light blue", "dark brown", "light brown"][i]
	except:
		print "ERROR color"
	return ''





num_ports = pnmp.config['num_distro_ports']
num_cores = pnmp.config['num_cores']

distros_in_core = [3,2]


def patchPins(lvl, c,d,p,n):
	res=""
	pin=1
	while pin <= 8:
		if (n >= len(statusmap)):
			return n,res
		res += "%s%s	%u.%u.%u.%u	(%s%s%s%s)\n" % ("\t"*lvl, statusmap[n-1][0], c,d,p,pin, BOLD, color(pin-1, True), color(pin-1), ENDC)
		pin += 1
		n += 1
	return n, res


def patchPorts(lvl, c,d,p,n):
	res=""
	res2 = ""
	for p in range(1, num_ports+1):
		res += "\n%s#Port %u\n" % ("\t"*lvl, p)
		n, res2 = patchPins(lvl+1, c,d,p,n)
		res += res2
	return n, res

def patchDistros(lvl, c,d,p,n):
	res=""
	res2 = ""
	for d in range(1, distros_in_core[c-1]+1):
		res += "\n%s#Distro %u\n" % ("\t"*lvl, d)
		n,res2 = patchPorts(lvl+1,c,d,p,n)
		res += res2
	return n, res



def patchCores(lvl=0,c=1,d=1,p=1,n=1 ):
	res=""
	res2=""

	n=1
	c=1
	d=1
	p=1
	res += """
#Patchlist.txt
#sysname	core.distro.port.pin

"""
	for c in range(1, num_cores+1):
		d=1
		res += "\n%s#Core %u\n" % ("\t"*lvl, c)
		n, res2  = patchDistros(lvl+1, c,d,p,n)
		res += res2
	return res

print ( patchCores())


