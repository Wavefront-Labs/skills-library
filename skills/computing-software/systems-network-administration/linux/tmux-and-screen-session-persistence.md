---
id: computing-software.systems-network-administration.linux.tmux-and-screen-session-persistence
name: tmux-and-screen-session-persistence
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, tmux, screen, terminal-multiplexer, session-persistence, detach, attach, nohup, long-running-jobs, ssh-disconnect, tmux-conf, panes, windows, scrollback, copy-mode, byobu, lfcs, sysadmin, send-keys, screen-serial]
level: intro
status: docs-checked
description: "Keep long jobs alive across SSH drops with tmux (and GNU screen): sessions, detach/attach, windows and panes, scrollback, the keybindings that matter, tmux.conf essentials."
sources:
  - https://github.com/tmux/tmux/blob/master/tmux.1
  - https://www.gnu.org/software/screen/manual/screen.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# tmux and screen — a shell that outlives your SSH connection

**Goal:** never lose an upgrade, migration or long copy to a dropped SSH session, and
work in several shells on a server from one connection.

Rule of thumb: anything that takes longer than a coffee runs inside tmux. When the
link drops, the tmux server (a normal process on the host) keeps running the job; you
reconnect and attach.

## 1. tmux sessions — the 90% workflow
```bash
tmux new -s upgrade          # new named session
# ... start the long command ...
# Ctrl-b d                   # detach (job keeps running)
tmux ls                      # list sessions on this host
tmux attach -t upgrade       # reattach (tmux a -t upgrade)
tmux attach -d -t upgrade    # reattach and kick other clients (fixes wrong window size)
tmux kill-session -t upgrade
```
Idempotent connect script (attach if it exists, otherwise create):
`tmux new -A -s main`. Put it in `~/.bash_profile` guarded by
`[[ -z $TMUX && -n $SSH_CONNECTION ]]` to auto-enter tmux on every SSH login.

The server socket is `default` in a `tmux-UID` directory under `$TMUX_TMPDIR`, or under `/tmp` if that is unset. After a reboot sessions
are gone — tmux persists across *disconnects*, not reboots. If `tmux ls` says
`no server running` after you are sure you detached, check you are the same user
(`sudo tmux ls` vs `tmux ls`) and the same host.

## 2. Keys (prefix is `Ctrl-b`, written `C-b`)
| Action | Key |
|---|---|
| Detach | `C-b d` |
| New window / next / previous / pick by number | `C-b c`, `C-b n`, `C-b p`, `C-b 0-9` |
| Rename window | `C-b ,` |
| Split pane vertical / horizontal | `C-b %`, `C-b "` |
| Move between panes | `C-b` + arrow, `C-b o` |
| Zoom pane to full window (toggle) | `C-b z` |
| Close pane | `exit` or `C-b x` |
| Scroll / copy mode | `C-b [` then PgUp/arrows, `q` to leave |
| Search in scrollback | in copy mode `C-s` (emacs) or `/` (vi mode) |
| Command prompt | `C-b :` (e.g. `:resize-pane -R 10`, `:setw synchronize-panes on`) |
| List sessions interactively | `C-b s`; windows `C-b w` |

`synchronize-panes` types the same command into every pane — handy for a small fleet
of hosts opened as panes, dangerous if you forget it is on (status bar shows nothing by
default; add it to your status line or toggle it off right after).

## 3. `~/.tmux.conf` essentials
```
set -g history-limit 50000        # default is 2000 lines per pane; applies to new panes only
set -g mouse on                   # click panes, drag to resize, wheel scrolls
set -g base-index 1               # windows start at 1 (keyboard-friendly)
setw -g mode-keys vi              # vi keys in copy mode
set -g default-terminal "tmux-256color"
set -g escape-time 10             # ms to wait after Escape (10 is already the default since tmux 3.5)
bind r source-file ~/.tmux.conf \; display "reloaded"
```
Reload without restarting: `tmux source ~/.tmux.conf`.

## 4. Running jobs the right way inside tmux
- Start the job with logging so you can read what happened while detached:
  `apt full-upgrade 2>&1 | tee ~/upgrade-$(date +%F).log`.
- For "fire and forget" with no interaction, `nohup cmd > out.log 2>&1 &` is simpler than tmux. tmux is for jobs you want to come back and *interact* with.
- Scripted use: `tmux send-keys -t upgrade 'ls' Enter`;
  `tmux capture-pane -p -t upgrade -S -200` grabs the last 200 lines for a ticket.

## 5. GNU screen (when tmux is not installed)
```bash
screen -S upgrade        # new named session
# C-a d                  # detach
screen -ls               # list
screen -r upgrade        # reattach; -d -r to detach elsewhere first; -x to share
screen -L                # log the session to screenlog.0
```
Keys: `C-a c` new window, `C-a n`/`C-a p` cycle, `C-a "` list, `C-a [` copy/scrollback mode,
`C-a k` kill window, `C-a ?` help. `screen` can also open a serial line: give it a tty device and a baud rate, e.g. `screen /dev/ttyUSB0 115200` (see the window types section of the screen manual).

## 6. Gotchas
- **Nested tmux** (tmux on your laptop, tmux on the server): the inner one needs
  `C-b C-b d` (send-prefix) or set a different prefix locally (`set -g prefix C-a`).
- `default-terminal` should be `screen`, `tmux` or a derivative of them (for example `tmux-256color`); if colours or keys break in vim/htop, check that the server has a terminfo entry for the value you set.
- SSH agent forwarding stops working in old shells after reconnecting because
  `SSH_AUTH_SOCK` changed. The `update-environment` option (its default includes `SSH_AUTH_SOCK`) refreshes it on attach, but only new shells see it — run
  `eval "$(tmux show-environment -s SSH_AUTH_SOCK)"` in an old shell.
- `sudo -i` then `tmux` creates sessions as root in a different socket dir; attach with
  the same user you created them as.
- Killing the SSH connection with `~.` is fine; killing the *tmux server*
  (`tmux kill-server`) ends every job.

## Verify
- [ ] Start `tmux new -s t`, run `sleep 600`, close the terminal window entirely,
      SSH back in: `tmux ls` shows `t` and `tmux a -t t` shows `sleep` still running.
- [ ] `C-b [` then PgUp scrolls through at least 10 000 lines of output after
      setting `history-limit`.
- [ ] `tmux capture-pane -p -t t | tail -3` prints the last lines of the session.

## Checked
Checked 2026-10-25 against the tmux manual page source and CHANGES file (tmux/tmux master, latest release 3.8 of 2026-09-09). Confirmed: `new-session -A -s`, `attach-session -d/-r`, `kill-session`, `kill-server`, default key bindings (`d`, `,`, `%`, `"`, `x`, `z`, `s`, `w`), emacs `C-s` search in copy mode, `history-limit` default 2000 lines, `escape-time` default 10 ms (since 3.5 per CHANGES), `update-environment` default including SSH_AUTH_SOCK, `show-environment -s`, `send-keys`, `capture-pane -p -S`, `send-prefix`, `synchronize-panes`, socket location. GNU screen options `-S`, `-ls`, `-r`, `-d -r`, `-x`, `-L`/`screenlog.0`, and the default bindings `C-a d/c/n/p/"/[/k/?` from the screen man page source (an unofficial GitHub mirror, alexander-naumov/screen, last pushed 2024-04) because the GNU manual returned HTTP 429. Removed unconfirmed claims: Shift-drag selection, DEBIAN_FRONTEND advice, systemd-run detail, byobu description, ncurses-term advice.

Method: documentation only; no commands were run.
