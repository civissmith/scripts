#!/usr/bin/python -B
################################################################################
# Copyright 2014 Phil Smith
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
################################################################################
# @Title: find_dups.py
#
# @Author: Phil Smith
#
# @Date: Mon, 22-Dec-14 05:44PM
#
# @Project:  Python Tools
#
# @Purpose: Finds duplicate files in the given file tree (based on MD5 hash).
#           Optionally creates a script to remove the duplicates.
#
################################################################################
import os
import os.path as op
import hashlib as hl
import argparse as ap


def find_files(path, kind):
  """
  Finds files of type KIND recursively from the directory rooted at PATH.
  """

  files = []

  # Create lists of extentions for picture or movie types instead of
  # checking the magic number of every file in the list.
  if "pics" in kind.lower():
    exts = ['jpg', 'jpeg', 'gif', 'bmp', 'png']
  elif "movies" in kind.lower():
    exts = ['mov', 'mpg', 'mp4', 'flv', 'avi', 'wmv']
  elif "songs" in kind.lower():
    exts = ['mp3', 'wav']

  # Add files matching the KIND to the file list
  for each in os.walk(path):
    dir_name = each[0]
    for file_name in each[2]:
      tokens = file_name.split(".")
      if tokens[-1].lower() in exts:
        files.append( op.join(dir_name, file_name) )
  return files


def gen_checksum( target ):
  """
  Generates an MD5 hash of the TARGET.
  """

  chksum = hl.md5()

  chksum.update( open(target, 'r').read() )
  return chksum.hexdigest()


def find_duplicates( file_dict ):
  """
  Inpsects the given dictionary for duplicates, returns list of just
  those elements that have duplicates.
  """

  # List of all duplicate sets discovered.
  all_dups = []

  for key in file_dict:
    # Only care about files that have a duplicate
    if len(file_dict[key]) <= 1:
      continue


    # All keys at this point have at least 2 elements. The first will be
    # saved, the rest will be considered duplicates.
    original = file_dict[key][0]
    file_dups = []

    # List the duplicates for the particular file.
    for file_name in file_dict[key][1:]:
      file_dups.append(file_name)

    all_dups.append( (original, file_dups) )

  return all_dups


def report_duplicates( duplicates, script=None ):
  """
  Outputs the given list of duplicates either to the display or to a removal
  script if SCRIPT is specified.
  """

  # Bail out if there were no duplicates
  if not duplicates:
    return

  # Structure of a 'duplicates' list element:
  # ( original file, duplicates[] )

  # The removal script was requested, write out as a BASH script.
  if script:
    script = open("rmscript.sh", 'w')
    script.write("#!/bin/bash\n")

    # For now, assume the machine has BASH in the normal location.
    # Also, don't set the execute bit since NTFS won't honor it.
    for duplicate in duplicates:
      script.write('# Original: %s\n' % duplicate[0] )

      for file_name in duplicate[1]:
        script.write('rm "%s"\n' % file_name)
      script.write('\n')

    script.close()

  else:
  # The report should just be displayed to the screen.

    for duplicate in duplicates:
       print "Original:\n%s" % duplicate[0]
       print "Duplicates:"
       for file_name in duplicate[1]:
         print file_name
       print ""


def run( args ):
  """
  Main entry point for the script. Gets file list, finds duplicates and reports.
  """

  file_dict = {}

  # If not specified, assume current dir for search
  if args.path:
    path = args.path
  else:
    path = '.'

  # If not specified, assume pictures as the type
  valid_kinds = ['pics', 'movies', 'songs']
  if args.kind:
    kind = args.kind
    if kind not in valid_kinds:
      print "Invalid file type specified!"
      print "Valid types:"
      for kind in valid_kinds:
        print kind
      exit(1)
  else:
    kind = "pics"

  # Get the list of files rooted at the input directory
  file_list = find_files(path, kind)

  # Generate the checksums of the files
  for file_name in file_list:
    chksum = gen_checksum( file_name )

    if chksum not in file_dict:
      file_dict[chksum] = []
    file_dict[chksum].append(file_name)

  # Create the list of duplicates
  duplicates = find_duplicates( file_dict )

  # Report on the duplicates
  report_duplicates( duplicates, args.script )


if __name__ == "__main__":

  desc_str = """
  Search the file tree rooted at PATH for duplicate files of type KIND. If the SCRIPT
  argument is set, create a script file (rmscript.sh) that can be run to delete duplicates.
  """

  parser = ap.ArgumentParser(description=desc_str)
  parser.add_argument("-p", "--path", help="Root directory of the search")
  parser.add_argument("-k", "--kind", help="Kind of files to inspect (pics, movies, songs)")
  parser.add_argument("-s", "--script", action="store_true",
                      help="Creates a removal script if specified")
  args = parser.parse_args()
  run( args )
