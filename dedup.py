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
# Copyright (c) 2015 Kenneth J. Pronovici.
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
# Language : Python (>= 2.7)
# Revision : $Id: dedup.py 1378 2015-02-21 21:28:16Z pronovic $
# Purpose  : De-duplicate a set of files in a directory
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

########################################################################
# Imported modules
########################################################################

import hashlib
import glob
import os.path
import shutil
from optparse import OptionParser


########################################################################
# Utility code
########################################################################

# Memory-efficient way to get crypographic hash for a file
# @param path  Path to a file on disk
# See: http://stackoverflow.com/questions/3431825/generating-a-md5-checksum-of-a-file
def cryptohash(path):
   blocksize = 65536
   hasher = hashlib.sha256()
   with open(path, 'rb') as fp:
      buf = fp.read(blocksize)
      while len(buf) > 0:
         hasher.update(buf)
         buf = fp.read(blocksize)
      return hasher.hexdigest()

# Parses command-line arguments.
# This function will not return if command-line arguments are invalid.
# @return Tuple of (duplicatesDir, source-glob)
def handleCommandLine():
   usage = "%prog [--help] duplicatesDir source-glob"
   optionParser = OptionParser(usage=usage)
   (options, args) = optionParser.parse_args()
   if len(args) != 2:
      optionParser.parse_args(["--help"])  # convenient way to get the error message
   return (args[0], args[1])


########################################################################
# Main routine
########################################################################

# Main routine for program
def main():
   (duplicatesDir, sourceGlob) = handleCommandLine()

   print ""
   print "De-duplicating %s" % sourceGlob
   print "Duplicates written to %s" % duplicatesDir

   print ""
   print "Generating crypto hashes for files..."
   hashes = { }
   for path in glob.iglob(sourceGlob):
      hashes[path] = cryptohash(path)

   print ""
   print "Checking for duplicates..."
   for i in glob.glob(sourceGlob):
      if os.path.exists(i):
         print "   Checking %s, hash %s" % (os.path.basename(i), hashes[i])
         for j in glob.glob(sourceGlob):
            if os.path.exists(j):
               if i != j: 
                  if hashes[i] == hashes[j]:
                     print "      Found duplicate %s" % os.path.basename(j)
                     shutil.move(j, duplicatesDir)
   

########################################################################
# Module entry point
########################################################################

# Run the main routine if the module is executed rather than sourced
if __name__ == '__main__':
   main()

