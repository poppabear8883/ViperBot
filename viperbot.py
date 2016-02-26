#!/usr/bin/python
"""
viperbot.py by Poppabear
"""
import os, sys, getopt, urllib2, tarfile

# OS Env Variables
HOME = os.getenv("HOME") + '/'

# Eggdrop Variables
egg18 = 'ftp://ftp.eggheads.org/pub/eggdrop/source/snapshot/eggdrop1.8-snapshot.tar.gz'
eggdir = 'eggdrop1.8'

# Viperbot Variables
viper_ver = 'v1.0'
viper_dir = HOME + "viperbot"
viper_tmp = HOME + 'viper_tmp'
viper_url = 'https://github.com/poppabear8883/ViperBot/raw/master/'
viper_botnetconf = viper_dir + 'botnet.conf'

# Main program entry point
def main(argv):
    banner()

    try:
        opts, args = getopt.getopt(argv, "ihn:u:s:o:", [
            "options="
        ])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            help()
        elif opt == '-i':
            viper_install()
        elif opt == '-n':
            viper_new(arg)
        elif opt == '-u':
            viper_update(arg)
        elif opt == '-s':
            viper_start(arg)
        elif opt in ("-o", "--options"):
            print 'Viper Options: ' + arg


def banner():
    print ' '
    print '%s (c) 2016 Poppabear @ Freenode Irc Network' % viper_ver
    print '____   ____ .__                             __________             __'
    print '\   \ /   / |__| ______     ____   _______  \______   \   ____   _/  |_'
    print ' \   Y   /  |  | \____ \  _/ __ \  \_  __ \  |    |  _/  /  _ \  \   __/'
    print '  \     /   |  | |  |_> > \  ___/   |  | \/  |    |   \ (  <_> )  |  |'
    print '   \___/    |__| |   __/   \___  >  |__|     |______  /  \____/   |__|'
    print '                 |__|          \/                   \/'
    print ' '
    print ' '
    print ' '

def help():
    print '-i'
    print '  Installs ViperBot for the first time'
    print '-n <hub,ahub,leaf>'
    print '  Creates a new bot'
    print '-u <filename>'
    print '  Updates a file from the remote repository'
    print '-s <botnick>'
    print '  Starts a bot. <botnick> is Case Sensitive'

def viper_install():
    if os.path.exists(viper_dir):
        print 'Viperbot is already installed.'
        print ' '

        reinstall = raw_input("Would you like to reinstall ViperBot? (y/N): ")
        if reinstall == 'y' or reinstall == 'Y':
            viper_reinstall()
        else:
            # exit script
            sys.exit(0)

    # Proceed with installing
    print 'Installing .....'
    viper_getegg()
    viper_build()

def viper_reinstall():
    # create a backup of old install
    os.rename(viper_dir, HOME + '/viper_old')
    viper_install()

def viper_new(type = 'leaf'):
    print 'Creating new ' + type + ' ...'


def viper_update(file):
    print 'Updating ' + file

def viper_start(botnick):
    print 'Starting ' + botnick

def viper_getegg():
    downloadFile(egg18, HOME + 'eggdrop18.tar.gz')
    extractFile(HOME + 'eggdrop18.tar.gz')
    os.rename(HOME + 'eggdrop1.8', viper_tmp)

def viper_build():
    os.chdir(viper_tmp)
    print 'ViperBot can be optionally compiled with TLS support. This requires OpenSSL'
    print '0.9.8 or more recent installed on your system.'
    print ' '
    print 'TLS support includes encryption for IRC, DCC, botnet, telnet and scripted'
    print 'connections as well as certificate authentication for users and bots.'
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
    os.system('make install DEST=' + viper_dir)

    if disable_tls != 'y' or disable_tls != 'Y':
        print 'Generating SSL Certificates ...'
        os.system('sslcert DEST=' + viper_dir)

    viper_setup()
    viper_getcore()

def viper_setup():
    print 'Setting up ViperBot ...'
    os.chdir(HOME)

    if os.path.exists(viper_tmp):
        os.remove(viper_tmp)

    if os.path.exists(viper_dir):
        os.system('cp ~/viperbot.py ' + viper_dir + '/viperbot')
        downloadFile(viper_url + '/motd', viper_dir + '/text/motd')
        downloadFile(viper_url + '/banner', viper_dir + '/text/banner')
        os.remove('README')
        os.remove(viper_dir + '/eggdrop.conf')
        os.remove(viper_dir + '/doc')
        os.rename(viper_dir + '/eggdrop', viper_dir + '/viper')

def viper_getcore():
    print 'Downloading ViperBot Core ...'


'''
HELPERS
'''
def downloadFile(url, filename):
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
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()
    print ' '

def extractFile(filename):
    print 'Extracting ...'
    tar = tarfile.open(filename)
    tar.extractall()
    tar.close()

if __name__ == "__main__":
  main(sys.argv[1:])
