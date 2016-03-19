import os
import signal
import subprocess

from tools import cmd
from tools.termcolor import colored

import viper
from bot import Bot
from tools.helpers import *
from tools.inputs import *

class ViperBotCLI(cmd.Cmd):

    intro = colored('v' + viper._VERSION + ' (c) 2016 Poppabear @ Freenode Irc Network\n' \
        '____   ____ .__                             __________             __\n' \
        '\   \ /   / |__| ______     ____   _______  \______   \   ____   _/  |_\n' \
        ' \   Y   /  |  | \____ \  _/ __ \  \_  __ \  |    |  _/  /  _ \  \   __/\n' \
        '  \     /   |  | |  |_> > \  ___/   |  | \/  |    |   \ (  <_> )  |  |\n' \
        '   \___/    |__| |   __/   \___  >  |__|     |______  /  \____/   |__|\n' \
        '                 |__|          \/                   \/\n' \
        '\n' \
        '\n' \
        'Welcome to the ViperBot shell.  Type help or ? to list commands.\n', 'blue')

    prompt = colored('ViperBot > ', "cyan")

    cwd = os.getcwd()

    def emptyline(self):
        pass

    def do_list(self, l):
        path = viper._NETWORKS_DIR
        for line in os.listdir(path):
                if os.path.isdir(path + '/' + line):
                    print line

    def help_list(self):
        print '# list\n' \
              '#   Lists the available Networks.\n' \
              '#\n' \
              '# "ls" is an alias for "list"\n' \

    def do_network(self, network):
        '    Switch to the specified network: network <network_name>'
        if network == '':
            print '*** Missing arguments: "? network" for help'
        elif not os.path.exists(viper._NETWORKS_DIR + '/' + network):
            print '*** Can\'t find network "'+network+'"! Make sure you have typed it correctly.'
            print '*** Also See: "? list" , "? network"'
        else:
            network_path = viper._NETWORKS_DIR + '/' + network + '/'
            net = NetworkCLI(network, network_path)
            net.cmdloop()

    def help_network(self):
        print '# network\n' \
              '#   Switches the shell to the network prompt.\n' \
              '#\n' \
              '# "net" is an alias for "network"'

    def do_quit(self, line):
        '    Quits the shell: quit'
        exit()

    def help_quit(self):
        print '# quit\n' \
              '#   Quits the ViperBot Shell.'

    # Alias's
    do_ls = do_list
    do_cd = do_network
    help_ls = help_list
    help_cd = help_network
    do_net = do_network
    help_net = help_network


'''
    NETWORK CLI
'''
class NetworkCLI(cmd.Cmd):

    intro = colored('Welcome to the Network CLI! "help" to list available commands.', 'magenta')

    cwd = os.getcwd()
    botnick = ''
    bot_path = ''

    def __init__(self, network, network_path):
        cmd.Cmd.__init__(self)
        self.network = network
        self.network_path = network_path
        self.prompt = colored('Network [' + str(network).title() + ']' + ' > ', "yellow")

    def emptyline(self):
        pass

    def do_list(self, l):
        path = self.network_path
        for line in os.listdir(path):
            if '.conf' in line and not 'botnet.conf' in line:
                print line.replace('.conf','')

    def help_list(self):
        print 'Help List ...'

    def do_bot(self, botnick):
        '    Switch to the specified bot: bot <botnick>'
        if botnick == '':
            print '*** Missing argument: "? bot" for help'
        elif not os.path.exists(self.network_path + botnick + '.conf'):
            print '*** Can\'t find bot "'+botnick+'"! Make sure you have typed it correctly.'
            print '*** Also See: "? list" , "? bot"'
        else:
            botnick = botnick
            bot_path = self.network_path + botnick+'.conf'
            bot = BotCLI(botnick, bot_path)
            bot.cmdloop()

    def do_start(self, botnick):
        '    Starts the specified bot: start <botnick>'
        if botnick == '':
            print '*** Missing argument: "? start" for help'
        elif not os.path.exists(self.network_path + botnick + '.conf'):
                print '*** Bot doesn\'t exist for this network.'
                print '*** Also See: "? list"'
        else:
            os.chdir(self.network_path)
            print 'Starting ' + botnick + ' ...'
            subprocess.call(['./'+botnick+'.conf'])
            os.chdir(self.cwd)

    def do_stop(self, botnick):
        '    Stops the specified bot: stop <botnick>'
        if botnick == '':
            print '*** Missing argument: "? stop" for help'
        elif not os.path.exists(self.network_path + botnick + '.conf'):
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

    def do_exit(self, line):
        return True

    def help_exit(self):
        print '# exit\n' \
              '#   Exits the current prompt and returns you to the previous prompt.\n' \
              '#   See also "? quit"'

    def do_quit(self, line):
        exit()

    def help_quit(self):
        print '# quit\n' \
              '#   Quits the ViperBot Shell.'

    # Alias's
    do_ls = do_list
    do_bots = do_list
    do_cd = do_bot
    help_ls = help_list


'''
    BOT CLI
'''
class BotCLI(cmd.Cmd):

    def __init__(self, botnick, bot_path):
        cmd.Cmd.__init__(self)
        self.botnick = botnick
        self.bot_path = bot_path
        self.bot = Bot(botnick)
        self.prompt = colored('Bot [' + str(botnick) + ']' + ' > ', "magenta")

    def emptyline(self):
        pass

    def do_start(self, l):
        self.bot.start()

    def do_stop(self, l):
        self.bot.stop()

    def do_find(self, searchFor):
        dict = findLinesInConf(self.bot_path, searchFor)
        for k, v in dict.items():
            print '('+str(k)+')' + ' ' + v

    def do_exit(self, line):
        return True

    def do_edit(self, num):

        if editLineInConf(self.bot_path, num, raw_input(':') or getLineInConf(self.bot_path,num)):
            print 'Successful'
        else:
            print '*** .tmp file does not exist!'


    def help_exit(self):
        print '# exit\n' \
              '#   Exits the current prompt and returns you to the previous prompt.\n' \
              '#   See also "? quit"'

    def do_quit(self, line):
        exit()

    def help_quit(self):
        print '# quit\n' \
              '#   Quits the ViperBot Shell.'

    # Alias's
