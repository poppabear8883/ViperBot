import os
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
        self.PORT = 3333
        self.ISV6 = False
        self.PREFERIPV6 = False
        self.LANGUAGE = 'english'
        self.SERVERS = []

    def create(self, type = 'leaf'):
        print 'Creating ' + self.BOTNICK + '.conf ...'
        INSTALLDIR = conf.VIPER_INSTALL_DIRECTORY
        VIPERPATH = INSTALLDIR + '/viper'

        print 'VIPERPATH: ' + VIPERPATH
        helpers.editBotConfig(self.NETWORK, self.BOTNICK,
                  '%VIPERPATH%', VIPERPATH)

        print 'OWNER: ' + self.OWNER
        helpers.editBotConfig(self.NETWORK, self.BOTNICK,
                  '%OWNER%', self.OWNER)

        print 'EMAIL: ' + self.EMAIL
        helpers.editBotConfig(self.NETWORK, self.BOTNICK,
                  '%EMAIL%', self.EMAIL)

        print 'NETWORK: ' + self.NETWORK
        helpers.editBotConfig(self.NETWORK, self.BOTNICK,
                  '%NETWORK%', self.NETWORK)

        print 'LISTENADDR: ' + self.LISTENADDR
        helpers.editBotConfig(self.NETWORK, self.BOTNICK,
                  '%LISTENADDR%', self.LISTENADDR)

        print 'NATIP: ' + self.NATIP
        helpers.editBotConfig(self.NETWORK, self.BOTNICK,
                  '%NATIP%', self.NATIP)

        print ' '
        print '***************************************************'
        print ' Done creating ' + self.BOTNICK + '.conf'
        print ' Location: '+INSTALLDIR+'/networks/'+self.NETWORK+'/'+self.BOTNICK+'.conf'
        print '***************************************************'
        print ' '

        os.chdir(INSTALLDIR)