#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from time import sleep

print "\nCooper requires various lib/modules to properly work."
print "This script serves to check if you have those libs."

sleep(2)

try:
    import BeautifulSoup
    print '[+]FOUND: BeautifulSoup'
except:
    print '[+]MISSING: BeautifulSoup'

try:
    import requests
    print '[+]FOUND: requests'
except:
    print '[+]MISSING: requests'
