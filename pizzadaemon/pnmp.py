#!/usr/bin/env python
# coding: utf-8

#	
#	Python API for the PNMP protocol
#
import serial
from serial.tools import list_ports
import time
import math

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

config = {
	'num_cores' : 2,
	'num_distro_ports': 4,
	'num_bits_per_shiftregister': 8
}




class api():
	""" The Pizza-Netmap Network Monitoring Protocol api """
	
	PUSHSTATE = [0xF0, 0xF1] #1 bit signaling command and not data (first)
	WRITE_LED = [0xF2]
	GET_NETWORK_GRAPH = [0xF3]

	def __init__(self, COM_PORT, BAUD_RATE=9600):
		
		
		try:
			# Opening a serial connection to the arduino :).
			self.arduino = serial.Serial(COM_PORT, BAUD_RATE, bytesize=8, timeout=2 )
			
			# The arduino will now reset. Lets wait for it to 
			# finish its boot sequence :). 
			print ("Pizza in owen...")
			time.sleep(3)
			print ("The Pizza is alive!")
			#self.arduino.write("hello\n")
			self.arduino.flush()
			#waiting for the reset of the arduino to finish.
			
			#print (self.arduino.timeout)
			#flushing the buffer.
			#self.arduino.flushOutput()
		except Exception as e: 
			print ("error, %s" % e )
			self.clean_the_mess_up_after_you() #die
		

	def mapNodes(self, nodemap):
		""" 
			This function is mapping a network node id 
			(like hostname, sysname switchname etc) with a 
			corresponding hardware address on the pizzanetmap.

			arguments: 
				-nodemap = { nodeid1 : hwaddr1, nodeid2 : hwaddr2 ... }

			returns: 
				0 on success, -1 on error.
		"""
		pass


	def mapNode(self, node, hwaddr):
		""" 
			This function is mapping ONE network node id 
			(like hostname, sysname switchname etc) with a 
			corresponding hardware address on the pizzanetmap.

			arguments: 
				-node 	=  <string> 	(nodeid)
				-hwaddr =  <u-int32> 	(core.distro.group.pin)

			returns: 
				0 on success, -1 on error.
		"""
		pass		


	def getMappedNodes(self):
		""" 
			This function retrives the current active node map (nodeid --> hwaddr) from the pizzanetmap. 

			arguments: 
					N/A
			returns: -nodemap (<dict>) = { nodeid1 : hwaddr1, nodeid2 : hwaddr2 ... }
		"""
		pass


	def getNodeHwAddr(self, node):
		"""
			This function queries the hardware address of a specific node from the pizzanetmap. 

			arguments:
				-node = <string>  unique id.

			returns:
				-hwaddr = <u-int32> (core.distro.group.pin)

			throws: 
				-NoSuchNodeException
		"""
		pass




	def pushState(self, statemap):
		""" 
			This function pushes states of all nodes to the pizzanetmap. 

			arguments: 
					statemap = { nodeid1(<string>): state1(<boolean>), ...}

			returns: 
				0 on success -1 on error.
		"""
		bits = ''
		b = 0


		
		
		# Start pushstate
		self.arduino.write(chr( self.PUSHSTATE [0] ) )
		
		#import pdb; pdb.set_trace()

		# Sending 7bits at a time.
		chunks = int( len(statemap) / 7 )  +  (1 if len(statemap)%7 > 0 else 0);
		c = chunks
		data = '0'
		bits_sent = 0

		for switch in statemap:
			# Translating on/off to 1/0
			bit = '0' if switch[1].lower() == "off" else '1' 
			# Adding the bit to the chunk to be sent
			data += bit
			b+=1
			
			# Checks if we have a chunk to send
			if (b==7):
				self.arduino.write( chr(int(data, 2)))
				print ( "Data to arduino: %s" % data  )
				b=0
				data = '0'
				c -=1
				bits_sent += 7


		#last chunk:
		if (bits_sent < len(statemap)):
			bits_sent += len(data) - 1
			pad = '0' * ( 8 -  ( len(statemap)-bits_sent) ) 
			self.arduino.write( 
				chr( int( pad + data, 2 ) ) 
			)
			print ( "Data to arduino: %s" % data  )

		
		print ("Sent %d chunks and %d bits" % (chunks, bits_sent))

		
		# End of transmit	
		self.arduino.write(chr( self.PUSHSTATE [1] ) )

		
			


	def getState(self):
		""" 
			This function retrives the current active node map (nodeid --> hwaddr) from the pizzanetmap. 

			arguments: 
					N/A

			returns: 
				statemap = { nodeid1(<string>): state1(<boolean>), ...}
		"""
		pass


	def getNodeInfo(self, node):
		""" 
			This function retrives a tripple of (nodeid, state, hwaddr) 
			for a given node from the pizzanetmap.

			arguments: 
					node: nodeid1(<string>)

			returns: 
				statemap = { nodeid1(<string>): state1(<boolean>), ...}
		"""
		pass


	def getNodeCount(self, line=-1):
		""" 
			This function retrives a the node count of a given line on the pizzanetmap (a core switch). If -1 is given as line argument, it will give all node count.

			arguments: 
					line: uint (core id)

			returns: 
				string of count.
		"""
		while True:
			data = self.arduino.readline()
			if len(data) > 0:
				return data




	def clean_the_mess_up_after_you(self):
		self.arduino.close()


