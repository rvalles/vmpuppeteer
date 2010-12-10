#!/usr/bin/python
from __future__ import division #1/2 = float, 1//2 = integer, python 3.0 behaviour in 2.6, to make future port to 3 easier.
from optparse import OptionParser
from PosOptionParser import PosOptionParser, Option, IndentedHelpFormatter
import cherrypy
import xmlrpclib
from mako.template import Template
from mako.lookup import TemplateLookup
mylookup = TemplateLookup(directories=['templates'],output_encoding='utf-8', encoding_errors='replace')
def main():
	global url
	optparser = PosOptionParser("usage: %prog [options] <url>",version="%prog 0.1")
	optparser.add_positional_argument(Option('--url', action='store_true',help='VM server URL'))
	(options, args) = optparser.parse_args()
	url = None
	for arg in args:
		url = arg
	if url == None:
		print "Server URL is needed and not provided."
		return
	cherrypy.quickstart(webfe(),'/','config.txt')
class webfe:
	def index(self):
		 redirect = cherrypy.HTTPRedirect("/vmlist")
                 redirect.set_response()
	index.exposed = True
	@cherrypy.expose
	def default(self):
		return "Something is going wrong."
	@cherrypy.expose
	def vmlist(self):
                server = xmlrpclib.ServerProxy(url)
 	        vmlist = {}
		for vm in server.listVm():
			vmlist[vm] = server.status(vm)
		mytemplate = mylookup.get_template("vmlisting.html")
		return mytemplate.render_unicode(vms=vmlist).encode('utf-8', 'replace')		
	@cherrypy.expose
	def startvm(self,vmname=None):
		if not vmname == None:
			server = xmlrpclib.ServerProxy(url)
			#server.start(unicode(vmname,"utf-8"))
			server.start(vmname)
		redirect = cherrypy.HTTPRedirect("/vmlist")
		redirect.set_response()
	@cherrypy.expose
        def stopvm(self,vmname=None):
                if not vmname == None:
                        server = xmlrpclib.ServerProxy(url)
                        server.stop(vmname)
                redirect = cherrypy.HTTPRedirect("/vmlist")
                redirect.set_response()
	@cherrypy.expose
        def shutdownvm(self,vmname=None):
                if not vmname == None:
                        server = xmlrpclib.ServerProxy(url)
			server.shutdown(vmname)
                redirect = cherrypy.HTTPRedirect("/vmlist")
                redirect.set_response()
        @cherrypy.expose
        def suspendvm(self,vmname=None):
                if not vmname == None:
                        server = xmlrpclib.ServerProxy(url)
			server.suspend(vmname)
                redirect = cherrypy.HTTPRedirect("/vmlist")
                redirect.set_response()
        @cherrypy.expose
        def resumevm(self,vmname=None):
                if not vmname == None:
                        server = xmlrpclib.ServerProxy(url)
			server.resume(vmname)
                redirect = cherrypy.HTTPRedirect("/vmlist")
                redirect.set_response()
        @cherrypy.expose
        def rebootvm(self,vmname=None):
                if not vmname == None:
                        server = xmlrpclib.ServerProxy(url)
			server.reboot(vmname)
                redirect = cherrypy.HTTPRedirect("/vmlist")
                redirect.set_response()
if __name__ == '__main__':
	main()
