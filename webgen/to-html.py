#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

"""\
Create full HTML pages from template files.

Usage:  to-html.py [-C] [SOURCE]...

  -C HTMLDIR  create the files within HTMLDIR instead of on stdout

Each SOURCE is processed specially according to the name or extension.
When a directory, find and process the "interesting" files it contains.
"""

import getopt, re, sys, os

sys.path.insert(0, sys.path[0]+'/../lib')
import htmlpage

os.umask(002)

def main(*arguments):
    if not arguments:
        sys.stdout.write(__doc__)
        sys.exit(0)
    htmldir = None
    options, arguments = getopt.getopt(arguments, 'C:')
    for option, value in options:
        if option == '-C':
            htmldir = value
    for argument in arguments:
        htmlpage.transform_generic(argument, htmldir)

if __name__ == '__main__':
    apply(main, tuple(sys.argv[1:]))
