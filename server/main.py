#!/usr/bin/python
from __future__ import division #1/2 = float, 1//2 = integer, python 3.0 behaviour in 2.6, to make future port to 3 easier.
import os
import libxml2
import signal
import time
import DocXMLRPCServer
from Vm import Vm
from VmRpc import VmRpc
from Disks import Disks
vmhash = {}
def handleFinished():
	vmdellst = list()
	for vm in vmhash.itervalues():
		if vm.hasFinished()!=None:
			vmdellst.append(vm.name)
			vm.handleFinished()
	for vmdel in vmdellst:
		del vmhash[vmdel]
	return
def shutdown(sigid,stackframe):
	print "Gracefully exiting..."
	for vm in vmhash.itervalues():
		vm.shutdown()
	while len(vmhash):
		time.sleep(1)
		handleFinished()
	quit()
	return
def main():
	print("vm server initializing")
	config = libxml2.parseFile("config.xml")
	for node in config.xpathEval('/vmconfig/path'):
		 vmpath = node.content
	print(vmpath)
	for node in config.xpathEval('/vmconfig/diskspath'):
		 diskspath = node.content
	print(diskspath)
	for node in config.xpathEval('/vmconfig/auth/login'):
		login = node.content
	for node in config.xpathEval('/vmconfig/auth/passwd'):
		passwd = node.content
	for node in config.xpathEval('/vmconfig/bind/ip'):
		bindip = node.content
	for node in config.xpathEval('/vmconfig/bind/port'):
		bindport = int(node.content)
	disks = Disks(diskspath)
	for vmfile in os.listdir(vmpath):
		vm = Vm(vmpath+'/'+vmfile,disks)
		if vm.autostart:
			print("autostarting "+vm.name)
			vm.awake()
			if vm.status=="running":
				vmhash[vm.name] = vm
	signal.signal(signal.SIGINT, shutdown)
	signal.signal(signal.SIGTERM, shutdown)
	#signal.pause()
	vmrpc = VmRpc(vmpath,disks,vmhash)
	server = DocXMLRPCServer.DocXMLRPCServer(tuple([bindip, bindport]))
	server.register_instance(vmrpc)
	print "Listening on: http://"+bindip+":"+str(bindport)+"/"
	server.timeout = 1
	while True:
		handleFinished()
		#server.serve_forever()
		server.handle_request()
	return
if __name__ == '__main__':
	main()
