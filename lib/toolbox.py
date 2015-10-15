#Toolbox contains simple tools that can be called when running Cooper
#and common tools used by all modules.
import sys
import SocketServer
import SimpleHTTPServer #For running the SimpleHTTP server
import requests #For wget-like action
from BeautifulSoup import BeautifulSoup #For parsing HTML
import codecs #Avoids encoding issue when opening HTML files, like apostrophes being replaced
import base64 #For encoding images in base64
import re #Used for RegEx
import urlparse #For joining URLs for <img> tags
import urllib #For opening image URLs

encoding = 'utf-8'

#Takes a URL, scrapes that webpage, and saves source to output file
def collectSource(URL,OUTPUT):
	print "[+] Collecting HTML source from: " + URL
	try:
		page = requests.get(URL) #Uses requests to open webpage
		source = page.text #Get the page source
		sourceFile = codecs.open(OUTPUT, "w", encoding=encoding) #Use codecs to create open file with utf-8 encoding
		sourceFile.write(source)
		sourceFile.close()
		print "[+] Succesfully collected source from: " + URL
	except:
		#If scraping fails, all is lost and we can only exit
		print "[-] Check URL - Must be valid and a fully quaified URL (ex: http://www.foo.bar)."
		sys.exit(0)

#Takes a txt or html file, ingests contents, and dumps it into a output file file for modification
#Original file is preserved and new output file file is created with utf-8 encoding to avoid encoding issues later
def openSource(FILE,OUTPUT):
	print "[+] Opening source HTML file: " + FILE
	try:
		inputFile = open(FILE, "r")
		source = inputFile.read()
		sourceFile = open(OUTPUT, "w")
		sourceFile.write(source)
		sourceFile.close()
	except:
		print "[-] Could not read the email source."
		sys.exit(0)

#Images are found, downloaded, encoded in Base64, and embedded in output file
def fixImageURL(URL,OUTPUT):
	#Provide user feedback
	print "[+] Finding IMG tags with src=/... for replacement:"
	#Open output file, read lines, and begin parsing to replace all incomplete img src URLs
	try:
		#Print img src URLs that will be modified and provide info
		print "\n".join(re.findall('src="(.*?)"', open(OUTPUT).read()))
		print "[+] Fixing src attribute with " + URL + "..."
		with open(OUTPUT, "r") as html:
			#Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html)
			#Find all <img> with src attribute and create a full URL to download and embed image(s)
			for img in soup.findAll('img'):
				imgurl = urlparse.urljoin(URL, img['src'])
				image = urllib.urlopen(imgurl)
				#Encode in Base64 and embed
				img_64 = base64.b64encode(image.read())
				img['src'] = "data:image/png;base64," + img_64
			source = str(soup.prettify(encoding='utf-8'))
			#Write the updated addresses to output file while removing the [' and ']
			output = open(OUTPUT, "w")
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print "[+] IMG parsing successful. All IMG src's fixed."
	except:
		#Exception may occur if file doesn't exist or can't be read/written to
		print "[-] IMG parsing failed. Some images may not have URLs (ex: src = cid:image001.jpg@01CEAD4C.047C2E50)."

#Takes a port number and starts a server at 127.0.0.1:PORT to view final files
def startHTTPServer(PORT):
	PORT = int(PORT)
	handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	try:
		httpd = SocketServer.TCPServer(("", PORT), handler)
		print "[+] Server started. Browse to 127.0.0.1:",PORT
		print "[!] Use CTRL+C to kill the web server."
		httpd.serve_forever()
	except:
		print "[-] Server stopped or could not be started. Please try a different port."

#Takes an image file, encodes it in Base64, and prints encoded output for embedding in a template
def encodeImage(IMAGE):
	#Encode in Base64 and print encoded string for copying
	with open(IMAGE, "rb") as image:
		print "[+] Image has been encoded. Copy this string:\n"
		img_64 = "data:image/png;base64," + base64.b64encode(image.read())
		print img_64 + "\n"
		print "[+] End of encoded string."
