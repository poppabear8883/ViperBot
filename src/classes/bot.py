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

        network_path = INSTALLDIR + '/networks/' + self.NETWORK + '/'
        botnick_conf = network_path + self.BOTNICK + '.conf'
        viperbot_conf = INSTALLDIR + '/configs/viperbot.conf'

        print 'VIPERPATH: ' + VIPERPATH
        helpers.replaceInFile(viperbot_conf, botnick_conf,
                  '%VIPERPATH%', VIPERPATH)

        print 'OWNER: ' + self.OWNER
        helpers.replaceInFile(viperbot_conf, botnick_conf,
                  '%OWNER%', self.OWNER)

        print 'EMAIL: ' + self.EMAIL
        helpers.replaceInFile(viperbot_conf, botnick_conf,
                  '%EMAIL%', self.EMAIL)

        print 'NETWORK: ' + self.NETWORK
        helpers.replaceInFile(viperbot_conf, botnick_conf,
                  '%NETWORK%', self.NETWORK)

        print 'LISTENADDR: ' + self.LISTENADDR
        helpers.replaceInFile(viperbot_conf, botnick_conf,
                  '%LISTENADDR%', self.LISTENADDR)

        print 'NATIP: ' + self.NATIP
        helpers.replaceInFile(viperbot_conf, botnick_conf,
                  '%NATIP%', self.NATIP)

        print ' '
        print '***************************************************'
        print ' Done creating ' + self.BOTNICK + '.conf'
        print ' Location: ' + botnick_conf
        print '***************************************************'
        print ' '