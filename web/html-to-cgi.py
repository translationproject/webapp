#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

"""\
Create redirection pages which launch the CGI script that produces the
page for the requested index, domain, or team.

Usage:  html-to-cgi.py [-CDT]

  -C HTMLDIR  store produced files within this directory (mandatory option)
  -D          process all registered domains
  -T          process all regsitered teams
"""

import getopt, re, sys, os

sys.path.insert(0, sys.path[0]+'/../lib')
import config, registry

os.umask(002)

def main(*arguments):
    if not arguments:
        sys.stdout.write(__doc__)
        sys.exit(0)
    # Decode options.
    htmldir = None
    domain_option = team_option = 0
    options, arguments = getopt.getopt(arguments, 'C:DT')
    for option, value in options:
        if option == '-C':
            htmldir = value
        elif option == '-D':
            domain_option = 1
        elif option == '-T':
            team_option = 1
    assert htmldir, "`-C HTMLDIR' is mandatory"
    if domain_option:
        relocate(htmldir and '%s/domains.html' % htmldir,
                 'domain index page', 'domain=index')
        for domain in registry.domain_list():
            relocate(htmldir and '%s/domain-%s.html' % (htmldir, domain.name),
                     'page for domain <code>%s</code>' % domain.name,
                     'domain=%s' % domain.name)
    if team_option:
        relocate(htmldir and '%s/teams.html' % htmldir,
                 'team index page', 'team=index')
        for team in registry.team_list():
            relocate(htmldir and '%s/team-%s.html' % (htmldir, team.name),
                     'page for the %s team' % team.language,
                     'team=%s' % team.name)

def relocate(name, description, params):
    if name:
        write = open(name, 'w').write
    else:
        write = sys.stdout.write
    write("""
<html>
 <head>
  <meta http-equiv=refresh content='0; url=%s/registry.cgi?%s'>
  <title>Redirection page</title>
 </head>
 <body>
  <h1>Computing %s...</h1>
  <p>If your browser supports page redirection,</p>
  <p>this page will get replaced within a few seconds.</p>
  <p></p>
  <p>If not, you may <a href='%s/registry.cgi?%s'>click here</a>
   to launch the page generation manually.</p>
 </body>
</html>
"""
          % (config.cgi_path, params, description, config.cgi_path, params))

if __name__ == '__main__':
    apply(main, tuple(sys.argv[1:]))