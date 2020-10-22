; vim: set ft=scheme:
; # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
; #
; #              C E D A R
; #          S O L U T I O N S       "Software done right."
; #           S O F T W A R E
; #
; # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
; #
; # Copyright (c) 2002-2003 Kenneth J. Pronovici.
; # All rights reserved.
; #
; # Portions of this code are based on a similar utility that is
; # (C) Copyright 1999 Rik Hemsley <rik@kde.org> and believed to
; # be released under the GPL.
; #
; # This program is free software; you can redistribute it and/or
; # modify it under the terms of the GNU General Public License,
; # Version 2, as published by the Free Software Foundation.
; #
; # This program is distributed in the hope that it will be useful,
; # but WITHOUT ANY WARRANTY; without even the implied warranty of
; # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
; #
; # Copies of the GNU General Public License are available from
; # the Free Software Foundation website, http://www.gnu.org/.
; #
; # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
; #
; # Author   : Kenneth J. Pronovici <pronovic@ieee.org>
; # Language : Gimp script-fu language (nomimally Scheme)
; # Project  : Gimp graphics utilities
; # Package  : xcf2png
; # Revision : $Id: xcf2png.scm,v 1.5 2003/09/08 20:39:40 pronovic Exp $
; # Purpose  : script-fu script to convert from XCF to PNG
; #
; # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

; ######################################################################
; # Notes
; ######################################################################
;
; This file is meant to be used with the xcf2png kshell script.  Place
; this file in ~/gimp-1.2/scripts (or the appropriate directory for your
; version of Gimp) before running the shell script.
;
; Call (xcf2png "file.xcf" "file.png" "file.xcf.temp") to convert
; file.xcf to PNG format using the highest possible compression.
; Remember to remove file.xcf.temp when you're done.
;
; It should be possible to make the Gimp flatten an XCF image and then
; save it as a PNG file.  However, I can't seem to make it do that in
; just a single step.  Instead, I first save a temporary XCF file that
; is flattened, and then convert that flattened file to PNG format.
;
; I am not much of a Scheme coder.  I guess the code below looks like
; I'm trying to program in C, instead.  Sorry...
;

; ############################
; # _xcf2png_flatten function
; ############################
; Takes an XCF file, flattens it, and saves it to a temporary file

(define ( _xcf2png_flatten xcffile tempfile)
  (let* ( 
          ( image ( car ( gimp-xcf-load 0 xcffile tempfile ) ) )
          ( drawable ( car ( gimp-image-active-drawable image ) ) ) 
        )
    (if ( > ( car ( gimp-image-get-layers image ) ) 1 )
      (gimp-image-flatten image )
    )
    ( gimp-xcf-save 1 image drawable tempfile tempfile ) 
  ) 
)

( script-fu-register "_xcf2png_flatten" 
                     "<Toolbox>/_xcf2png_flatten" 
                     "" "" "" "" "" )


; ############################
; # _xcf2png_flatten function
; ############################
; Converts a flattened XCF file to PNG format.

(define ( _xcf2png_convert xcffile pngfile)
   (let* ( 
           ( image ( car ( gimp-xcf-load 0 xcffile pngfile ) ) )
           ( drawable ( car ( gimp-image-active-drawable image ) ) )
         )
      ( file-png-save 1 image drawable pngfile pngfile 0 9 0 0 0 0 0 )
   ) 
)

( script-fu-register "_xcf2png_convert" 
                     "<Toolbox>/_xcf2png_convert" 
                     "" "" "" "" "" )

; ###################
; # xcf2png function
; ###################
; Converts an XCF file to PNG format

( define ( xcf2png xcffile pngfile tempfile)
  ( _xcf2png_flatten xcffile tempfile)
  ( _xcf2png_convert tempfile pngfile)
  ( gimp-quit 0 ) 
)

( script-fu-register "xcf2png" 
                     "<Toolbox>/xcf2png" 
                     "" "" "" "" "" )

