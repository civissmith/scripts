#!/usr/bin/python -B
################################################################################
# @Title: sw_config.py
#
# @Author: Phil Smith
#
# @Date: Sat, 03-Jan-15 12:48PM
#
# @Project: Scripts
#
# @Purpose: Installs packages.
#
#
################################################################################
import colorize as co
import subprocess as sp
from colorize import print_line

def get_pkgs( pkgs ):
  """
  Installs common packages used with Linux Mint.
  """

  installed = []
  # Get a list of installed packages (manual and auto)
  cmds = [ 'apt-mark showmanual', 'apt-mark showauto' ]
  for cmd in cmds:
    out = sp.Popen( cmd, shell=True, stdout=sp.PIPE )
    text = out.stdout.readlines()
    for line in text:
      installed.append( line.strip() )


  for pkg in pkgs:

    if pkg in installed:
      print_line( "%s is already installed" % pkg, st=co.ITALIC)
      continue


    cmd = "sudo apt-get install -y %s"% pkg

    print_line( "Installing: ", eol="" )
    print_line( pkg, st=co.BOLD )

    out = sp.Popen( cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE )
    text = out.stdout.readlines()
    text += out.stderr.readlines()

    # Parse the output of the apt-get install.
    for line in text:

      # Check to make sure that the install has root priv.
      if "permission denied" in line.lower():
        print_line("Permission denied. Probable causes:", st=co.BOLD)
        print_line("1. Could not get root privileges.")
        print_line("2. Another installer is already running.")
        exit(1)

      if "e:" in line.lower():
        print_line( line, fg=co.RED, st=co.BOLD, eol="" )


if __name__ == "__main__":

  common = [
           "vim", "openssh-server", "tcsh", "subversion",
           ]

  dev_pc = [
           # Misc.
           "dkms", "wireshark", "youtube-dl",
           "dpkg-dev", "bless", "eyed3", "openshot",
           "frei0r-plugins", "autoconf", "libtool", "libapr1-dev",
           "libaprutil1-dev", "nfs-common", "libcurl3",

           # Python Dev Packages
           "python", "ipython", "ipython3", "python-tk", "python-twisted",
           "python-pip", "python-requests", "python-scipy", "ipython-notebook",
           "python3-tk", "python-yaml", "python-flask", "python-virtualenv",

           # Version Control Software
           "git", "cvs", "mercurial",

           # Code analysis and formatting
           "indent", "doxygen", "doxygen-gui", "graphviz",

           # Kernel Build Packages
           "build-essential", "kernel-package", "libncurses5-dev", "fakeroot",
           "bzip2",

           # LaTeX
           "docbook-utils", "texlive-full", "texmaker",

           # GUI Builders
           "glade", "glade-gtk2",
           ]

  svn_serv = [
               "apache2",
               "apache2-utils",
               "libapache2-svn",
               "subversion-tools",
               "libgtk2.0-0:i386",
               "libnss3-1d:i386",
               "libnspr4-0d:i386",
               "lib32nss-mdns",
               "libxml2:i386",
               "libxslt1.1:i386",
               "libstdc++6:i386",
             ]

  pkgs = common + dev_pc
  get_pkgs( pkgs )
