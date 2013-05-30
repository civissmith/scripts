""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" @Title: .vimrc
"
" @Author: Phil Smith 
"
" @Date: <UNKNOWN>
"
" @Project: Personal Vim Config
"
" @Purpose: This file sets up various Vim features, shortcuts and preferences
"           based on how I like to Vim.
"
" @Modification History: 
"  Date      Author      Description
"  --------  ----------  ------------------------------------------------------
"  26Jan13   PAS         Added standard header and prepped for Git.
"
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"
" Add a new leader button for more custom commands
" ( This should be BEFORE anything that uses the new leader )
"
let mapleader=','
nnoremap <leader>w :w<CR>
nnoremap <leader>q :wq<CR>
nnoremap <leader>s :s/

"
" Set colorscheme
"
colorscheme desert

"
" Don't reach for ESC
"
inoremap qq <ESC>

"
" auto reload vimrc when editing it
"
autocmd! bufwritepost .vimrc source ~/.vimrc

"
" Sorry Vi, this is Vim's house.
"
set nocompatible

"
" Use the tab key instead of % to move between bracket pairs
"
nnoremap <tab> %
vnoremap <tab> %

inoremap <F1> <ESC>
nnoremap <F1> <ESC>
vnoremap <F1> <ESC>

"
" Setup syntax highlighting, search preferences and whitespace preferences
"
syntax on
set incsearch  " INCremental search
set hls        " HighLight Search 
set smarttab
set ts=3       " Tab Stops
set sw=3       " Shift Width
set sts=3      " Soft Tab Stop - should match shift width
set ignorecase
set smartcase

"
" Setup word wrapping, and window settings
"
set nowrap
set ruler
set background=dark

"
" Prompt if buffer has not been written instead of failing the command
"
set confirm

"
" Setup shortcut keys for splitting, (de)selecting numbers, search highlighting
" buffer switching, window moving and resizing
"
nnoremap <silent> <F4> :vsplit<CR>
nnoremap <silent> <S-F5> :split<CR>
" Fast buffer switching
nnoremap <silent> <F5> :buffers!<CR>:buffer<Space>
nnoremap <silent> <S-F6> :set relativenumber<CR>
"
" Set relativenumber to give lines-from-current instead of absolute
" (>= Vim 7.3)
"
nnoremap <silent> <F6> :set nu<CR>
nnoremap <silent> <F7> :set nonu norelativenumber<CR>
nnoremap <silent> <F8> :set hls<CR>
nnoremap <silent> <F9> :set nohls<CR>
nnoremap <silent> + :exe "resize " . (winheight(0) * 3/2)<CR>
nnoremap <silent> _ :exe "resize " . (winheight(0) * 2/3)<CR>
nnoremap <silent> <S-Up> <C-w>k
nnoremap <silent> <S-Down> <C-w>j
nnoremap <silent> <S-Left> <C-w>h
nnoremap <silent> <S-Right> <C-w>l


"
" Create a file type and preference set for personal "note" files.
"
au BufNewFile,BufRead  *.note :set tw=0 wrap linebreak 
au BufNewFile,BufRead  *.note colorscheme delek

"
" Setup environment for Python Files
"
au BufNewFile,BufRead  *.py :set expandtab ts=2 sw=2 sts=2

"
" Setup Auto-completion
"
inoremap qp <C-P>
inoremap qn <C-N>
inoremap <tab> <C-P>

au VimResized * exe "normal! \<c-w>="
