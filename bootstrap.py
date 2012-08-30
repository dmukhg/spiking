#!/usr/bin/env python

"""
- Create a virtualenv in the directory containing this file.
- Activate the above virtualenv
- Install the dependencies for the app, as declared in
  requirements.txt
"""

import os
import sys
import subprocess

from virtualenv import main as venv_main

def help():
  """ Print a help text. """
  print """
  usage: python bootstrap.py <command>

  Commands
  ========
  1. all : Installs a virtualenv and installs all the requirements as
  put forth by requirements.txt into this virtualenv.


  2. virtualenv : Only installs the virtualenv.  If there is an
  existing installation, overwrites it.  

  Note: Overwriting only rewrites the pip installer and the python
  installer.  No change is made to the installed packages. 


  3. packages : If changes have been made to the requirements file or
  a package wrongly uninstalled, use this to reinstall all packages
  from the requirements file.

  Note: If there is no current virtualenv installation, this command
  will create one and install all packages to that virtualenv.
  """
  return

def virtualenv_setup(dirpath):
  """ Installs virtualenv to the directory specified by dirpath.

  All paths are strings.
  """
  print "Installing virtualenv..."
  # add the dirpath to the argument vector for virtualenv to work 
  sys.argv.append(dirpath)
  
  # setup the virtualenv
  venv_main()
  return

def pip_install(pippath, reqpath):
  """ Install packages as declared in the requirements file as pointed
  to by reqpath.  This installation occurst to the virtualenv if the
  pippath references the pip binary in the bin directory of the local
  virtualenv.  
  
  All paths are strings.
  """
  # install the dependencies for the app
  subprocess.call([pippath, 'install', '-r', reqpath])
  return


if __name__ == "__main__":
  # Figure out the necessary paths
  filepath = os.path.realpath(__file__)
  dirpath  = os.path.dirname(filepath)
  pippath  = os.path.join(dirpath, 'bin', 'pip')
  reqpath  = os.path.join(dirpath, 'requirements.txt')
  actpath  = os.path.join(dirpath, 'bin', 'activate')

  # declare that none of the actions need to be taken
  flags = {
      'virtualenv': False,
      'pip': False
  }

  # now parse cmd-line arguments and figure out what actions to
  # undertake
  if len(sys.argv) > 1 and sys.argv[1] == 'all':
    sys.argv.pop()
    flags['pip'] = True
    flags['virtualenv'] = True

  if len(sys.argv) > 1 and sys.argv[1] == 'virtualenv':
    sys.argv.pop()
    flags['virtualenv'] = True  

  if len(sys.argv) > 1 and sys.argv[1] == 'packages':
    sys.argv.pop()
    flags['pip'] = True

  if len(sys.argv) > 1 \
    or (flags['virtualenv']==False \
    and flags['pip']==False):
    # Clearly means that there is an unrecognizable command
    help()

  # Execute commands as flags require
  if flags['virtualenv']: 
    virtualenv_setup(dirpath)

  if flags['pip']:
    if not os.path.exists(actpath):
      # Check fot the existence of a virtualenv. If not found, create
      # one.
      print "No virtualenv found. Creating one."
      virtualenv_setup(dirpath)
    # Install packages
    pip_install(pippath, reqpath)
