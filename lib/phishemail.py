import re # Used for RegEx
from bs4 import BeautifulSoup # For parsing HTML
import urllib.parse # For joining URLs for <img> tags
import xml.sax.saxutils # For unescaping ;lt ;gt ;amp

# This is Step 1 - URLs are replaced with our phishing URLs and new text is saved to output file
def replaceURL(OUTPUT):
	# Open output file, read lines, and begin parsing to replace all URLs inside <a> tags with href
	try:
		# Print href URLs that will be replaced
		with open(OUTPUT, 'rb') as html:
			# Read in the source html and parse with BeautifulSoup
			soup = BeautifulSoup(html,"html.parser")
			# Provide user feedback so they can verify the URLs being replaced
			results = re.findall('<a href="?\'?([^"\'>]*)', str(soup))
			print("[+] These {} URLs will be replaced in the HTML:".format(len(results)))
			counter = 1
			for result in results:
				print("[{}] {}".format(counter, result))
				counter += 1
			# Find all <a href... and replace URLs with our new text/URL
			for link in soup.findAll('a', href=True):
				link['href'] = '{{links.generic}}'
			source = soup.prettify()
			source = xml.sax.saxutils.unescape(source)
			# Write the updated URLs to output file while removing the [' and ']
			output = open(OUTPUT, 'w')
			output.write(source.replace('[','').replace(']',''))
			output.close()
			print("[+] URL parsing successful. All URLs have been replaced.")
	except:
		print("[-] URL parsing failed. Make sure the html file exists and is readable.")

# This is Step 2 - Inserts our tracking image and writes everything to the index file
def addTracking(OUTPUT):
	# Define the tracking image that will be inserted
	strTracking = '<img src="{{links.tracking}}" style="width:1px; height:1px;"/>'
	print("[+] Attempting to insert the tracking image.")
	try:
		with open(OUTPUT, 'r') as html:
			# Read in the source html and parse with BeautifulSoup
			source = html.read()
			index = source.find(r"</body")
			if index == -1:
				print("[!] Cooper could not find a closing body tag. There is probably an issue with the decoding or HTML! Tracking has not been inserted.")
			else:
				print("[+] Closing body tag found at index {!s}.".format(index))
				tracked = source[:index] + strTracking + source[index:]
				soup = BeautifulSoup(tracked.replace('[','').replace(']',''),"html.parser")
				source = soup.prettify()
				source = xml.sax.saxutils.unescape(source)
				output = open(OUTPUT, 'w')
				output.write(source)
				output.close()
				print("[+] Tracking has been inserted.")
	except:
		# Exception may occur if file doesn't exist or can't be read/written to
		print("[-] Failed to insert tracking. Make sure the html file exists and is readable.")
