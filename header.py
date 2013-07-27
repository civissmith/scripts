#!/usr/bin/python -B
################################################################################
# @Title: header.py 
#
# @Author: Phil Smith 
#
# @Date: 02-Jul-2013	12:05 AM
#
# @Project: Utility Scripts
#
# @Purpose: This script creates standard headers for various file types.
#           The supported types are: C/C++, FORTRAN, Python, Perl, Tcsh,
#           Bash and Makefiles. 
#           This script assumes that any file passed to it does not have a 
#           a header and will simply add its payload to the top of the file.
#           This script is safe to run on existing code in most cases.
#           In it's current state, the script assumes files are named in the
#           format: 
#             NAME.EXT 
#           If multiple '.' characters are used, the script will fail. E.g.
#             PREFIX.NAME.EXT = the script will not work.
# 
#           Exit Codes:
#           1  - Unknown Shell passed as --shell/-s argument
#           2  - 'Which' failed to find the shells
#           10 - File contains no extension and is not a Makefile
#           11 - File extension is unknown
#
# @Modification History: 
# $Id: header.py,v 1.5 2013/07/17 06:23:46 alpha Exp $
###############################################################################
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###############################################################################
import argparse
import subprocess
import stat
import sys
import os
import datetime as dt

#
# dayDict creates the month name mapping to month numbers.
#
dayDict = { '1':'Jan',
            '2':'Feb',
            '3':'Mar',
            '4':'Apr',
            '5':'May',
            '6':'Jun',
            '7':'Jul',
            '8':'Aug',
            '9':'Sep',
            '10':'Oct',
            '11':'Nov',
            '12':'Dec'
}

#
# shaBang list of file types that need a shabang (#!) line.
#
shaBang = [ 'python',
            'python3',
            'perl',
            'tcsh',
            'bash' ]


