'''
Coopers make barrels, like cooper.py makes barrels for phish.
Cooper.py was created by Chris Maddalena for use with eSentire's phishing tool.
The script will clone a website and automatically process the html to prepare it
for use in a phishing campaign.

Usage: python cooper.py URL_TO_CLONE PORT_FOR_HTTP_SERVER
'''
#Imports of importance
import sys
import phishgate #Custom functions for generating phishgates!
import phishemail #Custom functions for phishing emails!
import phishexit #Custom functions for exit pages!
import toolbox

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

strUsage = "Usage: cooper.py URL_TO_CLONE SERVER_PORT (ex: cooper.py http://www.google.com 8000)"

if len(sys.argv) < 3:
    print strUsage
else:
	URL = sys.argv[1]
	PORT = sys.argv[2]
	#Fetch the source of a given webpage and save it as index.html
	toolbox.collectSource(URL)
	#Process the index.html to replace links with phishgate links
	phishgate.replaceURL()
	#Process index.html to fix images that will break
	phishgate.fixImageURL(URL)
	#Start the SimpleHTTP server to view final index.html file
	#toolbox.startHTTPServer(PORT)