import urllib2
import tarfile
import os

from src import conf

def internet_on():
    try:
        response=urllib2.urlopen('http://173.194.206.102',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def appendToFile(filename, text):
    with open(filename, "a") as myfile:
        myfile.write(text + '\n')

def editBotConfig(network, botnick, search, replace):
    '''
    CURRENTLY THIS IS BROKEN AS F*CK!!
    I AM GOING ABOUT THIS FUNCTION ALL WRONG!

    :param network:
    :param botnick:
    :param search:
    :param replace:
    :return:
    '''
    INSTALLDIR = conf.VIPER_INSTALL_DIRECTORY
    network_path = INSTALLDIR + '/networks/' + network + '/'
    botnick_conf = botnick + '.conf'
    viperbot_conf = INSTALLDIR + '/configs/viperbot.conf'

    os.chdir(network_path)
    tmp = 'tmp.conf'

    if not os.path.exists(botnick_conf):
        f = open(viperbot_conf,'r')
        filedata = f.read()
        f.close()
    else:
        f = open(botnick_conf,'r')
        filedata = f.read()
        f.close()

    newdata = filedata.replace(search, replace)

    f = open(tmp, 'w')
    f.write(newdata)
    f.close()

    if os.path.exists(tmp):
        if os.path.exists(botnick_conf):
            os.rename(botnick_conf, botnick_conf+'.old')
        os.rename(tmp, botnick_conf)
    else:
        print 'Fatal Error: Temp File was not written'
        exit()

def download(url, filename):
    u = urllib2.urlopen(url)
    f = open(filename, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (filename, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print status,

    f.close()
    print ' '

def extract(filename):
    print 'Extracting ...'
    tar = tarfile.open(filename)
    tar.extractall()
    tar.close()