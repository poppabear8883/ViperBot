"""
viper.py (c) 2016 Poppabear @ Freenode Irc Network

WARNING:
THIS FILE SHOULD NOT BE EDITED BY THE USER!
EDITING THIS FILE COULD CORRUPT YOUR VIPERBOT INSTALL.
"""
import os
import sys
import conf

import libs.helpers as helper
import libs.inputs as inputs
from classes.bot import Bot

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

    if not disable_tls == 'y' or not disable_tls == 'Y':
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
    print ' '

    print ' '
    print '# Lets setup the Hub Bot first'
    print ' '
    # hubnick = newBot(network)
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

    hubBot.create('hub')

    print ' '
    print '# and now the AltHub bot'
    print ' '
    # althubnick = newBot(network)
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

    ahubBot.create('althub')

    hubBot.start('-m')
    ahubBot.start()

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

    return network

def newBot(network):
    INSTALLDIR = conf.VIPER_INSTALL_DIRECTORY
    os.chdir(INSTALLDIR)

    botnick = ''

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

    return botnick

'''
***************************
    end of main program
***************************
'''
# HELPERS
