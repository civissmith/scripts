" Vim color file
" Maintainer:   Phil Smith <civis.smith@gmail.com>
" Based on Template: http://www.vim.org/scripts/script.php?script_id=106

" your pick:
set background=dark
hi clear
if exists("syntax_on")
    syntax reset
endif
let g:colors_name="achilles"

hi Cursor   cterm=none ctermfg=lightred  ctermbg=none
"hi CursorIM   
"hi Directory   

hi DiffAdd cterm=none ctermfg=black ctermbg=white
hi DiffChange cterm=none ctermfg=yellow ctermbg=none
hi DiffDelete cterm=none ctermfg=black ctermbg=white  
hi DiffText cterm=bold ctermfg=black ctermbg=white

"hi ErrorMsg   
hi VertSplit cterm=none ctermfg=white ctermbg=white
"hi Folded      
"hi FoldColumn   
hi IncSearch   cterm=inverse ctermfg=darkred  ctermbg=none
hi Search  cterm=none ctermfg=darkred  ctermbg=none
"hi LineNr      
"hi ModeMsg      
"hi MoreMsg      
"hi NonText      
hi Question   cterm=bold ctermfg=darkred ctermbg=none
"hi SpecialKey   
"hi StatusLine   
"hi StatusLineNC   
"hi Title      
"hi Visual      
"hi VisualNOS   
"hi WarningMsg   
"hi WildMenu   
"hi Menu      
"hi Scrollbar   
"hi Tooltip      

" syntax highlighting groups
hi Comment cterm=bold ctermfg=green
hi Constant cterm=bold  
hi Identifier  cterm=bold ctermfg=lightblue 
hi Statement   cterm=none ctermfg=yellow
"hi PreProc   
"hi Type      
"hi Special   
"hi Underlined   
"hi Ignore      
"hi Error      
hi ColorColumn cterm=none ctermfg=lightcyan ctermbg=none
hi CursorColumn cterm=none ctermfg=magenta ctermbg=none
hi CursorLine cterm=none ctermfg=yellow ctermbg=none
hi Todo cterm=bold ctermfg=lightcyan ctermbg=black

