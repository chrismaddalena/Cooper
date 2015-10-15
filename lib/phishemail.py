import re #Used for RegEx
from BeautifulSoup import BeautifulSoup #For parsing HTML
import urlparse #For joining URLs for <img> tags
import base64 #For encoding and embedding images
import urllib #For opening image URLs
import quopri #Adds support for decoding quoted-printable text

#This is Step 1 - Determine encoding and decode if necessary
def decodeEmailText(ENCODING,OUTPUT):
	with open(OUTPUT, "r") as html:
		encoded = html.read()
		if ENCODING in ['quoted-printable', 'qp', 'q-p']:
			print"[+] Decoding quoted-printable text."
			#Decode the quoted-printable text
			source = quopri.decodestring(encoded)
		if ENCODING in ['base64', 'Base64', 'b64', 'B64']:
			print "[+] Decoding Base64 text."
			#Decode the Base64 text
			source = base64.b64decode(encoded)
        output = open(OUTPUT, "w")
        output.write(source)
        output.close()

#This is Step 2 - URLs are replaced with our phishing URLs and new text is saved to output file
def replaceURL(OUTPUT):
	#Provide user feedback
	print "[+] Replacing URLs."
	print "[+] URLs that will be replaced:"
	#Open output file, read lines, and begin parsing to replace all URLs inside <a> tags with href
	try:
		#Print href URLs that will be replaced
		print "\n".join(re.findall('<a href="?\'?([^"\'>]*)', open(OUTPUT).read()))
		with open(OUTPUT, "r") as html:
			#Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html)
			#Find all <a href... and replace URLs with our new text/URL
			for link in soup.findAll('a', href=True):
				link['href'] = '{{links.generic}}'
			source = str(soup.prettify(encoding='utf-8'))
			#Write the updated URLs to output file while removing the [' and ']
			output = open(OUTPUT, "w")
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print "[+] URL parsing successful. URLs replaced."
	except:
		print "[-] URL parsing failed. Make sure the html file exists and is readable."

#This is Step 3 - Images are found, downloaded, encoded in Base64, and embedded in output file
def fixImageURL(URL,OUTPUT):
	#Provide user feedback
	print "[+] Finding IMG tags with src=/... for replacement."
	print "[+] RegEx matches:"
	#Open output file, read lines, and begin parsing to replace all incomplete img src URLs
	try:
		#Print img src URLs that will be modified and provide info
		print "\n".join(re.findall('src="(.*?)"', open(OUTPUT).read()))
		print "[+] Fixing src with " + URL + "..."
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
			print "[+] IMG parsing successful. IMG src's fixed."
	except:
		#Exception may occur if file doesn't exist or can't be read/written to
		print "[-] IMG parsing failed. Make sure the html file exists and is readable."

#This is Step 4 - Inserts our tracking image and writes everything to the index file
def addTracking(OUTPUT):
	#Define the tracking image that will be inserted
	strTracking = '<img src="{{links.tracking}}" style="width:1px; height:1px;"/>'
	print "[+] Inserting tracking image."
	try:
		with open(OUTPUT, "r") as html:
			#Read in the source html and parse with BeautifulSoup
			source = html.read()
			index = source.find(r"</body")
			print "[+] Closing body tag found at index " + str(index)
			tracked = source[:index] + strTracking + source[index:]
			soup = BeautifulSoup(tracked.replace('[','').replace(']',''))
			output = open(OUTPUT, "w")
			output.write(soup.prettify(encoding='utf-8'))
			output.close()
			print "[+] Tracking has been inserted."
	except:
		#Exception may occur if file doesn't exist or can't be read/written to
		print "[-] Failed to insert tracking. Make sure the html file exists and is readable."
