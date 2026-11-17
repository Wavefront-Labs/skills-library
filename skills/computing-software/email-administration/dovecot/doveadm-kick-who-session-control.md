---
id: computing-software.email-administration.dovecot.doveadm-kick-who-session-control
name: doveadm-kick-who-session-control
category: computing-software
field: email-administration
product: dovecot
tags: [doveadm-kick, doveadm-who, anvil, disconnect-users, cidr, proxy-connections]
level: practitioner
status: docs-checked
description: "List connected users with doveadm who and disconnect them by name mask, IP network or proxy destination with doveadm kick."
sources:
  - https://doc.dovecot.org/main/core/man/doveadm-kick.1.html
  - https://doc.dovecot.org/main/core/man/doveadm-who.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both commands query the anvil process, whose socket defaults to `anvil` in the runtime directory.

`doveadm who` lists current connections. Default output is a table grouped by username:
- `-1` prints one line per user and connection.
- `--ps` prints one line per process with the process title as shown by ps(1), showing what each is doing; it cannot be combined with `-1`.
- Give an IP or CIDR range to filter, or a user mask (wildcards `*` and `?` allowed).
- `-f` uses an alternative username field from the passdb; only fields beginning `user_` are tracked.
- `-a` points to a different socket, a UNIX path or `hostname:port` for who; kick documents it as an alternative UNIX socket path.
- Output defaults to the table formatter.

`doveadm kick` disconnects sessions. Forms:
1. By user mask: all users whose login matches are disconnected.
2. By IP or network (`ip/bits`): all users from that address.
3. Both: only users matching the name from that address.
4. `-h dest_host` alone: all proxy connections to the destination host (`-h` is also accepted as an option in the other forms).

A user mask can be a login name like `jane` or `john@example.com`, with wildcards such as `*@example.org`. With `-f` the mask applies to the alternative `user_*` field.

Typical uses: kick a user after a password change or account lock, drain a backend before maintenance (kick proxy connections to it), or evict a compromised IP range. Check with `doveadm who` first so you do not disconnect everyone by accident.

## Checked

2026-11-08. Read doveadm-kick(1) and doveadm-who(1) in full. Fixed the who process option, which is --ps and not -p; clarified -h forms and the default table formatter.

Method: documentation only; no commands were run.
