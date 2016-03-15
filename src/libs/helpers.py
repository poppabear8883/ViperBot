import urllib2
import tarfile
import os
import sys

import conf

def internet_on():
    try:
        response=urllib2.urlopen('http://173.194.206.102',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def appendToFile(filename, text):
    with open(filename, "a") as myfile:
        myfile.write(text + '\n')

def download(url, filename):
    u = urllib2.urlopen(url)
    f = open(filename, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (filename, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print status,

    f.close()
    print ' '

def extract(filename):
    print 'Extracting ...'
    tar = tarfile.open(filename)
    tar.extractall()
    tar.close()