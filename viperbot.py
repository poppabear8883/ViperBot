#!/usr/bin/python
"""

viperbot.py (c) 2016 Poppabear @ Freenode Irc Network

"""
import getopt
import os
import sys

from src import viper
from src import conf


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


def viper_new(type='leaf'):
    print 'Creating new ' + type + ' ...'


def viper_update(file):
    print 'Updating ' + file

def viper_start(botnick):
    print 'Starting ' + botnick


if __name__ == "__main__":
    main(sys.argv[1:])
