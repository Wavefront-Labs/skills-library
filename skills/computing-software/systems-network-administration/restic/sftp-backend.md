---
id: computing-software.systems-network-administration.restic.sftp-backend
name: sftp-backend
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, sftp, ssh, backend, ssh-config, keepalive]
level: practitioner
status: docs-checked
description: "Use an SFTP repository: URL forms, ssh config aliases, sftp.command and sftp.args options, and keepalive settings for long runs."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
  - https://restic.readthedocs.io/en/stable/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SFTP backend

Basic form:

```
restic -r sftp:user@host:/srv/restic-repo init
```

A path without a leading `/` is relative to the remote home. There is no `~` expansion on SFTP servers. For domain-confined users write `user@domain@host`.

## URL form with a port or IPv6

```
sftp://user@[::1]:2222//srv/restic-repo
```

A double slash after the host means an absolute path; a single slash means relative to the home directory.

## Use ssh config

Restic starts `ssh`, so `~/.ssh/config` or `/etc/ssh/ssh_config` applies (`Host`, `User`, `Port`, `Hostname`). Then an alias works:

```
restic -r sftp:foo:/srv/restic-repo init
```

## Overrides

- `-o sftp.command="foobar"` replaces the SSH command entirely.
- `-o sftp.args="..."` passes extra arguments to the default SSH command and is ignored when `sftp.command` is set.

## Long jobs

Add keepalives in the client ssh config so idle connections survive:

```
ServerAliveInterval 60
ServerAliveCountMax 240
```

A Synology NAS can expose a different directory structure over SFTP than elsewhere. The FAQ says to use an absolute path, try removing a `/volume1` prefix, and use `sftp` and `ls` to explore the SFTP hierarchy.

## Checked

2026-11-03. Confirmed in the restic docs pages Preparing a new repository (SFTP section) and FAQ (Synology NAS): URL forms incl. double slash, relative paths, `user@domain@host`, no tilde expansion, ssh config usage, `sftp.command` and `sftp.args`, the keepalive lines. Removed: nothing beyond tightening the NAS note to what the FAQ says.

Method: documentation only; no commands were run.
