import os

try:
    pipUpdateTelethon = lambda: os.system('pip3 install -U telethon')
    pipUpdateTelethon()
except ImportError:
    pipInstallTelethon = lambda: os.system('pip3 install telethon')
    pipInstallTelethon()

import DualiAdder
