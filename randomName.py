#!/usr/bin/python
################################################################################
# @Title: randomName.py 
#
# @Author: Phil Smith 
#
# @Date: 30-Aug-2012	08:13 PM
#
# @Project: Scripts
#
# @Purpose: Random rename files to prevent name conflicts.
#
# @Modification History: 
#
###############################################################################
# Distribution Statement:
#    This software is free, open-source. It may be freely distributed
#    and/or modified. It is distributed as-is with no warranties (actual
#    or implied) and the original author is in no way responsible for 
#    any damages, inconveniences, or interruptions it may cause.
###############################################################################
"""
This module will generate a pseudo-random name for images in the child
directories of the target directory.
"""

from random import random, sample
from sys import argv
from os import chdir, listdir, getcwd, rename
from os.path import isdir 

if __name__ == '__main__':
   samplePopulace = "abcdefghijklmnopqrstuvwxyz"

   # Check to make sure you've been given a directory
   if isdir( argv[1] ):
  
      targetDir = argv[1]    

      # Confirm and change to the directory
      chdir( targetDir )

      # List the contents of the directory
      for subDir in listdir( getcwd() ): 
         # If I find the first subdirectory
         if isdir( subDir ):
            # Visit it to start changing files
            chdir( subDir )
            files = list(listdir( getcwd() ))
            for pictures in files:
               if not isdir( pictures ):
                  # Generate a random sequence number
                  randomString = int(random() * 7500)
                  # Generate a random alphabet string
                  alphaString = sample( samplePopulace, 4)
                  alphaString = "%s%s%s%s" % (alphaString[0], 
                                              alphaString[1], 
                                              alphaString[2], 
                                              alphaString[3])
                  newName = "%s_%s.jpg" % ( alphaString, randomString )
                  if not isfile(newName):
                     print( "Renaming %s to %s" % (pictures, newName))
                     rename( pictures, newName )
                  else:
                    # Try Again? -- Random name should be refactored to a function, and called through here.
            chdir( ".." ) # Return up so that we can continue
   print("Renames complete")
