import re #Used for RegEx
from BeautifulSoup import BeautifulSoup #For parsing HTML
import urlparse #For joining URLs for <img> tags
import base64, urllib

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

#This is Step 1
def replaceURL():
	#Provide user feedback
	print bcolors.OKBLUE + "[+] Here come the URLs..."
	print bcolors.OKBLUE + "[+] URLs that will be replaced:" + bcolors.ENDC
	#Open source, read lines, and begin parsing to replace all URLs inside <a> tags with href
	try:
		#Print href URLs that will be replaced
		print "\n".join(re.findall('<a href="?\'?([^"\'>]*)', open('source.html').read()))
		with open ('source.html', "r") as html:
			#Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html)
			#Find all <a href... and replace URLs with our new text/URL
			for link in soup.findAll('a', href=True):
				link['href'] = '{{links.phishgate}}'
			source = str(soup)
			#Write the updated URLs to source.html
			output = open("source.html", "w")
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print bcolors.OKGREEN + "[+] URL parsing successful. URLs replaced."
	except:
		print bcolors.FAIL + "[-] URL parsing failed. Make sure the html file exists and is readable." + bcolors.ENDC

#This is Step 2
def fixImageURL(strURL):
	#Provide user feedback
	print bcolors.OKBLUE + "[+] Finding IMG tags with src=/... for replacement."
	print bcolors.OKBLUE + "[+] RegEx matches:" + bcolors.ENDC
	#Open source, read lines, and begin parsing to replace all incomplete img src
	try:
		#Print img src URLs that will be modified and provide info
		print "\n".join(re.findall('src="(.*?)"', open('source.html').read()))
		print "[+] Fixing src with " + strURL + "..."
		with open ('source.html', "r") as html:
			#Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html)
			#Find all <img> with src attribute and create a full URL to download and embed image(s)
			for img in soup.findAll('img'):
				imgurl = urlparse.urljoin(strURL, img['src'])
				image = urllib.urlopen(imgurl)
				img_64 = base64.b64encode(image.read())
				img['src'] = "data:image/png;base64," + img_64
				#Encode in Base64 and embed
			source = str(soup)
			#Write the updated addresses to source.html
			output = open("index.html", "w")
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print bcolors.OKGREEN + "[+] IMG parsing successful. IMG src's fixed." + bcolors.ENDC
	except:
		#Exception may occur if file doesn't exist or can't be read/written to
		print bcolors.FAIL + "[-] IMG parsing failed. Make sure the html file exists and is readable." + bcolors.ENDC
