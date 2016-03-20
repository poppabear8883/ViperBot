import signal
import subprocess

import viper
from bot import Bot
from tools import cmd
from tools.helpers import *
from tools.termcolor import colored, cprint
import readline

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
        'Welcome to the ViperBot shell.  Type help or ? to list commands.\n', 'white')

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
        cprint('--------------------------------------\n'
               '  list\n'
               '--------------------------------------\n'
               '   Lists the available Networks.\n'
               '   "ls" is an alias for "list"\n'
               '--------------------------------------\n', 'green')

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
        cprint('--------------------------------------\n'
               '  network <network_name>\n'
               '--------------------------------------\n'
               '   Switches to the Network CLI\n'
               '   "cd" is an alias for "network"\n'
               '   Also See: "? list"\n'
               '--------------------------------------\n', 'green')

    def do_quit(self, line):
        exit()

    def help_quit(self):
        cprint('--------------------------------------\n'
               '  quit\n'
               '--------------------------------------\n'
               '   Quits the interactive Shell\n'
               '--------------------------------------\n', 'green')

    # Alias's
    do_ls = do_list
    do_cd = do_network
    help_ls = help_list
    help_cd = help_network

'''
    NETWORK CLI
'''
class NetworkCLI(cmd.Cmd):

    intro = colored('Welcome to the Network CLI! "help" to list available commands.', 'yellow')

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
            if '.conf' in line \
                    and not 'botnet.conf' in line\
                    and not '.bak' in line\
                    and not '~bak' in line:
                print line.replace('.conf','')

    def help_list(self):
        cprint('--------------------------------------\n'
               '  list\n'
               '--------------------------------------\n'
               '   Lists the available Bots.\n'
               '   "ls" and "bots" are aliases for "list"\n'
               '--------------------------------------\n', 'green')

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

    def help_bot(self):
        cprint('--------------------------------------\n'
               '  bot <bot>\n'
               '--------------------------------------\n'
               '   Switches to the Bot CLI\n'
               '   "cd" is an alias for "bot"\n'
               '   Also See: "? list"\n'
               '--------------------------------------\n', 'green')

    def do_start(self, botnick):
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

    def help_start(self):
        cprint('--------------------------------------\n'
               '  start <bot>\n'
               '--------------------------------------\n'
               '   Starts the specified bot.\n'
               '   Also See: "? list"\n'
               '--------------------------------------\n', 'green')

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

    def help_stop(self):
        cprint('--------------------------------------\n'
               '  stop <bot>\n'
               '--------------------------------------\n'
               '   Stops the specified bot.\n'
               '   Also See: "? list"\n'
               '--------------------------------------\n', 'green')

    def do_exit(self, line):
        return True

    def help_exit(self):
        cprint('--------------------------------------\n'
               '  exit\n'
               '--------------------------------------\n'
               '   Exits the current CLI.\n'
               '   Also See: "? quit"\n'
               '--------------------------------------\n', 'green')

    def do_quit(self, line):
        exit()

    def help_quit(self):
        cprint('--------------------------------------\n'
               '  quit\n'
               '--------------------------------------\n'
               '   Quits the interactive Shell\n'
               '--------------------------------------\n', 'green')

    # Alias's
    do_ls = do_list
    do_bots = do_list
    do_cd = do_bot
    help_ls = help_list
    help_bots = help_list
    help_cd = help_bot


'''
    BOT CLI
'''
class BotCLI(cmd.Cmd):

    intro = colored('Welcome to the Bot CLI! "help" to list available commands.', 'magenta')

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

    def do_rehash(self, l):
        self.bot.rehash()

    def do_find(self, searchFor):
        dict = findLinesInConf(self.bot_path, searchFor)
        for k, v in dict.items():
            print '('+str(k)+')' + ' ' + v

    def do_exit(self, line):
        return True

    def do_edit(self, num):
        readline.set_pre_input_hook(lambda: readline.insert_text(getLineInConf(self.bot_path,num))
                                            or readline.redisplay())

        if editLineInConf(self.bot_path, num, raw_input(':') or getLineInConf(self.bot_path,num)):
            print 'Successful'
        else:
            print '*** .tmp file does not exist!'

        readline.set_pre_input_hook()

    def help_exit(self):
        print '# exit\n' \
              '#   Exits the current prompt and returns you to the previous prompt.\n' \
              '#   See also "? quit"'

    def do_quit(self, line):
        exit()

    def help_quit(self):
        cprint('--------------------------------------\n'
               '  quit\n'
               '--------------------------------------\n'
               '   Quits the interactive Shell\n'
               '--------------------------------------\n', 'green')

    # Alias's