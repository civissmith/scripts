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

print STDOUT "Compiling with $compiler!\n";
#
# Use the compiler and start parsing the output.
#

#
# Open a file descriptor to capture the compilation output
#
$compilerArgs = join(" ", @ARGV );
open( COMPILE, "$compiler $compilerArgs 2>&1 |");
print STDOUT "$compilerArgs\n";
while( <COMPILE> ){
   $outLine = $_;

   #
   # Colorize ERROR lines.
   #
   if( $outLine =~ /\s+error:/i ){
      print color("red");
      print $outLine;
      print color("reset");
   }elsif( $outLine =~ /\s+warning/i ) {
      print color("yellow");
      print $outLine;
      print color("reset");
   }else{
      print $outLine;
   }
}
