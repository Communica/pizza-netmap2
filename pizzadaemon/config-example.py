#!/usr/bin/env python
# coding: utf-8
#CONFIG
import re

COM_PORT 		= 	'/dev/tty.usbmodemfa131'
#URL  			= 	"File:///Users/technocake/code/pizza-netmap2/nms-simulator/switchlist.txt"
URL 			= 	"http://nms-public.tg13.gathering.org/led.txt"
POLL_INTERVAL 	= 	5 #Seconds between update
COLOR_SUPPORT	=	False
SWITCH_DELIM	= 	"\s"
SWITCH_PATTERN	= 	r"(?m)^(?P<switch>(?P<name>e(?P<row>\d+)-(?P<col>\d+))\s+(?P<status>on|off))\n" #(?m) = multiline flag.
SWITCH_SORT		= 	lambda s:  4 * int(s['row']) + int(s['col'])
# END CONFIG