# Generating the documenting web pages for the Translation Project.
# Copyright © 2007 Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

homedir = /home/tp
sitedir = $(homedir)/site

cgidir = $(sitedir)/cgi
htmldir = $(sitedir)/html
cachedir= $(homedir)/cache
progsdir = $(homedir)/progs

CGI_FILES = registry.cgi domains.html teams.html
ALL_FILES = maintainers.all leaders.all translators.all \
            files.all robot.all software.all
HTMA_FILES = $(ALL_FILES:.all=.html)
HTMH_FILES = welcome.html thanks.html whydisclaim.html

LAYOUT_DEPS = ../lib/config.py layout.html.in html-to-cgi.py to-html.py


all: cgi allfiles htmlfiles \
     $(sitedir)/index.html $(sitedir)/disclaim.txt

$(htmldir) $(cgidir):
	mkdir -p $@


cgi: $(cgidir) $(addprefix $(cgidir)/,$(CGI_FILES))

$(cgidir)/%.cgi: %.cgi.in
	sed 's,@progsdir@,$(progsdir),g' $< > $@-tmp
	chmod a+rx $@-tmp
	mv -f $@-tmp $@

domains $(cgidir)/domains.html: $(LAYOUT_DEPS)
	./html-to-cgi.py -C $(cgidir) -D

teams $(cgidir)/teams.html: $(LAYOUT_DEPS)
	./html-to-cgi.py -C $(cgidir) -T


allfiles: $(htmldir) $(addprefix $(htmldir)/,$(HTMA_FILES))

htmlfiles: $(htmldir) $(addprefix $(htmldir)/,$(HTMH_FILES)) 

$(htmldir)/%.html: %.all $(LAYOUT_DEPS)
	./to-html.py -C $(htmldir) $<

$(htmldir)/%.html: %.html $(LAYOUT_DEPS)
	./to-html.py -C $(htmldir) $<

$(sitedir)/index.html: stepinto.html.in
	cp stepinto.html.in $(sitedir)/index.html

$(sitedir)/disclaim.txt: disclaim.txt
	cp disclaim.txt $(sitedir)/disclaim.txt


lint: all
	find $(htmldir) $(cgidir) -name '*.html' | while read file; do \
	  case $$file in \
	    *po*) nsgmls -s $$file 2>&1 | egrep -v '"P"|"SMALL"' ;; \
	    *gettext*) nsgmls -s $$file 2>&1 | egrep -v '"P"|"SMALL"' ;; \
	    *) nsgmls -s $$file ;; \
	  esac; \
	done
	-weblint -x Netscape $(htmldir) \
	| egrep -v 'cyan|empty container element <P>|'