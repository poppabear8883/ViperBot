import urllib2
import tarfile
import os

def findLinesInConf(bot_path, searchFor):
    dict = {}

    with open(bot_path) as search:
        for num, line in enumerate(search, 1):
            line = line.rstrip()
            if searchFor in line:
                if not line.startswith('#'):
                    dict[num] = line

    return dict

def getLineInConf(bot_path, lineNum):
    with open(bot_path) as search:
        for num, line in enumerate(search, 1):
            line = line.rstrip()
            if int(num) == int(lineNum):
                return line

    return ''

def editLineInConf(bot_path, lineNum, newLine):
    with open(bot_path+'.tmp', 'w') as fin:
        with open(bot_path, 'r') as fout:
            for num, line in enumerate(fout, 1):
                if int(num) == int(lineNum):
                    line = line.replace(line, newLine+'\n')

                fin.write(line)

    if os.path.exists(bot_path+'.tmp'):
        os.rename(bot_path, bot_path+'~bak')
        os.rename(bot_path+'.tmp', bot_path)
        print 'Done - ' + bot_path
    else:
        return False

    return True

def internet_on():
    try:
        response=urllib2.urlopen('http://173.194.206.102',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def appendToFile(filename, text):
    with open(filename, "a") as myfile:
        myfile.write(text + '\n')

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