#!/usr/bin/env python  
# coding: utf-8


__author__ = 'Yuta Hayashibe' 
__version__ = ""
__copyright__ = ""
__license__ = "GPL v3"

import string

base_html = string.Template(u"""Content-Type: text/html

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja">
<head>
        <title>${title}</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
${body}
</body>
</html>""")




form_html = string.Template(u"""Content-Type: text/html

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja">
<head>
        <title></title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<meta http-equiv="Content-Script-Type" content="text/javascript" />

	<script type='text/javascript' src='http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js'></script>
	<script type='text/javascript' src='aediter.js'></script>
</head>
	

<body>
<div id='notice' style="float:left; height:1em;"></div>
<div id='notice_r' style="float:right; height:1em; text-align:right;">${notice_r}</div>
<form id="editarea" method="post" onsubmit="return false;">
        <textarea id='mytext' style='min-width:10em; min-height:5em; resize: none; font-size:14pt;' name="mytext">$mytext</textarea>


        <input id="mytitle" type="hidden" value="$fname" />
        <input id="encoding" type="hidden" value="$encoding" />
        <input id="isNew" type="hidden" value="$isNew" />
</form>

</body>
</html>""")

json_base = string.Template(u"""Content-Type: application/json; charset=utf-8

${data}
""")

