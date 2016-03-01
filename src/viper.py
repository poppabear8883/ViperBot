"""
viper.py (c) 2016 Poppabear @ Freenode Irc Network

WARNING:
THIS FILE SHOULD NOT BE EDITED BY THE USER!
EDITING THIS FILE COULD CORRUPT YOUR VIPERBOT INSTALL.
"""
import os
import tarfile
import urllib2
import conf

def build():
    print 'Installing ...'
    # CD into ViperBot SRC Directory
    os.chdir(conf.VIPER_SRC_DIRECTORY)

    print ' '
    print '***************************************************************************'
    print 'ViperBot can be optionally compiled with TLS support. This requires OpenSSL'
    print '0.9.8 or more recent installed on your system.'
    print ' '
    print 'TLS support includes encryption for IRC, DCC, botnet, telnet and scripted'
    print 'connections as well as certificate authentication for users and bots.'
    print '***************************************************************************'
    print ' '

    disable_tls = raw_input('Would you like to disable TLS? (y/N): ')
    print 'Configuring ...' + ' log: ' + os.getcwd()
    if disable_tls == 'y' or disable_tls == 'Y':
        os.system('./configure --disable-tls')
    else:
        os.system('./configure')

    print 'Building ...'
    os.system('make config')
    os.system('make static')
    os.system('make install DEST=' + conf.VIPER_INSTALL_DIRECTORY)

    if disable_tls != 'y' or disable_tls != 'Y':
        print 'Generating SSL Certificates ...'
        os.system('make sslcert DEST=' + conf.VIPER_INSTALL_DIRECTORY)

    if os.path.exists(conf.VIPER_INSTALL_DIRECTORY):
        os.system('cp __init__.py ' + conf.VIPER_INSTALL_DIRECTORY)
        os.system('cp viper.py ' + conf.VIPER_INSTALL_DIRECTORY)
        os.system('cp viperbot.py ' + conf.VIPER_INSTALL_DIRECTORY)
        os.system('cp conf.py ' + conf.VIPER_INSTALL_DIRECTORY)
        os.system('cp viper.py ' + conf.VIPER_INSTALL_DIRECTORY)

    # Home Directory
    os.chdir(conf.HOME)

    print 'Install Successful ...'
    print ' '
    print 'Install Directory: ' + conf.VIPER_INSTALL_DIRECTORY

'''
    HELPERS
'''
def internet_on():
    try:
        response=urllib2.urlopen('http://173.194.206.102',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

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