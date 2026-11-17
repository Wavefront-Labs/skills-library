---
id: computing-software.systems-network-administration.linux.vim-registers-macros-buffers-and-splits
name: vim-registers-macros-buffers-and-splits
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, vim, vi, vim-registers, vim-macros, vim-buffers, vim-splits, vim-windows, text-editor, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Work faster in vim on servers: named and special registers, recording and replaying macros across many lines or files, buffers, windows and splits."
sources:
  - https://vimhelp.org/change.txt.html#registers
  - https://vimhelp.org/repeat.txt.html#recording
  - https://vimhelp.org/windows.txt.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vim: registers, macros, buffers and splits

**Goal:** edit several config files at once and apply a repeated change to hundreds of lines
without leaving vim (or installing anything on the server).

## 1. Registers
| Register | Holds |
|---|---|
| `""` | unnamed: last delete/yank |
| `"0` | last **yank** (survives later deletes — paste with `"0p`) |
| `"1`–`"9` | most recent deletes or changes of a line or more (each new delete shifts 1 into 2, 2 into 3, ...); `"-` holds smaller deletes |
| `"a`–`"z` | named; `"A` **appends** to `a` |
| `"+` / `"*` | system clipboard / X selection (only with `+clipboard` builds; `vim --version`) |
| `".` `":` `"%` | read-only: last insert, last command line, current file name (usable with `p`, `P`, `:put`, Ctrl-r) |
| `"/` | last search pattern |
| `"_` | black hole — delete without clobbering registers |
```vim
"ayy        " yank line into a          "Ayy   " append another line to a
"ap         " paste a                    :reg a  " show it   (:reg alone lists all)
Ctrl-r a    " in insert or : mode, insert contents of register a
"_dd        " delete line without touching ""
```

## 2. Macros
```vim
qa          " start recording into register a
...edits... " use motions that generalise: 0, w, f, /pattern, not arrow-key counts
j           " move to the next target line as part of the macro
q           " stop
@a  @@  50@a " replay, repeat last, replay 50 times
:5,40norm @a        " run on each line of a range
:g/^Listen/norm @a  " run on every matching line
:argdo exe "norm @a" | update   " across all files in the arg list (vim *.conf)
```
Edit a macro: `:let @a = substitute(@a, 'foo', 'bar', '')` (`:let @{reg} = {expr}`) or paste it (`"ap`), fix the text,
yank back with `"ay$`. Do not use the recording register for `y` or `p` while recording or replaying it: the put pastes the macro and the yank overwrites it. Recording is not possible while a register is executing, nor inside `:normal` or a mapping. Replaying a register works like a mapping, so undo may not sync the same way as typed commands.

## 3. Buffers
```vim
:e /etc/nginx/nginx.conf   :ls   :b 2   :b ngi<Tab>   :bn  :bp   :bd
:set hidden                " switch buffers without saving first
:bufdo %s/old/new/ge | update
```

## 4. Windows and splits
```vim
:sp file   :vsp file   Ctrl-w s / Ctrl-w v      " split current
Ctrl-w h/j/k/l  Ctrl-w w                         " move between windows
Ctrl-w =   Ctrl-w _   Ctrl-w |   :resize 10      " equalise / maximise
Ctrl-w o  (:only)   Ctrl-w c (:close)   Ctrl-w x (swap)
:windo set nu
vim -o a b   vim -O a b    " open files in horizontal / vertical splits
```
Tab pages (`:tabe`, `gt`) each hold their own set of windows.

## Gotchas
- `:q` closes a window, not the buffer; `:qa` / `:wqa` for all.
- `"+` and `"*` exist only in builds with the clipboard feature (`+clipboard`).

## Verify
- [ ] `:reg a` shows the macro you expect before running `100@a`.
- [ ] `:ls` lists every file you opened; `:wa` writes them all.

## Checked

2026-10-26. Documentation checked: Vim runtime/doc help files on vim/vim master (last commit 2026-10-25, Vim 9.2 series). Confirmed: register types and behaviour (change.txt: unnamed, numbered 0-9 shifting, small delete, named with uppercase append, read-only . : %, black hole, search, + and * with +clipboard), q and @ semantics and the recording-register warning (repeat.txt), :let @reg (eval.txt), :normal limits (various.txt), buffer and window commands (windows.txt), :wqa and :qa (editing.txt), vim -o/-O (starting.txt), tab pages (tabpage.txt). Corrected: :argdo norm @a | update would pass the pipe to :normal, so the example now uses :exe. Removed the unconfirmed recursive-macro claim, the insert-mode gotcha and the OSC 52 hint.

Method: documentation only; no commands were run.
