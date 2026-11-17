---
id: computing-software.systems-network-administration.linux.tmux-plugins-and-session-restore
name: tmux-plugins-and-session-restore
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, tmux, tmux-plugins, tpm, tmux-resurrect, tmux-continuum, session-restore, terminal-multiplexer, sysadmin]
level: practitioner
status: docs-checked
description: "Extend tmux with TPM and bring sessions back after a reboot using tmux-resurrect and tmux-continuum: install, save/restore keys, what is and isn't restored."
sources:
  - https://github.com/tmux-plugins/tpm
  - https://github.com/tmux-plugins/tmux-resurrect
  - https://github.com/tmux-plugins/tmux-continuum
  - https://github.com/tmux/tmux/blob/master/tmux.1
  - https://github.com/tmux/tmux/blob/master/CHANGES
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tmux plugins and session restore

**Goal:** a jump host or workstation where your windows, panes and working directories come
back after a reboot or tmux server crash.

## 1. Install TPM (plugin manager)
```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```
```tmux
# ~/.tmux.conf  (or $XDG_CONFIG_HOME/tmux/tmux.conf, searched from tmux 3.2)
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @continuum-restore 'on'          # auto-restore when the tmux server starts
set -g @continuum-save-interval '15'    # minutes (the default); '0' disables autosave
set -g @resurrect-capture-pane-contents 'on'
set -g @resurrect-processes 'ssh psql "~journalctl -f"'   # extra programs to relaunch
run '~/.tmux/plugins/tpm/tpm'           # MUST be the last line
```
```bash
tmux source ~/.tmux.conf
```
Inside tmux: `prefix + I` installs plugins, `prefix + U` updates, `prefix + alt-u` removes
ones no longer listed.

## 2. Save and restore
- `prefix + Ctrl-s` save, `prefix + Ctrl-r` restore (resurrect).
- Saves are kept in `~/.tmux/resurrect/` or `~/.local/share/tmux/resurrect` (unless `$XDG_DATA_HOME` says otherwise); change it with `set -g @resurrect-dir '/some/path'` (only `$HOME`, `$HOSTNAME` and `~` are expanded). Save files are timestamped; to roll back, start a fresh tmux, symlink `last` to the wanted file (`ln -sf <file> last`) and press `prefix + Ctrl-r`.
- continuum saves in the background every 15 minutes by default (it needs the status line on, because it hooks `status-right`; put it last in the plugin list so themes do not overwrite `status-right`). With `@continuum-restore 'on'`, restore happens only when the tmux server starts. `set -g @continuum-boot 'on'` starts the tmux server at boot via systemd on Linux (it does not start a terminal emulator).

## 3. What comes back
Sessions, windows and their order, pane layouts (even zoomed), working directories, active panes and windows, grouped sessions, and a conservative default list of programs (`vi vim nvim emacs man less more tail top htop irssi weechat mutt`) plus whatever is in `@resurrect-processes` (quote programs with arguments; prefix `~` to match a process containing the name; `:all:` restores everything and is dangerous). Pane contents are saved only with `@resurrect-capture-pane-contents 'on'`. Vim and neovim sessions restore with `set -g @resurrect-strategy-vim 'session'` (or `-nvim`) when a `Session.vim` exists, for example written by vim-obsession.

## Gotchas
- `run '…/tpm'` above any `set -g @plugin` lines = plugins silently not loaded.
- Plugins are shell scripts from GitHub — on shared/bastion hosts pin a commit or vendor them.
- resurrect is idempotent: it does not restore panes or windows that already exist (the one exception is a server started with a single pane). Rolling back to an older save needs a fresh tmux instance.
- TPM, resurrect and continuum require tmux 1.9 or newer; check `tmux -V`.
- With pane-content capture on, `default-command` must not contain `&&` or `||`.

## Verify
- [ ] `ls ~/.tmux/plugins/` lists the plugins after `prefix + I`.
- [ ] `tmux kill-server; tmux` restores the previous windows and paths.
- [ ] The resurrect directory gets a new save file every interval.

## Checked
Checked 2026-10-25 against the READMEs and docs of tmux-plugins/tpm, tmux-resurrect and tmux-continuum on GitHub (latest commits: resurrect 2023-03-06, continuum 2024-01-20, tpm 2026-05-17 per the GitHub API; the plugins are maintained sparsely, so verify behaviour on your tmux version) and the tmux CHANGES file (XDG config path added in 3.2). Confirmed: TPM clone path, `run` line placement at the bottom, `prefix + I`, `prefix + U`, `prefix + alt-u`, requirement tmux 1.9 + git + bash; resurrect key bindings, saved items, default program list, `@resurrect-processes` syntax, `@resurrect-capture-pane-contents`, `@resurrect-strategy-vim`, save directory and `@resurrect-dir`, `last` symlink rollback; continuum 15-minute default and `@continuum-save-interval` in minutes, `@continuum-restore` on server start only, status-right hook caveat, `@continuum-boot` with systemd. Removed unconfirmed claims: the idea that restoring into a populated server duplicates windows (the README says the opposite) and the systemd user-unit suggestion.

Method: documentation only; no commands were run.
