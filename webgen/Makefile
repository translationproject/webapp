# Generating the documenting web pages for the Translation Project.
# Copyright © 2007 Translation Project.
# Copyright © 1999, 2000 Progiciels Bourbeau-Pinard inc.
# François Pinard <pinard@iro.umontreal.ca>, 1999.

ALLOUT_FILES = maintainers.all leaders.all translators.all \
               changes.all files.all robot.all software.all
HTMA_FILES = $(ALLOUT_FILES:.all=.html)
HTMH_FILES = welcome.html thanks.html whydisclaim.html
CSS_FILES  = css/style.less css/desc.gif css/asc.gif css/bg.gif css/bootstrap.less $(wildcard css/bootstrap/*.less)
JS_FILES   = js/jquery-min.js js/jquery.tablesorter.min.js js/less.min.js js/layout.js

LAYOUT_DEPS = ../lib/config.py ../lib/htmlpage.py layout.html.in to-html.py


all: alloutfiles htmlfiles css js\
     $(sitedir)/disclaim.txt $(htmldir) $(htmldir)/authors.html $(extradir) $(extradir)/sendpo.sh

$(sitedir):
	mkdir -p $@
$(htmldir):
	mkdir -p $@
$(extradir):
	mkdir -p $@

alloutfiles: $(htmldir) $(addprefix $(htmldir)/,$(HTMA_FILES))

htmlfiles: $(htmldir) $(addprefix $(htmldir)/,$(HTMH_FILES))

css: $(sitedir) $(addprefix $(sitedir)/,$(CSS_FILES))

js: $(sitedir) $(addprefix $(sitedir)/,$(JS_FILES))

$(sitedir)/css/%.css: css/%.css
	cp $< $@
$(sitedir)/css/%.less: css/%.less
	cp $< $@
$(sitedir)/css/bootstrap/%.less: css/bootstrap/%.less
	@mkdir -p $(sitedir)/css/bootstrap/
	cp $< $@
$(sitedir)/css/%.gif: css/%.gif
	cp $< $@
$(sitedir)/js/%.js: js/%.js
	cp $< $@

$(htmldir)/%.html: %.all $(LAYOUT_DEPS)
	./to-html.py -C $(htmldir) $<

$(htmldir)/%.html: %.html $(LAYOUT_DEPS)
	./to-html.py -C $(htmldir) $<

disclaimer $(sitedir)/disclaim.txt: disclaim.txt
	cp disclaim.txt $(sitedir)/disclaim.txt

authors $(htmldir)/authors.html: ../registry/AUTHORS
	./to-html.py -C $(htmldir) ../registry/AUTHORS

script $(extradir)/sendpo.sh: ../tools/sendpo.sh
	cp ../tools/sendpo.sh $(extradir)/sendpo.sh

domains:
	../bin/generate-static-pages -d

teams:
	../bin/generate-static-pages -t


lint: all
	find $(htmldir) -name '*.html' | while read file; do \
	  case $$file in \
	    *po*) nsgmls -s $$file 2>&1 | egrep -v '"P"|"SMALL"' ;; \
	    *gettext*) nsgmls -s $$file 2>&1 | egrep -v '"P"|"SMALL"' ;; \
	    *) nsgmls -s $$file ;; \
	  esac; \
	done
	-weblint -x Netscape $(htmldir) \
	| egrep -v 'cyan|empty container element <P>|'