def main(args):

   commentChar = []

   #
   # Store the location of the Perl, Python, TCsh and Bash interpreters
   #
   try:
      myPerl = subprocess.check_output(['which', 'perl'])[:-1]
      myTcsh = subprocess.check_output(['which', 'tcsh'])[:-1]
      myBash = subprocess.check_output(['which', 'bash'])[:-1]
      myPython = subprocess.check_output(['which', 'python'])[:-1]
      myPython3 = subprocess.check_output(['which', 'python3'])[:-1]
   except subprocess.CalledProcessError, err:
      #
      # If any of the shells can't be found, give up.
      #
      print "Could not find shell: %s" % err.cmd[1]
      exit(2)

   # Stop Python from making .pyc files
   if sys.version_info >= (2,7,4):
      myPython = myPython + ' -B'
   myPython3 = myPython3 + ' -B'
   #
   # The keys are valid values of lang (filled below), the lookup results
   # in the script finding the installed location of the shell interpeter.
   #
   shells = { 'python' : myPython,
              'python3': myPython3,
              'perl'   : myPerl,
              'tcsh'   : myTcsh,
              'bash'   : myBash }


   #
   # Check for args that can be defaulted.
   #
   if not args.author:
      author = "Phil Smith"
   else:
      author = args.author

   if not args.columns:
      columns = 80
   else:
      columns = args.columns

   if not args.project:
      project = ''
   else:
      project = args.project

   if not args.shell:
      shell = 'tcsh'
   else:
      shell = args.shell.lower()
      if shell not in shaBang:
         print "%s is an unknown shell! Aborting!" % shell
         sys.exit(1)
   #
   # Reformat the date string
   #
   rawDate = dt.datetime.now()
   day = rawDate.day
   month = str(dayDict.get(str(rawDate.month)))
   year = rawDate.year
   hour = rawDate.hour
   minute = rawDate.minute
   if hour > 12:
      hour = hour - 12
      AM_PM = 'PM'
   elif hour == 12:
      AM_PM = 'PM'
   else:
      AM_PM = 'AM'

   if hour == 0:
      hour = 12
      AM_PM = 'AM'

   dateStr = '%d-%s-%d' % (day, month, year)
   dateStr = dateStr + ' %d:%02d %s' % (hour, minute, AM_PM)
   date = dateStr
   
   #
   # Process each file
   #
   for file in args.files:
      
      #
      # Determine the target language
      #
      lang = check_language(file)

      #
      # A correction is needed to determine which basic shell is requested
      #
      if lang == 'shell':
         lang = shell.lower()

      commentChar = set_comment_chars(lang)

      #
      # Check to see if the file exists
      #
      if os.path.isfile(file):
         #
         # If the file already exists, move it out of the way temporarily
         #
         tempFile = '.' + file + '.tmp'
         if os.path.isfile(tempFile):
            print "Removing temp file: %s" % tempFile
            os.remove(tempFile)
         os.rename(file, tempFile)   
      else:
         tempFile = ''

      outFile = open(file, 'w')
      #
      # Start filling the file
      #
      if lang in shaBang:
         mod = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
         mod = mod | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP
         mod = mod | stat.S_IROTH | stat.S_IXOTH
         outFile.write("#!" + shells.get(lang)+"\n")
      else:
         mod = stat.S_IRUSR | stat.S_IWUSR 
         mod = mod | stat.S_IRGRP | stat.S_IWGRP 
         mod = mod | stat.S_IROTH 

      os.chmod(file, mod)
      openCharSet = []
      closeCharSet = []
      openCharSet.append( commentChar[0] )
      openCharSet.append( commentChar[1] )
      openCharSet.append( commentChar[1] )

      if lang == 'fortran':
         closeCharSet.append( commentChar[0] )
         closeCharSet.append( commentChar[1] )
         closeCharSet.append( commentChar[1] )
         comment = commentChar[0]
      else:
         closeCharSet.append( commentChar[1] )
         closeCharSet.append( commentChar[1] )
         closeCharSet.append( commentChar[0] )
         comment = commentChar[1]

      #
      # The header will contain the following elements:
      # (optional) License
      # Title
      # Author
      # Date
      # Project
      # Purpose
      # Revision OR Modification History
      #

      #
      # Print the license agreement, if selected
      #
      if args.apache:
         print_line(outFile, columns, openCharSet )
         print_apache( outFile, comment, year, author )
         print_line(outFile, columns, closeCharSet )
      elif args.bsd:
         print_line(outFile, columns, openCharSet )
         print_bsd2( outFile, comment, year, author )
         print_line(outFile, columns, closeCharSet )
      elif args.gpl:
         print_line(outFile, columns, openCharSet )
         print_gpl3( outFile, comment, year, author )
         print_line(outFile, columns, closeCharSet )
      elif args.mit:
         print_line(outFile, columns, openCharSet )
         print_mit( outFile, comment, year, author )
         print_line(outFile, columns, closeCharSet )

      print_line(outFile, columns, openCharSet )
      outFile.write( comment + ' @Title: ' + file + '\n')
      outFile.write( comment + '\n' )
      outFile.write( comment + ' @Author: ' + author + '\n')
      outFile.write( comment + '\n' )
      outFile.write( comment + ' @Date: ' + str(date) + '\n')
      outFile.write( comment + '\n' )
      outFile.write( comment + ' @Project: ' + project + '\n')
      outFile.write( comment + '\n' )
      outFile.write( comment + ' @Purpose:\n')
      outFile.write( comment + '\n' )
      if not args.mod:
         #
         # Split the key out to prevent CVS from storing revisions in this file.
         #
         key = 'Id: '
         outFile.write( comment + ' @Revision:\n') 
         outFile.write( comment + ' $' + key +'$\n') 
         outFile.write( comment + '\n' )
      else:
         outFile.write( comment + ' @Modification History:\n')
         outFile.write( comment + '\n' )
      print_line(outFile, columns, closeCharSet )
      
      
      #
      # If there was a temp file, copy it's contents back into the new file.
      #
      if tempFile:
         temp = open( tempFile )
         for line in temp:
            outFile.write(line)
         temp.close()
         os.remove(tempFile)

      outFile.close()
     
#
# End of main()
#

