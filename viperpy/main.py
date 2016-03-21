#!/usr/bin/python
"""
viperbot.py (c) 2016 Poppabear @ Freenode Irc Network
"""
from modules.viperbotcli import ViperBotCLI

def main():
    vb = ViperBotCLI()
    vb.cmdloop()

if __name__ == '__main__':
    main()