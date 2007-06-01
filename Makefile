# Conveniently process the PO directory hierarchy.
# Copyright (C) 2004, 2007 Translation Project.
# Copyright (C) 1996, 1997, 1998, 1999, 2000, 2001 Free Software Foundation, Inc.
# Fran�ois Pinard <pinard@iro.umontreal.ca>, 1996.

VERSION=1.2


all: registry matrix

check: all
	@find latest-POs -type l | while read file; do \
	  echo; \
	  echo "Verifying \``ls -l $$file | sed 's,.*-> ../../,,'`'"; \
	  msgfmt --statistics -c -v -o /dev/null $$file; \
	done

expire:
	bin/po-expire

tags: tags-recursive
	etags -i bin/TAGS -i lib/TAGS

tags-recursive:
	$(MAKE) -C bin tags
	$(MAKE) -C lib tags

registry: ../cache/registry
../cache/registry: registry/registry.sgml
	$(MAKE) -C registry registry

mailrc: $(HOME)/.mailrc-tp
$(HOME)/.mailrc-tp: ../cache/registry 
	$(MAKE) -C registry mailrc 

.PRECIOUS: postats
postats: ../cache/postats
../cache/postats: FORCE
	VERSION_CONTROL=numbered cp -fb ../cache/postats ../cache/postats
	bin/postats-data -v -i -u
FORCE:

matrix: doc/matrix.texi
ifeq ($(SITE), iro.umontreal.ca)
doc/matrix.texi: PO-files/*
	bin/po-matrix
	mv tmp-matrix.html doc/matrix.html
	@if cmp -s tmp-matrix.texi doc/matrix.texi; then \
	  rm tmp-matrix.texi; \
	else \
	  mv tmp-matrix.texi doc/matrix.texi; \
	  mail -s "New PO file matrix" sv@li.org <doc/matrix.texi; \
	fi
	@if cmp -s tmp-matrix.xml doc/matrix.xml; then \
	  rm tmp-matrix.xml; \
	else \
	  mv tmp-matrix.xml doc/matrix.xml; \
	  mail -s "New PO file matrix" haible@ilog.fr <doc/matrix.xml; \
	fi
else
doc/matrix.texi:
	:
endif

.PHONY:	pot
pot:
	xgettext -o translationproject.pot -kt_ -L Python bin/[a-z]* lib/*.py
	# Add the list of language teams:
	python lib/registry.py >>translationproject.pot

dist:
	tar -czv -f $(HOME)/translationproject-${VERSION}.tgz \
	    --exclude=.svn  ../$(pwd)