#
# check_language() - determines the language of the file that will be created.
#
def check_language( file ):
   #
   # The basic list of languages:
   #   C/C++
   #   FORTRAN
   #   Perl
   #   Python
   #   Python3
   #   Tcsh/Bash
   #
   try:
      name, rawExt = file.split('.') 
   except ValueError:
      #
      # Makefiles have no extension and will thus always cause this exception.
      #
      if file.lower() == 'makefile':
         return 'makefile'
      else:
         print "No file extension found in file name: %s" % file
         print "Aborting!"
         sys.exit(10)

   # Force the extension to lower case for easier matching.
   ext = rawExt.lower()  
   if ext == 'c' or ext == 'cpp' or ext == 'h' or ext == 'hpp':
      return 'c'
   elif ext == 'f' or ext == 'f77' or ext == 'f90' or ext == 'inc' or ext == 'cmn':
      return 'fortran'
   elif ext == 'pl' or ext == 'p':
      return 'perl'
   elif ext == 'py':
      return 'python'
   elif ext == 'py3':
      return 'python3'
   elif ext == 'sh':
      return 'shell'
   else:
      print "%s is not a known extension! Aborting!" % ext
      sys.exit(11) 
#
# End of check_language
#

#
# set_comment_chars() - Set the comment characters based on the input language
#
def set_comment_chars( lang ):
   if lang == 'c':
      return ['/','*']
   elif lang == 'fortran':
      return ['!','*']
   elif lang == 'perl':
      return ['#','#']
   elif lang == 'python':
      return ['#','#']
   elif lang == 'python3':
      return ['#','#']
   elif lang == 'tcsh':
      return ['#','#']
   elif lang == 'bash':
      return ['#','#']
   elif lang == 'makefile':
      return ['#','#']
    
#
# End of set_comment_chars
#

#
# print_line( file, len, charSet ) - prints one line of length 'len' to
# the file. 
#
def print_line( file, len, charSet ):
   for i in range(0, len):
      if i == 0:
         # First character
         file.write( charSet[0] )
      elif i == len-1:
         # Last character
         file.write( charSet[2] + '\n' )
      else:
         # Fill character
         file.write( charSet[1] )
#
# End of print_line()
#

################################################################################
# License Printers
################################################################################
#
# print_apache() - Prints the Apache license
#
def print_apache( file, comment, year, author ):
   file.write( comment + ' Copyright ' + year + ' ' + author + '\n' )
   file.write( comment + '\n')
   file.write( comment + ' Licensed under the Apache License, Version 2.0 (the "License");\n' )
   file.write( comment + ' you may not use this file except in compliance with the License.\n' )
   file.write( comment + ' You may obtain a copy of the License at\n' )
   file.write( comment + '\n')
   file.write( comment + '   http://www.apache.org/licenses/LICENSE-2.0\n' )
   file.write( comment + '\n')
   file.write( comment + ' Unless required by applicable law or agreed to in writing, software\n' )
   file.write( comment + ' distributed under the License is distributed on an "AS IS" BASIS,\n' )
   file.write( comment + ' WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n' )
   file.write( comment + ' See the License for the specific language governing permissions and\n' )
   file.write( comment + ' limitations under the License.\n' )
#
# End of print_apache()
#

#
# print_bsd2() - Prints the BSD license
#
def print_bsd2( file, comment, year, author ):
   file.write( comment + ' Copyright (c) '+ year + ', ' + author +'\n' )
   file.write( comment + ' All rights reserved.\n' )
   file.write( comment + '\n')
   file.write( comment + ' Redistribution and use in source and binary forms, with or without modification,\n' )
   file.write( comment + ' are permitted provided that the following conditions are met:\n' )
   file.write( comment + '\n')
   file.write( comment + '    Redistributions of source code must retain the above copyright notice, this\n' )
   file.write( comment + '    list of conditions and the following disclaimer.\n' )
   file.write( comment + '\n')
   file.write( comment + '    Redistributions in binary form must reproduce the above copyright notice, \n' )
   file.write( comment + '    this list of conditions and the following disclaimer in the documentation \n' )
   file.write( comment + '    and/or other materials provided with the distribution.\n' )
   file.write( comment + '\n')
   file.write( comment + ' THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND\n' )
   file.write( comment + ' ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED \n' )
   file.write( comment + ' WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE \n' )
   file.write( comment + ' DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE \n' )
   file.write( comment + ' FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL \n' )
   file.write( comment + ' DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR \n' )
   file.write( comment + ' SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER \n' )
   file.write( comment + ' CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, \n' )
   file.write( comment + ' OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE \n' )
   file.write( comment + ' OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n' )
