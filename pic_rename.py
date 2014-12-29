#!/usr/bin/python -B
################################################################################
# Copyright (c) 2014 Phil Smith
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################
################################################################################
# @Title: pic_rename.py
#
# @Author: Phil Smith
#
# @Date: Sun, 28-Dec-14 03:19PM
#
# @Project: Python Tools
#
# @Purpose: Rename image files within a directory to prevent name conflicts.
#
################################################################################
import os
import os.path as op
import argparse as ap


def run( args ):
  """
  This function is the main entry point for the script.
  """

  #
  # Find all files and directories in the current dir
  # IF the recursive flag is set, directories will be inspected
  # SORT files by name
  # FOR each file, rename file to PREFIX_SEQ.jpg
  #   Where PREFIX is the designated prefix ("image_": default, folder_name"_": if recursive)
  #         SEQ is the numeric sequence of the image within the folder
  #
  rec_flag = args.recursive
  ver_flag = args.verbose

  if args.path:
    path = args.path
  else:
    path = '.'

  files = list_contents( path, recursive=rec_flag )
  pics  = find_pictures( files )
  rename_pics( pics, recursive=rec_flag, verbose=ver_flag )


def list_contents( tgt_dir, recursive=False ):
   """
   This function returns a list of files and directories within the target directory.
   If the recursive flag is set, then subdirectories will be included.
   """
   files = []

   # When not recursive, simply return a list of the current files.
   if not recursive:
     for item in os.listdir( tgt_dir ):
       file_name = op.join( tgt_dir, item )
       if op.isfile( file_name ):
          files.append(file_name)
     return files

   # When recursive, return files and directories.
   for each in os.walk( tgt_dir ):
     for item in each[2]:
       file_name = op.join(each[0], item)
       if op.isfile( file_name ):
         files.append( file_name )
   return files


def find_pictures( file_list ):
  """
  This function returns a list containing only picture files from the input
  file list.
  """

  pics = []

  # List contains file extensions used to determine if a file is an image.
  pic_exts = ['jpeg', 'jpg', 'png', 'gif', 'bmp']

  for file_name in file_list:
    file_ext = file_name.split('.')[-1].lower()

    if file_ext in pic_exts:
      pics.append( file_name )

  return pics


def rename_pics( pic_list, recursive=False, verbose=False ):
  """
  This function renames the files from the input list.
  """

  # When not recursive, all files will get the default prefix.
  # When recursive, the files will get the last parent folder as a prefix.
  if not recursive:
    sequence = 0
    prefix = "image"

    # Perform the renames
    for pic in sorted(pic_list):

      path = op.split(pic)[0]

      ext = pic.split('.')[-1].lower()
      new_name = "%s_%02d.%s" % (prefix, sequence, ext)
      new_name = op.join(path, new_name)

      # There is a chance that the script may have already ran,
      # the new name must not conflict with a pre-existing file
      while op.isfile(new_name):
        new_name = "%s_%02d.%s" % (prefix, sequence, ext)
        new_name = op.join(path, new_name)
        sequence += 1
      if verbose:
        print "%s ==> %s" % (pic, new_name)
      os.rename( pic, new_name )
    return

##                                                                            ##
##                              Recursive Rename                              ##
##                                                                            ##

  # Find the directories (needed so sequence can be restarted)
  dirs = {}

  for pic in pic_list:

    path = op.split(pic)[0]

    # Split the pictures up by their lowest parent directory
    # This ensures that './Pics' and './Foo/Pics' are evaluated separately.
    if path not in dirs:
      files = []
      dirs[path] = files[:]
      dirs[path].append(pic)
    else:
      dirs[path].append(pic)

  for path in dirs:
    sequence = 0

    # Grab the name of the last parent directory
    # Ex. ./foo/bar/baz/qux.jpg => 'baz'
    prefix = path.split('/')[-1]
    if prefix == '.':
      prefix = "image"

    # Perform the renames
    for item in sorted(dirs[path]):

      ext = item.split('.')[-1].lower()
      new_name = "%s_%02d.%s" % ( prefix, sequence, ext)
      new_name = op.join( path, new_name )

      # There is a chance that the script may have already ran,
      # the new name must not conflict with a pre-existing file
      while op.isfile(new_name):
        new_name = "%s_%02d.%s" % (prefix, sequence, ext)
        new_name = op.join( path, new_name )
        sequence += 1
      if verbose:
        print "%s ==> %s" % ( item, new_name )
      os.rename( item, new_name )


if __name__ == "__main__":
  descStr = """
    This command will rename picture files using a common naming scheme. If
  specified, the command can be run recursively.
    Files in the current directory will be rename 'image_{num}.{ext}' (num
  will be the next sequential file number available, ext will be the lower-
  case version of the original extension.
    When run recursively, files in lower directories will be given a prefix
  matching the name of the lowest level parent directory. For example:
     ./foo/bar/baz/qux.jpg will become ./foo/bar/baz/baz_00.jpg
  """
  parser = ap.ArgumentParser( description=descStr )
  parser.add_argument('-p', '--path', help='Base path from which to rename')
  parser.add_argument('-r', '--recursive', action="store_true",
                       help='Perform recursive renaming if flag is set')
  parser.add_argument('-v', '--verbose', action="store_true",
                       help='Show files being renamed')
  args = parser.parse_args()

  run(args)
