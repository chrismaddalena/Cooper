import sys
import SocketServer
import SimpleHTTPServer #For running the SimpleHTTP server
import urllib #For wget-like action
import requests #For wget-like action
from BeautifulSoup import BeautifulSoup #For parsing HTML
import codecs #Avoids encoding issue when opening HTML files, like apostrophes being replaced
import base64 #For encoding images in base64

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

#Takes a URL, scrape that webpage, and save source to source.html
def collectSource(strURL):
	print bcolors.OKGREEN + "[+] " + bcolors.ENDC + "Grabbing source HTML from " + strURL
	try:
		page = requests.get(strURL)
		source = page.text
		sourceFile = codecs.open("source.html", "w", encoding='utf-8')
		sourceFile.write(source)
		sourceFile.close()
		print bcolors.OKGREEN + "[+] "  + bcolors.ENDC + "Succesfully connected to " + strURL
	except:
		#If scraping fails, all is lost and we can only exit
		print bcolors.FAIL + "[-] Check URL - Must be valid (ex: http://www.foo.bar)" + bcolors.ENDC
		sys.exit(0)

#Takes a txt or html file, takes contents, and dumps it into a source.html file for modification
#Original file is preserved and new source.html file is created with utf-8 encoding to avoid encoding issues later
def openSource(strFile):
	print bcolors.OKGREEN + "[+] " + bcolors.ENDC + "Opening source HTML file: " + strFile
	try:
		inputFile = open(strFile, "r")
		source = inputFile.read()
		sourceFile = codecs.open("source.html", "w", encoding='utf-8')
		sourceFile.write(source)
		sourceFile.close()
	except:
		print bcolors.FAIL + "[-] Could not read in emil source. Check file." + bcolors.ENDC
		sys.exit(0)

#Takes a port number and starts a server at 127.0.0.1:PORT to view final index.html
def startHTTPServer(PORT):
	PORT = int(PORT)
	handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	try:
		httpd = SocketServer.TCPServer(("", PORT), handler)
		print bcolors.OKGREEN + "[+] "  + bcolors.ENDC + "Done. See output at 127.0.0.1:",PORT
		print ncolors.WARNING + "[!] " + bcolors.ENDC + "Use CTRL+C to kill the web server."
		httpd.serve_forever()
	except:
		print bcolors.FAIL + "[-] Server stopped or could not be started. Check port number." + bcolors.ENDC

#Takes an image file, encodes it in Base64, and prints encoded output for embedding in a template
def encodeImage(IMAGE):
	#Encode in Base64 and print encoded string for copying
	with open(IMAGE, "rb") as image:
		print bcolors.OKGREEN + "[+] " + bcolors.ENDC + "Image has been encoded. Copy this string:\n"
		img_64 = base64.b64encode(image.read())
		print img_64 + "\n"
		print ncolors.OKGREEN + "[+] " + bcolors.ENDC + "End of encoded string."
