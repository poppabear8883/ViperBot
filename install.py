#!/usr/bin/python
"""
install.py (c) 2016 Poppabear @ Freenode Irc Network

WARNING:
THIS FILE SHOULD NOT BE EDITED BY THE USER!
EDITING THIS FILE COULD CORRUPT YOUR VIPERBOT INSTALL.
"""
import os
import sys

from src import conf
from src import viper

# Main program entry point
def main(argv):
    banner()
    viper_install()

def banner():
    print ' '
    print '(c) 2016 Poppabear @ Freenode Irc Network'
    print '____   ____ .__                             __________             __'
    print '\   \ /   / |__| ______     ____   _______  \______   \   ____   _/  |_'
    print ' \   Y   /  |  | \____ \  _/ __ \  \_  __ \  |    |  _/  /  _ \  \   __/'
    print '  \     /   |  | |  |_> > \  ___/   |  | \/  |    |   \ (  <_> )  |  |'
    print '   \___/    |__| |   __/   \___  >  |__|     |______  /  \____/   |__|'
    print '                 |__|          \/                   \/'
    print ' '
    print ' '
    print '*************************************************************************'
    print 'install.py v1.0'
    print '   Use this program to install ViperBot.'
    print '*************************************************************************'
    print ' '
    print ' '

def viper_install():
    # if not viper.internet_on():
    #     print 'Error: You DO NOT seem to be connected to the internet.'
    #     print 'An internet connection is required to install ViperBot.'
    #     sys.exit(0)

    if os.path.exists(conf.VIPER_INSTALL_DIRECTORY):
        print 'Viperbot is already installed.'
        print ' '

        reinstall = raw_input("Would you like to reinstall ViperBot? (y/N): ")
        if reinstall == 'y' or reinstall == 'Y':
            viper_reinstall()
        else:
            # exit script
            sys.exit(0)

    install = raw_input("Would you like to install ViperBot? (y/N): ")
    if install == 'y' or install == 'Y':
        viper.build()
    else:
        # exit script
        sys.exit(0)

def viper_reinstall():
    if os.path.exists(conf.HOME + '/viperbot_old'):
        os.system('rm -rf ' + conf.HOME + '/viperbot_old')

    os.rename(conf.VIPER_INSTALL_DIRECTORY, conf.HOME + '/viperbot_old')
    viper.build()


if __name__ == "__main__":
    main(sys.argv[1:])
