#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import ( division, absolute_import, print_function, unicode_literals )

import sys, os, tempfile, logging

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse

def download_file(url, filename):
    u = urllib2.urlopen(url)
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")
        print()

    return filename

unicodeDataFiles = { 
		'UnicodeData.txt': 'ftp://ftp.unicode.org/Public/UNIDATA/UnicodeData.txt', 
		'PropList.txt': 'ftp://ftp.unicode.org/Public/UNIDATA/PropList.txt', 
		'SpecialCasing.txt': 'ftp://ftp.unicode.org/Public/UNIDATA/SpecialCasing.txt', 
		'WordBreakProperty.txt': 'ftp://ftp.unicode.org/Public/UNIDATA/auxiliary/WordBreakProperty.txt', 
	}

for filename, url in unicodeDataFiles.iteritems():
	print(download_file(url, filename))
