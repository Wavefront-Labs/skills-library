---
id: computing-software.systems-network-administration.linux.vim-global-and-normal-batch-edits
name: vim-global-and-normal-batch-edits
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, vim, vim-global-command, ex-commands, normal-command, batch-editing, ex-mode, vim-scripting]
level: advanced
status: docs-checked
description: "Batch-edit files in vim with :g/:v, :normal, ranges and :argdo/:cdo, plus non-interactive ex/vim -es runs for scripted config changes."
sources:
  - https://vimhelp.org/repeat.txt.html#:global
  - https://vimhelp.org/various.txt.html#:normal
  - https://vimhelp.org/editing.txt.html#:argdo
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# :g, :normal and batch edits

## Global command
`:[range]g/pattern/cmd` runs an Ex command on every matching line; `:v/pattern/` (or `:g!`) on non-matching.
```vim
:g/^\s*#/d                      " delete comment lines
:v/\S/d                         " delete blank lines
:g/DEBUG/s/true/false/          " substitute only on lines containing DEBUG
:g/^server {/,/^}/ y A          " append every server block to register a
:g/^/m0                         " reverse the file
:g/pattern/t$                   " copy matching lines to the end
:g/^Host /normal A  # managed   " append text to matching lines
```
## :normal
Run normal-mode keys on lines: `:%norm A;` (append ; to every line), `:'<,'>norm I# ` (comment a selection),
`:g/^key=/norm f=lC"redacted"`. Use `:exe "norm ..."` to include special keys like `\<Esc>`.

## Ranges
`:%` whole file, `:.,+5`, `:'<,'>` visual, `:/start/,/end/` pattern range, `:10,$`.

## Many files
```vim
:args /etc/nginx/sites-available/*
:argdo %s/listen 80;/listen 8080;/ge | update
:vimgrep /ssl_protocols/ **/*.conf | cdo s/TLSv1 //g | update
```
## Non-interactive (scripts)
```bash
vim -e -s -c '%s/^PermitRootLogin.*/PermitRootLogin no/' -c 'wq' /etc/ssh/sshd_config
ex -s +'g/^#/d' +'wq' file.conf
```
`-s` (silent/batch mode) only applies when Vim was started as `ex` or after `-e`; it switches off prompts and messages. If Vim appears stuck, type `qa!` and Enter.

## Gotchas
- `:g` first marks every matching line, then runs the command on each marked line; a deleted line loses its mark. Undo reverts the whole `:g` in one step.
- `:normal` arguments must be a complete command (an unfinished insert is aborted as if Esc was typed), cannot start with a space, and `:normal` cannot be followed by `|`.
- The `e` flag in `:s///ge` suppresses the "pattern not found" error that would otherwise stop `:argdo` on a file without a match.

## Verify
- [ ] Run on a copy first; `diff -u` shows only the intended changes.

## Checked

2026-10-26. Documentation checked: Vim runtime/doc help files on vim/vim master (last commit 2026-10-25, Vim 9.2 series). Confirmed: :g, :g! and :v semantics and mark-then-run behaviour (repeat.txt), :normal rules and the :execute alternative (various.txt), :argdo, :cdo, :vimgrep, :bufdo (editing.txt, quickfix.txt), the s///e flag (change.txt), and -e/-s batch mode with ex (starting.txt). Removed the unconfirmed advice to prefer sed or Ansible.

Method: documentation only; no commands were run.
