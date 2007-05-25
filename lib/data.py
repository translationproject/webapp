# Data base handling for the Translation Project.
# -*- coding: iso-8859-1 -*-
# Copyright � 2001, 2002, 2003 Translation Project.
# Copyright � 2000 Progiciels Bourbeau-Pinard inc.
# Fran�ois Pinard <pinard@iro.umontreal.ca>, 2000.

import cPickle
pickle = cPickle
del cPickle

import UserDict, types, os
import config

def load_postats():
    f = open('%s/cache/postats' % config.site_path)
    try:
        res = pickle.load(f)
    except:
        # data corrupted, try to load backup
        f.close()
        f = open('%s/cache/postats.bak' % config.site_path)
        res = pickle.load(f)
    f.close()
    if type(res) == types.DictType:
        res = UserDict.UserDict(res)
    return res

def save_postats(postats):
    name = '%s/cache/postats' % config.site_path
    suffix = "."+str(os.getpid())
    pickle.dump(postats, open(name+suffix , 'w'))
    try:
        os.unlink(name+".bak")
    except OSError:
        pass
    try:
        os.rename(name, name+".bak")
    except OSError:
        pass
    os.rename(name+suffix,name)
    
def load_registry():
    return pickle.load(open('%s/cache/registry' % config.site_path))

def save_registry(registry):
    pickle.dump(registry, open('%s/cache/registry' % config.site_path, 'w'))

def load_extstats():
    try:
        res = pickle.load(open('%s/cache/extstats' % config.site_path))
    except IOError:
        return UserDict.UserDict()
    return res

def save_extstats(postats):
    pickle.dump(postats, open('%s/cache/extstats' % config.site_path, 'w'))
