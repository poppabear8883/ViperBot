"""
viper.py (c) 2016 Poppabear @ Freenode Irc Network

WARNING:
THIS FILE SHOULD NOT BE EDITED BY THE USER!
EDITING THIS FILE COULD CORRUPT YOUR VIPERBOT INSTALL.
"""
import os
import subprocess
import sys

from distutils.dir_util import copy_tree
from distutils.file_util import copy_file

from bot import Bot
from tools import inputs

# Users Home Directory
_HOME = os.getenv("HOME") + '/'

# ViperBot's Version
_VERSION = '1.0'

# ViperBot's Install Directory
_INSTALL_DIR = _HOME + "viperbot"

#ViperBot's src Directory
_SRC_DIR = '../src'

_NETWORKS_DIR = _INSTALL_DIR + '/networks'

_CORE_SCRIPTS_DIR = _INSTALL_DIR + '/scripts'

_CONFIG_DIR = _INSTALL_DIR + '/configs'

_BOTNET_CONFIG = _CONFIG_DIR + '/botnet.conf'

_CONF = _CONFIG_DIR + '/viperbot.conf'

# todo: check_call() instead of call() -> wrap in try except, catch exceptions
def build():
    print '[ViperBot] Installing ... ' + os.getcwd()
    print ' '

    # CD into ViperBot SRC Directory
    # print '[ViperBot] Changing to: ' + conf.VIPER_SRC_DIRECTORY
    os.chdir('../')

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
        subprocess.call(['./configure', '--disable-tls'])
    else:
        subprocess.call('./configure')

    print '[ViperBot] Building ... ' + os.getcwd()
    subprocess.call(['make', 'config'])
    subprocess.call(['make', 'static'])
    subprocess.call(['make', 'install', 'DEST=' + _INSTALL_DIR])

    if not disable_tls == 'y' or not disable_tls == 'Y':
        print '[ViperBot] Generating SSL Certificates ...'
        subprocess.call(['make', 'sslcert', 'DEST=' + _INSTALL_DIR])

    if os.path.exists(_INSTALL_DIR):
        os.chmod('viperbot.py', 0774)
        os.chmod('./viperpy/main.py', 0744)
        os.chmod('./viperpy/install.py', 0744)

        copy_file('viperbot.py', _INSTALL_DIR)
        os.mkdir(_INSTALL_DIR + '/viperpy')
        copy_tree('./viperpy', _INSTALL_DIR + '/viperpy')

        print ' '
        print '***************************************************************************'
        print '[ViperBot] Yay! Installion of ViperBot was Successful ...'
        print '***************************************************************************'
        print ' '
        print '[ViperBot] has been Installed to: ' + _INSTALL_DIR
        print ' '
    else:
        print '[ViperBot] Fatal Error: INSTALL FAILED!'
        sys.exit(0)

    # Start the setup process
    print ' '
    print '***************************************************************************'
    print ' Setup a Network.'
    print ' '

    network = newNetwork()

    print ' '
    print '***************************************************************************'
    print ' Your new network has been added'
    print '***************************************************************************'

    # All Done!
    sys.exit(0)

def setup(network):
    print '[Viperbot] Changing to: ' + _INSTALL_DIR
    os.chdir(_INSTALL_DIR)

    print ' '
    print '***************************************************************************'
    print ' Lets setup a Hub and AltHub for this network.'
    print '***************************************************************************'
    print 'Note:'
    print ' Your Hub bot is what all other bots will link to, AltHub will be the bot '
    print ' that all bots will link to IF the Hub bot is not available for linking.'
    print ' '
    print ' EVERY bot will need its OWN IP or OWN Port, The IP and Port CANNOT '
    print ' be the same on any of the bots in your botnet!'
    print ' '

    print ' '
    print '# Lets setup the Hub Bot first'
    print ' '
    hubBot = newBot(network)
    # hubBot = tmpHub()

    hubBot.create('hub')

    print ' '
    print '# and now the AltHub bot'
    print ' '
    ahubBot = newBot(network)
    # ahubBot = tmpAltHub()

    ahubBot.create('althub')

    hubBot.start('-m')
    ahubBot.start()

    # Home Directory
    os.chdir(_HOME)

    print ' '
    print '***************************************************************************'
    print 'You have completed the setup process. You can now go to\n' \
          ' ' + _INSTALL_DIR + ' and run ./viperbot.py'
    print '***************************************************************************'
    print ' '

