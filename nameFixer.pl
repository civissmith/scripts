#!/usr/bin/perl
################################################################################
# @Title: nameFixer.pl 
#
# @Author: Phil Smith 
#
# @Date: 20-Jul-2011	10:27 PM
#
# @Project: Utility Scripts
#
# @Purpose: Recursively searches for poorly named files and corrects them.
#           Names that include "(", ")", and whitespace.
#
# @Modification History: 
# 20121104   PAS     Added distrubution statement and comments for initial
#                    Git version.
#
###############################################################################
# Distribution Statement:
#    This software is free, open-source. It may be freely distributed
#    and/or modified. It is distributed as-is with no warranties (actual
#    or implied) and the original author is in no way responsible for 
#    any damages, inconveniences, or interruptions it may cause.
###############################################################################
use Cwd;

# Get a list of files
chomp($temp = cwd);
&processDirs();
&processFiles();


################################################################################
# Sub: processDirs
#   This subroutine will find the names of all directories and change them 
#   according to the rule. All directories must be changed first or else the
#   paths to the files will go stale. It uses the built-in 'find' because
#   Perl's 'find' is just too wonky (sorry Larry).
#
################################################################################
sub processDirs{

   #
   # Store the names of all directories in an array
   #
   @dirs = `find $temp -type d`;

   #
   # Trudge through the array and perform the change rule on every directory.
   #
   foreach $dir (@dirs){
      chomp($dir);
      if( ($newName = $dir) =~ s/[\(\)\s+]//g ){
         rename($dir, $newName);

         #
         # This recursive call will cause the deepest children to be changed
         # first, otherwise path staleness will occur.
         #
         &processDirs($newName);
      }
   }
}

################################################################################
# Sub: processFiles
#   This subroutine will find the names of all files and change them 
#   according to the rule. All files are changed last because they are leafs
#   in the file system. Again, the built-in 'find' is used.
#
################################################################################
sub processFiles{

   #
   # Store the names of all files in an array
   #
   @files = `find $temp -type f`;

   #
   # Trudge through the array and perform the change rule on every file.
   #
   foreach $file (@files){
      chomp($file);
      if( ($newName = $file) =~ s/[\(\)\s+]//g ){
         if( ! -e $newName ){
            rename($file, $newName);
         }else{
            #
            # Simple conflic resolution: If names conflict, append an a
            # tag to the new name and try again.
            #
            # This has NEVER been tested!
            $newName = $newName . "_$i++";
            while( -e $newName ){
               rename($file, $newName);
            }
         }
      }   
   }
}
