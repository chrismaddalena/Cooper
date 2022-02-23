# Cooper, noun, a maker or repairer of casks and barrels

(It's a "fish in a barrel" joke. I enjoy puns!)

>A Python tool for ingesting HTML and producing HTML source suitable for phishing campaigns.

Cooper simplifies the process of cloning a target website or email for use in a phishing campaign. Just find a URL or download the raw contents of an email you want to use and feed it to Cooper. Cooper will clone the content and then automatically prepare it for use in your campaign. Scripts, images, and CSS can be modified to use direct links instead of relative links, links are changed to point to your phishing server, and forms are updated to send data to you -- all in a matter of seconds. Cooper is cross-platform and should work with macOS, Linux, and Windows.

No more manually editing links and forms after using `wget` to fetch a site. You can focus on the detail work.

### Basic Usage

Cooper offers several modules with different purposes:

* page - What will certainly be the most used module. This is used for cloning a target webpage. The output is an HTML file and a screenshot of the original webpage for checking the results.
* email - Like page, but it takes a file containing your raw email content. Just open the email in your email client, use your client's "view original" option, and save the contents. The output is an HTML file.
* encode - A handy tool that automates Base64 encoding for any images you want to manually embed into a landing page. Give it an image file and it will output the full text needed for setting the src attribute. The output is a (probably huge) blob of text like `<img src="data:image/png;base64,QUFBQUFBQUFBCg==">`. This is why piping the output into a file is often a good idea for easier copy/pasting.

#### Using page

Page is Cooper's primary module. The only argument required is `-t` to specify a target URL. You can then add `--selenium` to optionally use *Selenium* instead of *Requests*. Basically, if the output looks wrong or is incomplete (maybe just a background and some styling, for example) try using `--selenium`.

Some websites require JavaScript to generate the HTML content. If the output looks wrong or is incomplete, try using `--selenium`.

Additionally, you might add `-u` with a URL to be used as the base URL for images, scripts, and style sheets. Cooper will replace relative links (e.g. */wp-content/images/foo.bar*) with the full URL for you.

Always provide valid URLs with the correct protocol for `-t` and `-u` (i.e. *http://www.example.com*).

A full list of settings is below:

* -t, --target TEXT
  * [REQUIRED] The target webpage's URL.
* -o, --output TEXT
  * [Optional] Specifies the filename for the output HTML file. Default is index.html. Including the .html extension is recommended.
* -u, --url TEXT
  * [Optional] Specifies the root URL for images in the target email or webpage.
* -m, --embed
  * [Optional] Base64 encode images and embed them into the output.
* --selenium
  * [Optional] Use Selenium to fetch the webpage's HTML source.
* -s, --serverport TEXT
  * [Optional] Provide a port to use for an HTTP server to serve up output files.
* -c, --config FILE
  * [Optional] Provide an alternate config file for Cooper to use. This is helpful if you use different phishing platforms/servers.

#### Using email

The email module is handy when you want to use an email you have as the foundation for a new phish. Handling encoding and multi-part MIME messages can be a pain when done by hand, so let Cooper do it for you. This module will parse the message contents, throw away unneeded parts, like attachments, and get you a fully decoded version of the main email body, the plain/text or text/html parts you care about.

A full list of settings is below:

* -f, --file PATH
  * [REQUIRED] The file containing the raw email contents file to parse.
* -o, --output TEXT
  * [Optional] Specifies the filename for the output HTML file. Default is index.html. Including the .html extension is recommended.
* -s, --serverport TEXT
  * [Optional] Provide a port to use for an HTTP server to serve up output files.
  * -c, --config FILE
    * [Optional] Provide an alternate config file for Cooper to use. This is helpful if you use different phishing platforms/servers.

#### Using encode

As mentioned above, this module is a one-off. The required, and only, argument is `-i` for providing the image file to encode. It's handy if you're building your own landing page or editing a page and need to add an image. If you decide to embed it, give this module a shot. It will Base64 encode the provided file and produce the text necessary for embedding the image.

* -i, --image TEXT
  * [REQUIRED] The target file to Base64 encode.

### Setup

#### Python Requirements

Cooper requires several libs for scraping websites and parsing the HTML. Use `pip` or `pipenv` to install everything. There is a *requirements.txt* for `pip` and a *Pipfile* for `pipenv` virtual environments. If you use `pip`, be sure to use the proper one on your system for Python 3.9 (e.g., `pip3` or `pip3.9`)

You can be sure the proper version is used by calling `pip` with your Python version:

`python3 -m pip install -r requirements.txt`

A virtual environment is even easier to use:

1. Run this command: `pipenv install`
2. Enter the environment with: `pipenv shell`

#### Selenium Requirements

Using *Selenium* for a headless browser requires Google Chrome be installed and downloading a matching Chromewebdriver file from: https://chromedriver.chromium.org/downloads

Download and extract the webdriver to the root of this project. You can place it elsewhere, but make sure you update the config (see next section).

#### Set the Config

Then you need to setup your config file. The *cooper.config* file provided with this repo comes pre-setup for use with GoPhish (URLs are set to be changed to *{{.URL}}*). The default config also assumes you will place a Chrome webdriver in the root of the directory.

The config file looks like this:


```
[Replacement URLs]
landing_page_url_replacement: {{.URL}}
landing_page_form_action: {{.URL}}
email_replacement_url: {{.URL}}

[Browser]
driver_path: ./chromedriver
user_agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36
```

Make changes as necessary. You can create multiple config files for different phishing platforms you use, additional attack servers, or alternate user-agents. Different config files can be used by including the `-c` or `--config` arguments along with your alternate file. Otherwise, the *cooper.config* file will be used by default.

The `[Replacement URLs]` section contains all of the URLs that Cooper will use when replacing links and form actions.

The `landing_page_url_replacement` is the URL used for the landing page. You might want this set to the phishing server's IP so visitors are redirected back to the landing page or have them sent elsewhere.

The `landing_page_form_action` is the URL you want the form data sent to when a form is submitted.

The `email_replacement_url` is the URL used for emails and should be set to your phishing server's domain or IP address.

If any of these URLs are set to nothing, Cooper will not replace those URLs. This is most practical for `landing_page_url_replacement` where you may wish to have the landing page continue to point to real links. However, be warned, the target webpage may use relative links like */home.php* instead of direct links, which would mean your landing page will be full of broken links.

The `[Browser]` section is just for settings related to web browsing. Use this section to point *Selenium* and Cooper to your browser webdriver if you choose to use a different driver file or location. The user-agent used for web browsing is also defined here. Cooper has a default user-agent that you can override with the config file.

### Misc Info

* Images can be encoded in Base64 before being embedded in a template. This is to make it so the templates are not reliant on the website being available/keeping the images where they are. The added size for a website is (most likely) negligible, but using this option for an email could be a problem. Some email clients do not support Base64 images, like Outlook(!). Keep the target's email client in mind.

* The HTTP server option is there to enable you to easily review Cooper's output by hitting *127.0.0.1:PORT*. You could just open the HTML file, but that's not as neat.

### Known Issues
* If the website is hosted on a service like SquareSpace, Cooper will be unable to repair the images. The `img` tags look like: `<img src="//static1.squarespace.com/static/52ebedcae4b0ad4aad060b4a/t/533b687ae4b01d79d0ae12a3/1437187699809/?format=1500w"\>`

### Final Words

Special thanks to Ninjasl0th and Hagbard for his help with this project!
