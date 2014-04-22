#!/usr/bin/python -B
################################################################################
# @Title: pyd3v.py
#
# @Author: Phil Smith
#
# @Date: Mon, 14-Apr-14 05:50PM
#
# @Project: ID3 Tags
#
# @Purpose: Create folders for ID3v2 or ID3v1 songs
#
# @Revision:
# $Id: $
#
################################################################################
import argparse
import sys

#
# main(): Main entry point of this program
#{
def main( args ):

  for each in args.files:
    mp3_name = each
    mp3_file = open( mp3_name, 'rb' )
    mp3_data = mp3_file.read()

    id3_tag =  mp3_data[:3]
    v_major, v_minor = ord(mp3_data[3]), ord(mp3_data[4])
    flags = mp3_data[5]
  
    if int(v_major) < 3:
        print "Could not process: " + each
        return
    # TIT2
    print get_data("TIT2", mp3_data)

    # TPE1
    print get_data("TPE1", mp3_data)

    # TALB
    print get_data("TALB", mp3_data)

    mp3_file.close()
  
#}
#
#

#
# get_data: gets data requested in the 'tag' from the 'mp3' file
#{
def get_data( tag, mp3 ):
  data = mp3.find(tag)
  if data < 0:
    raise TypeError
  tag_len = mp3[data+4:data+8]
  tag_len = get_int_from_synch(tag_len)
  title_str = mp3[data+10:data+10+tag_len]

  return stringify(title_str)
#}
#
# 

#
# stringify: Strips out garbage from the different strings
#{
def stringify( string ):
  output = ""
  chars='&ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  for each in string:
    if each in chars:
      output += each
    if each in ' ':
      output += '_'

  return output
#}
#
# 

#
# get_int_from_synch: Get the integer value from the list of synchsafe ints.
#{
def get_int_from_synch( synch ):
  # Expect 32-bit integers
  if len(synch) != 4:
    return -1 
  
  one   = int(ord(synch[0]))
  two   = int(ord(synch[1]))
  three = int(ord(synch[2]))
  four  = int(ord(synch[3]))

  # Undo the 'synchsafe' encoding
  synch = (four << 0) | (three << 7) | (two << 14) | (one << 21)

  return synch
#}
#
# 

#
# Invocation Check:
#
if __name__ == "__main__":
   #
   # Parse the command line arguments
   #
   descStr="""
   Process FILE to extract enough data to create an entry in the music library.
   """
   progName = sys.argv[0]
   parser = argparse.ArgumentParser(prog=progName ,description=descStr)
   parser.add_argument('-l','--library', help='Path to music library')
   parser.add_argument('files', nargs='+', help='Files to be processed')
   args = parser.parse_args()

   main(args)
