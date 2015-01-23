'''
Setup script for Chaff.
'''

import sys

# Check if Python is 2.7 installed/invoked. 
major, minor, micro, releaselevel, serial = sys.version_info
if (major,minor) != (2,7):
	print 'Python %(maj)d.%(min)d detected; Chaff requires Python 2.7. Exiting...' % {'maj':major, 'min':minor}
	sys.exit(101)


import os

from setuptools import setup
import chaff_configure

#Get working directory
wd = os.path.dirname(os.path.abspath(__file__))
os.chdir(wd)
sys.path.insert(1, wd)


#Set some metadata
name = 'python-chaff'
author = 'Gabriel Deleon'
email = 'gabriel.deleon@nyu.edu'
version = '0.7.0'

description = 'Send a phishing site fake data to render their endeavor worthless.'

try:
    reqs = open(os.path.join(os.path.dirname(__file__), 'requirements.txt')).read()
except (IOError, OSError):
    reqs =''


#Egg Metadata
setup(name=name,
      version=version,
      author=author,
      author_email=email,
      maintainer=author,
      maintainer_email=email,
      description=description,
      install_requires=reqs,
      entry_points = {},
      py_modules=['chaff','chaff_configure','chaff_account','chaff_url'],
)


#Make a blank config script 
new_conf = chaff_configure.ChaffConfigure()
new_conf.new_config('chaff_config')
