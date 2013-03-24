#!/usr/bin/env python
# coding: utf-8

off = [13,37,1,3]
switches =[]

def sw(i, num):
	return "e%u-%u %s" % (i*2-1, num+1, 'off' if i in off else 'on')

for i in range(42 + 1):
	if not ( i >= 1 and i <= 5 ) :
		switches.append(sw(i, 0))
		switches.append(sw(i, 1))
	
	if  not (i >= 14 and i <= 21) and  not (i >= 38):
		switches.append(sw(i, 2))
		switches.append(sw(i, 3))

print ( '\n'.join(switches))