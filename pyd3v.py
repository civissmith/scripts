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
# Exit Codes:
# 1 - Library doesn't exist and cannot be created
# 2 - MP3 file couldn't be copied to library
#
# @Revision:
# $Id: $
#
################################################################################
import argparse
import shutil
import sys
import os

#
# main(): Main entry point of this program
#{
def main( args ):

  #
  # Tie this to the -l --library flag
  #
  library = "./temp/music_lib"

  #
  # Process each file given at the command line
  #
  for each in args.files:
    mp3_name = each
    mp3_file = open( mp3_name, 'rb' )
    mp3_data = mp3_file.read()

    id3_tag =  mp3_data[:3]
    v_major, v_minor = ord(mp3_data[3]), ord(mp3_data[4])
    flags = mp3_data[5]
  
    # The field names changed between v2.2 and v2.3
    if v_major == 3 or v_major == 4:
      title  = get_data("TIT2", mp3_data) + ".mp3"
      artist = get_data("TPE1", mp3_data)
      album  = get_data("TALB", mp3_data)

    elif v_major == 1 or v_major == 2:
      title  = get_data("TT2", mp3_data) + ".mp3"
      artist = get_data("TP1", mp3_data)
      album  = get_data("TAL", mp3_data)

    else: 
      # Getting here means that the tag is not one of the 
      # recognized versions.
      print "Unrecognized version: %d.%d" % (v_major, v_minor)

    mp3_file.close()

    #
    # Check to make sure that the library exists. If not, try to create it.
    # If the directory can't be made, quit.
    #
    full_path = os.path.join(library,artist,album)
    if not os.path.isdir(full_path):
      try:
        os.makedirs(full_path)
      except OSError as err:
        print "Could not create directory: %s" % full_path
        print "Error: %s" % err
        exit(1)

    #
    # Check to see if the file is already in the library. If not, try to copy
    # it there.
    #
    full_title = os.path.join(full_path, title)
    if not os.path.isfile(os.path.join(full_title)):
        try:
          print "Copying file (%s) to (%s)" % (mp3_name, full_title)
          shutil.copy(mp3_name, full_title)
        except IOError as err:
          print "Could not create file: %s" % full_title
          print "Error: %s" % err
          exit(2)

#   print title
#   print artist  
#   print album  
#}
#
#

#
# get_data: gets data requested in the 'tag' from the 'mp3' file
#{
def get_data( tag, mp3 ):
  id3v2_34 = ["TIT2", "TPE1", "TALB"]
  # ID3v2.
  id3v2_12  = ["TT2", "TP1", "TAL"]

  # Make sure the flags are ID3v2.1, ID3v2.2, ID3v2.3 or ID3v2.4
  if tag in id3v2_34 or tag in id3v2_12:
    data = mp3.find(tag)

    # If a tag isn't in the MP3 file, flag the field as "Unknown"
    if data < 0:
      return 'Unknown' 

    if tag in id3v2_34:
      tag_len = mp3[data+4:data+8]
      tag_len = get_int_from_synch(tag_len)
      title_str = mp3[data+10:data+10+tag_len]
    elif tag in id3v2_12:
      tag_len = mp3[data+3:data+6]
      tag_len = get_int_from_synch(tag_len)
      title_str = mp3[data+6:data+6+tag_len]

  else:
    # Handle the case for unknown flags
    return ("Tag (%s) not supported" % tag)

  return stringify(title_str)
#}
#
# 

#
# stringify: Strips out garbage from the different strings
#{
def stringify( string ):
  output = ""
  # Specials
  chars  ='-&'
  # Uppers
  chars +='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  # Lowers
  chars +='abcdefghijklmnopqrstuvwxyz'
  # Digits
  chars +='0123456789'

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
  # v2.1-v2.2 use 3 bytes, v2.3-v2.4 use 4 bytes
  # Undo the 'synchsafe' encoding
  if len(synch) == 4:
     one   = int(ord(synch[0]))
     two   = int(ord(synch[1]))
     three = int(ord(synch[2]))
     four  = int(ord(synch[3]))
     synch = (four << 0) | (three << 7) | (two << 14) | (one << 21)
  elif len(synch) == 3:
     one   = int(ord(synch[0]))
     two   = int(ord(synch[1]))
     three = int(ord(synch[2]))
     synch = (three << 0) | (two << 7) | (one << 14)
  else:
     synch = -1

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
