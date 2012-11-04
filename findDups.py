#!/usr/bin/python -B
################################################################################
# @Title: findDups.py 
#
# @Author: Phil Smith 
#
# @Date: 03-Sep-2012	05:55 PM
#
# @Project: Python Tools
#
# @Purpose: Practice Python data structures and clean up duplicate files
#           in file system. (Tested on Python 2.7.3)
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

'''
   This module is the Python core of a larger, mixed-environment script
   that is meant to search for duplicate files in your file system
   using the md5sum checksum value. It should NOT be imported directly.
'''
#
# Python can get info from the environment. In the full system, hashDB and
# reportFile will come in from the caller's environment. I've stubbed them
# here so that you can just drop a name in. I guess I could have been nice
# and added CLI interface - but whatevs...
#

# File containing the MD5 hashes, sorted by key
hashDB = open('md5db.lst', 'r')

# File that will contain results
reportFile = open( 'duplicate_analysis.lst', 'w' )

if __name__ == "__main__":
   #
   # Initialize an empty dictionary
   #
   fileDict = {}
   
   #
   # Now read every line in from the hashDB and break it into
   # key/value pairs. Any duplicates are flagged and added to
   # a list stored at the approriate key.
   #
   for eachline in hashDB:
      (key, value) = eachline.split()
   
      if key in fileDict:

         #
         # Add any duplicates to the list at the key index.
         #
         prevFiles = ( fileDict[key], value )

         #
         # The duplicates: phrase is here so that any regex
         # tool can weed out lines that need inspection. It
         # can be changed to suit your needs.
         #
         fileDict[key] = ' duplicates:  '.join(prevFiles)

      else:

         #
         # Otherwise, just store the single value.
         #
         fileDict[key] = value

   #
   # Print out the entire dictionary when the DB is done.
   # 
   for eachKey in fileDict:
      reportFile.write( eachKey +"   "+ fileDict[eachKey] + "\n" )
   
   reportFile.close()
   hashDB.close()

else:
   print "You really shouldn't import this module! See the DocString for info."
