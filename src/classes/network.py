from libs import cmd
from libs.termcolor import colored

class Network(cmd.Cmd):

    def __init__(self, network, network_path):
        cmd.Cmd.__init__(self)
        self.network = network
        self.network_path = network_path
        self.prompt = colored('Network [' + str(network).title() + ']' + ' > ', "yellow")

    def do_list(self, line):
        print 'listing ...'

    def help_list(self):
        print 'Help List ...'

    def do_exit(self, line):
        return True