def newNetwork():
    os.chdir(_INSTALL_DIR)
    network = ''

    while True:
        network = inputs.alphaNumInput('Network Name: ')
        if os.path.exists('networks/'+network):
            print 'You already have this network!'
            continue
        else:
            break

    print 'Creating Network ...'
    os.mkdir('networks/'+network)
    os.mkdir('networks/'+network+'/logs')
    os.mkdir('networks/'+network+'/scripts')

    setup(network)

    return network

def newBot(network, botnick=''):
    INSTALLDIR = _INSTALL_DIR
    os.chdir(INSTALLDIR)

    if botnick == '':
        while True:
            botnick = inputs.alphaNumInput('Bot\'s Nick: ')
            botnick_conf = INSTALLDIR+'/'+network+'/'+botnick+'.conf'
            if os.path.exists(botnick_conf):
                print 'This botnick already exists!'
                continue
            else:
                break

    # Create a Bot Object
    bot_o = Bot(botnick)

    bot_o.NETWORK = network

    bot_o.OWNER = inputs.alphaNumInput('Owner\'s Nick: ')
    bot_o.EMAIL = inputs.emailInput('Owner\'s Email: ')

    v4v6 = inputs.yesNoInput('Is this bot using IPv6? (y/N): ')
    if v4v6 == 'y' or v4v6 == 'Y':
        preferipv6 = inputs.yesNoInput('Do you prefer IPv6 over IPv4? (y/N): ')
        bot_o.ISV6 = True
        if preferipv6 == 'y' or preferipv6 == 'Y':
            bot_o.PREFERIPV6 = True

    bot_o.IP = inputs.ipInput('IP: ')

    bot_o.PORT = inputs.portInput('Port: ')

    nat = inputs.yesNoInput('Is this bot behind a NAT? (y/N): ')
    if nat == 'y' or nat == 'Y':
        bot_o.NATIP = inputs.ipInput('NAT IP: ')

    print '---------------------------------------------------------'
    print ' Here you will list the servers that this bot will\n' \
          ' attempt to connect to.\n' \
          '\n' \
          'Syntax: server:port'
    print 'Example: irc.freenode.net:6667,irc.freenode.net:6697\n' \
          '\n' \
          'Note: Do Not use spaces!'
    print '---------------------------------------------------------'
    print ' '

    servers = inputs.serversInput('Servers: ')
    bot_o.SERVERS = servers

    # Lets create our new bot!
    bot_o.create('hub')

    return bot_o


# for debugging and testing
def tmpHub():
    hubBot = Bot('ViperHub')
    hubBot.NETWORK = 'Freenode'
    hubBot.NATIP = ''
    hubBot.OWNER = 'Poppabear, PoppaWork'
    hubBot.EMAIL = 'servnx@gmail.com'
    hubBot.IP = '162.243.241.68'
    hubBot.PORT = '3456'
    hubBot.PREFERIPV6 = '0'
    hubBot.LISTENADDR = ''
    hubBot.ISV6 = False
    hubBot.SERVERS = 'irc.freenode.net:6667,chat.us.freenode.net:6667'

    return hubBot

def tmpAltHub():
    ahubBot = Bot('ViperAltHub')
    ahubBot.NETWORK = 'Freenode'
    ahubBot.NATIP = ''
    ahubBot.OWNER = 'Poppabear, PoppaWork'
    ahubBot.EMAIL = 'servnx@gmail.com'
    ahubBot.IP = '162.243.241.68'
    ahubBot.PORT = '3457'
    ahubBot.PREFERIPV6 = '0'
    ahubBot.LISTENADDR = ''
    ahubBot.ISV6 = False
    ahubBot.SERVERS = 'irc.freenode.net:6667,chat.us.freenode.net:6667'

    return ahubBot