#!/usr/bin/perl
################################################################################
# @Title: monitorCalc.pl 
#
# @Author: Phil Smith 
#
# @Date: 04-Jun-2011	02:47 PM
#
# @Project: 
#
# @Purpose: Calculate the display width and height given an aspect ratio
#           and diagonal size.
#
# @Modification History: 
# 20110605  PAS Corrected formatting for the case that no units are provided
###############################################################################
use Term::ANSIColor;

# Lets just pass things in from the command line.
# We'll go like this: command <aspect:ration> diagonal

if( @ARGV < 2 || @ARGV > 3 ){
# This is where the USAGE error will go tee hee.
   print STDOUT color("white"),"USAGE: ",color("reset");
   print STDOUT "cmd <";
   print STDOUT color("red"),"aspect",color("reset");
   print STDOUT ":";
   print STDOUT color("red"),"ratio",color("reset");
   print STDOUT "> <";
   print STDOUT color("red"),"diagonal",color("reset");
   print STDOUT "> [<";
   print STDOUT color("yellow blink"),"units", color("reset");
   print STDOUT ">]\n";

   color("reset");
   exit(1);
}
if( !(@ARGV[2] eq undef) ){
   $units = @ARGV[2];
}
# Okay, so I have an aspect ratio and a diagonal... lets
# put them in slush variables just for kicks.
$aspect   = @ARGV[0];
$diagonal = @ARGV[1];

# Now to split the aspect ratio into it's width/height components
# An aspect ratio is expressed 'width:height'.

($width,$height) = split/:/,$aspect;

#print STDOUT "aspect: $aspect\n"; --DEBUG
#print STDOUT "diagonal: $diagonal\n"; --DEBUG
#print STDOUT "width: $width\n"; --DEBUG
#print STDOUT "height: $height\n"; --DEBUG
# Coolio - everything to hear works!

# The width and height are coefficients multiplied by some unknown scalar.
# First things first, we need to find the scalar.
if( ($denom = ($width**2 + $height**2)) != 0 ){
   $scalar = sqrt( $diagonal**2 / $denom);
}else{
   print STDOUT "Hey man, nice shot! You almost divided by $denom!\n";
}
#print STDOUT "scalar: $scalar\n";  --DEBUG
# Coolio - everything to hear works!

$finalWidth  = $width * $scalar;
$finalHeight = $height * $scalar;
$screenArea  = $finalWidth * $finalHeight;
if( $units ){
   printf (STDOUT "Width:%14.2f %s\n",  $finalWidth, $units);
   printf (STDOUT "Height:%13.2f %s\n", $finalHeight, $units);
   printf (STDOUT "Screen Area:%8.2f %s\n", $screenArea, $units);
   
}else{
   printf (STDOUT "Width:\t%12.2f\n", $finalWidth);
   printf (STDOUT "Height:\t%12.2f\n", $finalHeight);
   printf (STDOUT "Screen Area:  %4.2f\n", $screenArea);
}
