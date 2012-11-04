#!/usr/bin/perl
################################################################################
# @Title: header.pl
#
# @Author: Phil Smith
#
# @Date: 13-Jun-2009	01:45 AM
#
# @Project: Personal
#
# @Purpose: This file creates standard boiler plates for various file types.
# @Modification History: 
# 20100201   PAS     Added 'java' files to known file types
# 20100208   PAS     Added ECE344 report format sections, added comments
# 20101021   PAS     Added multiple file support and cleaned up Ada code
# 20110604   PAS     Changed file/ext selection to use split
# -                  Added support for Arduino "pde" files
# -                  Added command-line flags for author, date and project
# 20120826   PAS     Added Python support
# 20121104   PAS     Changed 'pde' to 'ino' for newer Arduino format. Added
#                    distribution statement
###############################################################################
# Distribution Statement:
#    This software is free, open-source. It may be freely distributed
#    and/or modified. It is distributed as-is with no warranties (actual
#    or implied) and the original author is in no way responsible for 
#    any damages, inconveniences, or interruptions it may cause.
###############################################################################

#
# NOTE: This script is not pure Perl. It assumes that it is running on a Linux
#       platform. It does not play well with all Unix flavors and won't even
#       run on Windows.
#

use Getopt::Std;
$myTcsh = `which tcsh`;
$myPerl = `which perl`;

#
# By default, disable bytecode generation
#
$myPython = `which python`;  
chomp( $myPython );
$myPython = $myPython . " -B\n";
$numCol = 80;
if( @ARGV < 1 ){
   print "USAGE: cmd [-a \"Author\" -d \"Date\" -p \"Project\"] file(s)\n";
}

getopt("adp:");

# -a => Author
if( $opt_a ){
   $myAuthor = $opt_a;
}else{
   $myAuthor = 'REAL NAME';   #! Change this to your real name !
}

# -d => Date
if( $opt_d ){
   $myDate = $opt_d;
}else{
   $myDate = `date +"%d-%b-%Y%t%I:%M %p"`;
   chomp $myDate;
}

# -p => Project
if( $opt_p ){
   $myProject = $opt_p;
}else{
   $myProject = undef;
}

foreach (@ARGV){
   $myName = "$_";
   ($myExt,$myType) = split /\./,$myName;


   if( !(-e $myName) ) {
      setComment();
      printFile($myName);
   }else
   {
      $myOldName = $myName;
      setComment();
      $myName = "$myName.tmp";
      printFile($myOldName);

      `cat $myOldName >> $myName`;
      `mv $myName $myOldName`;
   }
}



sub setComment{

   @commentChar = ("\/" , "*" , "--" , "-" , "!" , "\#" , "\%") ;
   # commentChar 0 = /
   # commentChar 1 = *
   # commentChar 2 = --
   # commentChar 3 = -
   # commentChar 4 = !
   # commentChar 5 = #
   # commentChar 6 = %

   # Determine the appropriate file type
   # C/CPP, Java files
   if ( $myType eq "c" || $myType eq "cpp" || $myType eq "h"  ||
        $myType eq "ino" || $myType eq "hpp" || $myType eq "java")
   {
      $FirstComment  = $commentChar[0];
      $SecondComment = $commentChar[1];
      $upperLine     = $numCol - 1;
      $lowerLine     = $numCol;
   }
   # FORTRAN files
   elsif( $myType eq "f" || $myType eq "f77" || 
          $myType eq "inc" || $myType eq "cmn")
   {
      $FirstComment  = $commentChar[1];
      $SecondComment = $commentChar[1];
      $upperLine     = $numCol - 1;
      $lowerLine     = $numCol;
   }
   # Ada files
   elsif( $myType eq "adb" || $myType eq "ads" )
   {
      $FirstComment  = $commentChar[2];
      $SecondComment = $commentChar[2];
      $upperLine     = ($numCol/2)-1;
      $lowerLine     = ($numCol/2)+1;
   }
   # Perl scripts
   elsif( $myType eq "pl" || $myType eq "p" )
   {
      $FirstComment  = "$commentChar[5]!$myPerl";
      $SecondComment = $commentChar[5];
      $upperLine     = $numCol;
      $lowerLine     = $numCol;
   }
   # Python scripts
   elsif( $myType eq "py" )
   {
      $FirstComment  = "$commentChar[5]!$myPython";
      $SecondComment = $commentChar[5];
      $upperLine     = $numCol;
      $lowerLine     = $numCol;
   }
   # TC shell scripts
   elsif( $myType eq "sh" )
   { 
     # This make tcsh scripts only, edit line in file for bash, csh, or sh
      $FirstComment  = "$commentChar[5]!$myTcsh"; 
      $SecondComment = $commentChar[5];
      $upperLine     = $numCol;
      $lowerLine     = $numCol;
   }
   # Freemat/Matlab comments
   elsif( $myType eq "m" )
   {
      $FirstComment  = $commentChar[6];
      $SecondComment = $commentChar[6];
      $upperLine     = $numCol - 1;
      $lowerLine     = $numCol;
   }
   elsif( $myName eq "Makefile" || $myName eq "makefile" )
   {
      $FirstComment  = $commentChar[5];
      $SecondComment = $commentChar[5];
      $upperLine     = $numCol - 1;
      $lowerLine     = $numCol;
   }

}
sub printFile {
   $myRealName = "@_";
   open (FILE ,">", $myName) or die "Could not open file: $myName\n";
   # Fill the file with the appropriate comments fields
   print FILE $FirstComment;
   for( $i = 1 ; $i < $upperLine ; $i++)
   {
      print FILE "$SecondComment";
   }

   print FILE "$SecondComment\n";
   print FILE "$SecondComment \@Title: $myRealName \n";

   print FILE "$SecondComment\n";
   print FILE "$SecondComment \@Author: $myAuthor \n";
   print FILE "$SecondComment\n";
   print FILE "$SecondComment \@Date: $myDate\n";
   print FILE "$SecondComment\n";
   if( $myProject eq undef){
      print FILE "$SecondComment \@Project: \n";
   }else{
      print FILE "$SecondComment \@Project: $myProject\n";
   }
   print FILE "$SecondComment\n";
   print FILE "$SecondComment \@Purpose: \n";
   print FILE "$SecondComment\n";
   print FILE "$SecondComment \@Modification History: \n";
   print FILE "$SecondComment\n";

   for( $i = 1 ; $i < $lowerLine ; $i++)
   {
      print FILE "$SecondComment";
   }
   if( $myType eq "c" || $myType eq "cpp" || $myType eq "h" || 
       $myType eq "ino" || $myType eq "hpp" || $myType eq "java")
   {
      print FILE "$FirstComment\n";
   }else
   {
      print FILE "\n";
   }
   close(FILE);
   #Make scripts executable
   if( $myType eq "pl" || $myType eq "p" || 
       $myType eq "sh" || $myType eq "py" ) {
      chmod (0755, $myName);
   }
}
