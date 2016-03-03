"""
viper.py (c) 2016 Poppabear @ Freenode Irc Network

WARNING:
THIS FILE SHOULD NOT BE EDITED BY THE USER!
EDITING THIS FILE COULD CORRUPT YOUR VIPERBOT INSTALL.
"""
import os
import sys
import getpass
import tarfile
import urllib2
import conf

def build():
    print '[ViperBot] Installing ...'
    print ' '

    # CD into ViperBot SRC Directory
    print '[ViperBot] Changing to: ' + conf.VIPER_SRC_DIRECTORY
    os.chdir(conf.VIPER_SRC_DIRECTORY)

    print ' '
    print '***************************************************************************'
    print ' ViperBot can be optionally compiled with TLS support. This requires OpenSSL'
    print ' 0.9.8 or more recent installed on your system.'
    print ' '
    print ' TLS support includes encryption for IRC, DCC, botnet, telnet and scripted'
    print ' connections as well as certificate authentication for users and bots.'
    print '***************************************************************************'
    print ' '

    disable_tls = raw_input('Would you like to disable TLS? (y/N): ')
    print '[ViperBot] Configuring ...'
    if disable_tls == 'y' or disable_tls == 'Y':
        os.system('./configure --disable-tls')
    else:
        os.system('./configure')

    print '[ViperBot] Building ...'
    os.system('make config')
    os.system('make static')
    os.system('make install DEST=' + conf.VIPER_INSTALL_DIRECTORY)

    if disable_tls != 'y' or disable_tls != 'Y':
        print '[ViperBot] Generating SSL Certificates ...'
        os.system('make sslcert DEST=' + conf.VIPER_INSTALL_DIRECTORY)

    if os.path.exists(conf.VIPER_INSTALL_DIRECTORY):
        print ' '
        print '***************************************************************************'
        print '[ViperBot] Yay! Installion of ViperBot was Successful ...'
        print '***************************************************************************'
        print ' '
        print '[ViperBot] has been Installed to: ' + conf.VIPER_INSTALL_DIRECTORY
        print ' '
    else:
        print '[ViperBot] Fatal Error: INSTALL FAILED!'
        sys.exit(0)

    # Start the setup process
    setup()

    # All Done!
    sys.exit(0)

def setup():
    print '[Viperbot] Changing to: ' + conf.VIPER_INSTALL_DIRECTORY
    os.chdir(conf.VIPER_INSTALL_DIRECTORY)

    # we need to make sure that viperbot.py is executable
    os.chmod('viperbot.py', 0774)

    global_conf = conf.VIPER_GLOBAL_CONFIG

    print ' '
    print '***************************************************************************'
    print ' Now that ViperBot is installed, we need to setup a Network.'
    print ' '

    network = newNetwork()

    print ' '
    print '***************************************************************************'
    print ' Your new network has been added\n' \
          ' Lets setup a Hub and AltHub for this network.'
    print '***************************************************************************'
    print 'Note:'
    print ' Your Hub bot is what all other bots will link to, AltHub will be the bot '
    print ' that all bots will link to IF the Hub bot is not available for linking.'
    print ' '
    print ' EVERY bot will need its OWN IP or OWN Port, The IP and Port CANNOT '
    print ' be the same on any of the bots in your botnet!'

    hubnick = newHub(network)

    # Home Directory
    os.chdir(conf.HOME)

    print ' '
    print '***************************************************************************'
    print 'You have completed the setup process. You can now go to\n' \
          ' ' + conf.VIPER_INSTALL_DIRECTORY + ' and run ./viperbot.py'
    print '***************************************************************************'
    print ' '

def newNetwork():
    os.chdir(conf.VIPER_INSTALL_DIRECTORY)
    network = ''

    while True:
        network = userInput('Network Name: ')
        if os.path.exists('networks/'+network):
            print 'You already have this network!'
            continue
        else:
            break

    print 'Creating Network ...'
    os.mkdir('networks/'+network)
    os.mkdir('networks/'+network+'/logs')
    os.mkdir('networks/'+network+'/scripts')

    return network

"""
viperbot.conf
-------------
%VIPERPATH%
%BOTNICK%
%OWNER% %EMAIL%
%NETWORK%
%VHOST4%
%VHOST6%
%LISTENADDR%
%PREFERIPV6%
%LANGUAGE%
%LISTEN% %PORT%
%NATIP%
%SERVERS%

botnet.conf
-----------
%HUBNICK% %HUBIP% %HUBPORT%
%ALTHUBNICK% %ALTHUBIP% %ALTHUBPORT%
"""
def newHub(network):
    os.chdir(conf.VIPER_INSTALL_DIRECTORY)
    net_path = 'networks/'+network+'/'

    v6 = False
    viperpath = conf.VIPER_INSTALL_DIRECTORY
    botnick = ''

    botnick = userInput('Hub\'s Nick: ')
    while True:
        if os.path.exists(net_path+botnick+'.conf'):
            print 'This botnick already exists!'
            continue
        else:
            break

    owner = userInput('Owner\'s Nick: ')
    email = userInput('Owner\'s Email: ')
    v4v6 = userInput('Is this bot using IPv6? (y/N): ')
    if v4v6 == 'y' or v4v6 == 'Y':
        v6 = True

    replaceInFile('configs/viperbot.conf', net_path+botnick+'.conf',
                  '%VIPERPATH', conf.VIPER_INSTALL_DIRECTORY + '/viper')

    replaceInFile('configs/viperbot.conf', net_path+botnick+'.conf',
                  '%NETWORK%', network)

    replaceInFile('configs/viperbot.conf', net_path+botnick+'.conf',
                  '%BOTNICK%', botnick)

    replaceInFile('configs/viperbot.conf', net_path+botnick+'.conf',
                  '%OWNER%', owner)

    replaceInFile('configs/viperbot.conf', net_path+botnick+'.conf',
                  '%EMAIL%', email)

    return botnick


'''
***************************
    end of main program
***************************
'''
# HELPERS
def userInput(question):
    data = ''

    while True:
        data = raw_input(question)
        if not data.isalnum():
            print 'Must be an Alphanumeric value!'
            continue
        elif '' == data:
            print 'Can not be empty!'
            continue
        else:
            break

    print ' '
    return data

def internet_on():
    try:
        response=urllib2.urlopen('http://173.194.206.102',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def appendToFile(filename, text):
    with open(filename, "a") as myfile:
        myfile.write(text + '\n')

def replaceInFile(fin, fout, search, replace):
    f = open(fin,'r')
    filedata = f.read()
    f.close()

    newdata = filedata.replace(search, replace)

    f = open(fout,'w')
    f.write(newdata)
    f.close()

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