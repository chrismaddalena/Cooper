#!/usr/bin/env python

'''
Coopers make barrels, like cooper.py makes barrels for phish.
Cooper.py was created by Chris Maddalena for use with eSentire's phishing tool.
The script will clone a website and automatically process the html to prepare it
for use in a phishing campaign.
Usage: python cooper.py URL_TO_CLONE PORT_FOR_HTTP_SERVER
'''
#Imports of importance
import sys

#using init file and we'll import all modules from the lib dir.
#cleans up some code lines
from lib import *
from optparse import OptionParser

#Terminal colors!
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = OptionParser()
parser.add_option("-p", "--phishgate",  action="store", type="string", dest="gate", help="Specifies URL to use to create phishgate")
parser.add_option("-e", "--email",  action="store", type="string", dest="email", help="Specifies file to use to create phishing email template")
parser.add_option("-x", "--exit",  action="store", type="string", dest="exit", help="Specifies URL to use to create an exit template")
parser.add_option("-s", "--serverport", action="store", type="int", dest="serverport", help="Use to start HTTP server after template is created")
(menu, args) = parser.parse_args()

#Process script options
if menu.gate or menu.email or menu.exit or menu.server:
	if menu.gate:
		print bcolors.HEADER + "[+] Processing phishgate request..." + bcolors.ENDC
		URL = menu.gate
		toolbox.collectSource(URL)
		phishgate.replaceURL()
		phishgate.fixImageURL(URL)

	if menu.email:
		print bcolors.HEADER + "[+] Processing phishing email request..." + bcolors.ENDC
		URL = menu.email
		phishemail.replaceURL()
		phishemail.fixImageURL(URL)

	if menu.exit:
		print bcolors.HEADER + "[+] Processing exit template request..." + bcolors.ENDC
		URL = menu.exit
		toolbox.collectSource(URL)
		phishexit.replaceURL()
		phishexit.fixImageURL(URL)

	if menu.serverport:
		PORT = menu.serverport
		toolbox.startHTTPServer(PORT)
else:
	parser.print_help()
