#!/usr/bin/env python

import sys, os, urllib, gzip, stat, errno, string, getopt, re

urlprefix = "http://www.translationproject.org/nothingyet/"

def mkdir(p):
    try:
        os.mkdir(p)
    except OSError, e:
        if e.errno == errno.EEXIST:
            return
        if e.errno == errno.ENOENT:
            d, f = os.path.split(p)
            mkdir(d)
            os.mkdir(p)
            return
        raise

def usage(n):
    print "Usage: mirror_tp.py [options] destdir"
    print ""
    print "Possible options are:"
    print " -h,--help		Show this help"
    print ""
    print " -t,--team=langcode	Only mirror data from this team"
    print " -n,--name=domain	Only mirror data from this domain"
    print ""
    print " -b,--bin		Only mirror binaries"
    print " -d,--data		Only mirror data files"
    print ""
    print "If none of t, d, b, p option is given, everything is mirrored."
    print "If one of them is given, the other ones are assumed to be off."
    print "It is possible to use several of these options at the same time."
    sys.exit(n)

def retrieve(name):
    print "retrieving %s" % (name)
    urllib.urlretrieve(urlprefix+name, name)
    os.utime(name, (time,time))
    
partial=0
teams = []
domains = []
what = {"data": 0, "bin": 0, "doc": 1}
    
try:
    opts, args = getopt.getopt(sys.argv[1:], "ht:n:bp", ["help", "team=", "name=", "bin", "pot"])
except getopt.GetoptError:
    # print help information and exit:
    usage(2)

for o, a in opts:
    if o in ("-h", "--help"):
	usage(0)
    if o in ("-t", "--team"):
	partial=1
	teams.append(a)
    if o in ("-n", "--name"):
	partial=1
	domains.append(a)
    if o in ("-b", "--bin"):
	partial=1
	what["bin"]=1
    if o in ("-d", "--data"):
	partial=1
	what["data"]=1
	

if False:
    print "Partial=%s" % (partial)
    print "Teams="
    print teams
    print "Domains="
    print domains
    print "What="
    print what

if len(args) != 1:
    usage(2)

prefix = args[0]
if not os.path.exists(prefix):
    os.mkdir(prefix)
os.chdir(prefix)
try:
    os.link("domains/POT", "pot")
except OSError:
    pass
try:
    os.link("teams/PO", "trans")
except OSError:
    pass

print "Retrieving the index"
mkdir("mirror")
for i in range(5):
    sock = urllib.urlretrieve(urlprefix + "mirror/INDEX.gz","mirror/INDEX.gz")
    data = string.split(gzip.GzipFile("mirror/INDEX.gz").read(), '\n')
    if data[-1]=="END":
        del data[-1]
        break
else:
    # it is an incomplete file
    raise SystemExit

for line in data:
    time, name = string.split(line, ' ', 1)
    type = 'file'
    time = string.atoi(time, 16)
    if name[:5] == 'link ':
        try:
            type, name, dest = string.split(name, ' ')
#	    print "link %s to %s " % (name,dest)
        except ValueError:
            # file name with spaces, ignore
            print 'Splitting',name,'failed'
            continue
    try:
        st = os.lstat(name)
    except OSError:
        pass
    else:
        if st[stat.ST_MTIME] == time:
            continue
    dir, file = os.path.split(name)
    if dir:
        mkdir(dir)
    if type == 'link':
        try:
            os.remove(name)
        except OSError:
            os.symlink(dest, name)
        continue
    
    team=None
    domain=None
    kind=None
    if name[:9] == 'teams/PO/':
	team = re.match("^([^/]+)/",name[9:]).group(1)
	domain = re.match("^([^/])+/([^-]*)-",name[9:]).group(2)
	kind="data"
    if name[:12] == 'domains/POT/':
	domain = re.match("^([^-]*)-",name[12:]).group(1)
	kind="data"
    if name[:5] == 'data/':
	kind="bin" # because those data are used only in bin
    if name[:4] == 'web/':
	kind="bin"
    if name[:9] == 'registry/':
	kind="bin"
    if name[:4] == 'bin/':
	kind="bin"
    if name[:4] == 'doc/':
	kind="doc"

    if kind == None:
	print "Parse error on line %s" % name

    if partial:
	if team in teams or domain in domains or what[kind]:
	    retrieve(name)
    else:
	retrieve(name)
	    


# XXX: unlink files that are gone remotely.
