r"""This contains all the disk database access methods.
"""
import libxml2
class Disks(object):
        def __init__(self,diskspath):
		self.diskspath=diskspath
		self.disks=libxml2.parseFile(diskspath)
		return
	def privWrite(self):
                outfile=file(self.diskspath,'w')
                print >> outfile,self.disks
                outfile.close()
		return
	def getDisk(self,name):
		for node in self.disks.xpathEval('/disks/disk[name="'+name+'"]/path'):
			diskpath=node.content
		for node in self.disks.xpathEval('/disks/disk[name="'+name+'"]/type'):
			disktype=node.content
		return diskpath,disktype
	def list(self):
		for node in self.disks.xpathEval('/disks/disk/name'):
			yield unicode(node.content,"utf-8")
		return
	def delete(self,name):
		for node in self.disks.xpathEval('/disks/disk[name="'+name.encode("utf-8")+'"]'):
			node.unlinkNode()
			node.freeNodeList()
		self.privWrite()
		return
	def exists(self,name):
		for node in self.disks.xpathEval('/disks/disk[name="'+name.encode("utf-8")+'"]'):
			return True
		return False
	def add(self,name,path,type,format):
		for node in self.disks.xpathEval('/disks'):
			newnode = node.newChild(None, "disk", None)
			cnode = newnode.newChild(None, "name", name.encode("utf-8"))
			cnode = newnode.newChild(None, "path", path.encode("utf-8"))
			cnode = newnode.newChild(None, "type", type)
			cnode = newnode.newChild(None, "format", format)
		self.privWrite()
		return
