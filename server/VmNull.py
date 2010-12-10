r"""This is a null class based of the VmImpl superclass. As the name implies,
it does nothing.
"""
from VmImpl import VmImpl
class VmNull(VmImpl):
	def __init__(self,vmfile):
		super(VmNull,self)
