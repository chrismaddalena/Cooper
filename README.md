##Cooper [koo-per, koo p-er] - noun - a person who makes or repairs casks, barrels, etc.

>A Python tool for ingesting HTML and producing HTML source suitable for phishing campaigns.

Note: Cooper was designed to accomodate some specific, even unusual, needs. However, it should be easy to modify Cooper for other phishing tools and projects.

###cooper.py:
The main script. It may eventually offer a menu with more verbose information, so as to work better as a standalone tool. For now, Cooper has several options for specifying what you need it to do.

**Use just one...**
* -e for Email - Use Cooper's phishemail.py module. Specify a FILE.
* -p for Phishgate - Use Cooper's phishgate.py module. Specify a URL.
* -x for eXit - Use Cooper's phishexit.py module. Specify a URL.
* -n for eNcode - Use Cooper to encode an image file as a Base64 string. Useful for embedding different images into a template or customizing a cloned email/website.

**You can also use...**
* -d for Decode - Indicate an email needs to be deocded and specify the encoding (base64 or quoted-printable).
* -u for URL - Specify a URL you want Cooper to use when you need it to fix image links.
* -s for Server - Add this when you want Cooper to start the HTTP server. Specify a PORT #.
* -h - View this help information.

###Modules:
* toolbox.py - The toolbox handles the common tasks, such as retrieving HTML source from files and webpages and starting the HTTP server.

* phishemail.py - This module handles generating phishing emails. Use -e and feed it a file. Use -d to indicate if decoding is necessary. Use -u to provide a URL for img tags.

* phishgate.py - This module creates an index.html file suitable as a phishgate (a landing page for the phishing emails). Use -p and feed Cooper a URL or file (coming soon) to have Cooper output an index.html file so the webpage can be easily viewed in your browser via the HTTP server (if you start it).

* phishexit.py - This module creates an exit page for your phishing campaign. This might be a cloned copy of the phishgate website's 404 page. Use -x and feed it a URL or file (coming soon).

###Usage examples:
####Creating an email:
* Get the source of an email to clone and save it to a file.
* Remove the additional text (e.g. delivery info, etc.)
* To process an email encoded in base64 with images hosted on www.foo.bar: cooper.py -e email.html -d base64 -u http://www.foo.bar

####Creating a phishgate:
* Find a webpage to clone.
* To clone a webpage and view it in your browser: cooper.py -p http://www.foo.bar -s 8888

####Creating an exit page:
* Find a URL that pulls up the 404 page of your cloned website.
* To clone the 404 page: cooper.py -x http://www.foo.bar/garbage.php -u http://www.foo.bar

###Misc Info:
* URLs are replaced with text that will do **nothing** for you. This is text that was needed for the particular phishing tool Cooper was created to work with. Modify the replaceURL() functions as needed.

* Images are scraped and then encoded in Base64 before being embedded in the template. This is to make it so the templates are not reliant on the website being available/keeping the images where they are. If you do not want this, then remove the encoding lines from the fixImageURL() functions.

* The HTTP server option is there to enable you to easily review Cooper's output by hitting 127.0.0.1:PORT. You could just open the index.html, but why would that be cooler than this?

###Setup:
**Find the setup files inside the setup directory.**
Cooper requires several libs for scraping websites and parsing the HTML. Use pip and the requirements.txt to install dependencies.
>pip install -r requirements.txt

Then you can check the dependencies by running setup_check.py.

Special thanks to Ninjasl0th for his help with this project!
