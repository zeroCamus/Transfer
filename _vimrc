source $VIMRUNTIME/vimrc_example.vim
source $VIMRUNTIME/mswin.vim
behave mswin

set noundofile
set nobackup
set noswapfile

autocmd FileType python setlocal omnifunc=python3complete#Complete
set diffexpr=MyDiff()
function MyDiff()
  let opt = '-a --binary '
  if &diffopt =~ 'icase' | let opt = opt . '-i ' | endif
  if &diffopt =~ 'iwhite' | let opt = opt . '-b ' | endif
  let arg1 = v:fname_in
  if arg1 =~ ' ' | let arg1 = '"' . arg1 . '"' | endif
  let arg2 = v:fname_new
  if arg2 =~ ' ' | let arg2 = '"' . arg2 . '"' | endif
  let arg3 = v:fname_out
  if arg3 =~ ' ' | let arg3 = '"' . arg3 . '"' | endif
  if $VIMRUNTIME =~ ' '
    if &sh =~ '\<cmd'
      if empty(&shellxquote)
        let l:shxq_sav = ''
        set shellxquote&
      endif
      let cmd = '"' . $VIMRUNTIME . '\diff"'
    else
      let cmd = substitute($VIMRUNTIME, ' ', '" ', '') . '\diff"'
    endif
  else
    let cmd = $VIMRUNTIME . '\diff'
  endif
  silent execute '!' . cmd . ' ' . opt . arg1 . ' ' . arg2 . ' > ' . arg3
  if exists('l:shxq_sav')
    let &shellxquote=l:shxq_sav
  endif
endfunction

set nocompatible " 关闭 vi 兼容模式
syntax on " 自动语法高亮

set number " 显示行号
set cursorline " 突出显示当前行
set ruler " 打开状态栏标尺
set shiftwidth=4 " 设定 << 和 >> 命令移动时的宽度为 4

set tabstop=4
set softtabstop=4
set shiftwidth=4
set textwidth=79
set expandtab
set autoindent
set fileformat=unix

set autochdir " 自动切换当前目录为当前文件所在的目录
filetype plugin indent on " 开启插件
set backupcopy=yes " 设置备份时的行为为覆盖
set ignorecase smartcase " 搜索时忽略大小写，但在有一个或以上大写字母时仍保持对大小写敏感
set nowrapscan " 禁止在搜索到文件两端时重新搜索
set incsearch " 输入搜索内容时就显示搜索结果
set hlsearch " 搜索时高亮显示被找到的文本
set noerrorbells " 关闭错误信息响铃
set novisualbell " 关闭使用可视响铃代替呼叫
set t_vb= " 置空错误铃声的终端代码
" set showmatch " 插入括号时，短暂地跳转到匹配的对应括号
" set matchtime=2 " 短暂跳转到匹配括号的时间
set magic " 设置魔术
set hidden " 允许在有未保存的修改时切换缓冲区，此时的修改由 vim 负责保存

set guioptions-=T " 隐藏工具栏
set smartindent " 开启新行时使用智能自动缩进
set backspace=indent,eol,start
" 不设定在插入状态无法用退格键和 Delete 键删除回车符
set cmdheight=1 " 设定命令行的行数为 1
set laststatus=2 " 显示状态栏 (默认值为 1, 无法显示状态栏)
set statusline=\ %<%F[%1*%M%*%n%R%H]%=\ %y\ %0(%{&fileformat}\ %{&encoding}\ %c:%l/%L%)\ 
" 设置在状态行显示的信息
set foldenable " 开始折叠
set foldmethod=syntax " 设置语法折叠
set foldcolumn=0 " 设置折叠区域的宽度
setlocal foldlevel=1 " 设置折叠层数为
" set foldclose=all " 设置为自动关闭折叠 
" nnoremap <space> @=((foldclosed(line('.')) < 0) ? 'zc' : 'zo')<CR>
" 用空格键来开关折叠


" return OS type, eg: windows, or linux, mac, et.st..
function! MySys()
if has("win16") || has("win32") || has("win64") || has("win95")
return "windows"
elseif has("unix")
return "linux"
endif
endfunction

" 用户目录变量$VIMFILES
if MySys() == "windows"
let $VIMFILES = $VIM.'/vimfiles'
elseif MySys() == "linux"
let $VIMFILES = $HOME.'/.vim'
endif

" 设定doc文档目录
let helptags=$VIMFILES.'/doc'

