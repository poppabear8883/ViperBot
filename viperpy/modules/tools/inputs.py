import getpass
import re

import ipaddress


def yesNoInput(question):
    valid = ['','y','Y','ye','yes','YES','n','N','no','No','NO']

    data = ''

    while True:
        data = raw_input(question)
        if not data in valid:
            print 'Invalid input!'
            continue
        else:
            break

    print ' '
    return data

def passwordInput(question):
    data = ''

    while True:
        data = getpass.getpass(question)
        if not data.isalnum():
            print 'Must be an Alphanumeric value!'
            continue
        elif '' == data:
            print 'Can not be empty!'
            continue
        else:
            break

    print ' '
    return data

def alphaNumInput(question):
    data = ''

    while True:
        data = raw_input(question)
        if not data.isalnum():
            print 'Must be an Alphanumeric value!'
            continue
        elif '' == data:
            print 'Can not be empty!'
            continue
        else:
            break

    print ' '
    return data

def numInput(question):
    data = ''

    while True:
        data = raw_input(question)
        if not data.isdigit():
            print 'Must be an Number (integer/digit)'
            continue
        elif '' == data:
            print 'Can not be empty!'
            continue
        else:
            break

    print ' '
    return data

def channelInput(question):
    data = ''

    while True:
        data = raw_input(question)
        if not data.startswith('#'):
            print 'Must start with #! (#'+data+')'
            continue
        elif '' == data:
            print 'Can not be empty!'
            continue
        else:
            break

    print ' '
    return data

def serversInput(question):
    data = ''

    while True:
        data = raw_input(question)
        if not re.match(r'[^:,]+:\d+(?:,[^:,]+:\d+)*$', data):
            print 'Invalid Input! (server:port,server:port)'
            continue
        else:
            servers = data.split(',', 1)
            for server in servers:
                s = server.split(':', 1)
                if not re.match(r'(?=^.{1,254}$)(^(?:(?!\d+\.|-)[a-zA-Z0-9_\-]{1,63}(?<!-)\.)+(?:[a-zA-Z]{2,})$)', s[0]):
                    print 'The server portion is not a FQDN ie: (irc.freenode.net)'
                    continue
                else:
                    break
            break

    print ' '
    return data

def portInput(question):
    data = ''

    while True:
        data = raw_input(question)
        if not data.isdigit() and len(data) > 6 and not data.startswith('0'):
            print 'Must be a Number between 1-9 and no more than 6 digits!'
            continue
        elif '' == data:
            print 'Can not be empty!'
            continue
        else:
            break

    print ' '
    return data

def ipInput(question):
    data = ''

    while True:
        data = raw_input(question)
        try:
            if ipaddress.ip_address(data):
                break
        except ValueError:
            print 'Not a valid IP!'
            continue

    print ' '
    return data

def emailInput(question):
    data = ''

    while True:
        data = raw_input(question)
        if not re.match(r'(\w+[.|\w])*@(\w+[.])*\w+', data):
            print 'Not a valid Email Address!'
            continue
        elif '' == data:
            print 'Can not be empty!'
            continue
        else:
            break

    print ' '
    return data
