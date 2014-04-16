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
  print mp3_data[title:title+5]
  print get_int_from_synch( mp3_data[title+7] )
  mp3_file.close()
  
#}
#
#

#
# get_int_from_synch: Get the integer value from the list of synchsafe ints.
#{
def get_int_from_synch( synch ):
  synch = ord(struct.unpack( 'c', synch)[0])
  return synch
#}
#
# 

#
# Invocation Check:
#
if __name__ == "__main__":
  main()
