#!/usr/bin/env python
# coding: utf-8
#
#	./make-switches.py > switchlist.txt
#	
#	
#	

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
off = [13,37,1,3]
switches =[]

def sw(i, num):
	return "e%u-%u %s" % (i*2-1, num+1, 'off' if i in off else 'on')

for i in range(1, 42 + 1):
	if not ( i >= 1 and i <= 5 ):
		switches.append(sw(i, 0))
		switches.append(sw(i, 1))
	
	if  not (i >= 14 and i <= 21) and  not (i >= 38):
		switches.append(sw(i, 2))
		switches.append(sw(i, 3))

print ( '\n'.join(switches))