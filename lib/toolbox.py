#Toolbox contains simple tools that can be called when running Cooper
#and common tools used by all modules.
import sys
import os
import SocketServer
import SimpleHTTPServer # For running the SimpleHTTP server
from BeautifulSoup import BeautifulSoup # For parsing HTML
import codecs # Avoids encoding issue when opening HTML files, like apostrophes being replaced
import base64 # For encoding images in base64
import re # Used for RegEx
import urlparse # For joining URLs for <img> tags
import urllib2 # For collecting source
import subprocess # For calling wget
import time # Mostly for the option to sleep
import xml.sax.saxutils # For unescaping ;lt ;gt ;amp

# User-agent used for urllib
user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)"

# Takes a URL, scrapes that webpage, and saves source to output file
def collectSource(URL,OUTPUT):
	print "[+] Collecting HTML source from: " + URL
	try:
		# Spawn a detachced process to check for wget on the system
		# Detached process removes the wget test call results appearing in the terminal
		DNULL = open(os.devnull, 'w')
		wget = subprocess.call('wget', shell=True, stdout=DNULL, stderr=subprocess.STDOUT)
		if wget == 0:
			# Same command used by SET's, but without -k, convert links
			cmd = 'wget --no-check-certificate -O ' + OUTPUT + ' -c -U \"' + URL + '" "' + URL + '"'
			subprocess.Popen(cmd, shell=True).wait()
			time.sleep(10)
		else:
			headers = { 'User-Agent' : user_agent }
			page = urllib2.Request(URL, None, headers)
			source = urllib2.urlopen(page).read()
			sourceFile = file(OUTPUT, "w")
			sourceFile.write(source)
			sourceFile.close()
		print "[+] Succesfully collected source from: " + URL
	except Exception, err:
		# If scraping fails, all is lost and we can only exit
		print "[-] Check URL - Must be valid and a fully quaified URL (ex: http://www.foo.bar)."
		sys.stderr.write('Error: %sn' % str(err))
		sys.exit(0)

# Takes a txt or html file, ingests contents, and dumps it into a output file file for modification
def openSource(FILE,OUTPUT):
	print "[+] Opening source HTML file: " + FILE
	try:
		inputFile = open(FILE, "r")
		source = inputFile.read()
		sourceFile = open(OUTPUT, "w")
		sourceFile.write(source)
		sourceFile.close()
	except Exception, err:
		print "[-] Could not read the email source."
		sys.stderr.write('Error: %sn' % str(err))
		sys.exit(0)

# Images are found and the source URLs are updated
def fixImageURL(URL,OUTPUT):
	# Provide user feedback
	print "[+] Finding IMG tags with src=/... for replacement:"
	# Open output file, read lines, and begin parsing to replace all incomplete img src URLs
	try:
		# Print img src URLs that will be modified and provide info
		print "\n".join(re.findall('src="(.*?)"', open(OUTPUT).read()))
		print "[+] Fixing src attribute with " + URL + "..."
		with open(OUTPUT, "r") as html:
			# Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html)
			# Find all <img> with src attribute and create a full URL to download and embed image(s)
			for img in soup.findAll('img'):
				imgurl = urlparse.urljoin(URL, img['src'])
				img['src'] = imgurl
			source = soup.prettify()
			source = xml.sax.saxutils.unescape(source)
			# Write the updated addresses to output file while removing the [' and ']
			output = open(OUTPUT, "w")
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print "[+] IMG parsing successful. All IMG src's fixed."
	except Exception, err:
		# Exception may occur if file doesn't exist or can't be read/written to
		print "[-] IMG parsing failed. Some images may not have URLs (ex: src = cid:image001.jpg@01CEAD4C.047C2E50)."
		sys.stderr.write('Error: %sn' % str(err))

# Images are found, downloaded, encoded in Base64, and embedded in output file
# Just like fixImageURL(), but this is only used if the -m --embed option is used
def fixImageEncode(URL,OUTPUT):
	# Provide user feedback
	print "[+] Finding IMG tags with src=/... for replacement:"
	# Open output file, read lines, and begin parsing to replace all incomplete img src URLs
	try:
		# Print img src URLs that will be modified and provide info
		print "\n".join(re.findall('src="(.*?)"', open(OUTPUT).read()))
		print "[+] Fixing src attribute with " + URL + "..."
		with open(OUTPUT, "r") as html:
			# Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html)
			# Find all <img> with src attribute and create a full URL to download and embed image(s)
			for img in soup.findAll('img'):
				imgurl = urlparse.urljoin(URL, img['src'])
				image = urllib2.urlopen(imgurl)
				# Encode in Base64 and embed
				img_64 = base64.b64encode(image.read())
				img['src'] = "data:image/png;base64," + img_64
			source = soup.prettify()
			source = xml.sax.saxutils.unescape(source)
			# Write the updated addresses to output file while removing the [' and ']
			output = open(OUTPUT, "w")
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print "[+] IMG parsing successful. All IMG src's fixed."
	except Exception, err:
		# Exception may occur if file doesn't exist or can't be read/written to
		print "[-] IMG parsing failed. Some images may not have URLs (ex: src = cid:image001.jpg@01CEAD4C.047C2E50)."
		sys.stderr.write('Error: %sn' % str(err))

# Takes a port number and starts a server at 127.0.0.1:PORT to view final files
def startHTTPServer(PORT):
	PORT = int(PORT)
	handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	try:
		httpd = SocketServer.TCPServer(("", PORT), handler)
		print "[+] Server started. Browse to 127.0.0.1:",PORT
		print "[!] Use CTRL+C to kill the web server."
		httpd.serve_forever()
	except Exception, err:
		print "[-] Server stopped or could not be started. Please try a different port."
		sys.stderr.write('Error: %sn' % str(err))

# Takes an image file, encodes it in Base64, and prints encoded output for embedding in a template
# Used with -n --encode and imae files
def encodeImage(IMAGE):
	#Encode in Base64 and print encoded string for copying
	with open(IMAGE, "rb") as image:
		print "[+] Image has been encoded. Copy this string:\n"
		img_64 = "data:image/png;base64," + base64.b64encode(image.read())
		print img_64 + "\n"
		print "[+] End of encoded string."
