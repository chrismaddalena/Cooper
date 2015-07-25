import re #Used for RegEx
from BeautifulSoup import BeautifulSoup #For parsing HTML
import urlparse #For joining URLs for <img> tags
import base64 #For encoding and embedding images
import urllib #For opening image URLs

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

#This is Step 1 - URLs are replaced with our phishing URLs and new text is saved to source.html
def replaceURL():
	#Provide user feedback
	print bcolors.OKGREEN + "[+] " + bcolors.ENDC + "Replacing URLs..."
	print bcolors.OKGREEN + "[+] " + bcolors.ENDC + "URLs that will be replaced:"
	#Open source, read lines, and begin parsing to replace all URLs inside <a> tags with href
	try:
		#Print href URLs that will be replaced
		print "\n".join(re.findall('<a href="?\'?([^"\'>]*)', open('source.html').read()))
		with open('source.html', "r") as html:
			#Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html)
			#Find all <a href... and replace URLs with our new text/URL
			for link in soup.findAll('a', href=True):
				link['href'] = '{{links.generic}}'
			source = str(soup)
			#Write the updated URLs to source.html while removing the [' and ']
			output = open("source.html", "w")
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print bcolors.OKGREEN + "[+] " + bcolors.ENDC + "URL parsing successful. URLs replaced."
	except:
		print bcolors.FAIL + "[-] URL parsing failed. Make sure the html file exists and is readable." + bcolors.ENDC

#This is Step 2 - Images are found, downloaded, encoded in Base64, and embedded in index.html
def fixImageURL(strURL):
	#Provide user feedback
	print bcolors.OKGREEN + "[+] " + bcolors.ENDC + "Finding IMG tags with src=/... for replacement."
	print bcolors.OKGREEN + "[+] " + bcolors.ENDC + "RegEx matches:"
	#Open source, read lines, and begin parsing to replace all incomplete img src URLs
	try:
		#Print img src URLs that will be modified and provide info
		print "\n".join(re.findall('src="(.*?)"', open('source.html').read()))
		print bcolors.OKGREEN + "[+] " + bcolors.ENDC + "Fixing src with " + strURL + "..."
		with open('source.html', "r") as html:
			#Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html)
			#Find all <img> with src attribute and create a full URL to download and embed image(s)
			for img in soup.findAll('img'):
				imgurl = urlparse.urljoin(strURL, img['src'])
				image = urllib.urlopen(imgurl)
				#Encode in Base64 and embed
				img_64 = base64.b64encode(image.read())
				img['src'] = "data:image/png;base64," + img_64
			source = str(soup.prettify(encoding='utf-8'))
			#Write the updated addresses to source.html while removing the [' and ']
			output = open("index.html", "w")
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print bcolors.OKGREEN + "[+] " + bcolors.ENDC + "IMG parsing successful. IMG src's fixed."
	except:
		#Exception may occur if file doesn't exist or can't be read/written to
		print bcolors.FAIL + "[-] IMG parsing failed. Make sure the html file exists and is readable." + bcolors.ENDC
