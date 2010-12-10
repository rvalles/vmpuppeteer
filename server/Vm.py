r"""This handles details specific to each virtual machine, without concerning
itself with vm implementation-specific details. Among other things, it reads
the configuration details of the machine from the configuration file,
maintains these details and the status of the virtual machine and contains the
implementation dependant object, to which it sends the requests that need
to be handled according to vm implementation.
"""
#import os
import libxml2
from VmImpl import VmImpl
from VmNull import VmNull
from VmQemu import VmQemu
class Vm(object):
	def __init__(self,vmfile,disks):
		self.disks = disks
		self.vmfile = vmfile
		print("Parsing:"+vmfile)
		self.vmconfig=libxml2.parseFile(vmfile)
		for node in self.vmconfig.xpathEval('/vm/name'):
			self.name = unicode(node.content,"utf-8")
			print("name: "+self.name)
		for node in self.vmconfig.xpathEval('/vm/autostart'):
			if node.content == "false":
				self.autostart = False
			else:
				self.autostart = True	
			print("autostart: "+str(self.autostart))
		for node in self.vmconfig.xpathEval('/vm/status'):
			self.status = node.content
			print("status: "+self.status)
		if self.status == "running":
			self.status = "stopped"
		elif self.status == "suspending":
			self.status = "stopped"
		for node in self.vmconfig.xpathEval('/vm/ram/mb'):
			self.ram = node.content
			print("ram: "+self.ram)
		for node in self.vmconfig.xpathEval('/vm/cpu/number'):
			self.cpu = node.content
			print("cpu: "+self.cpu)
		self.vmdisks=list()
		for node in self.vmconfig.xpathEval('/vm/disks/disk'):
			self.vmdisks.append(node.content)
		for node in self.vmconfig.xpathEval('/vm/type'):
			self.type = node.content
			print("type: "+self.type)
			if self.type=="qemu":
				self.impl = VmQemu(self)
			elif self.type=="null":
				self.impl = VmImpl(self)
			else:
				self.impl = VmImpl(self)
		return
	def privSetState(self,status):
		self.status=status
		for node in self.vmconfig.xpathEval('/vm/status'):
			node.setContent(status)
		outfile=file(self.vmfile,'w')
		print >> outfile,self.vmconfig
		outfile.close()
		return
	def handleFinished(self):
		returncode = self.hasFinished()
		if self.status=="running":
			self.privSetState("stopped")
		elif self.status=="suspending":
			self.privSetState("suspended")
		return
	def start(self):
		self.impl.start()
		self.privSetState("running")
		return
	def stop(self):
		self.impl.stop()
		self.privSetState("stopped")
		return
	def awake(self):
		if self.status=="stopped":
			self.start()
		elif self.status=="suspended":
			self.resume()
		return
	def shutdown(self):
		self.impl.shutdown()
		return
	def reboot(self):
		self.impl.reboot()
		return
	def suspend(self):
		self.impl.suspend()
		self.privSetState("suspending")
		return
	def resume(self):
		self.impl.resume()
		self.privSetState("running")
		return
	def hasFinished(self):
		return self.impl.hasFinished()
