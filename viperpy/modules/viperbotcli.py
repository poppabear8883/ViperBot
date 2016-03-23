import signal
import subprocess

import viper
from bot import Bot
from tools import cmd
from tools.helpers import *
from tools.termcolor import colored, cprint
import readline
'''
    'grey', # debug, might not work
    'red', # errors
    'green', # success
    'yellow', # warnings
    'blue', # misc, debug
    'magenta', # important notices
    'cyan', # notices
    'white', # default
'''
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
               '--------------------------------------\n', 'cyan')

    def do_network(self, network):
        if network == '':
            cprint('*** Missing arguments: "? network" for help', 'red')
        elif not os.path.exists(viper._NETWORKS_DIR + '/' + network):
            cprint('*** Can\'t find network "'+network+'"! Make sure you have typed it correctly.', 'red')
            cprint('*** Also See: "? list" , "? network"', 'red')
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
               '--------------------------------------\n', 'cyan')

    def do_quit(self, line):
        exit()

    def help_quit(self):
        cprint('--------------------------------------\n'
               '  quit\n'
               '--------------------------------------\n'
               '   Quits the interactive Shell\n'
               '--------------------------------------\n', 'cyan')

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
        os.chdir(network_path)
        self.prompt = colored('Network [' + str(network).title() + ']' + ' > ', "yellow")

    def emptyline(self):
        pass

    def do_list(self, l):
        path = self.network_path
        for line in os.listdir(path):
            if '.conf' in line \
                    and not 'botnet.conf' in line \
                    and not '.bak' in line \
                    and not '~bak' in line:
                cprint(line.replace('.conf',''), 'cyan')

    def help_list(self):
        cprint('--------------------------------------\n'
               '  list\n'
               '--------------------------------------\n'
               '   Lists the available Bots.\n'
               '   "ls" and "bots" are aliases for "list"\n'
               '--------------------------------------\n', 'cyan')

    def do_new(self, botnick):
        if botnick == '':
            bot_o = viper.newBot(self.network, '', 'leaf')
        else:
            bot_o = viper.newBot(self.network, botnick, 'leaf')

        os.chdir(self.network_path)
        bot_o.start()
        os.chdir(viper._INSTALL_DIR)

        cprint('\n'
               'Leafs must be added to the botnet\n'
               'in order for them to link properly.\n'
               '\n'
               'This can be done either by telnet, or\n'
               'DCC/CTCP chatting the "Hub" bot.\n'
               'Partyline command: .addleaf <botnick> <ip> <port>\n'
               '\n', 'magenta')

        cprint('Please Note:\n'
               'After the leaf bot is added to the botnet,\n'
               'it MAY restart!\n'
               'This is normal!', 'red')

    def help_new(self):
        cprint('--------------------------------------\n'
               '  new [botnick]\n'
               '--------------------------------------\n'
               '   Creates a new leaf bot.\n'
               '   [botnick] is optional, not specifing\n'
               '   not specifing [botnick] will simply\n'
               '   ask for botnick when ran.\n'
               '   Also See: "? list"\n'
               '--------------------------------------\n', 'cyan')


    def do_bot(self, botnick):
        '    Switch to the specified bot: bot <botnick>'
        if botnick == '':
            cprint('*** Missing argument: "? bot" for help', 'red')
        elif not os.path.exists(self.network_path + botnick + '.conf'):
            cprint('*** Can\'t find bot "'+botnick+'"! Make sure you have typed it correctly.', 'red')
            cprint('*** Also See: "? list" , "? bot"', 'red')
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
               '--------------------------------------\n', 'cyan')

    def do_start(self, botnick):
        if botnick == '':
            cprint('*** Missing argument: "? start" for help', 'red')
        elif not os.path.exists(self.network_path + botnick + '.conf'):
                cprint('*** Bot doesn\'t exist for this network.', 'red')
                cprint('*** Also See: "? list"', 'red')
        else:
            cprint('Starting ' + botnick + ' ...', 'cyan')
            subprocess.call(['./'+botnick+'.conf'])

    def help_start(self):
        cprint('--------------------------------------\n'
               '  start <bot>\n'
               '--------------------------------------\n'
               '   Starts the specified bot.\n'
               '   Also See: "? list"\n'
               '--------------------------------------\n', 'cyan')

    def do_stop(self, botnick):
        if botnick == '':
            cprint('*** Missing argument: "? stop" for help', 'red')
        elif not botnick == 'all' and not os.path.exists(self.network_path + botnick + '.conf'):
            cprint('*** Bot doesn\'t exist for this network.', 'red')
            cprint('*** Also See: "? list"', 'red')
        else:
            p = subprocess.Popen(['ps', 'x'], stdout=subprocess.PIPE)
            out, err = p.communicate()
            for line in out.splitlines():
                if botnick == 'all':
                    if '/viperbot/viper' in line:
                        pid = int(line.split(None, 1)[0])
                        os.kill(pid, signal.SIGTERM)
                elif botnick+'.conf' in line:
                        cprint('Stopping ' + botnick + ' ...', 'cyan')
                        pid = int(line.split(None, 1)[0])
                        os.kill(pid, signal.SIGTERM)

    def help_stop(self):
        cprint('--------------------------------------\n'
               '  stop <bot>\n'
               '--------------------------------------\n'
               '   Stops the specified bot.\n'
               '   Specifying "all" will stop all bots.'
               '   "kill" is an alias for "stop"\n'
               '   Also See: "? list"\n'
               '--------------------------------------\n', 'cyan')

    def do_exit(self, line):
        os.chdir('../')
        return True

    def help_exit(self):
        cprint('--------------------------------------\n'
               '  exit\n'
               '--------------------------------------\n'
               '   Exits the current CLI.\n'
               '   Also See: "? quit"\n'
               '--------------------------------------\n', 'cyan')

    def do_quit(self, line):
        exit()

    def help_quit(self):
        cprint('--------------------------------------\n'
               '  quit\n'
               '--------------------------------------\n'
               '   Quits the interactive Shell\n'
               '--------------------------------------\n', 'cyan')

    # Alias's
    do_ls = do_list
    do_bots = do_list
    do_cd = do_bot
    do_kill = do_stop
    help_ls = help_list
    help_bots = help_list
    help_cd = help_bot
    help_kill = help_stop


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

    def do_start(self, mode=''):
        if not mode == '':
            self.bot.start(mode)
        else:
            self.bot.start()

    def help_start(self):
        cprint('--------------------------------------\n'
               '  start [mode]\n'
               '--------------------------------------\n'
               '   Starts the current bot.\n'
               '   Available [Optional] modes:\n'
               '     -n\n'
               '        Don\'t background.\n'
               '     -nt\n'
               '        Don\'t background, use terminal.\n'
               '     -nc\n'
               '        Don\'t background, show channel info.\n'
               '     -h\n'
               '        Show help\n'
               '     -v\n'
               '        Show version info, then quit.\n'
               '--------------------------------------\n', 'cyan')

    def do_stop(self, l):
        self.bot.stop()

    def help_stop(self):
        cprint('--------------------------------------\n'
               '  stop\n'
               '--------------------------------------\n'
               '   Stops the current bot.\n'
               '--------------------------------------\n', 'cyan')

    def do_rehash(self, l):
        self.bot.rehash()

    def help_rehash(self):
        cprint('--------------------------------------\n'
               '  rehash\n'
               '--------------------------------------\n'
               '   Rehashes the current bot.\n'
               '   Note: run this command after editing\n'
               '   configuration settings.\n'
               '\n'
               '   Changes using "edit" will NOT take\n'
               '   effect until you "rehash" or "restart"\n'
               '\n'
               '   See Also "? edit" , "? find"\n'
               '--------------------------------------\n', 'cyan')

    def do_find(self, searchFor):
        dict = findLinesInConf(self.bot_path, searchFor)
        for k, v in dict.items():
            print '('+colored(str(k), 'magenta')+')' + ' ' + colored(v, 'cyan')

    def help_find(self):
        cprint('--------------------------------------\n'
               '  find <word or phrase>\n'
               '--------------------------------------\n'
               '   Searches the bots configuration file\n'
               '   for the specified word or phrase.\n'
               '     The results will show the line number\n'
               '   and the line contents.\n'
               '\n'
               '   Example:\n'
               '     Bot [ViperAltHub] > find username\n'
                     '(31) set username "ViperAltHub"\n'
               '\n'
               '   See Also "? edit"\n'
               '--------------------------------------\n', 'cyan')

    def do_edit(self, num):
        readline.set_pre_input_hook(lambda: readline.insert_text(getLineInConf(self.bot_path,num))
                                            or readline.redisplay())

        if editLineInConf(self.bot_path, num, raw_input(':') or getLineInConf(self.bot_path,num)):
            cprint('Success ...', 'green')
        else:
            cprint('*** .tmp file does not exist!', 'red')

        readline.set_pre_input_hook()

    def help_edit(self):
        cprint('--------------------------------------\n'
               '  edit <line number>\n'
               '--------------------------------------\n'
               '   Edits the bots configuration file\n'
               '   at the specified line number.\n'
               '\n'
               '   Example:\n'
               '     Bot [ViperAltHub] > edit 31\n'
                     ':set username "myNewNick"\n'
               '\n'
               '   See Also "? find", "? rehash"\n'
               '--------------------------------------\n', 'cyan')

    def do_exit(self, line):
        return True

    def help_exit(self):
        cprint('--------------------------------------\n'
               '  exit\n'
               '--------------------------------------\n'
               '   Exits the current CLI.\n'
               '   Also See: "? quit"\n'
               '--------------------------------------\n', 'cyan')

    def do_quit(self, line):
        exit()

    def help_quit(self):
        cprint('--------------------------------------\n'
               '  quit\n'
               '--------------------------------------\n'
               '   Quits the interactive Shell\n'
               '--------------------------------------\n', 'cyan')

    # Alias's