---
id: computing-software.systems-network-administration.linux.screenrc-configuration
name: screenrc-configuration
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, screen, screenrc, gnu-screen, hardstatus, scrollback, multiuser]
level: practitioner
status: docs-checked
description: "Configure GNU screen with ~/.screenrc and /etc/screenrc: scrollback, hardstatus bar, startup windows, escape key, logging, multiuser ACLs, and screen vs tmux on legacy hosts."
sources:
  - https://man7.org/linux/man-pages/man1/screen.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# screenrc configuration

GNU screen is still the multiplexer on many old and minimal hosts.

## ~/.screenrc
```
startup_message off
defscrollback 10000                # default is 100 lines
vbell off
escape ^Aa                      # default; ^Bb if Ctrl-A (line start) conflicts with your shell use
hardstatus always lastline
hardstatus string '%{= kG}[%H] %{w}%-w%{r}(%n %t)%{w}%+w %=%{y}%Y-%m-%d %c'
termcapinfo xterm* ti@:te@      # let the terminal scrollback work
# windows at start
screen -t shell 0
screen -t logs 1 tail -F /var/log/messages
select 0
logfile $HOME/screenlog.%n.%Y%m%d
deflog off
```
Reload in a running session: `C-a :source ~/.screenrc`.

## Useful commands
| Keys | Action |
|---|---|
| `C-a c` / `C-a "` | new window / window list |
| `C-a A` | rename window |
| `C-a [` | copy/scrollback mode (`/` search) |
| `C-a H` | toggle logging current window |
| `C-a S` / `C-a |` / `C-a tab` | split horizontal / vertical / move focus |
| `C-a d` | detach |
`screen -ls`, `screen -r name`, `screen -x name` (attach to an attached session), `screen -dmS job cmd` (start detached).

## Multiuser
```
multiuser on
acladd bob
```
Attaching to another user's multiuser session requires screen to be installed setuid-root, which is security-sensitive; consider tmux sockets instead.

## Verify
- [ ] New session shows the status bar and 10k scrollback; `screen -ls` lists named sessions.

## Checked

Documentation check. Checked 2026-10-27 against the screen(1) page from the man-pages project (man7.org): `startup_message`, `defscrollback` (initial 100), `vbell`, `hardstatus [always] firstline|lastline` and `hardstatus string`, `termcapinfo` (only effective at startup and reattach), `deflog` (initial off), `acladd`, `source`, the `-d -m`, `-S` and `-x` options, setuid-root needed for another user's multiuser session, and the key bindings `C-a H`, `S`, `|`, `tab`, `A`, `[` and `"`. Removed the RHEL packaging claim, `C-a n` and the `alwayslastline` spelling.
Method: documentation only; no commands were run.
