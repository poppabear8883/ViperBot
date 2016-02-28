#!/usr/bin/python
"""

install.py (c) 2016 Poppabear @ Freenode Irc Network

"""
import getopt
import os
import sys

from src import viper
from src import conf

# Main program entry point
def main(argv):
    banner()
    viper_install()

def banner():
    print ' '
    print 'v%s (c) 2016 Poppabear @ Freenode Irc Network' % conf.VIPER_VERSION
    print '____   ____ .__                             __________             __'
    print '\   \ /   / |__| ______     ____   _______  \______   \   ____   _/  |_'
    print ' \   Y   /  |  | \____ \  _/ __ \  \_  __ \  |    |  _/  /  _ \  \   __/'
    print '  \     /   |  | |  |_> > \  ___/   |  | \/  |    |   \ (  <_> )  |  |'
    print '   \___/    |__| |   __/   \___  >  |__|     |______  /  \____/   |__|'
    print '                 |__|          \/                   \/'
    print ' '
    print ' '
    print ' '

def viper_install():
    if os.path.exists(conf.VIPER_DIRECTORY):
        print 'Viperbot is already installed.'
        print ' '

        reinstall = raw_input("Would you like to reinstall ViperBot? (y/N): ")
        if reinstall == 'y' or reinstall == 'Y':
            viper_reinstall()
        else:
            # exit script
            sys.exit(0)

    viper.build()

def viper_reinstall():
    os.rename(conf.VIPER_DIRECTORY, conf.HOME + '/viper_old')
    viper_install()


if __name__ == "__main__":
    main(sys.argv[1:])
