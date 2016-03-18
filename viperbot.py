#!/usr/bin/python
'''
 viperbot.py wrapper script for main.py
'''
import os
import subprocess

def main():
    os.chdir('viperpy')
    print '[DEBUG] viperbot.py - ' + os.getcwd()
    os.system('./main.py')

if __name__ == "__main__":
    main()
