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
import struct
import binascii
#
# main(): Main entry point of this program
#{
def main():
  mp3_name = "TheFuneral.mp3"
  mp3_file = open( mp3_name, 'rb' )
  mp3_data = mp3_file.read()

  id3_tag =  mp3_data[:3]
  v_major, v_minor = ord(mp3_data[3]), ord(mp3_data[4])
  flags = mp3_data[5]
  
  title = mp3_data.find("TIT2") 
  
  print id3_tag
  print v_major
  print v_minor
  print title
  print mp3_data[title:title+4]
  tag_len = mp3_data[title+4:title+8]
  tag_len = get_int_from_synch(tag_len)
  title_str = mp3_data[title+10:title+10+tag_len]
  print stringify(title_str)
#  print get_int_from_synch( mp3_data[title+7] )
#  print get_int_from_synch( mp3_data[6:10] )
  mp3_file.close()
  
#}
#
#

#
# stringify: Strips out garbage from the different strings
#{
def stringify( string ):
  output = ""
  chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  for each in string:
    if each in chars:
      output += each

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
   
#  one   = struct.unpack('c', synch[0])
#  two   = struct.unpack('c', synch[1])
#  three = struct.unpack('c', synch[2])
#  four  = struct.unpack('c', synch[3])
  
  one   = int(ord(synch[0]))
  two   = int(ord(synch[1]))
  three = int(ord(synch[2]))
  four  = int(ord(synch[3]))
  print one
  print two
  print three
  print four
  synch = (four << 0) | (three << 7) | (two << 14) | (one << 21)


  return int(synch)
#}
#
# 

#
# Invocation Check:
#
if __name__ == "__main__":
  main()
