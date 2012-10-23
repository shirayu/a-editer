#!/usr/bin/env python  
# coding: utf-8

__author__ = 'Yuta Hayashibe' 
__version__ = ""
__copyright__ = ""
__license__ = "GPL v3"

import message
import os
import urllib
import cgi

import const
def is_localhost():
    ip = 'unkwon'
    if os.environ.has_key('REMOTE_ADDR'):
        ip = os.environ['REMOTE_ADDR']
        if ip == 'localhost':
            return True
    out =  message.base_html.substitute(title=u"DENY", body=ip)
    print out.encode(const.OUTPUT_ENCODING)
    return False


SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
            1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}

def pretty_size(size, strict=True):
    if size < 0:
        raise size

    multiple = 1024 if strict else 1000
    if size < multiple:
        return "%d%s" %(size, 'Byte')
    for suffix in SUFFIXES[multiple]:
        size /= multiple
        if size < multiple:
            return "%0.1f %s" %(size, suffix)
    return "%0.1f %s" %(size, SUFFIXES[multiple][-1])


import sys
import os
def get_dir(document_root, dire):
    mydire = (document_root + dire).encode(const.FILESYSTEM_ENCODING)
    if not os.path.isdir(mydire):
        return False
    if not os.path.exists(mydire):
        out =  message.base_html.substitute(title="not found", body=u"Nof Found[" + dire + "]")
        print out.encode(const.OUTPUT_ENCODING)
        return True
    dire = dire + '/'

    dirlist = u''
    filelist = u''

    for f in sorted(os.listdir(mydire)):
        _ret_path = u"%s%s" % (dire, f.decode(const.FILESYSTEM_ENCODING))
        ret_path = urllib.quote_plus(_ret_path.replace(u'/', u'|').encode(const.FILESYSTEM_ENCODING))
        fpath = u"%s/%s%s" % (document_root, dire, f.decode(const.FILESYSTEM_ENCODING))
        if os.path.isdir(fpath.encode(const.FILESYSTEM_ENCODING)):
            dirlist += u"""
            <a href="./?f=%s">%s</a><br />
            """ % (ret_path,  cgi.escape(f.decode(const.FILESYSTEM_ENCODING)))
        else:
            size = os.path.getsize(fpath.encode(const.FILESYSTEM_ENCODING))
            filelist += u"""
            <a href="./?f=%s">%s</a> [%s]<br />
            """ % (ret_path, cgi.escape(f.decode(const.FILESYSTEM_ENCODING)), pretty_size(size))

    myret = u"""
   <div id='notice_r' style="height:1em; text-align:right;">%s</div> 
    <h1>[%s]</h1>
<h2>Directories</h2>
   %s
<h2>Files</h2>
   %s
    """ % (_getParentLink(dire), dire, dirlist, filelist)
    out =  message.base_html.substitute(title=dire, body=myret)
    print out.encode(const.OUTPUT_ENCODING)
    return True


CODECS = ['utf-8','euc_jp','cp932', 'shift_jis',
        'euc_jis_2004','euc_jisx0213','iso2022_jp','iso2022_jp_1',
        'iso2022_jp_2','iso2022_jp_2004','iso2022_jp_3','iso2022_jp_ext',
        'shift_jis_2004','shift_jisx0213','utf_16','utf_16_be',
        'utf_16_le','utf_7','utf_8_sig'];

def _getParentLink(fname):
    if fname.endswith(u'/'):
        tmp = fname[:-1]
    else:
        tmp = fname
    _pos = tmp.rfind(u'/')
    if _pos != -1:
        parent = tmp[:_pos]
    else:
        parent = tmp
    link = """<a href="?f=%s">Back</a>""" % cgi.escape(parent)

    return link

import codecs
def form(document_root, fname):
    myfname = document_root + fname.encode(const.FILESYSTEM_ENCODING)
    body = u''
    isNew = u''
    if os.path.exists(myfname):
        for _mycodec in CODECS:
            mycodec = _mycodec
            try:
                fin  = codecs.open(myfname, 'rU', _mycodec)
                body = fin.read()
                if len(body) > 0 and body[-1]==u'\n':
                    body = body[:-1] #FIXME
                fin.close()
                break
            except:
                continue
    else:
        isNew = u'*'
        mycodec = const.DEFAULT_ENCODING
    myret =  message.form_html.substitute(mytext=cgi.escape(body), fname=cgi.escape(fname), encoding=cgi.escape(mycodec), isNew=cgi.escape(isNew), notice_r= _getParentLink(fname))
    print myret.encode(const.OUTPUT_ENCODING)


import json
def save(fname, encoding, body):

    myfname = fname.encode(const.FILESYSTEM_ENCODING)
    try:
        mybody = unicode(body, const.DEFAULT_ENCODING)
        outf = codecs.open(myfname, "w", encoding)
        outf.write(mybody)
        outf.close()
        out =  message.json_base.substitute(data=u"%s" % json.dumps({'status' : 'ok'}))
    except:
        raise
        out =  message.json_base.substitute(data=u"%s" % json.dumps({'status' : 'error'}))
    print out.encode(const.OUTPUT_ENCODING)                


