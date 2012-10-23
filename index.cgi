#!/usr/bin/env python  
# coding: utf-8

__author__ = 'Yuta Hayashibe' 
__version__ = ""
__copyright__ = ""
__license__ = "GPL v3"

import tool
import message
import cgi
import const


if const.PERMIT_ONLY_LOCALHOST and not tool.is_localhost():
    quit()

f = cgi.FieldStorage()

cmd = f.getfirst('cmd', None)
body = f.getfirst('mytext', None)
fname = f.getfirst('f', '')
encoding = f.getfirst('encoding', '')

fname = fname.decode(const.FILESYSTEM_ENCODING)
fname = fname.replace(u'|', u'/')
if fname in [u"..\\", u"../"]:
    out =  message.base_html.substitute(title=u"DENY", body=u"DENY[" + fname + u"]")
    print out.encode(const.OUTPUT_ENCODING)
    quit()
elif fname.endswith(u"/"):
    fname = fname[:-1]

if fname == '':
    fname = '.'

if cmd is None:
    is_dir = tool.get_dir(const.DOCUMENT_ROOT, fname)
    if not is_dir:
        tool.form(const.DOCUMENT_ROOT, fname)
        pass
elif cmd == 'save' and body and encoding and fname:
    tool.save(const.DOCUMENT_ROOT + fname, encoding, body)
else:
    out =  message.base_html.substitute(title=u"Illegal format", body=u"Illegal format")
    print out.encode(const.OUTPUT_ENCODING)                


