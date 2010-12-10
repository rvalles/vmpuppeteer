#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division #1/2 = float, 1//2 = integer, python 3.0 behaviour in 2.6, to make future port to 3 easier.
from optparse import OptionParser
from PosOptionParser import PosOptionParser, Option, IndentedHelpFormatter
import xmlrpclib
#import time
def main():
	optparser = PosOptionParser("usage: %prog [options] <url>",version="%prog 0.1")
	optparser.add_option("--start", dest="start",help="Start VM", metavar="vm")
	optparser.add_option("--stop", dest="stop",help="Stop VM", metavar="vm")
	optparser.add_option("--status", dest="status",help="Inquiry status of VM", metavar="vm")
	optparser.add_option("--shutdown", dest="shutdown",help="Sends friendly shutdown signal to VM", metavar="vm")
	optparser.add_option("--reboot", dest="reboot",help="Reboots VM", metavar="vm")
	optparser.add_option("--suspend", dest="suspend",help="Suspends VM", metavar="vm")
	optparser.add_option("--resume", dest="resume",help="Resume VM", metavar="vm")
	optparser.add_option("--deldisk", dest="deldisk",help="Delete disk", metavar="disk")
	optparser.add_option("--adddisk", dest="adddisk",help="Add disk. Needs remote path, type and format", metavar="disk")
	optparser.add_option("--path", dest="path",help="Path of the file", metavar="path")
	optparser.add_option("--type", dest="type",help="Type of the disk image", metavar="type")
	optparser.add_option("--format", dest="format",help="Format of the disk image", metavar="format")
	optparser.add_option("--listvm", action="store_true", dest="listvm", help="List VMs in the server", default=False)
	optparser.add_option("--listdisk", action="store_true", dest="listdisk", help="List disks in the server", default=False)
	optparser.add_option("--getvm", dest="getvm",help="Obtain VM config file", metavar="vm")
	optparser.add_option("--postvm", dest="postvm",help="Send VM config file. Needs path of the local file.", metavar="remote_filename")
	optparser.add_option("--delvm", dest="delvm",help="Delete vm", metavar="vm")
	#positional args
	optparser.add_positional_argument(Option('--url', action='store_true',help='VM server URL'))
	(options, args) = optparser.parse_args()
	if len(args) != 1:
		optparser.error("incorrect number of arguments")
	for arg in args:
		url = arg
	server = xmlrpclib.ServerProxy(url)
	if options.start!=None:
		print server.start(unicode(options.start,"utf-8"))
	if options.stop!=None:
		print server.stop(unicode(options.stop,"utf-8"))
	if options.status!=None:
		print server.status(unicode(options.status,"utf-8"))
	if options.shutdown!=None:
		print server.shutdown(unicode(options.shutdown,"utf-8"))
	if options.reboot!=None:
		print server.reboot(unicode(options.reboot,"utf-8"))
	if options.suspend!=None:
		print server.suspend(unicode(options.suspend,"utf-8"))
	if options.resume!=None:
		print server.resume(unicode(options.resume,"utf-8"))
	if options.deldisk!=None:
		print server.delDisk(unicode(options.deldisk,"utf-8"))
	if options.adddisk!=None:
		if options.path!=None and options.type!=None and options.format!=None:
			print server.addDisk(unicode(options.adddisk,"utf-8"),unicode(options.path,"utf-8"),options.type,options.format)
		else:
			optparser.error("Missing arguments")
	if options.listvm:
		for name in server.listVm():
			print name.encode("utf-8")
	if options.listdisk:
		for name in server.listDisk():
			print name.encode("utf-8")
	if options.getvm!=None:
		print server.getVm(unicode(options.getvm,"utf-8"))
	if options.postvm!=None:
		if options.path!=None:
			f = open(unicode(options.path,"utf-8"),"r")
			print server.postVm(unicode(options.postvm,"utf-8"),unicode(f.read(),"utf-8"))
			f.close()
		else:
			optparser.error("Missing arguments")
	if options.delvm!=None:
		print server.delVm(unicode(options.delvm,"utf-8"))
if __name__ == '__main__':
	main()
