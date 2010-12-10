r"""This implements the methods that are specific to the vm implementation for
Qemu and KVM, as KVM's userspace component is derived from Qemu, holds almost
the same syntax and will likely merge back into Qemu at some point.
"""
from VmImpl import VmImpl
import subprocess
class VmQemu(VmImpl):
	def __init__(self,vm):
		super(VmQemu,self).__init__(vm)
		return
	def privLaunch(self):
		disklst=list()
		for diskname in self.vm.vmdisks:
			(diskpath,disktype) = self.vm.disks.getDisk(diskname)
			print("disk is"+disktype+"found in"+diskpath)
			if disktype=="cdrom":
				disklst.append("-cdrom")
				disklst.append(diskpath)
			if disktype=="hd":
				disklst.append("-drive")
				disklst.append("file="+diskpath)
		self.proc = subprocess.Popen(["qemu-system-x86_64","-S","-monitor","stdio","-m",self.vm.ram,"-smp",self.vm.cpu]+disklst, 0, None, subprocess.PIPE)
		return
	def start(self):
		self.privLaunch()
		self.proc.stdin.write("cont\n")
		return
	def stop(self):
		print("stopping:"+self.vm.name)
		if self.hasFinished()==None:
			self.proc.stdin.write("quit\n")
		return
	def shutdown(self):
		print("shutting down:"+self.vm.name)
		if self.hasFinished()==None:
			self.proc.stdin.write("system_powerdown\n")
		return
	def reboot(self):
		print("rebooting:"+self.vm.name)
		if self.hasFinished()==None:
			self.proc.stdin.write("system_reset\n")
	def suspend(self):
		print("suspending:"+self.vm.name)
		if self.hasFinished()==None:
			self.proc.stdin.write("stop\nsavevm VmQemu\nquit\n")
		return
	def resume(self):
		print("resuming:"+self.vm.name)
		self.privLaunch()
		self.proc.stdin.write("loadvm VmQemu\ndelvm VmQemu\ncont\n")
		return
	def hasFinished(self):
		return self.proc.poll()
