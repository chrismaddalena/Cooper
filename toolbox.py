import sys, SocketServer, SimpleHTTPServer #For running the SimpleHTTP server
import urllib #For wget-like action
import requests #For wget-like action
from BeautifulSoup import BeautifulSoup #For parsing HTML

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
	print "[+] Grabbing source HTML from " + strURL
	try:
		page = requests.get(strURL)
		source = page.text
		sourceFile = open("source.html", "w")
		sourceFile.write(source)
		sourceFile.close()
		print bcolors.OKGREEN + "[+] Succesfully connected to " + strURL + bcolors.ENDC
	except:
		print bcolors.FAIL + "[-] Could not retrieve HTML. Check your internet connection." + bcolors.ENDC

#Takes a port number and starts a server at 127.0.0.1:PORT to view final index.html
def startHTTPServer(PORT):
	PORT = int(PORT)
	handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	try:
		httpd = SocketServer.TCPServer(("", PORT), handler)
		print "[+] Done. See output at port", PORT
		print "[+] Use CTRL+C to kill the web server."
		httpd.serve_forever()
	except:
		print bcolors.FAIL + "[-] Server could not be started. Check port number." + bcolors.ENDC