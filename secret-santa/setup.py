#!/usr/bin/env python
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
# Author   : Kenneth J. Pronovici <pronovic@ieee.org>
# Project  : Secret Santa
# Revision : $Id: setup.py 1289 2010-12-02 03:08:10Z pronovic $
# Purpose  : Python distutils setup script
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Note that right now, I must BY HAND synchronize the version number
# between secret-santa, Makefile and this file!

######################
# Pydoc documentation
######################

"""
Secret Santa distutils setup script.
"""

__author__  = "Kenneth J. Pronovici"
__date__    = "$Date: 2003/09/08 21:07:25 $"


########################################################################
# Imported modules
########################################################################

from distutils.core import setup


########################################################################
# Setup configuration
########################################################################


LONG_DESCRIPTION = """

A "Secret Santa" exchange is one where a group of a people get together
and each exchange gifts with one other person from that group.  The
exchange assignments are supposed to be secret, so that no one knows
ahead of time who they will get their gift from.  Usually, there's a
small ($5, $10, $15) limit on the size of the gift.  Another name for
this type of exchange is a "grab bag" exchange.

Every Secret Santa exchange has several elements:

   A group of people 
   A "theme" for the exchange
   A maximum cost for each gift
   A date/time that the exchange will take place

We sometimes place limits on the way the exchange is generated.  For
instance, a person should not be assigned themselves as a partner, and
we may sometimes not want to group two other particular people together
(say, husband and wife at a big party).

This script will generate an exchange and then notify the group
partipants of their assignment via email.

"""

setup (

   name             = 'SecretSanta',
   version          = "1.4",
   description      = 'Provide Secret Santa assignments for a group of people',
   long_description = LONG_DESCRIPTION,
   keywords         = ('secret', 'santa', 'christmas', 'grab bag'),

   author           = 'Kenneth J. Pronovici',
   author_email     = 'pronovic@ieee.org',

   url              = 'http://www.cedar-solutions.com:70/software.html',

   licence          = "Copyright (c) 2002-2003,2005,2010 Kenneth J. Pronovici.   Licensed under the GNU GPL.",

   platforms        = ('Any',),

   packages         = None,
   scripts          = ['secret-santa',], 
)

