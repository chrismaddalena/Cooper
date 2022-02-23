#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This contains the ``Toolbox`` class used for Cooper. ``Toolbox`` contains all of the
carpentry tools necessary to making a fine barrel for some phish.
"""

# Standard Libraries
import base64
import configparser
import email
import http.server
import socketserver
import sys
import urllib.parse
import xml.sax.saxutils
from mimetypes import guess_extension

# 3rd Party Libraries
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Toolbox(object):
    """
    A class containing all of the tools needed to clone and process the contents
    of webpages and emails. The source is collected and then processed to
    automatically modify links, form actions, and images on the fly.
    """

    # Setup variables for config file parsing and values
    configparser = None
    cooper_config_file = "cooper.config"

    user_agent = None
    output_file_name = None
    email_tracker_url = None
    path_to_chromedriver = None
    email_replacement_url = None
    landing_page_form_action = None
    landing_page_url_replacement = None

    def __init__(self, cooper_config_file):
        """Everything that should be initiated with a new ``Toolbox`` object goes here."""

        # Determine if the default config file will be used or a user-defined file
        try:
            if cooper_config_file is None:
                print(
                    "[+] Using the default config file: {}".format(
                        self.cooper_config_file
                    )
                )
            else:
                self.cooper_config_file = cooper_config_file
                print(
                    "[+] Alternate config file identified: {}".format(
                        self.cooper_config_file
                    )
                )
        except Exception as err:
            print("[!] Failed to load the config file!")
            print("L.. Details: {}".format())

        # Open the config file for parsing
        try:
            self.config_parser = configparser.ConfigParser()
            self.config_parser.read(self.cooper_config_file)
        except Exception as err:
            print(
                "[!] Could not open the config file -- make sure it exists and is readable."
            )
            print(f"L.. Details: {err}")

        # Parse the config file's values
        try:
            self.landing_page_url_replacement = self.config_section_map(
                "Replacement URLs"
            )["landing_page_url_replacement"]
            self.landing_page_form_action = self.config_section_map("Replacement URLs")[
                "landing_page_form_action"
            ]
            self.email_replacement_url = self.config_section_map("Replacement URLs")[
                "email_replacement_url"
            ]
            self.email_tracker_url = self.config_section_map("Replacement URLs")[
                "email_tracker_url"
            ]
            self.path_to_chromedriver = self.config_section_map("Browser")["driver_path"]
            self.user_agent = self.config_section_map("Browser")["user_agent"]
        except Exception as err:
            print("[!] Failed to read all values from the config file! Exiting...")
            print(f"L.. Details: {err}")
            sys.exit()

    def config_section_map(self, section):
        """Read a config file section from ``cooper.config`` and return a dictionary."""

        section_dict = {}
        options = self.config_parser.options(section)
        for option in options:
            try:
                section_dict[option] = self.config_parser.get(section, option)
                if section_dict[option] == -1:
                    print(f"[-] Skipping: {option}")
            except:
                print(f"[!] There was an error with: {option}")
                section_dict[option] = None
        return section_dict

    def process_webpage(self, target, output_file, url, embed, selenium):
        """Primary function used for cloning a target webpage."""

        self._build_output_file(output_file)
        with open(self.output_file_name, "w") as output:
            self.collect_source(target, output, url, embed, selenium)

    def process_email(self, email_file, output_file):
        """Primary function used for processing raw email contents."""

        self._build_output_file(output_file)
        with open(self.output_file_name, "w") as output:
            self.parse_email(email_file, output)

    def collect_source(self, target, file_descriptor, url, embed, selenium):
        """
        Takes a URL, scrapes that webpage, modifies the URLs and form actions,
        and then saves source to the output file.
        """

        print(f"[+] Collecting HTML source from:\n{target}")
        try:
            headers = {"User-Agent": self.user_agent}
            if selenium:
                print("[*] Using Selenium to load the webage")
                timeout = 10
                driver = webdriver.Chrome(executable_path=self.path_to_chromedriver)

                driver.get(target)
                WebDriverWait(driver, timeout).until(
                    lambda driver: driver.execute_script("return document.readyState")
                    == "complete"
                )

                source = driver.page_source

                screenshot_file_name = target.split(".")[1]
                print(f"[+] Taking a snapshot of the original page and saving it as {screenshot_file_name}.png")
                driver.save_screenshot(f"{screenshot_file_name}.png")

                driver.quit()
            else:
                r = requests.get(target, headers=headers)
                source = r.text

            # Parse the source with BeautifulSoup
            soup = BeautifulSoup(source, "html.parser")
            print("[+] Succesfully collected source from the target.")
        except Exception as err:
            # If scraping fails, all is lost and we can only exit
            print(
                "[!] Failed to connect to target -- This must be valid and a fully qualified URL, e.g. http://www.foo.bar."
            )
            print(f"L.. Details: {err}\n")
            sys.exit()

        # Find and replace the source code's URLs
        try:
            if self.landing_page_url_replacement != "":
                print(f"[+] Replacing the URLs in the HTML source with: {self.landing_page_url_replacement}")
                for link in soup.findAll("a", href=True):
                    link["href"] = self.landing_page_url_replacement
            else:
                print(
                    "[*] Warning: No URL provided for `landing_page_url_replacement` in config file, so the webpage's links will be preserved."
                )

            if url is not None:
                # Check the URL because if it's invalid it will not work here
                try:
                    r = requests.get(url)
                    print(f"[+] Updating the link and script tag src attrbitues with: {url}")
                    # Find all links and replace URLs with our new text/URLs
                    for link in soup.findAll("link", href=True):
                        link["href"] = urllib.parse.urljoin(url, link["href"])
                    for link in soup.findAll("script", src=True):
                        link["src"] = urllib.parse.urljoin(url, link["src"])
                    print("[+] URL parsing successful! All URLs have been replaced.")
                    if embed:
                        soup = self.fix_images_encode(url, soup, file_descriptor)
                    else:
                        soup = self.fix_images_url(url, soup, file_descriptor)
                except Exception as err:
                    print(f"[!] The provided base URL, {url}, did not work for repairing links and images. This must be valid and a fully qualified URL, e.g. http://www.foo.bar.")
                    print(f"L.. Details: {err}")
            else:
                print(
                    "[*] Warning: No URL provided with `--url` for updating links, so skipping updating `img`, `link`, and `script` tags."
                )
        except Exception as err:
            print("[!] URL parsing failed!")
            print(f"L.. Details: {err}")

        # Find and replace the source code's form actions
        print("[+] Proceeding with updating form actions...")
        try:
            # Find all ``<form>`` tags with an action attribute and modify that attribute
            for form in soup.findAll("form"):
                form["action"] = self.landing_page_form_action
            print("[+] Form parsing was successful!")
        except Exception as err:
            print("[!] Form parsing failed!")
            print(f"L.. Details: {err}")

        try:
            # Fix/unescape characters translated to ;lt ;gt ;amp
            source = soup.prettify()
            source = xml.sax.saxutils.unescape(source)
            file_descriptor.write(source)
            print(f"[+] All operations are complete and the output written to {self.output_file_name}")
        except Exception as err:
            print("[!] Could not write to the output file!")
            print(f"L.. Details: {err}")

    def _build_output_file(self, output):
        """Set an output file name -- either default or user defined."""
        if output is None:
            self.output_file_name = "index.html"
        else:
            self.output_file_name = output

    def fix_images_url(self, url, soup):
        """
        Look for images in the source and update the src attrtibutes with
        the provided base URL from ``--url``.
        """

        # Open output file, read lines, and begin parsing to replace all incomplete img src URLs
        print(f"[+] Proceeding with updating IMG tag src attributes using: {url}")
        print("[+] The src attributes that will be modified:")
        try:
            # Find all ``<img>`` with ``src`` attribute and create a full URLs
            for img in soup.findAll("img"):
                print(f"* {img}")
                imgurl = urllib.parse.urljoin(url, img["src"])
                img["src"] = imgurl

            print("[+] IMG parsing was successful!")
        except Exception as err:
            # Exception may occur if file doesn't exist or can't be read/written to
            print(
                "[!] IMG parsing failed. Some images may not have URLs, ex: src = cid:image001.jpg@01CEAD4C.047C2E50."
            )
            print(f"L.. Details: {err}\n")

        return soup

    def fix_images_encode(self, url, soup):
        """Update the ``src`` attribute to a Base64 encoded verison of the images."""

        # Open output file, read lines, and begin parsing to replace all incomplete img src URLs
        print(f"[+] Proceeding with updating IMG tag src attributes using: {url}")
        print("[+] The src attrbitues that will be modified:")
        try:
            # Find all ``<img>`` with ``src`` attribute and create a full URLs
            for img in soup.findAll("img"):
                print(f"* {img}")
                imgurl = urllib.parse.urljoin(url, img["src"])
                image = urllib.request.urlopen(imgurl)
                # Encode in Base64 and embed
                img_64 = base64.b64encode(image.read())
                img["src"] = f"data:image/png;base64,{img_64.decode('ascii')}"

            print("[+] IMG parsing was successful!")
        except Exception as err:
            # Exception may occur if file doesn't exist or can't be read/written to
            print(
                "[!] IMG parsing failed. Some images may not have URLs, ex: src = cid:image001.jpg@01CEAD4C.047C2E50."
            )
            print(f"L.. Details: {err}\n")

        return soup

    def start_http_server(self, port):
        """Start a simple HTTP server for serving the cloned webpages."""

        handler = http.server.SimpleHTTPRequestHandler
        # Check to see if the provided port is valid
        try:
            port = int(port)
        except Exception as err:
            print("[!] Make sure the provided port, {port}, is a valid port number.")
            sys.exit()
        # Try to start the web server on the localhost using the provided port
        try:
            httpd = socketserver.TCPServer(("", port), handler)
            print(f"[+] Server started. Browse to 127.0.0.1:{port}")
            print("[!] Use CTRL+C to kill the web server.")
            # Serve until it is killed
            httpd.serve_forever()
        except Exception as err:
            print(
                "[-] Server stopped or could not be started. Please try a different port."
            )
            print(f"L.. Details: {err}")

    def encode_image(self, image):
        """
        Take an image file, encode it in Base64, and print encoded output for
        embedding in a template.
        """

        # Encode in Base64 and print encoded string for copying
        with open(image, "rb") as image:
            print("[+] Image has been encoded. Copy this string:\n")
            img_64 = '<img src="data:image/png;base64,{}">'.format(
                base64.b64encode(image.read()).decode("ascii")
            )
            print(f"{img_64}\n")
            print("[+] End of encoded string.")

    def decode_image(self, encoded_string, filename):
        """Take a Base64-encoded attachment, decode it, and save contents to a file."""

        with open(filename, "wb") as f:
            print(f"[+] Decoded attachment to {filename}")
            f.write(base64.b64decode(encoded_string))

    def parse_email(self, email_file, file_descriptor):
        """
        Takes a txt or html file with raw email source, ingests contents, and
        modifies it for phishing.
        """
        inline_images = {}

        # Open the email file and parse its contents
        print(f"[+] Opening source email file: {email_file}")
        with open(email_file, "r") as input_file:
            # Read-in the raw email content
            try:
                e = email.message_from_string(input_file.read())
            except Exception as err:
                print("[!] Failed to open the email file!")
                print(f"L.. Details: {err}")

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
                            if content_disposition == "inline":
                                print(f"[+] Attempting to save detected inline image: {attachment}")
                                cid = payload.get("Content-ID")
                                cid = cid.strip("<").strip(">")
                                content_type = payload.get_content_type()
                                ext = guess_extension(content_type)
                                filename = f"{cid}{ext}"
                                encoded_image = payload.get_payload(decode=False)
                                if cid:
                                    inline_images[cid] = filename
                                    self.decode_image(encoded_image, filename)
                                else:
                                    print(f"[+] Detected inline image did not have a `cid`, so skipped {attachment}")
                            else:
                                print(f"[+] Attachment detected and discarded: {content_disposition}, {attachment}")
                        # Find the plaintext and HTML parts
                        elif payload.get_content_type() == "text/html":
                            source += payload.get_payload(decode=True).decode(
                                payload.get_content_charset()
                            )
                        elif payload.get_content_type() == "plain/text":
                            source += payload.get_payload(decode=True).decode(
                                payload.get_content_charset()
                            )

                    # Replace the URLs
                    soup = BeautifulSoup(source, "html.parser")
                    if self.email_replacement_url != "":
                        print(f"[+] Replacing any URLs in the email content: {self.email_replacement_url}")
                        for link in soup.findAll("a", href=True):
                            link["href"] = self.email_replacement_url
                    else:
                        print(
                            "[-] Warning: No URL provided for `email_replacement_url` in config file, so the email's links will be preserved."
                        )

                    # Replace inline images with new filenames
                    for img in soup.findAll("img", src=True):
                        src = img["src"].replace("cid:", "")
                        if src in inline_images.keys():
                            img["src"] = inline_images[src]

                    try:
                        # Prettify update source from a blob of HTML to human readable source
                        source = soup.prettify()

                        # Fix/unescape characters translated to ;lt ;gt ;amp
                        source = xml.sax.saxutils.unescape(source)

                        # Add tracker URL
                        source = self.add_tracker_to_email(source)

                        # Write the updated source while removing the added [' and ']
                        file_descriptor.write(source.replace("[", "").replace("]", ""))
                    except Exception as err:
                        print("[!] Could not write to the output file!")
                        print(f"L.. Details: {err}")
                else:
                    # We have a non-multipart message, so write out what we have
                    print("[+] Processing non-multipart email message...")
                    for payload in e.walk():
                        source += payload.get_payload(decode=True).decode(
                            payload.get_content_charset()
                        )

                    # Replace the URLs
                    soup = BeautifulSoup(source, "html.parser")
                    if self.email_replacement_url != "":
                        print(f"[+] Replacing any URLs in the email content: {self.email_replacement_url}")
                        for link in soup.findAll("a", href=True):
                            link["href"] = self.email_replacement_url
                    else:
                        print(
                            "[-] Warning: No URL provided for email_replacement_url in config file, so the email's links will be preserved."
                        )

                    try:
                        # Prettify update source from a blob of HTML to human readable source
                        # This also makes it a string we can use for this next part
                        source = soup.prettify()
                        source = self.add_tracker_to_email(source)
                        # Fix/unescape characters translated to ;lt ;gt ;amp
                        source = xml.sax.saxutils.unescape(source)
                        # Write the updated source while removing the added [' and ']
                        file_descriptor.write(source.replace("[", "").replace("]", ""))
                    except Exception as err:
                        print("[!] Could not write to the output file!")
                        print(f"L.. Details: {err}")

                print(f"[+] All processes are complete! Check your output file: {self.output_file_name}")
            except Exception as err:
                print("[!] Failed to write out the email contents!")
                print(f"L.. Details: {err}")

    def add_tracker_to_email(self, source):
        """Insert a tracking image and write everything to the index file."""

        # Define the tracking image that will be inserted
        tracking_string = f'<img src="{self.email_tracker_url}" style="width:1px; height:1px;"/>'
        print("[+] Attempting to insert the tracking image.")
        try:
            # Find the closing body tag in the email
            index = source.find(r"</body")
            if index == -1:
                print(
                    "[!] Cooper could not find a closing body tag. A tracking image has not been inserted."
                )
                print(f'L.. If desired, manually add: <img src="{self.email_tracker_url}" style="width:1px; height:1px;"/>')

                return source
            else:
                print(f"[+] Closing body tag found at index {index}.")
                tracked_source = source[:index] + tracking_string + source[index:]
                print("[+] Tracking has been inserted.")

                return tracked_source
        except:
            # Exception may occur if file doesn't exist or can't be read/written to
            print(
                "[!] Cooper could not find a closing body tag. A tracking image has not been inserted."
            )
            print(f'L.. If desired, manually add: <img src="{self.email_tracker_url}" style="width:1px; height:1px;"/>')
