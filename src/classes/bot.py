from src import conf
from src.libs import helpers

class Bot:

    def __init__(self):
        self.BOTNICK = ''
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

    def create(self):
        INSTALLDIR = conf.VIPER_INSTALL_DIRECTORY
        VIPERPATH = INSTALLDIR + '/viper'

        network_path = INSTALLDIR + '/networks/' + self.NETWORK + '/'
        botnick_conf = network_path + self.BOTNICK + '.conf'
        viperbot_conf = INSTALLDIR + '/configs/viperbot.conf'

        helpers.replaceInFile(viperbot_conf, botnick_conf,
                  '%VIPERPATH%', VIPERPATH)

        # helpers.replaceInFile('configs/viperbot.conf', net_path+botnick+'.conf',
        #               '%NETWORK%', self.NETWORK)
        #
        # helpers.replaceInFile('configs/viperbot.conf', net_path+botnick+'.conf',
        #               '%BOTNICK%', botnick)
        #
        # helpers.replaceInFile('configs/viperbot.conf', net_path+botnick+'.conf',
        #               '%OWNER%', owner)
        #
        # helpers.replaceInFile('configs/viperbot.conf', net_path+botnick+'.conf',
        #               '%EMAIL%', email)