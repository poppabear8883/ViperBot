#!/usr/bin/python
"""

viperbot.py (c) 2016 Poppabear @ Freenode Irc Network

"""
import getopt
import sys
import conf
import viper
from classes.bot import Bot

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
        elif opt == '-a':
            viperNewBot(arg)
        elif opt == '-u':
            viperUpdate(arg)
        elif opt == '-s':
            viperStart(arg)
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
    print '-a [network]'
    print '  Creates a new bot'
    print '-u <filename>'
    print '  Updates a file from the remote repository'
    print '-s <botnick>'
    print '  Starts a bot. <botnick> is Case Sensitive'

def viperNewNetwork():
    print ' '

def viperNewBot(network):
    print 'Creating bot for network: ' + network + ' ...'

def viperUpdate(file):
    print 'Updating ' + file

def viperStart(botnick):
    print 'Starting ' + botnick
    sbot = Bot(botnick)
    sbot.start()


if __name__ == "__main__":
    main(sys.argv[1:])
