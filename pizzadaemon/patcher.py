#!/usr/bin/env python
#coding: utf-8

#
#	Code to create patchlist for the pizzanetmap :)
#

import pnmp
import urllib2
import string
import re

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

distros_in_core = [2,3]


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