#
# End of print_bsd2()
#

#
# print_gpl3() - Prints the GNU General Public License
#
def print_gpl3( file, comment, year, author ):
    file.write( comment + ' Copyright ' + year + ' ' + author + '\n' )
    file.write( comment + ' This program is free software: you can redistribute it and/or modify\n' )
    file.write( comment + ' it under the terms of the GNU General Public License as published by\n' )
    file.write( comment + ' the Free Software Foundation, either version 3 of the License, or\n' )
    file.write( comment + ' (at your option) any later version.\n' )
    file.write( comment + '\n')
    file.write( comment + ' This program is distributed in the hope that it will be useful,\n' )
    file.write( comment + ' but WITHOUT ANY WARRANTY; without even the implied warranty of\n' )
    file.write( comment + ' MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n' )
    file.write( comment + ' GNU General Public License for more details.\n' )
    file.write( comment + '\n')
    file.write( comment + ' You should have received a copy of the GNU General Public License\n' )
    file.write( comment + ' along with this program.  If not, see <http://www.gnu.org/licenses/>.\n' )
#
# End of print_gpl3()
#

#
# print_mit() - Prints the MIT license
#
def print_mit( file, comment, year, author ):
   file.write( comment + ' Copyright (c) ' + year + ' '+ author +'\n' )
   file.write( comment + '\n' )
   file.write( comment + ' Permission is hereby granted, free of charge, to any person obtaining a copy\n' )
   file.write( comment + ' of this software and associated documentation files (the "Software"), to deal\n' )
   file.write( comment + ' in the Software without restriction, including without limitation the rights\n' )
   file.write( comment + ' to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n' )
   file.write( comment + ' copies of the Software, and to permit persons to whom the Software is\n' )
   file.write( comment + ' furnished to do so, subject to the following conditions:\n' )
   file.write( comment + '\n' )
   file.write( comment + ' The above copyright notice and this permission notice shall be included in\n' )
   file.write( comment + ' all copies or substantial portions of the Software.\n' )
   file.write( comment + '\n' )
   file.write( comment + ' THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n' )
   file.write( comment + ' IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n' )
   file.write( comment + ' FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n' )
   file.write( comment + ' AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n' )
   file.write( comment + ' LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n' )
   file.write( comment + ' OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n' )
   file.write( comment + ' THE SOFTWARE.\n' )
#
# End of print_mit()
#

################################################################################
# END License Printers
################################################################################

#
# Invocation check
#
if __name__ == "__main__":
   #
   # Parse the command line arguments
   #
   descStr="""
   Create FILE with a pre-formatted header and optional license. If FILE already
   exists, then the header and optional license will be written to the top of the
   existing content."""
   progName = sys.argv[0]
   parser = argparse.ArgumentParser(prog=progName ,description=descStr)
   parser.add_argument('-a','--author', help='Author of the files')
   parser.add_argument('-c','--columns', type=int, help='Number of columns in a line')
   parser.add_argument('-p','--project', help='Project name')
   parser.add_argument('-s','--shell', help='Tcsh or Bash shell')
   parser.add_argument('-m','--mod',  action='store_true',
                        help='Determines whether to use mod history or revision number')
   parser.add_argument('--bsd',  action='store_true',
                        help='Use the BSD 2 license')
   parser.add_argument('--gpl',  action='store_true',
                        help='Use the GPL 3 license')
   parser.add_argument('--mit',  action='store_true',
                        help='Use the MIT license')
   parser.add_argument('--apache',  action='store_true',
                        help='Use the Apache license')
   parser.add_argument('files', nargs='+', help='Files to be created')
   args = parser.parse_args()

   main(args)
