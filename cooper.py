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

#Using init file and we'll import all modules from the lib dir.
#This cleans up some code lines.
from lib import *
from optparse import OptionParser

#Create options
parser = OptionParser()
parser.add_option("-p", "--phishgate",  action="store", type="string", dest="gate", help="Specifies the URL to use to create phishgate")
parser.add_option("-e", "--email",  action="store", type="string", dest="email", help="Specifies the file to use to create phishing email template")
parser.add_option("-u", "--url",  action="store", type="string", dest="url", help="Specifies the root URL for images in the target email or webpage")
parser.add_option("-x", "--exit",  action="store", type="string", dest="exit", help="Specifies the URL to use to create an exit template")
parser.add_option("-d", "--decode",  action="store", type="string", dest="decode", help="Tells Cooper to decode email source (accepts base64 and quoted-printable)")
parser.add_option("-s", "--serverport", action="store", type="int", dest="serverport", help="Use to start HTTP server after template is created")
parser.add_option("-n", "--encode", action="store", type="string", dest="encode", help="Use to encode an image in Base64 for embedding -- recommend using with > output.txt")
parser.add_option("-c", "--collect",  action="store", type="string", dest="collect", help="Specifies the URL to use to create a source.html file without any changes.")
(menu, args) = parser.parse_args()

#Process script options
if menu.gate or menu.email or menu.exit or menu.encode or menu.serverport or menu.decode:
	#If phishgate is selected
	if menu.gate:
		print "[+] Processing phishgate request..."
		URL = menu.gate
		toolbox.collectSource(URL)
		phishgate.replaceURL(URL)
		phishgate.insertPwdEval()
		phishgate.fixForms()
		if menu.url:
			URL = menu.url
			phishgate.fixImageURL(URL)
		else:
			print "[!] No URL provided, so images will not be processed."

	#If email is selected
	if menu.email:
		print "[+] Processing phishing email request..."
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
			print "[!] No URL provided, so images will not be processed."
		phishemail.addTracking()

	#If exit tempalte is selected
	if menu.exit:
		print "[+] Processing exit template request..."
		URL = menu.exit
		toolbox.collectSource(URL)
		phishexit.replaceURL()
		if menu.url:
			URL = menu.url
			phishexit.fixImageURL(URL)
		else:
			print "[!] No URL provided, so images will not be processed."

	#If image encoding is selected
	if menu.encode:
		toolbox.encodeImage(menu.encode)

	#If page source collection is selected
	if menu.collect:
		toolbox.collectSource(mnu.collect)

	#If the user requests the HTTP server to be started
	if menu.serverport:
		PORT = menu.serverport
		print "[+] Starting HTTP server on port", PORT
		toolbox.startHTTPServer(PORT)
else:
	#Print help if -h is used or an invalid combination of options/input is used
	parser.print_help()
