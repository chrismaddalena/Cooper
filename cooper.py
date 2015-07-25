#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Coopers make barrels, like cooper.py makes barrels for phish.
Cooper.py was created by Chris Maddalena for use with eSentire's phishing tool.
The script will clone a website and automatically process the html to prepare it
for use in a phishing campaign.
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
parser.add_option("-u", "--url",  action="store", type="string", dest="url", help="Specifies URL for images in phishing email templates")
parser.add_option("-x", "--exit",  action="store", type="string", dest="exit", help="Specifies URL to use to create an exit template")
parser.add_option("-d", "--decode",  action="store", type="string", dest="decode", help="Tells Cooper to decode email source (accepts base64 and quoted-printable)")
parser.add_option("-s", "--serverport", action="store", type="int", dest="serverport", help="Use to start HTTP server after template is created")
parser.add_option("-n", "--encode", action="store", type="string", dest="encode", help="Use to encode an image in Base64 for embedding")
(menu, args) = parser.parse_args()

#Process script options
if menu.gate or menu.email or menu.exit or menu.encode or menu.serverport or menu.decode:
	if menu.gate:
		print bcolors.HEADER + "[+] " + bcolors.ENDC + "Processing phishgate request..."
		URL = menu.gate
		toolbox.collectSource(URL)
		phishgate.replaceURL()
		phishgate.fixImageURL(URL)

	if menu.email:
		print bcolors.HEADER + "[+] "  + bcolors.ENDC + "Processing phishing email request..."
		FILE = menu.email
		toolbox.openSource(FILE)
		if menu.decode:
			ENCODING = menu.decode
			phishemail.decodeEmailText(ENCODING)
		phishemail.replaceURL()
		if menu.url:
			URL = menu.url
			phishemail.fixImageURL(URL)
		else:
			print bcolors.WARNING + "[!] "  + bcolors.ENDC + "No URL specified, so images will not be processed."
		phishemail.addTracking()

	if menu.exit:
		print bcolors.HEADER + "[+] " + bcolors.ENDC + "Processing exit template request..."
		URL = menu.exit
		toolbox.collectSource(URL)
		phishexit.replaceURL()
		phishexit.fixImageURL(URL)

	if menu.encode:
		toolbox.encodeImage(menu.encode)

	if menu.serverport:
		PORT = menu.serverport
		print bcolors.HEADER + "[+] "  + bcolors.ENDC + "Starting HTTP server on port", PORT
		toolbox.startHTTPServer(PORT)
else:
	parser.print_help()
