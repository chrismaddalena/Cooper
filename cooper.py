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
#import phishgate #Custom functions for generating phishgates!
#import phishemail #Custom functions for phishing emails!
#import phishexit #Custom functions for exit pages!
#import toolbox
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
parser.add_option("-s", action="store", type="string", dest="server", help="Use to start HTTP server after template is created")
(menu, args) = parser.parse_args()

if menu.gate or menu.email or menu.exit:
	#TODO: Add code to run different functions based on options.
	#TODO: Make sure only p,e, OR x can be used
	#TODO: Make sure input for p, e, and x matches requirements
	print "yay"
else:
	parser.print_help()

#OLD STUFFS
#strUsage = "Usage: cooper.py URL_TO_CLONE SERVER_PORT (ex: cooper.py http://www.google.com 8000)"

#if len(sys.argv) < 3:
#    print strUsage
#else:
#	URL = sys.argv[1]
#	PORT = sys.argv[2]
	#Fetch the source of a given webpage and save it as index.html
#	toolbox.collectSource(URL)
	#Process the index.html to replace links with phishgate links
#	phishgate.replaceURL()
	#Process index.html to fix images that will break
#	phishgate.fixImageURL(URL)
	#Start the SimpleHTTP server to view final index.html file
	#toolbox.startHTTPServer(PORT)
