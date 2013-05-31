#!/usr/bin/perl
################################################################################
# @Title: compile.pl 
#
# @Author: Phil Smith 
#
# @Date: 27-May-2013	09:43 PM
#
# @Project: Compile
#
# @Purpose: This script cleans up the output from GCC and G++. It colorizes
#           errors and warnings to make it a little more readable.
#
# @Modification History: 
# $Id: compile.pl,v 1.2 2013-05-28 16:18:53 alpha Exp $
###############################################################################
require Term::ANSIColor;
use Term::ANSIColor;

#
# The first thing I need is to determine which compiler to run. This will
# be given from the command line.
#
# Shift the argument vector so that the rest of the flags will stay in line.
$compiler = shift(@ARGV);

#
# Exit if no compiler is specified.
#
die "FATAL: No compiler specified! Exiting!\n" if $compiler eq undef;

#
# Check to make sure that the argument I caught was the compiler.
#
if( $compiler ne "g++" && $compiler ne "gcc" ){
   print STDERR "Unrecognized compiler( $compiler )\n!";
   exit(1);
}

#
# Open a file descriptor to capture the compilation output
#
$compilerArgs = join(" ", @ARGV );
open( COMPILE, "$compiler $compilerArgs 2>&1 |");
while( <COMPILE> ){
   $outLine = $_;

   #
   # Colorize ERROR and WARNING lines.
   #

   #
   # For ERROR and WARNING lines, split out the error level and reformat the
   # line to make the level more prominent.
   #
   if( $outLine =~ /\s+error:/i ){

      ($fileInfo, $text ) = split(/\s+error:/, $outLine);
      print color("BOLD RED");
      print "ERROR: ";
      print color("reset");
      ($fileName, $lineNo ) = split(/:/, $fileInfo);
      print "File: ";
      print color("BOLD RED");
      print "$fileName";
      print color("reset");
      print ", Line: ";
      print color("BOLD RED");
      print "$lineNo";
      print color("reset");
      print " >> $text";    # Contains diagnosis info

   }elsif( $outLine =~ /\s+warning:/i ) {

      ($fileInfo, $text ) = split(/\s+warning:/, $outLine);
      print color("BOLD YELLOW");
      print "WARNING: ";
      print color("reset");
      ($fileName, $lineNo ) = split(/:/, $fileInfo);
      print "File: ";
      print color("BOLD YELLOW");
      print "$fileName";
      print color("reset");
      print ", Line: ";
      print color("BOLD YELLOW");
      print "$lineNo";
      print color("reset");
      print " >> $text";    # Contains diagnosis info

   }else{

      #
      # Don't change any normal lines.
      #
      print $outLine;
   }
}
