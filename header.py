#!/usr/bin/python -B
################################################################################
# Copyright (c) 2013 Phil Smith
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
#
#           Exit Codes:
#           1  - Unknown Shell passed as --shell/-s argument
#           11 - File extension is unknown
#
###############################################################################
import os
import sys
import stat
import argparse
import subprocess
from datetime import datetime
from time import strftime, localtime


def get_shell_locations(shells):
#{
    """
    Given a list of shells, returns a dict whose keys are shells and values are
    the locations of the shell in the file system. If a shell is not installed,
    a filler location will be used.
    """

    locations = {}
    # Check to make sure shells are available and store locations (if present).
    # A missing shell is only a problem if any input file is of that type.
    for shell in shells:
        try:
            location = subprocess.check_output(['which', shell])[:-1]
        except subprocess.CalledProcessError:
            location = "/usr/bin/env {0}".format(shell)
        if shell not in locations:
            locations[shell] = location

    return locations
#} End of get_shell_locations()

def run(args):
#{

    """
    Entry point for script execution. Passed in arguments, creates output file.
    """

    commentChar = []

    known_shells = ['python', 'python3','perl', 'tcsh', 'bash']
    shell_locations = get_shell_locations(known_shells)


    shell = args.shell.lower()
    if shell not in known_shells:
        print('"{0}" is an unknown shell. Aborting.'.format(shell))
        exit(1)

    #
    # Process each file
    #
    for file_ in args.files:

        # Determine the target language
        try:
            lang = check_language(file_)
        except KeyError:
            # A key error was likely caused by an unknown extension. Skip that
            # file and attempt to carry on.
            continue

        # If the language was a shell, then get the proper name of that shell 
        # from the command line argument.
        if lang == 'shell':
            lang = shell.lower()

        # Remove the '3' from Python3 modules so import still works
        if lang == 'python3':
            file_ = file_[:-1]

        commentChar = set_comment_chars(lang)

        # Check to see if the file exists
        if os.path.isfile(file_):

            # If the file already exists, move it out of the way temporarily
            tempFile = '.' + file_ + '.tmp'
            if os.path.isfile(tempFile):
                print "Removing temp file: %s" % tempFile
                os.remove(tempFile)
            os.rename(file_, tempFile)
        else:
            tempFile = ''


        #
        # Start filling the file
        #
        outFile = open(file_, 'w')
        if lang in known_shells:
            mod = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
            mod = mod | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP
            mod = mod | stat.S_IROTH | stat.S_IXOTH
            outFile.write("#!" + shell_locations.get(lang)+"\n")
        else:
            mod = stat.S_IRUSR | stat.S_IWUSR
            mod = mod | stat.S_IRGRP | stat.S_IWGRP
            mod = mod | stat.S_IROTH

        os.chmod(file_, mod)
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
            print_line(outFile, args.columns, openCharSet )
            print_apache( outFile, comment, args.author )
            print_line(outFile, args.columns, closeCharSet )
        elif args.bsd:
            print_line(outFile, args.columns, openCharSet )
            print_bsd2( outFile, comment,  args.author )
            print_line(outFile, args.columns, closeCharSet )
        elif args.gpl:
            print_line(outFile, args.columns, openCharSet )
            print_gpl3( outFile, comment,  args.author )
            print_line(outFile, args.columns, closeCharSet )
        elif args.mit:
            print_line(outFile, args.columns, openCharSet )
            print_mit( outFile, comment, args.author )
            print_line(outFile, args.columns, closeCharSet )

        print_line(outFile, args.columns, openCharSet )
        outFile.write( comment + ' >Title: ' + file_ + '\n')
        outFile.write( comment + '\n' )
        outFile.write( comment + ' >Author: ' + args.author + '\n')
        outFile.write( comment + '\n' )
        outFile.write( comment + ' >Date: ' + strftime("%a, %d-%b-%y %I:%M%p", localtime()) + '\n')
        outFile.write( comment + '\n' )
        outFile.write( comment + ' >Project: ' + args.project + '\n')
        outFile.write( comment + '\n' )
        outFile.write( comment + ' >Purpose:\n')
        outFile.write( comment + '\n' )
        outFile.write( comment + '\n' )
        print_line(outFile, args.columns, closeCharSet )


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

# } End of run()


def check_language( file_ ):
#{
    """
    Determines the language of the file that will be created and returns it to
    the caller. Can raise KeyErrors if an input file has an unknown extension.
    """

    # Makefiles are special
    if file_.lower() == 'makefile':
        return 'makefile'

    # Get the file name and extension
    name_data = file_.split('.')
    extension = name_data[-1].lower()
    name = ".".join(name_data)

    language_map = { 'c'   :'c',
                     'cpp' :'c',
                     'h'   :'c',
                     'hpp' :'c',
                     'f'   :'fortran',
                     'f77' :'fortran',
                     'f90' :'fortran',
                     'inc' :'fortran',
                     'cmn' :'fortran',
                     'pl'  :'perl',
                     'pm'  :'perl',
                     't'   :'perl',
                     'pod' :'perl',
                     'py'  :'python',
                     'py3' :'python3',
                     'sh'  :'shell',
                     'bash':'shell',
                     'tcsh':'shell',
                     'mak' :'makefile',
                     'make':'makefile',
                   }
    try:
        return language_map[extension]
    except KeyError:
        # Print out that an error was encountered, then re-raise the exception
        sys.stderr.write("Error: '{0}' has an unknown file extension.\n".format(file_))
        raise

#} End of check_language

def set_comment_chars( lang ):
#{
    """
    Returns the comment character for the given language.
    """
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

#} End of set_comment_chars


