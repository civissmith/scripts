#!/bin/bash
################################################################################
# @Title: go_to_file.sh 
#
# @Author: Phil Smith 
#
# @Date: 09-Sep-2010	12:51 PM
#
# @Project: Utilities
#
# @Purpose: This script sets the current working dir to the dir containing the
#           file. This script must be sourced so that the shell will actually
#           change dir.
#
###############################################################################

# Foreground Text
fg_black='\e[01;30m'
fg_red='\e[01;31m'
fg_green='\e[01;32m'
fg_yellow='\e[01;33m'
fg_blue='\e[01;34m'
fg_magenta='\e[01;35m'
fg_cyan='\e[01;36m'
fg_white='\e[01;37m'

# Background Text
bg_black='\e[01;40m'
bg_red='\e[01;41m'
bg_green='\e[01;42m'
bg_yellow='\e[01;43m'
bg_blue='\e[01;44m'
bg_magenta='\e[01;45m'
bg_cyan='\e[01;46m'
bg_white='\e[01;47m'

# End control sequences
end_color='\e[m'

if [[ $# != 1 ]]
then
    printf "$fg_red\bUsage: go_to_file.bash <file>\n$end_color"
    exit 1
fi

if [[ -n $SEARCHBASE ]]
then
    filepath=`find $SEARCHBASE -iname $1 | head -1 | xargs dirname`
else
    filepath=`find . -iname $1 | head -1 | xargs dirname`
fi

# Print the directory where the file was found.
printf "$fg_yellow$filepath$end_color\n"

# Switch to the dir
cd $filepath
