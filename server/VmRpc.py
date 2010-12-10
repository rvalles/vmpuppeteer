r"""This is the remote API. The enclosed methods are what's offered to the outside
through the XMLRPC interface. They're bound to calls to Vm and Disks objects,
exclusively. Since Python doesn't support private methods, this class
shouldn't contain any non-public method.
"""
import os
import libxml2
from Vm import Vm
class VmRpc(object):
        def __init__(self,vmpath,disks,vmhash):
		self.vmpath = vmpath
		self.disks = disks
		self.vmhash = vmhash
                return
	def start(self,vmname):
		"""Starts a virtual machine
		vmname: Name of the virtual machine"""
		if vmname in self.vmhash:
			return "Error: VM is already running"
		for vmfile in os.listdir(self.vmpath):
			vm = Vm(self.vmpath+'/'+vmfile,self.disks)
			if vm.name==vmname:
				if vm.status=="stopped":
					self.vmhash[vm.name] = vm
					vm.start()
					return "started VM"
				else:
					return "Error: VM is not stopped"
		return "Error: VM not found"
	def stop(self,vmname):
		"""Stops a virtual machine.
		vmname: Name of the virtual machine"""
		if vmname in self.vmhash:
			self.vmhash[vmname].stop()
			return "Stopped VM"
		return "Error: VM not running"
	def shutdown(self,vmname):
		"""Sends gentle shutdown signal to a virtual machine.
		vmname: Name of the virtual machine"""
		if vmname in self.vmhash:
			self.vmhash[vmname].shutdown()
			return "Shutdown sent"
		return "Error: VM not running"
	def reboot(self,vmname):
		"""Forcibly reboots a virtual machine.
		vmname: Name of the virtual machine"""
		if vmname in self.vmhash:
			self.vmhash[vmname].reboot()
			return "Rebooted VM"
		return "Error: VM not running"
	def suspend(self,vmname):
		"""Suspends a virtual machine to a snapshot.
		vmname: Name of the virtual machine"""
		if vmname in self.vmhash:
			self.vmhash[vmname].suspend()
			return "Suspending VM"
		return "Error: VM not running"
	def resume(self,vmname):
		"""Resumes a suspended virtual machine from a snapshot.
		vmname: Name of the virtual machine"""
		if vmname in self.vmhash:
			if self.vmhash[vmname].hasFinished()==None:
				return "Error: VM is still running"
		for vmfile in os.listdir(self.vmpath):
			vm = Vm(self.vmpath+'/'+vmfile,self.disks)
			if vm.name==vmname:
				if vm.status=="suspended":
					self.vmhash[vm.name] = vm
					vm.resume()
					return "Resumed VM"
				else:
					return "Error: VM not suspended"
		return "Error: VM not found"
	def status(self,vmname):
		"""Returns the current status of a virtual machine.
		vmname: Name of the virtual machine"""
		if vmname in self.vmhash:
			return self.vmhash[vmname].status
		for vmfile in os.listdir(self.vmpath):
			vm = Vm(self.vmpath+'/'+vmfile,self.disks)
			if vm.name==vmname:
				return vm.status
		return "Error: VM not found"
	def getVm(self,vmname):
		"""Obtains the XML configuration file of a virtual machine.
		vmname: Name of the virtual machine"""
		#vmname = unicode(vmname.decode("utf-7"))
		#vmname.decode("utf-7").encode("utf-8")
		print("name: "+vmname)
		if vmname in self.vmhash:
			return str(self.vmhash[vmname].vmconfig)
		else:
			for vmfile in os.listdir(self.vmpath):
				vm = Vm(self.vmpath+'/'+vmfile,self.disks)
				if vm.name==vmname:
					return str(vm.vmconfig)
		return "Error: VM not found"
	def postVm(self,filename,vmtext):
		"""Stores the provided virtual machine XML configuration file.
		filename: File to store the XML to
		vmtext: XML of configuration file"""
		#vmtext = unicode(vmtext.decode("utf-7"))
		vmdoc = libxml2.parseDoc(vmtext.encode("utf-8"))
		outfile=file(unicode(self.vmpath)+u"/"+unicode(filename),'w')
		print >> outfile,vmdoc
		outfile.close()
                for node in vmdoc.xpathEval('/vm/name'):
			name = unicode(node.content,"utf-8")
			print("name: "+name)
		return "received VM"
	def listVm(self):
		"""Lists the known virtual machines.
		Returns a list of the virtual machine names."""
		lvm=list()
		for vmfile in os.listdir(self.vmpath):
			vm = Vm(self.vmpath+'/'+vmfile,self.disks)
			lvm.append(vm.name)
		return lvm
	def listDisk(self):
		"""Lists the known disks.
		Returns a list of the disk names"""
		ld=list(self.disks.list())
		return ld
	def delVm(self,vmname):
		"""Deletes a virtual machine.
		vmname: Name of the virtual machine"""
		if vmname in self.vmhash:
			return "Error: VM is still running"
		return "Error: Not Implemented"
	def delDisk(self,diskname):
		"""Deletes a disk from the db.
		diskname: Name of the disk"""
		#diskname = unicode(diskname.decode("utf-7"))
		if self.disks.exists(diskname):
			self.disks.delete(diskname)
			return "Deleted Disk"
		return "Error: Disk not found"
	def addDisk(self,name,path,type,format):
		"""Adds a disk to the db.
		name: Name of the disk
		path: Path there the disk is stored
		type: Type of disk. 'cdrom' and 'hd' are the current supported types
		format: Format in which the disk image is stored; 'raw' for block devices and plain images"""
		#name = unicode(name.decode("utf-7"))
		#path = unicode(path.decode("utf-7"))
		if self.disks.exists(name)==False:
			self.disks.add(name,path,type,format)
			return "Added Disk."
		return "Error: Disk already exists!"
	"""def serveDisk(self,name):
		name = unicode(name.decode("utf-7"))
		if self.disks.exists(name):
			return "Error: TODO"
		return "Error: Disk not found"
	def fetchDisk(self,name,type,format,host,port):
		return "Error: TODO"
		"""
