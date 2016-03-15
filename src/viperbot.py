#!/usr/bin/python
"""

viperbot.py (c) 2016 Poppabear @ Freenode Irc Network

"""
from libs import cmd
from classes.bot import Bot
import conf, sys, os, viper

class ViperBot(cmd.Cmd):

    intro = 'v'+conf.VIPER_VERSION + ' (c) 2016 Poppabear @ Freenode Irc Network\n' \
        '____   ____ .__                             __________             __\n' \
        '\   \ /   / |__| ______     ____   _______  \______   \   ____   _/  |_\n' \
        ' \   Y   /  |  | \____ \  _/ __ \  \_  __ \  |    |  _/  /  _ \  \   __/\n' \
        '  \     /   |  | |  |_> > \  ___/   |  | \/  |    |   \ (  <_> )  |  |\n' \
        '   \___/    |__| |   __/   \___  >  |__|     |______  /  \____/   |__|\n' \
        '                 |__|          \/                   \/\n' \
        '\n' \
        '\n' \
        'Welcome to the ViperBot shell.  Type help or ? to list commands.\n'

    prompt = 'ViperBot > '

    network = ''
    network_path = ''

    bot = ''
    bot_path = ''

    def do_network(self, network):
        '    Switch to the specified network: network <network_name>'
        if network == '':
            print 'Missing argument: network <network_name>'
        elif not os.path.exists(conf.VIPER_NETWORKS_DIRECTORY + '/' + network):
            print 'Error: can\'t find network "'+network+'"! Make sure you have typed it correctly.'
        else:
            self.network = network
            self.network_path = conf.VIPER_NETWORKS_DIRECTORY+'/'+network+'/'

            print 'Switching to the network prompt ...'
            print ' '

            self.prompt = 'Network ['+str(network).title()+']' + ' > '

    def do_bot(self, botnick):
        '    Switch to the specified bot: bot <botnick>'
        if self.network == '':
            print 'You must be in the network prompt to use this command: use <network>'
        elif botnick == '':
            print 'Missing argument: bot <botnick>'
        elif not os.path.exists(self.network_path + botnick + '.conf'):
            print 'Error: can\'t find bot "'+botnick+'"! Make sure you have typed it correctly.'
        else:
            self.bot = botnick
            self.bot_path = self.network_path + botnick+'.conf'
            print 'Switching to the bot prompt ...'
            print ' '
            self.prompt = 'Bot ['+str(botnick)+']' + ' > '

    def do_start(self, botnick):
        '    Starts the specified bot: start <botnick>'
        if self.network == '':
            print 'You must be in the network prompt to use this command!'
            print 'type: ? network'
        elif botnick == '' and self.bot == '':
            print 'Missing argument: start <botnick>'
        elif self.bot == '':
            print 'Starting ' + botnick + ' ...'
        else:
            print 'Starting ' + self.bot + ' ...'

    def do_quit(self, line):
        '    Quits the shell: quit'
        exit()

    def do_exit(self, line):
        '    Exits the prompt: exit'
        if self.network == '':
            print 'You are at the root prompt. If you want to quit the shell type: quit'
        elif not self.network == '' and not self.bot == '':
            self.bot = ''
            self.prompt = 'Network ['+str(self.network).title()+']' + ' > '
        elif not self.network == '' and self.bot == '':
            self.network = ''
            self.prompt = 'ViperBot > '

    # shortcuts
    do_net = do_network


if __name__ == '__main__':
    ViperBot().cmdloop()