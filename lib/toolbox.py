# Toolbox contains simple tools that can be called when running Cooper
# and common tools used by all modules.
import sys
import os
import socketserver
import http.server # For running the SimpleHTTP server
from bs4 import BeautifulSoup # For parsing HTML
import base64 # For encoding images in base64
import re # Used for RegEx
import requests # Used for opening webpages
import urllib.parse # For joining URLs for <img> tags
import xml.sax.saxutils # For unescaping ;lt ;gt ;amp
import email # Used for parsing raw email content

# User-agent used for urllib
user_agent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"

# Takes a URL, scrapes that webpage, and saves source to output file
def collectSource(URL,OUTPUT):
	print("[+] Collecting HTML source from: {}".format(URL))
	try:
		header = { 'User-Agent' : user_agent }
		r = requests.get(URL, headers=header)
		source = r.text
		sourceFile = open(OUTPUT, 'w')
		sourceFile.write(source)
		sourceFile.close()
		print("[+] Succesfully collected source from: {}".format(URL))
	except Exception as err:
		# If scraping fails, all is lost and we can only exit
		print("[-] Check URL - Must be valid and a fully qualified URL (ex: http://www.foo.bar).")
		sys.stderr.write("Error: {!s}\n".format(err))
		sys.exit(0)

# Takes a txt or html file (an email), ingests contents, and dumps it into a output file for modification
def openEmail(FILE,OUTPUT):
	print("[+] Opening source HTML file: {}".format(FILE))
	with open(FILE, 'r') as inputFile:
		b = email.message_from_string(inputFile.read())
		if b.is_multipart():
			print("[+] Processing multi-part email message.")
			for payload in b.get_payload():
				print("[+] Processing {} content...".format(payload.get_content_charset()))
				with open(OUTPUT, 'wb') as sourceFile:
					sourceFile.write(payload.get_payload(decode=True))
		else:
			print("[+] Processing {} content...".format(payload.get_content_charset()))
			with open(OUTPUT, 'wb') as sourceFile:
				sourceFile.write(payload.get_payload(decode=True))

# Images are found and the source URLs are updated
def fixImageURL(URL,OUTPUT):
	# Provide user feedback
	print("[+] Finding IMG tags with src=/... for replacement:")
	# Open output file, read lines, and begin parsing to replace all incomplete img src URLs
	try:
		# Print img src URLs that will be modified and provide info
		print("\n".join(re.findall('src="(.*?)"', open(OUTPUT).read())))
		print("[+] Fixing src attribute with {}...".format(URL))
		with open(OUTPUT, 'r') as html:
			# Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html,"html.parser")
			# Find all <img> with src attribute and create a full URL to download and embed image(s)
			for img in soup.findAll('img'):
				imgurl = urllib.parse.urljoin(URL, img['src'])
				img['src'] = imgurl
			source = soup.prettify()
			source = xml.sax.saxutils.unescape(source)
			# Write the updated addresses to output file while removing the [' and ']
			output = open(OUTPUT, 'w')
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print("[+] IMG parsing successful. All IMG src's fixed.")
	except Exception as err:
		# Exception may occur if file doesn't exist or can't be read/written to
		print("[-] IMG parsing failed. Some images may not have URLs (ex: src = cid:image001.jpg@01CEAD4C.047C2E50).")
		sys.stderr.write("Error: {!s}\n".format(err))

# Images are found, downloaded, encoded in Base64, and embedded in output file
# Just like fixImageURL(), but this is only used if the -m --embed option is used
def fixImageEncode(URL,OUTPUT):
	# Provide user feedback
	print("[+] Finding IMG tags with src=/... for replacement:")
	# Open output file, read lines, and begin parsing to replace all incomplete img src URLs
	try:
		# Print img src URLs that will be modified and provide info
		print("\n".join(re.findall('src="(.*?)"', open(OUTPUT).read())))
		print("[+] Fixing src attribute with {}...".format(URL))
		with open(OUTPUT, 'r') as html:
			# Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html,"html.parser")
			# Find all <img> with src attribute and create a full URL to download and embed image(s)
			for img in soup.findAll('img'):
				imgurl = urllib.parse.urljoin(URL, img['src'])
				image = urllib.request.urlopen(imgurl)
				# Encode in Base64 and embed
				img_64 = base64.b64encode(image.read())
				img['src'] = "data:image/png;base64,{}".format(img_64.decode('ascii'))
			source = soup.prettify()
			source = xml.sax.saxutils.unescape(source)
			# Write the updated addresses to output file while removing the [' and ']
			output = open(OUTPUT, 'w')
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print("[+] IMG parsing successful. All IMG src's fixed.")
	except Exception as err:
		# Exception may occur if file doesn't exist or can't be read/written to
		print("[-] IMG parsing failed. Some images may not have URLs (ex: src = cid:image001.jpg@01CEAD4C.047C2E50).")
		sys.stderr.write("Error: {!s}\n".format(err))

# Takes a port number and starts a server at 127.0.0.1:PORT to view final files
def startHTTPServer(PORT):
	PORT = int(PORT)
	handler = http.server.SimpleHTTPRequestHandler
	try:
		httpd = socketserver.TCPServer(("", PORT), handler)
		print("[+] Server started. Browse to 127.0.0.1:",PORT)
		print("[!] Use CTRL+C to kill the web server.")
		httpd.serve_forever()
	except Exception as err:
		print("[-] Server stopped or could not be started. Please try a different port.")
		sys.stderr.write("Error: {!s}\n".format(err))

# Takes an image file, encodes it in Base64, and prints encoded output for embedding in a template
# Used with -n --encode and imae files
def encodeImage(IMAGE):
	#Encode in Base64 and print encoded string for copying
	with open(IMAGE, 'rb') as image:
		print("[+] Image has been encoded. Copy this string:\n")
		img_64 = '<img src="data:image/png;base64,{}">'.format(base64.b64encode(image.read()))
		print(img_64.decode('ascii') + "\n")
		print("[+] End of encoded string.")
