#!/home/sergio/Projects/mxious/bin/python
import os
import sys
import django

path = '/home/sergio/Projects/mxious/mxious'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mxious.settings")

django.setup()

# Functions
def clear():
	os.system('clear')