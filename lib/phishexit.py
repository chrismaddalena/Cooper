import re # Used for RegEx
from BeautifulSoup import BeautifulSoup #For parsing HTML
import urlparse # For joining URLs for <img> tags
import base64 # For encoding and embedding images
import urllib2 # For opening image URLs

# This is Step 1 - URLs are replaced with our phishing URLs and new text is saved to output file
def replaceURL(URL,OUTPUT):
	# Provide user feedback
	print "[+] Replacing URLs..."
	print "[+] URLs that will be replaced:"
	# Open source, read lines, and begin parsing to replace all URLs inside <a> tags with href
	try:
		# Print href URLs that will be replaced
		print "\n".join(re.findall('<a href="?\'?([^"\'>]*)', open(OUTPUT).read()))
		with open(OUTPUT, "r") as html:
			# Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html)
			# Find all links and replace URLs with our new text/URL
			for link in soup.findAll('a', href=True):
				link['href'] = '{{links.phishgate}}'
			for link in soup.findAll('link', href=True):
				link['href'] = urlparse.urljoin(URL, link['href'])
			for link in soup.findAll('script', src=True):
				link['src'] = urlparse.urljoin(URL, link['src'])
			source = soup.prettify()
			source = xml.sax.saxutils.unescape(source)
			# Write the updated URLs to the output file while removing the [' and ']
			output = open(OUTPUT, "w")
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print "[+] URL parsing successful. URLs replaced."
	except:
		print "[-] URL parsing failed. Make sure the html file exists and is readable."

# This is Step 2 - Images are found, downloaded, encoded in Base64, and embedded in the output file
def fixImageURL(URL,OUTPUT):
	# Provide user feedback
	print "[+] Finding IMG tags with src=/... for replacement."
	print "[+] RegEx matches:"
	# Open source, read lines, and begin parsing to replace all incomplete img src URLs
	try:
		# Print img src URLs that will be modified and provide info
		print "\n".join(re.findall('src="(.*?)"', open(OUTPUT).read()))
		print "[+] Fixing src with " + URL + "..."
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
			# Write the updated addresses to the output file while removing the [' and ']
			output = open(OUTPUT, "w")
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print "[+] IMG parsing successful. IMG src's fixed."
	except:
		# Exception may occur if file doesn't exist or can't be read/written to
		print "[-] IMG parsing failed. Make sure the html file exists and is readable."
