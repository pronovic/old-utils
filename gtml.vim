" Vim syntax file
" Language:     gtml 
" Maintainer:   Kenneth J. Pronovici <pronovic@ieee.org>
" Last Change:  $Date: 2002/05/03 21:49:29 $
" Filenames:    *.gtml
" URL:          ftp://cedar-solutions.com/software/gtml.vim
"
" GTML is an HTML preprocessor.  Essentially, it adds #define and
" #include functionality and lets you reference #defined values
" as <<NAME>>.  See http://www.lifl.fr/~beaufils/gtml/ for more
" information.
"
" The syntax is based on the HTML syntax, with a few GTML things added
" in.  I also modify the way HTML highlighting of things like <i></i>
" works, but let the user change them just like the HTML syntax file
" would.  The whole thing works based on the @htmlPreproc functionality
" in the html.vim file.

" Clear previous syntax settings unless this is v6 or above, in which case just
" exit without doing anything.
if version < 600
   syn clear
elseif exists("b:current_syntax")
   finish
endif

" The HTML syntax file included below uses this variable.
if !exists("main_syntax")
   let main_syntax = 'gtml'
endif

" Set up my preferences for highlighting (user can override this)
if !exists("html_my_rendering")
   let html_my_rendering=1
   hi def htmlBold                term=bold cterm=bold gui=bold
   hi def htmlBoldUnderline       term=bold cterm=bold gui=bold
   hi def htmlBoldItalic          term=bold cterm=bold gui=bold
   hi def htmlBoldUnderlineItalic term=bold cterm=bold gui=bold
   hi def htmlUnderline           term=bold cterm=bold gui=bold
   hi def htmlUnderlineItalic     term=bold cterm=bold gui=bold
   hi def htmlItalic              term=bold cterm=bold gui=bold
endif

" Pull in the HTML syntax file.
" The syntax file obeys either my rendering values above, or the user's if set
if version < 600
   so <sfile>:p:h/html.vim
else
   runtime! syntax/html.vim
   unlet b:current_syntax
endif

" Explain to html.vim which preprocessor-language things should be highlighted
syn cluster htmlPreproc add=@gtmlTop

" First, commands (we ignore the \ line continuation character, as I don't know how to deal with it)
syn region gtmlCommand   start="^#include" end="$"
syn region gtmlCommand   start="^#define" end="$"
syn region gtmlCommand   start="^#newdefine" end="$"
syn region gtmlCommand   start="^#undef" end="$"
syn region gtmlCommand   start="^#timestamp" end="$"
syn region gtmlCommand   start="^#mtimestamp" end="$"
syn region gtmlCommand   start="^#literal" end="$"
syn region gtmlCommand   start="^#definechar" end="$"
syn region gtmlCommand   start="^#entities" end="$"
syn region gtmlCommand   start="^#if" end="$"
syn region gtmlCommand   start="^#ifdef" end="$"
syn region gtmlCommand   start="^#ifndef" end="$"
syn region gtmlCommand   start="^#elsif" end="$"
syn region gtmlCommand   start="^#elsifdef" end="$"
syn region gtmlCommand   start="^#elsifndef" end="$"
syn region gtmlCommand   start="^#else" end="$"
syn region gtmlCommand   start="^#endif" end="$"
syn region gtmlCommand   start="^#compress" end="$"
syn region gtmlCommand   start="^#sitemap" end="$"
syn region gtmlCommand   start="^#toc" end="$"

" Then, the actual contants in the code
syn region gtmlConstant  start="<<" end=">>"

" Then, list what @gtmlTop contains
syn cluster gtmlTop contains=gtmlCommand,gtmlConstant

" Set up default highlighting. Almost all of this is done in the HTML syntax file
if version >= 508 || !exists("did_gtml_syn_inits")
   if version < 508
      let did_gtml_syn_inits = 1
      com -nargs=+ HiLink hi link <args>
   else
      com -nargs=+ HiLink hi def link <args>
   endif

   HiLink gtmlCommand Comment
   HiLink gtmlConstant    Comment

   delcommand HiLink
endif

let b:current_syntax = "gtml"

if main_syntax == 'gtml'
   unlet main_syntax
endif

