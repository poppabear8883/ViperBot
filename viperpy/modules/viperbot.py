import os
import signal
import subprocess

from network import Network
from tools import cmd
from tools.termcolor import colored

import conf


class ViperBot(cmd.Cmd):

    intro = colored('v' + conf.VIPER_VERSION + ' (c) 2016 Poppabear @ Freenode Irc Network\n' \
        '____   ____ .__                             __________             __\n' \
        '\   \ /   / |__| ______     ____   _______  \______   \   ____   _/  |_\n' \
        ' \   Y   /  |  | \____ \  _/ __ \  \_  __ \  |    |  _/  /  _ \  \   __/\n' \
        '  \     /   |  | |  |_> > \  ___/   |  | \/  |    |   \ (  <_> )  |  |\n' \
        '   \___/    |__| |   __/   \___  >  |__|     |______  /  \____/   |__|\n' \
        '                 |__|          \/                   \/\n' \
        '\n' \
        '\n' \
        'Welcome to the ViperBot shell.  Type help or ? to list commands.\n', 'magenta')

    prompt = colored('ViperBot > ', "cyan")

    working_path = os.getcwd()
    network = ''
    network_path = ''

    botnick = ''
    bot_path = ''

    def emptyline(self):
        pass

    def do_list(self, type):

        if type == '':
            print '*** Missing argument: "? list" for help'
        elif type == 'nets' or type == 'networks':
            path = conf.VIPER_NETWORKS_DIRECTORY
            for line in os.listdir(path):
                    if os.path.isdir(path + '/' + line):
                        print line
        elif type == 'bots':
            if self.network == '':
                print '*** Must be in the Network prompt. "? network" for help'
            else:
                path = self.network_path
                for line in os.listdir(path):
                    if '.conf' in line and not 'botnet.conf' in line:
                        print line.replace('.conf','')

    def help_list(self):
        print '# list <argument>\n' \
              '#   Available arguments: networks, nets, bots\n' \
              '#      networks: Lists the available Networks.\n' \
              '#      nets: An alias for networks\n' \
              '#      bots: Lists the available Bots "from the network prompt"\n' \
              '# "ls" is an alias for "list"\n' \

    def help_ls(self):
        print '# "ls" is an alias for "list"\n' \
              '# ? list'

    def do_snet(self, network):
        '    Switch to the specified network: network <network_name>'
        if network == '':
            print '*** Missing arguments: "? network" for help'
        elif not os.path.exists(conf.VIPER_NETWORKS_DIRECTORY + '/' + network):
            print '*** Can\'t find network "'+network+'"! Make sure you have typed it correctly.'
            print '*** Also See: "? list" , "? network"'
        else:
            self.network = network
            self.network_path = conf.VIPER_NETWORKS_DIRECTORY + '/' + network + '/'

            print 'Switching to the network prompt ...'
            print ' '
            net = Network(network, self.network_path)
            net.cmdloop()

    def do_network(self, network):
        '    Switch to the specified network: network <network_name>'
        if network == '':
            print '*** Missing arguments: "? network" for help'
        elif not os.path.exists(conf.VIPER_NETWORKS_DIRECTORY + '/' + network):
            print '*** Can\'t find network "'+network+'"! Make sure you have typed it correctly.'
            print '*** Also See: "? list" , "? network"'
        else:
            self.network = network
            self.network_path = conf.VIPER_NETWORKS_DIRECTORY + '/' + network + '/'

            print 'Switching to the network prompt ...'
            print ' '

            self.prompt = colored('Network [' + str(network).title() + ']' + ' > ', "yellow")

    def help_network(self):
        print '# network\n' \
              '#   Switches the shell to the network prompt.\n' \
              '#   The network must exist in the "viperbot/networks" directory\n' \
              '# "net" or "nw" are alias\'s for "network"\n' \
              '\n' \
              '# Available network commands:'

    def help_net(self):
        print '# "net" is an alias for "network"\n' \
              '# ? network'

    def help_nw(self):
        print '# "nw" is an alias for "network"\n' \
              '# ? network'

    def do_bot(self, botnick):
        '    Switch to the specified bot: bot <botnick>'
        if self.network == '':
            print '*** Must be in the network prompt to use this command: "? network" for help'
        elif botnick == '':
            print '*** Missing argument: "? bot" for help'
        elif not os.path.exists(self.network_path + botnick + '.conf'):
            print '*** Can\'t find bot "'+botnick+'"! Make sure you have typed it correctly.'
            print '*** Also See: "? list" , "? bot"'
        else:
            self.botnick = botnick
            self.bot_path = self.network_path + botnick+'.conf'
            print 'Switching to the bot prompt ...'
            print ' '
            self.prompt = colored('Bot [' + str(botnick) + ']' + ' > ', "magenta")

    def do_start(self, botnick):
        '    Starts the specified bot: start <botnick>'
        if self.network == '':
            print '*** Must be in the network prompt to use this command: "? network" for help'
        elif botnick == '' and self.botnick == '':
            print '*** Missing argument: "? start" for help'
        elif self.botnick == '':
            if not os.path.exists(self.network_path + botnick + '.conf'):
                print '*** Bot doesn\'t exist for this network.'
                print '*** Also See: "? list"'
            else:
                os.chdir(self.network_path)
                print 'Starting ' + botnick + ' ...'
                subprocess.call(['./'+botnick+'.conf'])
                #os.system('./'+botnick+'.conf')
                os.chdir(self.working_path)
        else:
            if not os.path.exists(self.network_path + self.botnick + '.conf'):
                print '*** Bot doesn\'t exist for this network.'
                print '*** Also See: "? list"'
            else:
                os.chdir(self.network_path)
                print 'Starting ' + self.botnick + ' ...'
                subprocess.call(['./'+self.botnick+'.conf'])
                #os.system('./'+self.botnick+'.conf')
                os.chdir(self.working_path)


    def do_stop(self, botnick):
        '    Stops the specified bot: stop <botnick>'
        if self.network == '':
            print '*** Must be in the network prompt to use this command: "? network" for help'
        elif botnick == '' and self.botnick == '':
            print '*** Missing argument: "? stop" for help'
        elif self.botnick == '':
            if not os.path.exists(self.network_path + botnick + '.conf'):
                print '*** Bot doesn\'t exist for this network.'
                print '*** Also See: "? list"'
            else:
                p = subprocess.Popen(['ps', 'x'], stdout=subprocess.PIPE)
                out, err = p.communicate()
                for line in out.splitlines():
                    if botnick+'.conf' in line:
                        print 'Stopping ' + botnick + ' ...'
                        pid = int(line.split(None, 1)[0])
                        os.kill(pid, signal.SIGTERM)

        else:
            if not os.path.exists(self.network_path + self.botnick + '.conf'):
                print '*** Bot doesn\'t exist for this network.'
                print '*** Also See: "? list"'
            else:
                p = subprocess.Popen(['ps', 'x'], stdout=subprocess.PIPE)
                out, err = p.communicate()
                for line in out.splitlines():
                    if self.botnick+ '.conf' in line:
                        print 'Stopping ' + self.botnick + ' ...'
                        pid = int(line.split(None, 1)[0])
                        os.kill(pid, signal.SIGTERM)

    def do_quit(self, line):
        '    Quits the shell: quit'
        exit()

    def help_quit(self):
        print '# quit\n' \
              '#   Quits the ViperBot Shell.\n' \
              '#   "q" is an alias for "quit"'

    def help_q(self):
        print '# "q" is an alias for "quit"\n' \
              '# ? quit'

    def do_exit(self, line):
        '    Exits the prompt: exit'
        if self.network == '':
            print '*** You are at the root prompt: "? exit" for help'
        elif not self.network == '' and not self.botnick == '':
            self.botnick = ''
            self.prompt = colored('Network [' + str(self.network).title() + ']' + ' > ', "yellow")
        elif not self.network == '' and self.botnick == '':
            self.network = ''
            self.prompt = colored('ViperBot > ', "cyan")

    def help_exit(self):
        print '# exit\n' \
              '#   Exits the current prompt and returns you to the previous prompt.\n' \
              '#   See also "? quit"'


    def switchPrompt(self, p):
        if p == 'net':
            self.prompt = colored('Network [' + str(self.network).title() + ']' + ' > ', "yellow")
        elif p == 'bot':
            self.prompt = colored('Bot [' + str(self.botnick) + ']' + ' > ', "magenta")


    # Alias's
    do_ls = do_list
    do_net = do_network
    do_nw = do_network
    do_q = do_quit