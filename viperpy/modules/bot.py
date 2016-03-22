import os
import signal
import subprocess
import time

from tools import helpers
from tools import inputs
from tools.termcolor import cprint, colored

import viper
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
class Bot:

    def __init__(self, botnick):
        self.HOMECHAN = '#viperbot'
        self.PASS = ''
        self.BOTNICK = botnick
        self.OWNER = ''
        self.EMAIL = ''
        self.NETWORK = ''
        self.LISTENADDR = ''
        self.NATIP = ''

        self.IP = ''
        self.PORT = '3033'
        self.ISV6 = False
        self.PREFERIPV6 = '0'
        self.SERVERS = ''

        self.__INSTALLDIR__ = viper._INSTALL_DIR

    def botnetTemplateVars(self):

        return {
            '{{%HOMECHAN%}}':self.HOMECHAN,
            '{{%PASS%}}':self.PASS,

            '{{%HUBNICK%}}':self.BOTNICK,
            '{{%HUBIP%}}':self.IP,
            '{{%HUBPORT%}}':self.PORT,

            '{{%ALTHUBNICK%}}':self.BOTNICK,
            '{{%ALTHUBIP%}}':self.IP,
            '{{%ALTHUBPORT%}}':self.PORT,
        }

    def botTemplateVars(self):
        VIPERPATH = self.__INSTALLDIR__ + '/viper'
        return {
            '{{%VIPERPATH%}}':VIPERPATH,
            '{{%NETWORK%}}':self.NETWORK,
            '{{%BOTNICK%}}':self.BOTNICK,
            '{{%OWNER%}}':self.OWNER,
            '{{%EMAIL%}}':self.EMAIL,
            '{{%VHOST4%}}':self.IP,
            '{{%VHOST6%}}':self.IP,
            '{{%PORT%}}':self.PORT,
            '{{%PREFERIPV6%}}':self.PREFERIPV6,
            '{{%NATIP%}}':self.NATIP,
            '{{%SERVERS%}}':self.SERVERS.replace(',','\n  '),
            '{{%LISTENADDR%}}':self.LISTENADDR
        }

    def new(self, network, botnick='', type='leaf'):
        cprint('new() [DEBUG] Type: ' + type, 'blue')

        INSTALLDIR = viper._INSTALL_DIR
        os.chdir(INSTALLDIR)

        if botnick == '':
            while True:
                botnick = inputs.alphaNumInput('Bot\'s Nick: ')
                botnick_conf = INSTALLDIR+'/'+network+'/'+botnick+'.conf'
                if os.path.exists(botnick_conf):
                    cprint('*** This botnick already exists!', 'red')
                    continue
                else:
                    break

        # Create a Bot Object
        self.BOTNICK = botnick

        self.NETWORK = network

        self.OWNER = inputs.alphaNumInput('Owner\'s Nick: ')
        self.EMAIL = inputs.emailInput('Owner\'s Email: ')

        v4v6 = inputs.yesNoInput('Is this bot using IPv6? (y/N): ')
        if v4v6 == 'y' or v4v6 == 'Y':
            preferipv6 = inputs.yesNoInput('Do you prefer IPv6 over IPv4? (y/N): ')
            self.ISV6 = True
            if preferipv6 == 'y' or preferipv6 == 'Y':
                self.PREFERIPV6 = True

        self.IP = inputs.ipInput('IP: ')

        self.PORT = inputs.portInput('Port: ')

        nat = inputs.yesNoInput('Is this bot behind a NAT? (y/N): ')
        if nat == 'y' or nat == 'Y':
            self.NATIP = inputs.ipInput('NAT IP: ')

        cprint('---------------------------------------------------------\n'
        ' Here you will list the servers that this bot will\n'
        ' attempt to connect to.\n'
        '\n'
        ' Syntax: server:port\n'
        ' Example: irc.freenode.net:6667,chat.us.freenode.net:6667\n'
        '\n'
        ' Note: Do Not use spaces!\n'
        '---------------------------------------------------------\n'
        '\n', 'magenta')

        servers = inputs.serversInput('Servers: ')
        self.SERVERS = servers

        self.create(type)

    def create(self, type):

        cprint('create() [DEBUG] Type: ' + type, 'blue')

        cprint('Creating ' + self.BOTNICK + '.conf ...', 'cyan')
        network_path = self.__INSTALLDIR__ + '/networks/' + self.NETWORK + '/'
        viperbot_conf = self.__INSTALLDIR__ + '/configs/viperbot.conf'
        botnet_conf = self.__INSTALLDIR__ + '/configs/botnet.conf'

        botnick_conf = self.BOTNICK + '.conf'
        netbotnet_conf = self.NETWORK + '-botnet.conf'

        os.chdir(network_path)

        os.system('cp ' + viperbot_conf + ' ' + network_path)
        os.rename('viperbot.conf', botnick_conf)

        # CREATE NETWORK-BOTNET.CONF
        if type == 'hub':
            if not os.path.exists(network_path+netbotnet_conf):
                os.system('cp ' + botnet_conf + ' ' + network_path)
                os.rename('botnet.conf', netbotnet_conf)

                cprint('\n'
                'This setting lets you choose the home channel that every bot in your\n'
                'botnet will idle. We call this the "home" channel.\n'
                'You will NOT be asked this question again for this network.\n'
                '\n', 'magenta')

                self.HOMECHAN = inputs.channelInput('Home Channel: ')

                cprint('\n'
                'This password is used when you "AUTH" to your botnet for the first time\n'
                'You will NOT be asked this question again for this network.\n'
                '\n', 'magenta')

                self.PASS = inputs.passwordInput('Password: ')


            f = open(netbotnet_conf)
            net_conf = f.read()
            f.close()

            netnew_conf = ''

            for line in net_conf.splitlines():
                for k, v in self.botnetTemplateVars().items():
                    if k in line and not 'ALTHUB' in line:
                        line = line.replace(k, v)

                netnew_conf += line + '\n'

            f = open(netbotnet_conf, "w")
            f.write(netnew_conf)
            f.close()


        if type == 'althub':

            f = open(netbotnet_conf)
            net_conf = f.read()
            f.close()

            netnew_conf = ''

            for line in net_conf.splitlines():
                for k, v in self.botnetTemplateVars().items():
                    if k in line and 'ALTHUB' in line:
                        line = line.replace(k, v)

                netnew_conf += line + '\n'

            f = open(netbotnet_conf, "w")
            f.write(netnew_conf)
            f.close()

        # CREATE BOTNICK.CONF
        f = open(botnick_conf)
        bot_conf = f.read()
        f.close()

        new_conf = ''

        for line in bot_conf.splitlines():
            for k, v in self.botTemplateVars().items():
                if k in line:
                    if '{{%VHOST4%}}' in line and not self.ISV6:
                        line = line.replace('#', '')
                    elif '{{%VHOST6%}}' in line and self.ISV6:
                        line = line.replace('#', '')

                line = line.replace(k, v)

            new_conf += line + '\n'

        f = open(botnick_conf, "w")
        f.write(new_conf)
        f.close()

        os.chmod(botnick_conf, 0744)

        cprint('\n'
        '***************************************************\n'
        ' Done creating ' + self.BOTNICK + '.conf\n'
        ' Location: '+network_path+self.BOTNICK+'.conf\n'
        '***************************************************\n'
        '\n', 'green')

        if not os.path.exists(self.BOTNICK + '.user'):
            os.system('touch ' + self.BOTNICK + '.user')
            os.chmod(self.BOTNICK + '.user', 0600)
            now = time.strftime("%c")
            helpers.appendToFile(self.BOTNICK + '.user',
                                 '#4v: eggdrop v1.8.0+tclconfig -- ' + self.BOTNICK +' -- written ' + now)


        os.chdir(self.__INSTALLDIR__)

    def start(self, mode=''):
        cprint('Starting ' + self.BOTNICK, 'cyan')
        os.system('./'+self.BOTNICK+'.conf ' + mode)

    def stop(self):
        p = subprocess.Popen(['ps', 'x'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            if self.BOTNICK + '.conf' in line:
                cprint('Stopping ' + self.BOTNICK, 'cyan')
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGTERM)
                return True

        return False

    def rehash(self):
        p = subprocess.Popen(['ps', 'x'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            if self.BOTNICK + '.conf' in line:
                cprint('Rehashing ' + self.BOTNICK, 'cyan')
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGHUP)
                return True

        return False