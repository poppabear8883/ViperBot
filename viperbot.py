#!/usr/bin/python
"""
viperbot.py by Poppabear
"""
import os
HOME = os.getenv("HOME")

viper_ver = 'v1.0'
viper_dir = HOME + "/viper"
viper_tmp = HOME + '/viper_tmp'
viper_url = 'https://github.com/poppabear8883/ViperBot/raw/master/'
viper_eggurl = 'ftp://ftp.eggheads.org/pub/eggdrop/source/snapshot/'
viper_egg = 'eggdrop1.8-snapshot.tar.gz'
viper_botnetconf = viper_dir + '/botnet.conf'

def main():
        banner()


def banner():
        print ' '
        print '%s (c) 2016 Poppabear @ Freenode Irc Network' % viper_ver
        print '____   ____ .__                             __________             __'
        print '\   \ /   / |__| ______     ____   _______  \______   \   ____   _/  |_'
        print ' \   Y   /  |  | \____ \  _/ __ \  \_  __ \  |    |  _/  /  _ \  \   __/'
        print '  \     /   |  | |  |_> > \  ___/   |  | \/  |    |   \ (  <_> )  |  |'
        print '   \___/    |__| |   __/   \___  >  |__|     |______  /  \____/   |__|'
        print '                 |__|          \/                   \/'



if __name__ == "__main__":
  main()
