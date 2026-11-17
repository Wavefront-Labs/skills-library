---
id: computing-software.systems-network-administration.bash.readline-and-inputrc
name: readline-and-inputrc
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, readline, inputrc, bind, key-bindings, vi-mode, emacs-mode, completion-ignore-case, show-all-if-ambiguous, history-search, editing-mode, shell-environment, lpic-1, sysadmin]
level: practitioner
status: gated
description: "Tune the bash command line via readline: ~/.inputrc settings, history prefix search, vi vs emacs modes, bind for custom keys, and the keys worth knowing."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#Command-Line-Editing
  - https://www.gnu.org/software/bash/manual/bash.html#Readline-Init-File
  - https://tiswww.case.edu/php/chet/readline/rluserman.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# readline and ~/.inputrc — the line editor under bash, python, psql and gdb

**Goal:** make completion and history behave the way you want in every readline-based
program at once, and bind keys you actually use.

## 1. A productive ~/.inputrc
```
$include /etc/inputrc                 # keep distro defaults (arrow keys, Home/End)
set completion-ignore-case on         # cd doc<Tab> → Documents
set show-all-if-ambiguous on          # list options on first Tab, not second
set menu-complete-display-prefix on
set colored-stats on                  # ls-style colours in completion lists
set colored-completion-prefix on
set mark-symlinked-directories on
set skip-completed-text on
set bell-style none
set enable-bracketed-paste on         # pasted newlines don't execute (default on in 5.1+)
# search history by typed prefix with Up/Down
"\e[A": history-search-backward
"\e[B": history-search-forward
# Tab cycles through matches
TAB: menu-complete
"\e[Z": menu-complete-backward        # Shift-Tab
$if Bash
  "\C-xr": re-read-init-file
  "\e\C-l": "ls -la\n"               # macro: Alt-Ctrl-L types and runs
$endif
```
Apply without restarting: `bind -f ~/.inputrc`.

## 2. Editing modes
```
set editing-mode vi         # or:  set -o vi  in bash
set show-mode-in-prompt on
set vi-ins-mode-string "\1\e[6 q\2"   # cursor shape in insert
set vi-cmd-mode-string "\1\e[2 q\2"   # block cursor in command mode
```
Emacs mode (default) keys worth knowing: `C-a/C-e` line start/end, `M-b/M-f` word,
`C-w` delete word back, `M-d` forward, `C-u/C-k` kill to start/end, `C-y` yank,
`M-.` last argument, `C-x C-e` edit line in `$EDITOR`, `C-_` undo, `M-#` comment line,
`C-r` reverse search, `M-*` insert all completions.

## 3. bind — inspect and set at runtime
```bash
bind -P | grep -v 'is not bound' | head     # current bindings with function names
bind -p | grep yank-last-arg
bind '"\C-f": forward-word'
bind -x '"\C-g": git status'                # run a shell command on a key (bash only)
bind 'set completion-ignore-case on'
read -e -p "name: " n                       # scripts: -e gives readline editing to read
```
Find a key's escape sequence with `cat -v` or `showkey -a`, or `C-v` then the key in bash.

## 4. Programs that honour inputrc
bash, python REPL, psql, mysql, gdb, bc, sqlite3, ftp — anything linked to readline.
`$if program-name` sections (`$if Python`) scope settings. zsh and fish do not use it.
`INPUTRC=/path` overrides the location; system file is `/etc/inputrc`.

## 5. Completion vs readline
Completion *candidates* come from bash's programmable completion (`complete`,
`bash-completion` package); readline only decides how they are shown/cycled. If `ssh h<Tab>`
offers nothing, install `bash-completion` and source `/etc/bash_completion` — not an
inputrc problem.

## Failure modes
- Arrow keys print `^[[A`: terminal type unknown or `$include /etc/inputrc` missing.
- Setting ignored: typo in name (`bind -v | grep name` lists valid variables), or it is a
  bash `shopt`/`set -o` option, not readline.
- vi mode confusing in `read -e` prompts: scripts inherit the user's mode; set
  `bind 'set editing-mode emacs'` locally if required.
- Pasting multi-line text executes line by line: bracketed paste off (old bash) — upgrade or
  paste into `C-x C-e`.

## Verify
- [ ] `bind -v | grep completion-ignore-case` shows `on` after `bind -f ~/.inputrc`.
- [ ] Typing `ssh` then Up recalls only ssh commands (history-search works).

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; Readline docs fetched as a very large page but key sequences and bind examples were not individually checked. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
