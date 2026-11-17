---
id: computing-software.systems-network-administration.linux.tmux-shared-and-pair-sessions
name: tmux-shared-and-pair-sessions
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, tmux, tmux-shared-session, tmux-pairing, pair-programming, socket-permissions, grouped-sessions]
level: practitioner
status: docs-checked
description: "Share a tmux session between people or terminals: same-session attach, grouped sessions, shared sockets with group permissions and read-only clients."
sources:
  - https://github.com/tmux/tmux/blob/master/tmux.1
  - https://github.com/tmux/tmux/blob/master/CHANGES
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shared and paired tmux sessions

## Same user, two terminals
```bash
tmux new -s incident          # terminal 1
tmux attach -t incident       # terminal 2 — both see and type into the same windows
tmux attach -d -t incident    # take over, detaching others
```
Window size is controlled by the `window-size` option (`latest` is available from tmux 3.1) and the `aggressive-resize` window option.

## Grouped sessions (shared windows, independent view)
`tmux new -t incident -s incident-bob` — same window list, each client can look at a different window.

## Two different users
```bash
# owner
tmux -S /srv/tmux/pair new -s pair
chgrp devops /srv/tmux/pair && chmod 660 /srv/tmux/pair        # the guest must be able to reach the socket file
# tmux 3.3+: also allow the user explicitly (the server owner and root are always permitted)
tmux -S /srv/tmux/pair server-access -a bob
tmux -S /srv/tmux/pair server-access -r bob                     # optional: make bob's clients read-only
# guest
tmux -S /srv/tmux/pair attach -t pair        # add -r for a read-only client
```
Anyone attached has a shell **as the owner** — only share with people you'd hand your account to.
A read-only client can still see everything; only keys bound to detach-client or switch-client work for it.

## Alternatives
GNU screen has a multiuser mode (`multiuser on`, `acladd bob`; `screen -x` attaches to an attached session and needs the setuid-root screen binary for other users' sessions).

## Gotchas
- The default socket lives in a per-user `tmux-UID` directory under `$TMUX_TMPDIR` or `/tmp`; `-S` takes a full socket path you control, `-L` only a name.
- Record incident sessions (`pipe-pane -o 'cat >> ~/incident.log'`).

## Verify
- [ ] Second user attaches read-only, sees live output, cannot type; `server-access -l` lists the entry.

## Checked
Checked 2026-10-25 against the tmux manual page source and CHANGES file (tmux/tmux master, latest release 3.8 of 2026-09-09). Confirmed: `-S socket-path` and the `tmux-UID` socket directory, `attach-session -d/-r`, `new-session -t` (session groups share windows), `server-access -a/-d/-r/-w/-l` (added in 3.3 per CHANGES), read-only client behaviour, `window-size latest` (added in 3.1 per CHANGES), `pipe-pane -o`, screen `multiuser` and `acladd`. Fixed: `window-size latest` was stated as 2.9+. Removed unconfirmed claims: tmate, the systemd-tmpfiles cleanup remark and the 700 permission statement.

Method: documentation only; no commands were run.
