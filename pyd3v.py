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
  mp3_name = "Enjoy.mp3"
  mp3_file = open( mp3_name, 'rb' )
  mp3_data = mp3_file.read()

  id3_tag =  mp3_data[:3]
  v_major, v_minor = ord(mp3_data[3]), ord(mp3_data[4])
  flags = mp3_data[5]
  
  
  print id3_tag
  print v_major
  print v_minor
 
  # TIT2 := Title/songname/content description
  tit2 = mp3_data.find("TIT2") 

  # TPE1 := Lead performer(s)/Soloist(s)
  tpe1 = mp3_data.find("TPE1")

  # TALB := Album/Movie/Show title
  talb = mp3_data.find("TALB")

  # TIT2
# print mp3_data[tit2:tit2+4]
  tag_len = mp3_data[tit2+4:tit2+8]
  tag_len = get_int_from_synch(tag_len)
  title_str = mp3_data[tit2+10:tit2+10+tag_len]
  print stringify(title_str)

  # TPE1
# print mp3_data[tpe1:tpe1+4]
  tag_len = mp3_data[tpe1+4:tpe1+8]
  tag_len = get_int_from_synch(tag_len)
  title_str = mp3_data[tpe1+10:tpe1+10+tag_len]
  print stringify(title_str)

  # TALB
# print mp3_data[talb:talb+4]
  tag_len = mp3_data[talb+4:talb+8]
  tag_len = get_int_from_synch(tag_len)
  title_str = mp3_data[talb+10:talb+10+tag_len]
  print stringify(title_str)

  mp3_file.close()
  
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
   
#  one   = struct.unpack('c', synch[0])
#  two   = struct.unpack('c', synch[1])
#  three = struct.unpack('c', synch[2])
#  four  = struct.unpack('c', synch[3])
  
  one   = int(ord(synch[0]))
  two   = int(ord(synch[1]))
  three = int(ord(synch[2]))
  four  = int(ord(synch[3]))

  synch = (four << 0) | (three << 7) | (two << 14) | (one << 21)

  return synch
#}
#
# 

#
# Invocation Check:
#
if __name__ == "__main__":
  main()
