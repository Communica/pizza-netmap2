#!/usr/bin/env python
# coding: utf-8

#	
#	Python API for the PNMP protocol
#
import serial
from serial.tools import list_ports
import time

class api():
	""" The Pizza-Netmap Network Monitoring Protocol api """
	

	def __init__(self, COM_PORT, BAUD_RATE=9600):
		
		
		try:
			# Opening a serial connection to the arduino :).
			self.arduino = serial.Serial(COM_PORT, BAUD_RATE, timeout=0 )
			
			print ("Done sleeping")
			self.arduino.write("hello\n")
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
		pass


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
