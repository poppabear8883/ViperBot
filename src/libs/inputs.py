import helpers
import re
import ipaddress

def yesNoInput(question):
    data = ''

    conditions = (data == 'y') or (data == 'Y') \
                 or (data == 'n') or (data == 'N') \
                 or (data == 'yes') or (data == 'Yes') or (data == 'YES') \
                 or (data == 'no') or (data == 'No') or (data == 'NO')

    while True:
        data = raw_input(question)
        if not conditions:
            print 'Invalid input!'
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
        except ipaddress.AddressValueError:
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
