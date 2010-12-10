r"""This is the superclass of all the objects handling implementation specific
virtual machine details. It contains all the methods and attributes that are
common, with empty methods meant to serve as a skeleton.
"""
import libxml2
class VmImpl(object):
        def __init__(self,vm):
		self.vm = vm
                return
	def start(self):
		return
	def stop(self):
		return
	def shutdown(self):
		return
	def suspend():
		return
	def resume():
		return
	def hasFinished(self):
		return
