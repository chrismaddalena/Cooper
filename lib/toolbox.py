#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  CCC
 C
 C    ooo ooo ppp  eee rrr
 C    o o o o p  p e e r
  CCC ooo ooo ppp  ee r
		  p
		  p

Developer: Chris Maddalena

This contains the Toolbox class used for Cooper. Toolbox contains all of the
carpentry tools necessary to making a fine barrel for some phish.
"""

import sys						# Just used for exiting on fatal errors
import socketserver 			# Used for running the SimpleHTTP server
import http.server 				# Used for running the SimpleHTTP server
from bs4 import BeautifulSoup 	# Use for parsing HTML
import base64 					# Used for encoding images in base64
import requests 				# Used for opening webpages
import urllib.parse 			# For joining URLs for <img> tags
import xml.sax.saxutils 		# For unescaping ;lt ;gt ;amp
import email 					# Used for parsing raw email content
from selenium import webdriver 	# Used for alternative HTML source collection
import configparser 			# Used for loading calues from te config file


class Toolbox(object):
	"""A class containing all of the tools needed to clone and process the contents
	of webpages and emails. The source is collected and then processed to
	automatically modify links, form actions, and images on the fly.
	"""
	# Setup variables for config file parsing and values
	configparser = None
	cooper_config_file = "cooper.config"
	landing_page_url_replacement = None
	landing_page_form_action = None
	email_replacement_url = None
	email_tracker_url = None
	path_to_chromedriver = None
	user_agent = None
	output_file_name = None

	def __init__(self, cooper_config_file):
		"""Everything that should be intiiated with a new Toolbox object goes here."""
		# Determine if the default config file will be used or a user-defined file
		try:
			if cooper_config_file is None:
				print("[+] Using the default config file: {}".format(self.cooper_config_file))
			else:
				self.cooper_config_file = cooper_config_file
				print("[+] Alternate config file identified: {}".format(self.cooper_config_file))
		except Exception as err:
			print("[!] ")
			print("L.. Details: {}".format())
		# Open the config file for parsing
		try:
			self.config_parser = configparser.ConfigParser()
			self.config_parser.read(self.cooper_config_file)
		except Exception as err:
			print("[!] Could not open the config file -- make sure it exists and is readable.")
			print("L.. Details: {}".format(err))
		# Parse the config file's values
		try:
			self.landing_page_url_replacement = self.config_section_map("Replacement URLs")["landing_page_url_replacement"]
			self.landing_page_form_action = self.config_section_map("Replacement URLs")["landing_page_form_action"]
			self.email_replacement_url = self.config_section_map("Replacement URLs")["email_replacement_url"]
			self.email_tracker_url = self.config_section_map("Replacement URLs")["email_tracker_url"]
			self.path_to_chromedriver = self.config_section_map("Browser")["driver_path"]
			if self.config_section_map("Browser")["user_agent"] == "":
				self.user_agent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
			else:
				self.user_agent = self.config_section_map("Browser")["user_agent"]
		except Exception as err:
			print("[!] Failed to read all values from the config file! Exiting...")
			print("L.. Details: {}".format(err))
			sys.exit()

	def config_section_map(self, section):
		"""This function helps by reading a config file section, from cooper.config,
		and returning a dictionary object that can be referenced for configuration
		settings.
		"""
		section_dict = {}
		options = self.config_parser.options(section)
		for option in options:
			try:
				section_dict[option] = self.config_parser.get(section, option)
				if section_dict[option] == -1:
					DebugPrint("[-] Skipping: {}".format(option))
			except:
				print("[!] There was an error with: {}".format(option))
				section_dict[option] = None
		return section_dict

	def process_webpage(self, target, output_file, url, embed, selenium):
		"""Primary function used for cloning a target webpage."""
		# Build the output file's name
		self._build_output_file(output_file)
		# Open the output file and clone the webpage
		with open(self.output_file_name, "w") as output:
			self.collect_source(target, output, url, embed, selenium)

	def process_email(self, email_file, output_file):
		"""Primary function used for processing raw email contents."""
		# Build the output file's name
		self._build_output_file(output_file)
		# Open the output file and email file and process it
		with open(self.output_file_name, "w") as output:
			self.parse_email(email_file, output)

	def collect_source(self, target, file_descriptor, url, embed, selenium):
		"""This function takes a URL, scrapes that webpage, modifies the URLs and
		form actions, and then saves source to the output file.
		"""
		# Collect the raw page source from the target -- like wget or curl
		print("[+] Collecting HTML source from:\n{}".format(target))
		try:
			headers = { 'User-Agent' : self.user_agent }
			if selenium:
				print("[+] Using Selenium mode to load webage.")
				# Setup the Selenium web browser for Chrome
				selenium_browser = webdriver.Chrome(executable_path=self.path_to_chromedriver)
				# Launch the Selenium browser and browse to the target webpage
				selenium_browser.get(target)
				# Grab a snapshot of the original webpage for comparison/reference later
				source = selenium_browser.page_source
				screenshot_file_name = target.split(".")[1]
				print("[+] Taking a snapshot of the original page and saving it as {}.png".format(screenshot_file_name))
				selenium_browser.save_screenshot("{}.png".format(screenshot_file_name))
			else:
				r = requests.get(target, headers=headers)
				source = r.text
			# Parse the source with BeautifulSoup
			soup = BeautifulSoup(source, "html.parser")
			print("[+] Succesfully collected source from the target.")
		except Exception as err:
			# If scraping fails, all is lost and we can only exit
			print("[!] Failed to connect to target -- This must be valid and a fully qualified URL, e.g. http://www.foo.bar.")
			print("L.. Details: {!s}\n".format(err))
			sys.exit()

		# Find and replace the source code's URLs
		try:
			if self.landing_page_url_replacement != "":
				print("[+] Replacing the URLs in the HTML source with: {}".format(self.landing_page_url_replacement))
				for link in soup.findAll('a', href=True):
					link['href'] = self.landing_page_url_replacement
			else:
				print("[-] Warning: No URL provided for landing_page_url_replacement in config file, so the webpage's links will be preserved.")

			if url is not None:
				# Check the URL because if it's invalid it will not work here
				try:
					r = requests.get(url)
					print("[+] Updating the link and script tag src attrbitues with: {}".format(url))
					# Find all links and replace URLs with our new text/URLs
					for link in soup.findAll('link', href=True):
						link['href'] = urllib.parse.urljoin(url, link['href'])
					for link in soup.findAll('script', src=True):
						link['src'] = urllib.parse.urljoin(url, link['src'])
					print("[+] URL parsing successful! All URLs have been replaced.")
					if embed:
						soup = self.fix_images_encode(url, soup, file_descriptor)
					else:
						soup = self.fix_images_url(url, soup, file_descriptor)
				except Exception as err:
					print("[!] The provided base URL, {}, did not work for repairing links and images. This must be valid and a fully qualified URL, e.g. http://www.foo.bar.".format(url))
					print("L.. Details: {}".format(err))
			else:
				print("[-] Warning: No URL provided with --url for updating links, so skipping updating img, link, and script tags.")
		except Exception as err:
			print("[!] URL parsing failed!")
			print("L.. Details: {}".format(err))

		# Find and replace the source code's form actions
		print("[+] Proceeding with updating form actions...")
		try:
			# Find all <form> tags with an action attribute and modify that attribute
			for form in soup.findAll('form'):
				form['action'] = self.landing_page_form_action
				# form['method'] = "post"
				# form['onsubmit'] = "return checkForm(this);"
			print("[+] Form parsing was successful!")
		except Exception as err:
			print("[!] Form parsing failed!")
			print("L.. Details: {}".format(err))

		try:
			# Prettify update source from a blob of HTML to human readable source
			source = soup.prettify()
			# Fix/unescape characters translated to ;lt ;gt ;amp
			source = xml.sax.saxutils.unescape(source)
			# Write the updated source while removing the added [' and ']
			file_descriptor.write(source.replace('[','').replace(']',''))
			print("[+] All operations are complete and the output written to {}".format(self.output_file_name))
		except Exception as err:
			print("[!] Could not write to the output file!")
			print("L.. Details: {}".format(err))

	def _build_output_file(self, output):
		"""Set an output file name -- either default or user defined."""
		if output is None:
			self.output_file_name = "index.html"
		else:
			self.output_file_name = output

	def fix_images_url(self, url, soup, file_descriptor):
		""""Look for images in the source and update the src attrtibutes with
		the provided base URL from --url.
		"""
		# Open output file, read lines, and begin parsing to replace all incomplete img src URLs
		print("[+] Proceeding with updating IMG tag src attributes using: {}".format(url))
		print("[+] The src attrbitues that will be modified:")
		try:
			# Print img src URLs that will be modified and provide info
			# Find all <img> with src attribute and create a full URL to download and embed image(s)
			for img in soup.findAll('img'):
				print("* {}".format(img))
				imgurl = urllib.parse.urljoin(url, img['src'])
				img['src'] = imgurl

			print("[+] IMG parsing was successful!")
		except Exception as err:
			# Exception may occur if file doesn't exist or can't be read/written to
			print("[!] IMG parsing failed. Some images may not have URLs, ex: src = cid:image001.jpg@01CEAD4C.047C2E50.")
			print("L.. Details: {!s}\n".format(err))

		return soup

	def fix_images_encode(self, url, soup, file_descriptor):
		"""Just like fix_images_url, but the src attribute is updated to a Base64
		encoded verison of the images. This is used when the --embed option is used.
		"""
		# Open output file, read lines, and begin parsing to replace all incomplete img src URLs
		print("[+] Proceeding with updating IMG tag src attributes using: {}".format(url))
		print("[+] The src attrbitues that will be modified:")
		try:
			# Print img src URLs that will be modified and provide info
			# Find all <img> with src attribute and create a full URL to download and embed image(s)
			for img in soup.findAll('img'):
				print("* {}".format(img))
				imgurl = urllib.parse.urljoin(url, img['src'])
				image = urllib.request.urlopen(imgurl)
				# Encode in Base64 and embed
				img_64 = base64.b64encode(image.read())
				img['src'] = "data:image/png;base64,{}".format(img_64.decode('ascii'))

			print("[+] IMG parsing was successful!")
		except Exception as err:
			# Exception may occur if file doesn't exist or can't be read/written to
			print("[!] IMG parsing failed. Some images may not have URLs, ex: src = cid:image001.jpg@01CEAD4C.047C2E50.")
			print("L.. Details: {!s}\n".format(err))

		return soup

	def start_http_server(self, port):
		"""A quick function for firing up a simple HTTP server for serving the
		cloned webpages for easy viewing in a browser.

		This only takes a port number as an argument.
		"""
		handler = http.server.SimpleHTTPRequestHandler
		# Check to see if the provided port is valid
		try:
			port = int(port)
		except Exception as err:
			print("[!] Make sure the provided port, {}, is a valid port number.".format(port))
			sys.exit()
		# Try to start the web server on the localhost using the provided port
		try:
			httpd = socketserver.TCPServer(("", port), handler)
			print("[+] Server started. Browse to 127.0.0.1:{}".format(port))
			print("[!] Use CTRL+C to kill the web server.")
			# Serve until it is killed
			httpd.serve_forever()
		except Exception as err:
			print("[-] Server stopped or could not be started. Please try a different port.")
			print("L.. Details: {}".format(err))

	def encode_image(self, image):
		"""This function takes an image file, encodes it in Base64, and prints
		encoded output for embedding in a template."""
		# Encode in Base64 and print encoded string for copying
		with open(image, 'rb') as image:
			print("[+] Image has been encoded. Copy this string:\n")
			img_64 = '<img src="data:image/png;base64,{}">'.format(base64.b64encode(image.read()).decode('ascii'))
			print(img_64 + "\n")
			print("[+] End of encoded string.")

	def parse_email(self, email_file, file_descriptor):
		"""Takes a txt or html file with raw email source, ingests contents, and
		modifies it for phishing.
		"""
		# Open the email file and parse its contents
		print("[+] Opening source email file: {}".format(email_file))
		with open(email_file, 'r') as input_file:
			# Read-in the raw email content
			try:
				e = email.message_from_string(input_file.read())
			except Exception as err:
				print("[!] Failed to open the email file!")
				print("L.. Details: {}".format(err))

			try:
				# Check if the email is a multipart MIME message or not
				source = ""
				if e.is_multipart():
					print("[+] Processing multi-part email message...")
					# Walk through the multi-part MIME message
					for payload in e.walk():
						# Check the content disposition, such as "attachment"
						content_disposition = payload.get_content_disposition()
						attachment = None
						attachment = payload.get_filename()
						# We need to ditch the attachments, so detect and drop them
						if attachment is not None:
							print("[+] Attachment detected and discarded: {}, {}".format(content_disposition, attachment))
						# Find the plaintext and HTML parts
						elif payload.get_content_type() == "text/html":
							source += payload.get_payload(decode=True).decode(payload.get_content_charset())
						elif payload.get_content_type() == "plain/text":
							source += payload.get_payload(decode=True).decode(payload.get_content_charset())

					# Replace the URLs
					soup = BeautifulSoup(source, "html.parser")
					if self.email_replacement_url != "":
						print("[+] Replacing any URLs in the email content: {}".format(self.email_replacement_url))
						for link in soup.findAll('a', href=True):
							link['href'] = self.email_replacement_url
					else:
						print("[-] Warning: No URL provided for email_replacement_url in config file, so the email's links will be preserved.")

					try:
						# Prettify update source from a blob of HTML to human readable source
						source = soup.prettify()
						# Fix/unescape characters translated to ;lt ;gt ;amp
						source = xml.sax.saxutils.unescape(source)

						source = self.add_tracker_to_email(source)

						# Write the updated source while removing the added [' and ']
						file_descriptor.write(source.replace('[','').replace(']',''))
						print("[+] All operations are complete and the output written to {}".format(self.output_file_name))
					except Exception as err:
						print("[!] Could not write to the output file!")
						print("L.. Details: {}".format(err))
				else:
					# We have a non-multipart message, so write out what we have
					print("[+] Processing non-multipart email message...")
					for payload in e.walk():
						source += payload.get_payload(decode=True).decode(payload.get_content_charset())

					# Replace the URLs
					soup = BeautifulSoup(source, "html.parser")
					if self.email_replacement_url != "":
						print("[+] Replacing any URLs in the email content: {}".format(self.email_replacement_url))
						for link in soup.findAll('a', href=True):
							link['href'] = self.email_replacement_url
					else:
						print("[-] Warning: No URL provided for email_replacement_url in config file, so the email's links will be preserved.")

					try:
						# Prettify update source from a blob of HTML to human readable source
						# This also makes it a string we can use for this next part
						source = soup.prettify()
						source = self.add_tracker_to_email(source)
						# Fix/unescape characters translated to ;lt ;gt ;amp
						source = xml.sax.saxutils.unescape(source)
						# Write the updated source while removing the added [' and ']
						file_descriptor.write(source.replace('[','').replace(']',''))
						print("[+] All operations are complete and the output written to {}".format(self.output_file_name))
					except Exception as err:
						print("[!] Could not write to the output file!")
						print("L.. Details: {}".format(err))

				print("[+] All processes are complete! Check your output file: {}".format(self.output_file_name))
			except Exception as err:
				print("[!] Failed to write out the email contents!")
				print("L.. Details: {}".format(err))

	def add_tracker_to_email(self, source):
		"""Inserts a tracking image and writes everything to the index file."""
		# Define the tracking image that will be inserted
		tracking_string = '<img src="{}" style="width:1px; height:1px;"/>'.format(self.email_tracker_url)
		print("[+] Attempting to insert the tracking image.")
		try:
			# Find the closing body tag in the email
			index = source.find(r"</body")
			if index == -1:
				print("[!] Cooper could not find a closing body tag. A tracking image has not been inserted.")
				print('L.. If desired, manually add: <img src="{}" style="width:1px; height:1px;"/>'.format(self.email_tracker_url))

				return source
			else:
				print("[+] Closing body tag found at index {!s}.".format(index))
				tracked_source = source[:index] + tracking_string + source[index:]
				print("[+] Tracking has been inserted.")

				return tracked_source
		except:
			# Exception may occur if file doesn't exist or can't be read/written to
			print("[!] Cooper could not find a closing body tag. A tracking image has not been inserted.")
			print('L.. If desired, manually add: <img src="{}" style="width:1px; height:1px;"/>'.format(self.email_tracker_url))
