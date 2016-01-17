#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Coopers make barrels, like cooper.py makes barrels for phish.
Cooper.py was created by Chris Maddalena for use with eSentire's phishing tool.
The script will clone a website and automatically process the html to prepare it
for use in a phishing campaign.
'''
import sys
import os
import time
#Using init file and we'll import all modules from the lib dir.
#This cleans up some code lines.
from lib import *
from optparse import OptionParser

#Create options
parser = OptionParser()
parser.add_option("-o", "--output",  action="store", type="string", dest="output", help="Specifies the filename for the output HTML file. Default is output.html. Including the *.html extension is recommended.")
parser.add_option("-e", "--email",  action="store", type="string", dest="email", help="Specifies the HTML file to use to create a phishing email template")
parser.add_option("-m", "--embed",  action="store_true", dest="embed", help="If enabled, images will be Base64 encoded and embedded into the template")
parser.add_option("-d", "--decode",  action="store", type="string", dest="decode", help="Tells Cooper to decode email source (accepts base64 and quoted-printable)")
parser.add_option("-p", "--phishgate",  action="store", type="string", dest="gate", help="Specifies the URL to use to create a phishgate template")
parser.add_option("-x", "--exit",  action="store", type="string", dest="exit", help="Specifies the URL to use to create an exit template")
parser.add_option("-u", "--url",  action="store", type="string", dest="url", help="Specifies the root URL for images in the target email or webpage")
parser.add_option("-s", "--serverport", action="store", type="int", dest="serverport", help="Use to start an HTTP server to serve up output files")
parser.add_option("-n", "--encode", action="store", type="string", dest="encode", help="Use to encode an image in Base64 for embedding -- recommend using with > output.txt")
parser.add_option("-c", "--collect",  action="store", type="string", dest="collect", help="Pass a URL to create an output file with unchanged page source")
(menu, args) = parser.parse_args()

#Default filename for the output files
OUTPUT = "index.html"

#Does the user want images to be encoded/embedded? True or False
EMBED = menu.embed

try:
    os.system('cls')
except Exception:
    os.system('clear')
time.sleep(1)

print "Welcome to Cooper!"
print ("""\

      CCC
     C
     C    ooo ooo ppp  eee rrr
     C    o o o o p  p e e r
      CCC ooo ooo ppp  ee r
                  p
                  p          _
                             |
    o   o                  ^ |
                  /^^^^^7  L_/
    '  '     ,oO))))))))Oo,
           ,'))))))))))))))), /{
      '  ,'o  ))))))))))))))))={
         >    ))))))))))))))))={
         `,   ))))))\ \)))))))={
           ',))))))))\/)))))' \{
             '*O))))))))O*'

""")

#Process script options
if menu.gate or menu.email or menu.exit or menu.encode or menu.collect:
	#If an output name is specified
	if menu.output:
		OUTPUT = menu.output
		print "[+] Output file will be: " + OUTPUT

	#If email is selected
	if menu.email:
		print "[+] Processing phishing email request..."
		FILE = menu.email
		toolbox.openSource(FILE,OUTPUT)
		if menu.decode:
			ENCODING = menu.decode
			phishemail.decodeEmailText(ENCODING,OUTPUT)
		phishemail.replaceURL(OUTPUT)
		if menu.url:
			URL = menu.url
			if menu.embed == True:
				toolbox.fixImageEncode(URL,OUTPUT)
			else:
				toolbox.fixImageURL(URL,OUTPUT)
		else:
			print "[!] No URL provided, so images will not be processed."
		phishemail.addTracking(OUTPUT)

	#If phishgate is selected
	if menu.gate:
		print "[+] Processing phishgate request..."
		URL = menu.gate
		toolbox.collectSource(URL,OUTPUT)
		phishgate.replaceURL(URL,OUTPUT)
		#phishgate.fixForms(OUTPUT)
		#if menu.url:
		#	if menu.embed == True:
		#		toolbox.fixImageEncode(URL,OUTPUT)
		#	else:
		#		toolbox.fixImageURL(URL,OUTPUT)
		#else:
		#	print "[!] No URL provided, so images will not be processed."
		#Insert this URL last to avoid fixImageURL() & replaceURL() replacing the JS link
		#phishgate.insertPwdEval(OUTPUT)

	#If exit template is selected
	if menu.exit:
		print "[+] Processing exit template request..."
		URL = menu.exit
		toolbox.collectSource(URL,OUTPUT)
		if menu.url:
			URL = menu.url
			if menu.embed == True:
				toolbox.fixImageEncode(URL,OUTPUT)
			else:
				toolbox.fixImageURL(URL,OUTPUT)
		else:
			print "[!] No URL provided, so images will not be processed."

	#If image encoding is enabled
	if menu.encode:
		toolbox.encodeImage(menu.encode)

	#If page source collection is selected
	if menu.collect:
		print "[+] Collecting source and exiting..."
		URL = menu.collect
		toolbox.collectSource(URL,OUTPUT)
		if menu.url:
			URL = menu.url
			if menu.embed == True:
				toolbox.fixImageEncode(URL,OUTPUT)
			else:
				toolbox.fixImageURL(URL,OUTPUT)
		else:
			print "[!] No URL provided, so images will not be processed."

	#If the user requests the HTTP server to be started
	if menu.serverport:
		PORT = menu.serverport
		print "[+] Starting HTTP server on port", PORT
		toolbox.startHTTPServer(PORT)
else:
	#Print help if -h is used or an invalid combination of options/input is used
	parser.print_help()
