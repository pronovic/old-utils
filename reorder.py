#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# vim: set ft=python ts=3 sw=3 expandtab:
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#              C E D A R
#          S O L U T I O N S       "Software done right."
#           S O F T W A R E
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Copyright (c) 2010-2011 Kenneth J. Pronovici.
# All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License,
# Version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# Copies of the GNU General Public License are available from
# the Free Software Foundation website, http://www.gnu.org/.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Authors  : Kenneth J. Pronovici <pronovic@ieee.org>
# Language : Python (>= 2.7), plus PIL (Python Imaging Library)
# Revision : $Id: reorder.py 1336 2013-07-27 19:16:21Z pronovic $
# Purpose  : Reorder images by their EXIF creation date.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

########################################################################
# Notes
########################################################################

"""
This program reorders the images in a directory by their EXIF creation date.
This is useful if you are trying to cull through a set of pictures taken by
more than one camera and turn them into one cohesive image gallery.
@author: Kenneth J. Pronovici <pronovic@ieee.org>
"""


########################################################################
# Imported modules
########################################################################

# System modules
import sys
import os
import re
import math
import shutil
from datetime import datetime
from datetime import timedelta

# PIL modules (Python Imaging Library)
import Image   
from ExifTags import TAGS


#######################################################################
# Functions
#######################################################################

def usage():
   """Prints out program usage information."""
   print ""
   print "Usage: %s source-dir target-dir [offsets]" % os.path.basename(sys.argv[0])
   print ""
   print "Finds all image files in source-dir and reorders them into"
   print "target-dir based on EXIF creation date.  The target directory"
   print "will be created if it does not already exist."
   print ""
   print "You may optionally provide offsets by camera model, in case"
   print "the clocks on your cameras are not in sync.  Use the format"
   print "\"model=+/-hours:minutes\", for instance \"PowerShot A70=+06:55\"."
   print "The configured number of hours and minutes will be added to or"
   print "subtracted from the actual time on the camera."

def findImages(sourcedir, offsets):
   """
   Recurses through a directory, building a list of image files in it.
   @param sourcedir: Source directory to recurse through
   @param offsets: Configured offsets as from parseOffsets()
   @returns: List of (filename, EXIF creation date) tuples.
   """
   images = []
   def visit(items, dir, entries):
      for entry in entries[:]:
         filename = os.path.join(dir, entry)
         if os.path.isfile(filename):
            exifCreationDate = getExifCreationDate(filename, offsets)
            if exifCreationDate is not None:
               images.append((filename, exifCreationDate))
   os.path.walk(sourcedir, visit, images)
   return images

def copyImages(images, targetdir):
   """
   Copies images into the target directory, ordering them by EXIF creation date.
   @param images: List of image tuples, as from findImages()
   @param targetdir: Target directory to write images into
   """
   prefix = "image"
   if not os.path.exists(targetdir):
      os.makedirs(targetdir)
   digits = digitsRequired(len(images))
   images.sort(key=lambda x: x[1])
   index = 0
   for image in images:
      index += 1
      source = image[0]
      prepend = prefix + '{0:0{digits}}__'.format(index, digits=digits)
      target = os.path.join(targetdir, prepend + os.path.basename(source))
      shutil.copyfile(source, target)
#      print "%s\t%s\t%s" % (image[0], image[1], prepend + os.path.basename(source))

def getExifCreationDate(filename, offsets):
   """
   Get the EXIF creation date for a file.
   If the file is not an image, then we'll just return None.
   @param filename: Absolute path to a file
   @param offsets: Configured offsets as from parseOffsets()
   @return: EXIF creation date, or None if there is no such information.
   """
   dateTime = None
   cameraModel = None
   try:
      i = Image.open(filename)
      info = i._getexif()
      keymap = { }
      if info is not None:
         for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            keymap[decoded] = value
         # Some cameras have DateTimeOrignal, and some only have DateTime.  On
         # the ones that have DateTimeOriginal, it looks like DateTime might be
         # different (newer), possibly because the file was modified on the
         # camera or something.  We definitely want to use DateTimeOriginal if
         # we have it.
         if keymap.has_key("DateTimeOriginal"):
            dateTime = keymap["DateTimeOriginal"]
         elif keymap.has_key("DateTime"):
            dateTime = keymap["DateTime"]
         if keymap.has_key("Model"):
            cameraModel = keymap["Model"]
   except IOError: pass
   if dateTime is None:
      sys.stderr.write("Warning, file has no date/time: %s\n" % filename)
      return None
   else:
      exifCreationTime = datetime.strptime(dateTime, "%Y:%m:%d %H:%M:%S")
      if cameraModel in offsets:
         exifCreationTime += offsets[cameraModel]
      return exifCreationTime

def digitsRequired(value):
   """Returns the number of digits required to represent a number."""
   return int(math.ceil(math.log(value+1, 10)))

def parseOffsets(args):
   """
   Parse offsets from the command-line.

   Offsets are int the form "model=[+-]hours:minutes".  For instance, use
   "Canon PowerShot A70=+06:55" to add 6 hours 55 minutes to the times in
   images shot by model "Canon PowerShot A70".  Of course, this falls apart
   if you have two separate cameras that have the same model.
   
   @param args: Command-line arguments to be parsed.

   @return: Map of model to timedelta that should be added to the actual time.
   """
   offsets = { }
   pattern = re.compile(r"(^)(.*)(=)([+-])([0-9][0-9])(:)([0-9][0-9])($)")
   for arg in args:
      result = pattern.match(arg)
      if result is None:
         raise Exception("Invalid offset configuration")
      cameraModel = result.group(2)
      plusOrMinus = result.group(4)
      hours = int(result.group(5))
      minutes = int(result.group(7))
      delta = timedelta(hours=hours, minutes=minutes)
      if plusOrMinus == "-":
         delta *= -1
      offsets[cameraModel] = delta
   return offsets


##################
# main() function
##################

def main():

   """Main routine for program."""

   offsets = { }

   try:
      sourcedir = sys.argv[1]
      targetdir = sys.argv[2]
      offsets = parseOffsets(sys.argv[3:])
   except Exception, e:
      usage()
      sys.exit(1)

   print "Building list of image files in: %s" % sourcedir
   images = findImages(sourcedir, offsets)
   if len(images) == 0:
      print "Completed -- no images to process"
   else:
      print "Copying %d images to target: %s" % (len(images), targetdir)
      sets = copyImages(images, targetdir)
      print "Completed -- finished copying all images"
      

########################################################################
# Module entry point
########################################################################

# Run the main routine if the module is executed rather than sourced
if __name__ == '__main__':
   main()

