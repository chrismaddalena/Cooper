#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  CCC
 C
 C    ooo ooo ppp  eee rrr
 C    o o o o p  p e e r
  CCC ooo ooo ppp  ee  r
	          p
	          p

Developer: Christopher Maddalena

Cooper simplifies the process of cloning a target website or email for use in a
phishing campaign. Just find a URL or download the raw contents of an email you
want to use and feed it to Cooper. Cooper will clone the content and then
automatically prepare it for use in your campaign. Scripts, images, and CSS can
be modified to use direct links instead of relative links, links are changed to
point to your phishing server, and forms are updated to send data to you -- all
in a matter of seconds. Cooper is cross-platform and should work with MacOS,
Linux, and Windows.
"""

# Standard Libraries
import os  # Used primarily to identify OS and clear terminal

# 3rd Party Libraries
import click  # The awesome Command Line Interface Creation Kit
from lib import banners  # Import sweet ASCII art
from lib import toolbox  # Import the custom Toolbox class


# Setup for CLICK interface
class AliasedGroup(click.Group):
    """Allows commands to be called by their first unique character."""

    def get_command(self, ctx, cmd_name):
        """
        Allows commands to be called by thier first unique character
        :param ctx: Context information from click
        :param cmd_name: Calling command name
        :return:
        """
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail("Too many matches: %s" % ", ".join(sorted(matches)))


# Create a CLICK alias group for help text
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
def cooper():
    """
    Coopers make barrels, like cooper.py makes barrels for phish.
    Cooper.py was created by Chris Maddalena as a helpful tool compatible with
    any phishing tool. The script will clone a website and automatically process
    the html to prepare it for use in a phishing campaign.
    """
    # Everything starts here
    pass


# Create the PAGE module
@cooper.command(name="page", short_help="Used to clone a target webpage.")
@click.option("-t", "--target", help="The target webpage's URL.", required=True)
@click.option(
    "-o",
    "--output",
    help="[Optional] Specifies the filename for the output HTML file. Default is index.html. Including the *.html extension is recommended.",
)
@click.option(
    "-u",
    "--url",
    help="[Optional] Specifies the root URL for images in the target email or webpage.",
)
@click.option(
    "-m",
    "--embed",
    is_flag=True,
    help="[Optional] Base64 encode images and embed them into the output.",
)
@click.option(
    "--selenium",
    is_flag=True,
    help="[Optional] Use Selenium to fetch the webpage's HTML source.",
)
@click.option(
    "-c", "--config", help="[Optional] Provide an alternate config file for Cooper."
)
@click.option(
    "-s",
    "--serverport",
    help="[Optional] Provide a port to use for an HTTP server to serve up output files.",
)
@click.pass_context
def page(self, target, output, url, embed, selenium, serverport, config):
    """Used to clone a target webpage."""
    t = toolbox.Toolbox(config)
    t.process_webpage(target, output, url, embed, selenium)

    if serverport is not None:
        print("[+] Starting HTTP server on port", serverport)
        t.start_http_server(serverport)


# Create the EMAIL module
@cooper.command(
    name="email",
    short_help="Used to process files contianing raw email text collected from an email client.",
)
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, readable=True, resolve_path=True),
    help="The file containing the raw email contents file to parse.",
    required=True,
)
@click.option(
    "-o",
    "--output",
    help="[Optional] Specifies the filename for the output HTML file. Default is index.html. Including the *.html extension is recommended.",
)
@click.option(
    "-c", "--config", help="[Optional] Provide an alternate config file for Cooper."
)
@click.option(
    "-s",
    "--serverport",
    help="[Optional] Provide a port to use for an HTTP server to serve up output files.",
)
@click.pass_context
def email(self, file, output, serverport, config):
    """Used to process files contianing raw email text collected from an email client."""
    t = toolbox.Toolbox(config)
    t.process_email(file, output)

    if serverport is not None:
        print("[+] Starting HTTP server on port", serverport)
        t.start_http_server(serverport)


# Create the ENCODE module
@cooper.command(
    name="encode",
    short_help="Used to encode image files and get the Base64 string for embedding. Piping the output to a file is recommended.",
)
@click.option("-i", "--image", help="The target file to Base64 encode.", required=True)
@click.pass_context
def encode(self, image):
    """
    Used to encode image files and get the Base64 string for embedding.
    Piping the output to a file is recommended.
    """
    t = toolbox.Toolbox(None)
    t.encode_image(image)


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    banners.printArt()
    cooper()
