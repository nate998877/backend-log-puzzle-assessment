#!/usr/bin/env python3
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib.request
import urllib.parse
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    puzzle_match = []
    with open(filename) as opened_file:
        for line in opened_file.readlines():
            match = re.findall("(\S*puzzle\S*.jpg)", line)
            if match:
                puzzle_match.append(match[0])
    return sorted(list(set(puzzle_match)), key=lambda x: x.rsplit("-")[-1])


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    img_paths = []
    if not os.path.exists(dest_dir):
        print(f"{dest_dir} doesn't exist! Creating directory automagically.")
        os.mkdir(dest_dir)
    os.chdir(dest_dir)

    for i, url in enumerate(img_urls):
        img_paths.append(urllib.request.urlretrieve(
            f"http://code.google.com{url}", f"img{i}.jpg")[0])

    html_text = "<html> \n <style> body {font-size: 0; }</style>"
    with open("index.html", "w+") as html:
        for f_path in img_paths:
            html_text += f"<img src={f_path}>\n"
        html_text += "</html>"
        html.write(html_text)


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
