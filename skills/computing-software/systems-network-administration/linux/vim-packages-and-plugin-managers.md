---
id: computing-software.systems-network-administration.linux.vim-packages-and-plugin-managers
name: vim-packages-and-plugin-managers
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, vim, vim-plugins, vim-packages, vim-plug, packadd, neovim, lazy-nvim]
level: practitioner
status: docs-checked
description: "Install vim plugins with native packages (pack/*/start, packadd) or vim-plug, neovim lazy.nvim basics, keeping server vim lean and generating helptags."
sources:
  - https://vimhelp.org/repeat.txt.html#packages
  - https://github.com/junegunn/vim-plug
  - https://github.com/folke/lazy.nvim
  - https://neovim.io/doc/user/pack.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vim packages and plugin managers

## Native packages (vim 8+/neovim, no manager)
```bash
mkdir -p ~/.vim/pack/plugins/start ~/.vim/pack/plugins/opt
git clone --depth 1 https://github.com/tpope/vim-fugitive ~/.vim/pack/plugins/start/vim-fugitive
git clone --depth 1 https://github.com/dense-analysis/ale ~/.vim/pack/plugins/opt/ale
vim -c 'helptags ALL' -c q                  # tags for every doc directory in 'runtimepath'
vim -c 'helptags ~/.vim/pack/plugins/start/vim-fugitive/doc' -c q   # or one plugin at a time
```
`start/` is added to the runtime path and loaded at startup; `opt/` only after `:packadd ale`. `:packadd!` (useful in vimrc) only adds the directory to `runtimepath`, and the plugin is then loaded during initialisation.
Neovim path: `~/.local/share/nvim/site/pack/...`. Update = `git pull` in each dir (or git submodules in a dotfiles repo).

## vim-plug
```vim
call plug#begin()
Plug 'tpope/vim-surround'
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'preservim/nerdtree', { 'on': 'NERDTreeToggle' }   " lazy-load on command
call plug#end()
```
`:PlugInstall` installs, `:PlugUpdate` installs or updates, `:PlugClean` removes plugins no longer listed. `plug#end()` also runs `filetype plugin indent on` and `syntax enable`.

## Neovim lazy.nvim
lazy.nvim records the installed plugin versions in a lockfile, `lazy-lock.json`; commit it.

## Server hygiene
- Keep root's and servers' vim plugin-free: a plain `~/.vimrc` with settings is enough, and every plugin adds startup work.
- `vim -u NONE` skips initialisations and plugins; `vim --clean` also excludes home-directory entries from `runtimepath` and `packpath`. Use them to rule out plugins when something misbehaves.
- `:scriptnames` lists sourced scripts in order; `vim --startuptime st.log` writes timing messages that show where startup time goes (needs the +startuptime feature).

## Verify
- [ ] `:scriptnames` shows the plugin; `:help <plugin>` works (helptags built); `vim --clean` still opens fast.

## Checked

2026-10-26. Documentation checked: Vim runtime/doc help files on vim/vim master (last commit 2026-10-25, Vim 9.2 series). Also: vim-plug README (last commit 2026-10-15), lazy.nvim README, Neovim pack.txt. Confirmed: pack/*/start and opt, :packadd and :packadd! semantics, :helptags ALL and per-directory form, Neovim site/pack path, vim-plug commands and the on/do options, lazy-lock.json, -u NONE, --clean, :scriptnames, --startuptime. Corrected: helptags ALL under -u NONE would not see start packages because plugin loading is skipped; removed :PlugSnapshot, the lazy.nvim layout claims and the modeline remark, none of which the docs confirm.

Method: documentation only; no commands were run.
