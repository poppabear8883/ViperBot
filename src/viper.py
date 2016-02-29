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
    # Home Directory
    os.chdir(conf.HOME)

    download(conf.EGG_SRC_URL, conf.HOME + 'eggdrop18.tar.gz')
    extract(conf.HOME + 'eggdrop18.tar.gz')
    os.remove(conf.HOME + 'eggdrop18.tar.gz')
    os.system('mv ' + conf.HOME + "eggdrop-* " + conf.VIPER_TMP_DIRECTORY)

    # TMP Directory
    os.chdir(conf.VIPER_TMP_DIRECTORY)

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
    print 'Configuring ...'
    if disable_tls == 'y' or disable_tls == 'Y':
        os.system('./configure --disable-tls')
    else:
        os.system('./configure')

    print 'Building ...'
    os.system('make config')
    os.system('make static')
    os.system('make install DEST=' + conf.VIPER_DIRECTORY)

    if disable_tls != 'y' or disable_tls != 'Y':
        print 'Generating SSL Certificates ...'
        os.system('make sslcert DEST=' + conf.VIPER_DIRECTORY)

    if os.path.exists(conf.VIPER_TMP_DIRECTORY):
        os.chdir(conf.HOME)
        os.system('rm -rf ' + conf.VIPER_TMP_DIRECTORY)

    if os.path.exists(conf.VIPER_DIRECTORY):
        # Viper Install Directory
        os.chdir(conf.VIPER_DIRECTORY)

        # cleanup files
        os.remove('eggdrop.conf')
        os.remove('README')
        os.remove('eggdrop')

        # cleanup directories
        os.system('rm -rf doc')

        # rename files
        os.rename('eggdrop-1.8.0', 'viperbot-' + conf.VIPER_VERSION)
        os.rename('eggdrop.crt', 'viper.crt')
        os.rename('eggdrop.key', 'viper.key')

        # create symlinks
        os.system('ln -s viperbot-' + conf.VIPER_VERSION + ' viper')

    update()

    # Home Directory
    os.chdir(conf.HOME)

    print 'Install Successful ...'
    print ' '
    print 'Install Directory: ' + conf.VIPER_DIRECTORY

def update():
    # todo: Create an array of paths in conf.py, and loop ...
    conf_py = conf.VIPER_DIRECTORY + '/conf.py'
    conf_py_old = conf.VIPER_DIRECTORY + '/conf.py.old'
    tcl = conf.VIPER_DIRECTORY + '/viper.tcl'
    tcl_old = conf.VIPER_DIRECTORY + '/viper.tcl.old'
    botnet = conf.VIPER_DIRECTORY + '/botnet.conf'
    botnet_old = conf.VIPER_DIRECTORY + '/botnet.conf.old'
    vb_conf = conf.VIPER_DIRECTORY + '/viperbot.conf'
    vb_conf_old = conf.VIPER_DIRECTORY + '/viperbot.conf.old'
    vb_py = conf.VIPER_DIRECTORY + '/viperbot.py'
    vb_py_old = conf.VIPER_DIRECTORY + '/viperbot.py.old'

    print 'Updating core ...'
    if os.path.exists(conf.VIPER_DIRECTORY):
        os.chdir(conf.VIPER_DIRECTORY)

        if os.path.exists(tcl):
            if os.path.exists(tcl_old):
                os.remove(tcl_old)
            os.rename(tcl, tcl_old)
        download(conf.VIPER_SRC_URL + '/scripts/viper.tcl', tcl)

        if os.path.exists(botnet):
            if os.path.exists(botnet_old):
                os.remove(botnet_old)
            os.rename(botnet, botnet_old)
        download(conf.VIPER_SRC_URL + '/configs/botnet.conf', botnet)

        if os.path.exists(vb_conf):
            if os.path.exists(vb_conf_old):
                os.remove(vb_conf_old)
            os.rename(vb_conf, vb_conf_old)
        download(conf.VIPER_SRC_URL + '/configs/viperbot.conf', vb_conf)

        if os.path.exists(vb_py):
            if os.path.exists(vb_py_old):
                os.remove(vb_py_old)
            os.rename(vb_py, vb_py_old)
        download(conf.VIPER_SRC_URL + '/viperbot.py', vb_py)

        if os.path.exists(conf_py):
            if os.path.exists(conf_py_old):
                os.remove(conf_py_old)
            os.rename(conf_py, conf_py_old)
        download(conf.VIPER_SRC_URL + '/src/conf.py', conf_py)

        if os.path.exists(conf.VIPER_SRC_URL + '/text/motd'):
            if os.path.exists(conf.VIPER_SRC_URL + '/text/motd.old'):
                os.remove(conf.VIPER_SRC_URL + '/text/motd.old')
            os.rename(conf.VIPER_SRC_URL + '/text/motd', conf.VIPER_SRC_URL + '/text/motd.old')
        download(conf.VIPER_SRC_URL + '/text/motd', 'text/motd')

        if os.path.exists(conf.VIPER_SRC_URL + '/text/banner'):
            if os.path.exists(conf.VIPER_SRC_URL + '/text/banner.old'):
                os.remove(conf.VIPER_SRC_URL + '/text/banner.old')
            os.rename(conf.VIPER_SRC_URL + '/text/banner', conf.VIPER_SRC_URL + '/text/banner.old')
        download(conf.VIPER_SRC_URL + '/text/banner', 'text/banner')

'''
    HELPERS
'''
def internet_on():
    try:
        response=urllib2.urlopen('http://8.8.8.8',timeout=1)
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