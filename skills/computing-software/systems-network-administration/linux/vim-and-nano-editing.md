---
id: computing-software.systems-network-administration.linux.vim-and-nano-editing
name: vim-and-nano-editing
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, vim, vi, nano, editor, text-editor, vimrc, nanorc, visudo, vipw, sudoedit, swap-file, recovery, search-replace, config-editing, editor-env, update-alternatives, lpic-1, sysadmin, visual-mode, visual-block]
level: intro
status: draft
description: "Edit server configs with vim and nano safely: essential vi commands, search/replace, swap-file recovery, sudoedit/visudo, validating before leaving, and the default editor."
sources:
  - https://vimhelp.org/usr_02.txt.html
  - https://www.nano-editor.org/dist/latest/nano.html
  - https://man7.org/linux/man-pages/man8/visudo.8.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# vim and nano — edit a config on a server and leave it in a working state

**Goal:** make a precise change to a file on a machine with no GUI, save it, and
not leave behind swap files, broken syntax or a root-owned mess.

## 1. vim: the minimum that is not a toy
`vi` on RHEL-family minimal installs is `vim-minimal` (no syntax highlighting, no
`:set` niceties); `dnf install vim-enhanced` gives `vim`. Debian ships `vim.tiny` as
`vi`; `apt install vim` for the real one.

Modes: **Normal** (default; keys are commands), **Insert** (`i`, typing goes into the
file), **Command-line** (`:`). `Esc` always returns to Normal. If the screen seems
frozen, you are probably in a half-typed command — press `Esc` twice.

| Task | Keys (Normal mode) |
|---|---|
| Insert before/after cursor, at line start/end, new line below/above | `i` `a` `I` `A` `o` `O` |
| Save / save and quit / quit without saving / force | `:w` `:wq` (or `ZZ`) `:q!` `:w!` |
| Undo / redo | `u` / `Ctrl-r` |
| Delete line / N lines / to end of line / word | `dd` `5dd` `D` `dw` |
| Copy (yank) line, paste below/above | `yy` `p` `P` |
| Go to line N / top / bottom / line start / end | `:N` or `NG` `gg` `G` `0` `$` |
| Search forward/back, next/prev match | `/pattern` `?pattern` `n` `N` |
| Replace on current line / whole file / confirm each | `:s/old/new/` `:%s/old/new/g` `:%s/old/new/gc` |
| Comment out lines 10–20 | `:10,20s/^/#/` |
| Visual select (char/line/block), then `d`/`y`/`>` | `v` `V` `Ctrl-v` |
| Show line numbers / turn off | `:set nu` `:set nonu` |
| Open another file / show current file path | `:e file` `Ctrl-g` |
| Run shell command, insert its output | `:!cmd` `:r !cmd` |
| Write as root when you forgot sudo | `:w !sudo tee % >/dev/null` then `:e!` |

Search/replace uses vim regex: `\(`, `\)`, `\+` need backslashes by default, `.` and
`*` do not. Use another delimiter for paths: `:%s#/old/path#/new/path#g`.

Paste from the clipboard without auto-indent cascading: `:set paste`, paste, `:set
nopaste` — or `vim --clean` for a pristine session.

## 2. Recovering from a crash: swap files
vim writes `.<name>.swp` beside the file. If you open a file and see
`E325: ATTENTION ... Found a swap file`: another vim has it open (check the PID shown,
`ps -p <pid>`) or a previous session died. Choose `R` to recover unsaved edits,
inspect them, `:w`, then delete the swap (`:e` after `D`, or `rm .name.swp`). Never
leave swap files in `/etc` — some daemons (`sshd` for `sshd_config.d/*.conf`,
`sysctl --system` for `sysctl.d/*.conf`) ignore them, but `apt`/`sudoers.d` and
`cron.d` can choke on stray files. `vim -r` lists recoverable swap files.

## 3. `~/.vimrc` for servers (short, safe)
```vim
syntax on
set number ruler showcmd
set hlsearch incsearch ignorecase smartcase
set tabstop=4 shiftwidth=4 expandtab      " not for Makefiles; vim detects those
set backspace=indent,eol,start
set nocompatible
```
Put it in `/root/.vimrc` too if you edit as root. YAML: `autocmd FileType yaml setlocal
ts=2 sw=2`. Do not install plugin managers on production hosts.

## 4. nano: fewer surprises, fewer powers
`nano file`. Bottom bar shows shortcuts; `^` means Ctrl, `M-` means Alt.
- Save `Ctrl-o` (confirm filename with Enter), exit `Ctrl-x`, cut line `Ctrl-k`, paste
  `Ctrl-u`, search `Ctrl-w`, set the mark to select text with `Alt-a` or `Ctrl-6` then move
  the cursor. The bottom bar lists the other shortcuts.
- Useful flags: `nano -l` line numbers, `-w`/`--nowrap` (old versions wrap long
  lines and silently break configs — on nano < 4 always pass `-w`), `-m` mouse,
  `-B` backup (`file~`), `-T 4 -E` tabs as 4 spaces.
- `/etc/nanorc` or `~/.nanorc`: `set linenumbers`, `set tabsize 4`, `set tabstospaces`,
  `include "/usr/share/nano/*.nanorc"` for syntax colouring.
- A dropped SSH session can lose unsaved edits; with `-B` you
  at least get the previous version.

## 5. Editing privileged files safely
- `sudoedit /etc/foo.conf` (= `sudo -e`) copies the file to a temp, opens it as **you**
  with **your** editor config, and writes back on exit — no root-owned swap files, no
  root `.vimrc` needed, and `:!cmd` inside vim does not run as root.
- `visudo` (sudoers), `vipw`/`vigr` (passwd/group), `crontab -e`, `systemctl edit`
  lock the file and syntax-check before saving. `visudo -f /etc/sudoers.d/ops` for
  drop-ins. A sudoers syntax error locks everyone out of sudo; visudo's "What now?"
  prompt — press `e` to re-edit, never `Q`.
- Set the editor those tools use: `export EDITOR=vim VISUAL=vim` in
  `~/.bash_profile`; `sudo` keeps `EDITOR` only if `env_keep` allows it, otherwise
  `sudoedit` uses `SUDO_EDITOR`/`VISUAL`/`EDITOR` from your environment and `visudo`
  falls back to vi. System-wide default on Debian:
  `sudo update-alternatives --config editor`.

## 6. Check before you leave
Validate the config you just edited with the daemon's own checker:
`sshd -t`, `nginx -t`, `apachectl configtest`, `visudo -c`, `named-checkconf`,
`systemd-analyze verify unit.service`, `python -c 'import yaml,sys;yaml.safe_load(open(sys.argv[1]))' file.yml`.
Keep a copy first for anything you cannot validate: `cp -a file file.bak-$(date +%F)`.

## Verify
- [ ] `vim /tmp/t.conf`, insert two lines, `:%s/foo/bar/g`, `:wq` — file contains the change.
- [ ] `ls -a /etc | grep '\.swp$'` is empty after editing in `/etc`.
- [ ] `sudoedit /etc/hosts` opens in your editor and `ls -l /etc/hosts` is still `root:root 644`.
- [ ] `nano --version` ≥ 4, or every nano invocation on configs uses `-w`.
