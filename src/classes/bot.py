import os

from tempfile import mkstemp
from src import conf
from src.libs import helpers
from src.libs import inputs

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
        INSTALLDIR = conf.VIPER_INSTALL_DIRECTORY
        VIPERPATH = INSTALLDIR + '/viperbot'
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

    def create(self, type):

        print 'Creating ' + self.BOTNICK + '.conf ...'
        INSTALLDIR = conf.VIPER_INSTALL_DIRECTORY

        network_path = INSTALLDIR + '/networks/' + self.NETWORK + '/'
        viperbot_conf = INSTALLDIR + '/configs/viperbot.conf'
        botnet_conf = INSTALLDIR + '/configs/botnet.conf'

        botnick_conf = self.BOTNICK + '.conf'
        netbotnet_conf = self.NETWORK + '-botnet.conf'

        os.chdir(network_path)

        os.system('cp ' + viperbot_conf + ' ' + network_path)
        os.rename('viperbot.conf', botnick_conf)

        print '[DEBUG] Type: ' + type

        # CREATE NETWORK-BOTNET.CONF
        if type == 'hub':
            if not os.path.exists(network_path+netbotnet_conf):
                os.system('cp ' + botnet_conf + ' ' + network_path)
                os.rename('botnet.conf', netbotnet_conf)

                print ' '
                print '# This setting lets you choose the home channel that every bot in your'
                print '# botnet will idle. We call this the "home" channel.'
                print '# You will NOT be asked this question again for this network.'
                print ' '
                self.HOMECHAN = inputs.channelInput('Home Channel: ')

                print ' '
                print '# This password is used when you "AUTH" to your botnet for the first time'
                print '# You will NOT be asked this question again for this network.'
                print ' '
                self.PASS = inputs.passwordInput('Password: ')

            netnew_conf = ''

            f = open(netbotnet_conf)
            netnew_conf = f.read()
            f.close()

            for line in netnew_conf.splitlines():
                for k, v in self.botnetTemplateVars().items():
                    if k in line and not 'ALTHUB' in line:
                        line = line.replace(k, v)

                netnew_conf += line + '\n'

            f = open(netbotnet_conf, "w")
            f.write(netnew_conf)
            f.close()

        if type == 'althub':
            netnew_conf = ''

            f = open(netbotnet_conf)
            netnew_conf = f.read()
            f.close()

            for line in netnew_conf.splitlines():
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

        print ' '
        print '***************************************************'
        print ' Done creating ' + self.BOTNICK + '.conf'
        print ' Location: '+network_path+self.BOTNICK+'.conf'
        print '***************************************************'
        print ' '

        if type == 'hub':
            self.start(self.NETWORK, self.BOTNICK, '-m')
        else:
            self.start(self.NETWORK, self.BOTNICK)

        os.chdir(INSTALLDIR)

    def start(self, network, botnick, mode=''):
        INSTALLDIR = conf.VIPER_INSTALL_DIRECTORY
        network_path = INSTALLDIR + '/networks/' + network + '/'
        os.chdir(network_path)

        print 'Starting ' + botnick
        os.system('./'+botnick+'.conf ' + mode)

    def editBotConfig(self, network, botnick, search, replace, isCSV=False):
        INSTALLDIR = conf.VIPER_INSTALL_DIRECTORY
        network_path = INSTALLDIR + '/networks/' + network + '/'
        botnick_conf = botnick + '.conf'

        os.chdir(network_path)

    def findLinesInFile(self, filename, searchFor):
        arr = []

        with open(filename) as search:
            for num, line in enumerate(search, 1):
                line = line.rstrip()
                if searchFor in line:
                    if not line.startswith('#'):
                        arr.append(num)

        return arr