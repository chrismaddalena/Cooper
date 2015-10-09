import re #Used for RegEx
from BeautifulSoup import BeautifulSoup #For parsing HTML
import urlparse #For joining URLs for <img> tags
import base64 #For encoding and embedding images
import urllib #For opening image URLs

#This is Step 1 - URLs are replaced with our phishing URLs and new text is saved to source.html
def replaceURL():
	#Provide user feedback
	print "[+] Replacing URLs..."
	print "[+] URLs that will be replaced:"
	#Open source, read lines, and begin parsing to replace all URLs inside <a> tags with href
	try:
		#Print href URLs that will be replaced
		print "\n".join(re.findall('<a href="?\'?([^"\'>]*)', open('source.html').read()))
		with open('source.html', "r") as html:
			#Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html)
			#Find all links and replace URLs with our new text/URL
			for link in soup.findAll('a', href=True):
				link['href'] = '{{links.generic}}'
			for link in soup.findAll('link', href=True):
				link['href'] = urlparse.urljoin(strURL, link['href'])
			for link in soup.findAll('script', src=True):
				link['src'] = urlparse.urljoin(strURL, link['src'])
			source = str(soup.prettify(encoding='utf-8'))
			#Write the updated URLs to source.html while removing the [' and ']
			output = open("index.html", "w")
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print "[+] URL parsing successful. URLs replaced."
	except:
		print "[-] URL parsing failed. Make sure the html file exists and is readable."

#This is Step 2 - Images are found, downloaded, encoded in Base64, and embedded in index.html
def fixImageURL(strURL):
	#Provide user feedback
	print "[+] Finding IMG tags with src=/... for replacement."
	print "[+] RegEx matches:"
	#Open source, read lines, and begin parsing to replace all incomplete img src URLs
	try:
		#Print img src URLs that will be modified and provide info
		print "\n".join(re.findall('src="(.*?)"', open('source.html').read()))
		print "[+] Fixing src with " + strURL + "..."
		with open('index.html', "r") as html:
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
			print "[+] IMG parsing successful. IMG src's fixed."
	except:
		#Exception may occur if file doesn't exist or can't be read/written to
		print "[-] IMG parsing failed. Make sure the html file exists and is readable."