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
# @Title: picresize.py
#
# @Author: Phil Smith
#
# @Date: 27-Jul-2013 2:36 AM
#
# @Project: SimpleCV Picture Resize
#
# @Purpose: This script will resize an image or group of images. It must use
#           Python2 due to its reliance SimpleCV.
#           This script will work with any file type supported by SimpleCV's
#           Image type and scale/adaptiveScale functions. 
#
#           Exit Codes:
#           1 - Could not import SimpleCV
#           2 - Non-image file was passed as argument
# @Revision:
# $Id: picresize.py,v 1.4 2013/07/27 19:22:09 alpha Exp $
#
################################################################################
import argparse as ap
from os import mkdir
from os.path import isdir
#
# Setup the templates for warnings, errors, informational and pass/fail
# statements.
#
def _warn_(msg):
  print '[W] ' + msg
def _err_(msg):
  print '[E] ' + msg
def _info_ (msg):
  print '[I] ' + msg
def _pass_(msg):
  print '[+] ' + msg
def _fail_(msg):
  print '[-] ' + msg

#
# The SimpleCV ImageSet is required, quit if it's not installed.
#
try:
  from SimpleCV import ImageSet
  from SimpleCV import Image
except ImportError:
  _err_('Could not import SimpleCV!')
  _info_('(http://www.simplecv.org/download)')
  exit(1)

#
# main()
#
def main( args ):

  #
  # Set these flags so they can be checked for validity later.
  #
  res = None
  fac = None

  #
  # Check for any args that can safely be defaulted.
  #
  if args.dest:
    outdir = args.dest
    #
    # Append a trailing slash if it's not there.
    #
    if outdir[-1] != '/':
      outdir = outdir + '/'
  else:
    outdir = 'scaled_thumbs/'

  #
  # Check for scale or resolution. The default action is to scale
  # by 1/2.
  #
  if args.res:
    (width, height) = args.res.split('x')
    #
    # Just set this to something other than None, so the script can
    # tell whether or not to use the resolution later.
    #
    res = args.res
  elif args.fac:
    #
    # Limit the scale factor so super-large images are made even bigger.
    #
    fac = float(args.fac)
    if fac >= 2.0:
      fac = 2.0
    if fac <= 0.0:
      fac = 0.1
  else:
    fac = .5
  #
  # Make sure the new files have a home.
  #
  if not isdir(outdir):
    mkdir(outdir)
 
  #
  # Load the files from the command line
  #
  images = ImageSet()

  _info_('Adding images to image set... this may take a moment.')
  for item in args.files:
    #
    # Make sure I don't try to convert something that's not an image.
    #
    try:
      image = Image(item)
    except IOError, err:
      _err_("Invalid/unuseable file: " + item)
      exit(2)

    images.append(image)
  _pass_('Completed adding images to image set.')

  #
  # If the scale was given, then just scale the image. If a new resolution
  # was given, then use the adaptiveScale. The image will be resized and
  # padded, if necessary.
  #
  for image in images:
    _pass_("Processing "+image.filename)

    if fac:
      image.scale(fac).save(outdir + image.filename)
    elif res:
      image.adaptiveScale((int(width), int(height))).save(outdir + image.filename)
#
# End of main()
#

#
# Invocation check
#
if __name__ == "__main__":
  #
  # Check for command-line args.
  # 
  descStr = """
  Resize a picture or group of pictures using SimpleCV. The picture(s) can be resized
  using a scaling factor between 0.1 and 2.0, or they can be set to a defined resolution.
  There are no bounds checks on resolutions within this script, so be careful. Resolutions
  also use an adaptive scaling; the final image will be padded if the new resolution is
  not the same aspect ratio. This is an attempt to prevent distortion in the final image.
  The default action of this script is to scale the picture(s) by 1/2.
  """
  parser = ap.ArgumentParser(description=descStr)
  parser.add_argument('-d', '--dest', help='Output directory for scaled images.')
  parser.add_argument('-f', '--fac', help='Scale factor by which the images should be scaled.')
  parser.add_argument('-r', '--res', help='New desired resolution in [width]x[height] format.')
  parser.add_argument('files', nargs='+', help='Files to be converted.')

  args = parser.parse_args()

  main( args )
