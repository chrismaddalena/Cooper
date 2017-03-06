#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from time import sleep

print("\nCooper requires a few lib/modules to properly work.")
print("This script serves to check if you have those libs.")
print("This must be run with Python 3!")

sleep(2)

try:
	from bs4 import BeautifulSoup
	print('[+] FOUND: BeautifulSoup4')
except:
	print('[!] MISSING: BeautifulSoup4')

try:
	import requests
	print('[+] FOUND: Requests')
except:
	print('[!] MISSING: Requests')

try:
	import click
	print('[+] FOUND: Click')
except:
	print('[!] MISSING: Click')
