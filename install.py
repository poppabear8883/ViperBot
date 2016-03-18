#!/usr/bin/python
'''
 install.py wrapper script
'''
import os
import subprocess

def main():
    os.chdir('./viperpy')
    subprocess.call('./install.py')

if __name__ == "__main__":
    main()
