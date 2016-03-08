import os

from tempfile import mkstemp
from src import conf
from src.libs import helpers

class Bot:

    def __init__(self, botnick):
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

    def confTemplateVars(self):
        INSTALLDIR = conf.VIPER_INSTALL_DIRECTORY
        VIPERPATH = INSTALLDIR + '/viper'
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

    def create(self, type = 'leaf'):

        print 'Creating ' + self.BOTNICK + '.conf ...'
        INSTALLDIR = conf.VIPER_INSTALL_DIRECTORY

        network_path = INSTALLDIR + '/networks/' + self.NETWORK + '/'
        botnick_conf = self.BOTNICK + '.conf'
        viperbot_conf = INSTALLDIR + '/configs/viperbot.conf'

        os.chdir(network_path)

        os.system('cp ' + viperbot_conf + ' ' + network_path)
        os.rename('viperbot.conf', botnick_conf)

        f = open(botnick_conf)
        text = f.read()
        f.close()

        for k, v in self.confTemplateVars().items():
            text = text.replace(k, v)

        f = open(botnick_conf, "w")
        f.write(text)
        f.close()

        print ' '
        print '***************************************************'
        print ' Done creating ' + self.BOTNICK + '.conf'
        print ' Location: '+INSTALLDIR+'/networks/'+self.NETWORK+'/'+self.BOTNICK+'.conf'
        print '***************************************************'
        print ' '

        os.chdir(INSTALLDIR)

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