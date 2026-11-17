---
id: computing-software.systems-network-administration.restic.rclone-backend
name: rclone-backend
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, rclone, backend, rclone-program, ssh]
level: practitioner
status: docs-checked
description: "Reach any rclone remote from restic with rclone: URLs, the rclone.program, rclone.args and rclone.timeout options, and bandwidth limits."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rclone backend

Restic starts `rclone serve restic --stdio` and talks to it. Configure the remote in rclone first, then:

```
restic -r rclone:foo:bar init
restic -r rclone:b2prod:yggdrasil/foo/bar/baz init
```

The format is `rclone:<remote>:<path>`.

## Options

- `-o rclone.program` the executable; default `rclone`. A relative executable in the current directory needs `-o rclone.program=./rclone`.
- `-o rclone.args` arguments; default `serve restic --stdio --b2-hard-delete`.
- `-o rclone.timeout` start-up timeout; default `1m`.

The command is assembled as program, then args, then the `<remote>:<path>` value.

## Run rclone on another host

```
restic -o rclone.program="ssh user@remotehost rclone" -r rclone:remote:path init
```

## Debugging and throttling

Use environment variables read by rclone itself:

- `RCLONE_VERBOSE=2` for debug output
- `RCLONE_BWLIMIT=1M` to cap bandwidth

Restic takes care of starting and stopping rclone. If rclone is found in the current directory, restic refuses to run it implicitly for security reasons (error: cannot implicitly run relative executable); pass `-o rclone.program=./rclone`.

## Checked

2026-11-03. Confirmed in the restic docs page Preparing a new repository (Other Services via rclone): `rclone:<remote>:<path>` format, the three options and defaults (`serve restic --stdio --b2-hard-delete`, `1m`), the argument assembly order, running rclone over ssh, `RCLONE_BWLIMIT` and `RCLONE_VERBOSE=2`. Removed: the SSH-tunnel cross-reference and the rclone lsd test paragraph (not in the docs).

Method: documentation only; no commands were run.
