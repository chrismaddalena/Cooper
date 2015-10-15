##Cooper [koo-per, koo p-er] - noun - a person who makes or repairs casks, barrels, etc.

>A Python tool for ingesting HTML and producing HTML source suitable for phishing campaigns.

Note: Cooper was designed to accommodate some specific, even unusual, needs. However, it should be easy to modify Cooper for other phishing tools and projects.

###cooper.py:
The main script. It may eventually offer a menu with more verbose information, so as to work better as a standalone tool. For now, Cooper has several options for specifying what you need it to do.

**Use just one...**
* -e for Email - Use Cooper's phishemail.py module. Specify a FILE.
* -p for Phishgate - Use Cooper's phishgate.py module. Specify a URL.
* -x for eXit - Use Cooper's phishexit.py module. Specify a URL.
* -n for eNcode - Use Cooper to encode an image file as a Base64 string. Useful for embedding different images into a template or customizing a cloned email/website.
* -c for Collect - Use Cooper to collect the source of a webpage. Useful if you just want to quickly grab the source and have Cooper fix the images.

**You can also use...**
* -o for Output - Specify a filename for the output HTML file. If a name is not provided with -o, Cooper will use output.html.
* -d for Decode - Indicate an email needs to be decoded and specify the encoding (base64 or quoted-printable).
* -u for URL - Specify a URL you want Cooper to use when you need it to fix links for images, CSS, and/or scripts.
* -m for eMbed - Set embedding to True. Images will be Base64 encoded and embedded into the template when this flag is used.
* -s for Server - Add this when you want Cooper to start the HTTP server. Specify a PORT #.
* -h for Help - View this help information.

###Modules:
* toolbox.py - The toolbox handles the common tasks, such as retrieving HTML source from files and webpages and starting the HTTP server.

* phishemail.py - This module handles generating phishing emails. Use -e and feed it a file. Use -d to indicate if decoding is necessary. Use -u to provide a URL for img tags, scripts, and CSS.

* phishgate.py - This module creates an HTML file suitable as a phishgate (a landing page for the phishing emails). Use -p and feed Cooper a URL for a webpage you want to use for phishing (probably some sort of form). Use -x to feed Cooper an exit page for your campaign (like a 404 page).

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

* Images can be encoded in Base64 before being embedded in a template. This is to make it so the templates are not reliant on the website being available/keeping the images where they are. The added size for a website is (most likely) negligible, but using this option for an email could be a problem. Some email clients do not support Base64 images, like Outlook (!). Keep the target's email client in mind.

* The HTTP server option is there to enable you to easily review Cooper's output by hitting 127.0.0.1:PORT. You could just open the HTML file, but that's not as neat.

###Known issues
* If the website is hosted on a service like SquareSpace, Cooper will be unable to repair the images. The img tags look like "<img src="//static1.squarespace.com/static/52ebedcae4b0ad4aad060b4a/t/533b687ae4b01d79d0ae12a3/1437187699809/?format=1500w">.

###Setup:
**Find the setup files inside the setup directory.**
Cooper requires several libs for scraping websites and parsing the HTML. Use pip and the requirements.txt to install dependencies.
>pip install -r requirements.txt

Then you can check the dependencies by running setup_check.py.

Special thanks to Ninjasl0th for his help with this project!
