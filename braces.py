#!/usr/bin/python -B
################################################################################
# @Title: braces.py
#
# @Author: Phil Smith
#
# @Date: Tue, 30-Dec-14 02:23AM
#
# @Project: Scripts
#
# @Purpose: Adds jump braces to large blocks of Python code. Settle down,
#           white-space delimiting is fine, but even code folding gets wonky
#           without braces.
#
#
################################################################################
################################################################################
# Usage:
# To use the folding with these markers. Set the fold method to manual:
#
# <vim>
# :set foldmethod=manual
#
# Move cursor to highlight the opening curly brace and type the following
# command in normal mode:
#
# zfa}
#
# The code will fold to the closing curly brace that matches.
################################################################################
import re
import os
import stat
import argparse as ap


def main( file_name, args ):
   """
   This is the main point of entry for the script.
   """

   if args.limit:
     limit = args.limit
   else:
     limit = 15
   file_data = []

   file = open( file_name, 'r')
   for line in file:

     # Read the line data and preserve leading whitespace.
     written_line = re.search( '(\s*.*)', line )

     if written_line:
       file_data.append(written_line.group(1))
   file.close()

   # The close_stacks are a dict of stacks holding close braces
   # The dictionary key is a line number, the associated data is 
   # stack of closing braces. When the line number is reached, 
   # the stack is popped until empty.
   open_lines, close_stacks = find_keywords( file_data, limit )
   new_file = add_braces( file_data, open_lines, close_stacks )


   # Don't overwrite the input file.
   if args.prefix:
     old_perms = os.stat(file_name)
     file_name = args.prefix + file_name

   file = open( file_name, 'w')
   for line in new_file:
     file.write( line + "\n" )
   file.close()
   
   # Change the mode of new files to match the original 
   if args.prefix:
     os.chmod( file_name, old_perms.st_mode )


def find_keywords( data, limit ):
   """
   This function finds Python keywords that require indentation
   following them. It returns dictionaries marking the start and
   end blocks.
   """

   # These are the keywords in Python that require indentation
   # following them.
   key_words = 'class if while def else: elif for try except'
   key_words = key_words.split()

   # Queue dict to hold opening braces.
   openings = {}

   # Stack dict to hold closing indices.
   closures = {}

   # Find key words ( line number and ending line ).
   for index in range(0, len(data)):

     line = data[index]

     # Tokenize the line to check for key words.
     tokens = line.split()

     # Disregard all lines that don't have a keyword.
     if not tokens:
       continue

     # Found a key word, so grab it's index.
     if tokens[0] in key_words:

       # Since keyword was found, save opening brace.
       # Also figure out when to close.
       spaces = ws_count( line )
       close_idx = find_closure( index+1, spaces, data )

       # The brace closing brace should be written BEFORE the line on
       # which indentation matches the start.
       close_idx -= 1

       # Note: This count will include blank lines preceding the closing
       #       indentation.
       if close_idx - index >= limit:

         # If the gap is large enough, store an opening and closing brace set.
         openings[index] = "%s# %s {" %( " "*spaces, tokens[0])
         if close_idx not in closures:
           closures[close_idx] = []
           closures[close_idx].append( "%s# } %s "  % ( " "*spaces, tokens[0]))
         else:
           closures[close_idx].append( "%s# } %s "  % ( " "*spaces, tokens[0]))

   return openings, closures


def add_braces( file_data, open_lines, close_lines ):
   """
   This function adds braces to the file data based on the two line numbers
   in the two dictionaries passed in.
   """

   new_data = []

   # Write the output.
   for index in range(0, len(file_data)):
     line = file_data[index]

     if line.split():
        new_data.append( line )
     else:
        new_data.append( "" )

     if index in open_lines:
       new_data.append( open_lines[index] )

     if index in close_lines:
       for each in reversed(close_lines[index]):
         new_data.append( each )
   return new_data


def find_closure( start, spaces, data ):
  """
  This function finds the first line that has matching or less indentation
  to the block starting at START.
  """

  for index in range( start, len(data)):

    line = data[index]

    # Ignore blank lines and comments.
    tokens = line.split()
    if (not tokens) or tokens[0][0] == '#' :
      continue

    # Find the first line to at least match indentation.
    if ws_count( line ) <= spaces:
      return index

  # EOF reached, closure is forced.
  return index+1


def ws_count( line ):
  """
  Returns the count of leading whitespace on a line.
  """
  count = 0

  for char in line:
   if char == ' ': 
     count += 1
   else:
     return count


if __name__ == "__main__":

  descStr = """
  This script adds braces to Python indented blocks to make code folding
  in Vim a little easier.
  """

  parser = ap.ArgumentParser( description=descStr) 
  limitStr = "How many lines must be in an indented block to add braces"
  parser.add_argument('-l', '--limit', type=int, help=limitStr)
  parser.add_argument('-p', '--prefix',
                       help="Optional prefix to add to file names")
  parser.add_argument('files', nargs='+', help='Files to be processed')
  args = parser.parse_args()

  for file_name in args.files:
    main( file_name, args )
