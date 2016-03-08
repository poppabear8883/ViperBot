'''
conf.py v1.0

WARNING:
THIS FILE SHOULD NOT BE EDITED BY THE USER!
EDITING THIS FILE COULD CORRUPT YOUR VIPERBOT INSTALL.
'''
import os

# Users Home Directory
HOME = os.getenv("HOME") + '/'

# ViperBot's Version
VIPER_VERSION = '1.0'

#ViperBot's src Directory
VIPER_SRC_DIRECTORY = 'src/'

# ViperBot's Install Directory
VIPER_INSTALL_DIRECTORY = HOME + "viperbot"

VIPER_CONFIG_DIRECTORY = 'configs'

VIPER_BOTNET_CONFIG = VIPER_CONFIG_DIRECTORY + '/botnet.conf'

VIPERBOT_CONF = VIPER_CONFIG_DIRECTORY + '/viperbot.conf'