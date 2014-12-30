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
import re

def main():
   """
   This is the main point of entry for the script.
   """

   LIMIT = 15
   file_name = "header.py"

   file_data = []

   # Queue to hold opening braces
   key_queue = []

   # Stack to hold closing braces
   key_stack = []

   # List to store index for opening braces
   open_idx = []
   close_idx = []
   closures = {}

   key_words = 'class if while def else: elif for'
   key_words = key_words.split()

   file = open( file_name, 'r')
   for line in file:
     
     # Read the line data and preserve leading whitespace
     written_line = re.search( '(\s*.*)', line )

     if written_line:
       file_data.append(written_line.group(1))
   file.close()

   # First pass, find key words ( line number and ending line )
   for index in range(0, len(file_data)):

     line = file_data[index]

     # Tokenize the line to check for key words
     tokens = line.split()
     if not tokens:
       continue

     # Found a key word, so grab it's index
     if tokens[0] in key_words:
       

       # Since keyword was found, save opening brace
       # Also figure out when to close
       spaces = ws_count( line )
       closing = find_closure( index+1, spaces, file_data )
       closing -= 1
       if closing - index >= LIMIT:
         key_queue.append( "%s# %s {" %( " "*spaces, tokens[0]))
         if closing not in closures:
           closures[closing] = []
           closures[closing].append( "%s# } %s "  % ( " "*spaces, tokens[0]))
         else:
           closures[closing].append( "%s# } %s "  % ( " "*spaces, tokens[0]))

         # if the gap is large enough, store opening and closing indices
         # so queue and stack know when to print
         open_idx.append( index )

   # Second pass - write the output
   for index in range(0, len(file_data)):
     line = file_data[index]
     
     if line.split():
        print line
     else:
        print ""

     if index in open_idx:
       print key_queue.pop(0)

     if index in closures:
       for each in reversed(closures[index]):
         print each

   for remaining in reversed(key_stack):
     print remaining

def find_closure( start, spaces, data ):

  for index in range( start, len(data)):

    line = data[index]
    
    # Ignore blank lines
    if not line.split():
      continue

    if ws_count( line ) <= spaces:
      return index
  return index+1
#       for each in range( index, len(file_data)):
#         if ws_count( file_data[each] ) == spaces:
#           return each
  


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
  main()