" 设置字体 以及中文支持
if has("win32")


set guifont=Monaco:h12:cANSI
"set guifontwide=微软雅黑:h12:cGB2312
"set gfw=新宋体:h12:cGB2312
endif

" 配置多语言环境
if has("multi_byte")
" UTF-8 编码
set encoding=utf-8
set termencoding=utf-8
set formatoptions+=mM
set fencs=utf-8,gbk

if v:lang =~? '^\(zh\)\|\(ja\)\|\(ko\)'
set ambiwidth=double
endif

if has("win32")
source $VIMRUNTIME/delmenu.vim
source $VIMRUNTIME/menu.vim
language messages zh_CN.utf-8
endif
else
echoerr "Sorry, this version of (g)vim was not compiled with +multi_byte"
endif

" Buffers操作快捷方式!
nnoremap <C-RETURN> :bnext<CR>
nnoremap <C-S-RETURN> :bprevious<CR>

" Tab操作快捷方式!
nnoremap <C-TAB> :tabnext<CR>
nnoremap <C-S-TAB> :tabprev<CR>

"窗口分割时,进行切换的按键热键需要连接两次,比如从下方窗口移动
"光标到上方窗口,需要<c-w><c-w>k,非常麻烦,现在重映射为<c-k>,切换的
"时候会变得非常方便.
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l


" 选中状态下 Ctrl+c 复制
vmap <C-c> "+y

set splitbelow
set splitright
"split navigations
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>


" 有了自动括号插件之后，就不用使用如下设置了
" inoremap ( ()<ESC>i
" inoremap [ []<ESC>i
" inoremap { {}<ESC>i
" inoremap ' ''<ESC>i
" inoremap " ""<ESC>i



let Tlist_Show_One_File=1  
let Tlist_Exit_OnlyWindow=1  

set nocompatible              " required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=D:\Vim\vim80\bundle\Vundle.vim
call vundle#begin('D:\Vim\vim80\bundle')




" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'

Plugin 'vim-scripts/indentpython.vim'
Plugin 'jnurmine/Zenburn'
Bundle 'davidhalter/jedi-vim'
Bundle 'jiangmiao/auto-pairs'
Plugin 'altercation/vim-colors-solarized'
Plugin 'skywind3000/asyncrun.vim'
Plugin 'scrooloose/nerdcommenter'
let g:NERDSpaceDelims = 1 

" Commentary: 快速注释。
" gc注释， gcu取消注释
Plugin 'tpope/vim-commentary'


if has('gui_running')
  set background=dark
  colorscheme solarized
else
  colorscheme Zenburn
endif


" Add all your plugins here (note older versions of Vundle used Bundle instead of Plugin)


Plugin 'scrooloose/nerdtree'
let NERDTreeIgnore=['\.pyc$', '\~$'] "ignore files in NERDTree

map <F6> :w<cr>:NERDTree<cr>
nnoremap <space> za

Plugin 'nvie/vim-flake8'

let python_highlight_all=1
syntax on




" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required

call togglebg#map("<F5>")

map <F9> :call CompileRun()<CR>
    func! CompileRun()
        exec "w"
        if &filetype == 'c'
            exec "!g++ % -o %<"
            exec "!%<"
        elseif &filetype == 'cpp'
            exec "!g++ % -o %<"
            exec "!%<"
        elseif &filetype == 'java'
            exec "!javac %"
            exec "!java %<"
        elseif &filetype == 'sh'
            :!time bash %
        elseif &filetype == 'python'
            exec "!python %"
        elseif &filetype == 'go'
    "        exec "!go build %<"
            exec "! go run %"
        
        endif
    endfunc

map <F10> :call AsyncRun()<CR>
    func! AsyncRun()
        exec "w"
        if &filetype == 'c'
            exec "AsyncRun g++ % -o %<"
            exec "AsyncRun %<"
        elseif &filetype == 'cpp'
            exec "AsyncRun g++ % -o %<"
            exec "AsyncRun %<"
        elseif &filetype == 'java'
            exec "AsyncRun javac %"
            exec "AsyncRun java %<"
        elseif &filetype == 'sh'
            :AsyncRun time bash %
        elseif &filetype == 'python'
            exec "AsyncRun python %"
        elseif &filetype == 'go'
    "        exec "AsyncRun go build %<"
            exec "AsyncRun  go run %"
        
        endif
    endfunc