def print_line( file_, len, charSet ):
#{
    """
    Utility function to print one line of a specified length to the file.
    """
    for i in range(0, len):
        if i == 0:
            # First character
            file_.write( charSet[0] )
        elif i == len-1:
            # Last character
            file_.write( charSet[2] + '\n' )
        else:
            # Fill character
            file_.write( charSet[1] )

#} End of print_line()


################################################################################
# License Printers
################################################################################
def print_apache( file_, comment, author ):
    """
    Prints the Apache license into the file.
    """
    file_.write( comment + ' Copyright ' + str(datetime.now().year) + ' ' + author + '\n' )
    file_.write( comment + '\n')
    file_.write( comment + ' Licensed under the Apache License, Version 2.0 (the "License");\n' )
    file_.write( comment + ' you may not use this file_ except in compliance with the License.\n' )
    file_.write( comment + ' You may obtain a copy of the License at\n' )
    file_.write( comment + '\n')
    file_.write( comment + '   http://www.apache.org/licenses/LICENSE-2.0\n' )
    file_.write( comment + '\n')
    file_.write( comment + ' Unless required by applicable law or agreed to in writing, software\n' )
    file_.write( comment + ' distributed under the License is distributed on an "AS IS" BASIS,\n' )
    file_.write( comment + ' WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n' )
    file_.write( comment + ' See the License for the specific language governing permissions and\n' )
    file_.write( comment + ' limitations under the License.\n' )

def print_bsd2( file_, comment, author ):
    """
    Prints the BSD 2 license into the file.
    """
    file_.write( comment + ' Copyright (c) '+ str(datetime.now().year) + ', ' + author +'\n' )
    file_.write( comment + ' All rights reserved.\n' )
    file_.write( comment + '\n')
    file_.write( comment + ' Redistribution and use in source and binary forms, with or without modification,\n' )
    file_.write( comment + ' are permitted provided that the following conditions are met:\n' )
    file_.write( comment + '\n')
    file_.write( comment + '    Redistributions of source code must retain the above copyright notice, this\n' )
    file_.write( comment + '    list of conditions and the following disclaimer.\n' )
    file_.write( comment + '\n')
    file_.write( comment + '    Redistributions in binary form must reproduce the above copyright notice, \n' )
    file_.write( comment + '    this list of conditions and the following disclaimer in the documentation \n' )
    file_.write( comment + '    and/or other materials provided with the distribution.\n' )
    file_.write( comment + '\n')
    file_.write( comment + ' THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND\n' )
    file_.write( comment + ' ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED \n' )
    file_.write( comment + ' WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE \n' )
    file_.write( comment + ' DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE \n' )
    file_.write( comment + ' FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL \n' )
    file_.write( comment + ' DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR \n' )
    file_.write( comment + ' SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER \n' )
    file_.write( comment + ' CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, \n' )
    file_.write( comment + ' OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE \n' )
    file_.write( comment + ' OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n' )

def print_gpl3( file_, comment, author ):
    """
    Prints the GPL 3 license into the file.
    """
    file_.write( comment + ' Copyright ' + str(datetime.now().year) + ' ' + author + '\n' )
    file_.write( comment + ' This program is free software: you can redistribute it and/or modify\n' )
    file_.write( comment + ' it under the terms of the GNU General Public License as published by\n' )
    file_.write( comment + ' the Free Software Foundation, either version 3 of the License, or\n' )
    file_.write( comment + ' (at your option) any later version.\n' )
    file_.write( comment + '\n')
    file_.write( comment + ' This program is distributed in the hope that it will be useful,\n' )
    file_.write( comment + ' but WITHOUT ANY WARRANTY; without even the implied warranty of\n' )
    file_.write( comment + ' MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n' )
    file_.write( comment + ' GNU General Public License for more details.\n' )
    file_.write( comment + '\n')
    file_.write( comment + ' You should have received a copy of the GNU General Public License\n' )
    file_.write( comment + ' along with this program.  If not, see <http://www.gnu.org/licenses/>.\n' )


def print_mit( file_, comment, author ):
    """
    Prints the MIT license into the file.
    """
    file_.write( comment + ' Copyright (c) ' + str(datetime.now().year) + ' '+ author +'\n' )
    file_.write( comment + '\n' )
    file_.write( comment + ' Permission is hereby granted, free of charge, to any person obtaining a copy\n' )
    file_.write( comment + ' of this software and associated documentation files (the "Software"), to deal\n' )
    file_.write( comment + ' in the Software without restriction, including without limitation the rights\n' )
    file_.write( comment + ' to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n' )
    file_.write( comment + ' copies of the Software, and to permit persons to whom the Software is\n' )
    file_.write( comment + ' furnished to do so, subject to the following conditions:\n' )
    file_.write( comment + '\n' )
    file_.write( comment + ' The above copyright notice and this permission notice shall be included in\n' )
    file_.write( comment + ' all copies or substantial portions of the Software.\n' )
    file_.write( comment + '\n' )
    file_.write( comment + ' THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n' )
    file_.write( comment + ' IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n' )
    file_.write( comment + ' FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n' )
    file_.write( comment + ' AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n' )
    file_.write( comment + ' LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n' )
    file_.write( comment + ' OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n' )
    file_.write( comment + ' THE SOFTWARE.\n' )

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
    parser.add_argument('-a','--author',default="Phil Smith",
                        help='Author of the files')
    parser.add_argument('-c','--columns',default=80, type=int,
                        help='Number of columns in a line')
    parser.add_argument('-p','--project',default="", help='Project name')
    parser.add_argument('-s','--shell',default="bash",
                        help='Tcsh or Bash shell')
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

    run(args)
