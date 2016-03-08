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
        self.editBotConfig(self.NETWORK, self.BOTNICK,
                  '%VIPERPATH%', VIPERPATH)

        print 'OWNER: ' + self.OWNER
        self.editBotConfig(self.NETWORK, self.BOTNICK,
                  '%OWNER%', self.OWNER)

        print 'NETWORK: ' + self.NETWORK
        self.editBotConfig(self.NETWORK, self.BOTNICK,
                  '%NETWORK%', self.NETWORK)

        print 'LISTENADDR: ' + self.LISTENADDR
        self.editBotConfig(self.NETWORK, self.BOTNICK,
                  '%LISTENADDR%', self.LISTENADDR)

        print 'NATIP: ' + self.NATIP
        self.editBotConfig(self.NETWORK, self.BOTNICK,
                  '%NATIP%', self.NATIP)

        print ' '
        print '***************************************************'
        print ' Done creating ' + self.BOTNICK + '.conf'
        print ' Location: '+INSTALLDIR+'/networks/'+self.NETWORK+'/'+self.BOTNICK+'.conf'
        print '***************************************************'
        print ' '

        os.chdir(INSTALLDIR)

    def editBotConfig(self, network, botnick, search, replace):
        INSTALLDIR = conf.VIPER_INSTALL_DIRECTORY
        network_path = INSTALLDIR + '/networks/' + network + '/'
        botnick_conf = botnick + '.conf'
        viperbot_conf = INSTALLDIR + '/configs/viperbot.conf'

        os.chdir(network_path)

        if not os.path.exists(network_path + botnick_conf):
            os.system('cp ' + viperbot_conf + ' ' + network_path)
            os.rename('viperbot.conf', botnick_conf)

        lines = self.findLinesInFile(botnick_conf, search)

        #Create temp file
        fh, abs_path = mkstemp()
        with open(abs_path, 'w') as new_file:
            with open(botnick_conf, 'r') as old_file:
                for num, line in enumerate(old_file, 1):
                    new_file.write(line)
                    if num in lines:
                        new_file.write(line.replace(search, replace))

        os.close(fh)

        #Remove original file
        os.remove(botnick_conf)

        #Rename new file
        os.rename(abs_path, botnick_conf)

    def findLinesInFile(self, filename, searchFor):
        arr = []

        with open(filename) as search:
            for num, line in enumerate(search, 1):
                line = line.rstrip()
                if searchFor in line:
                    if not line.startswith('#'):
                        arr.append(num)

        return arr