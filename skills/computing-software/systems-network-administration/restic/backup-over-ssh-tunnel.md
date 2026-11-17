---
id: computing-software.systems-network-administration.restic.backup-over-ssh-tunnel
name: backup-over-ssh-tunnel
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, ssh-tunnel, reverse-tunnel, rest-server, rclone-serve]
level: advanced
status: docs-checked
description: "Back up a remote host to an internal repository server through a reverse SSH tunnel using rest-server or rclone serve restic."
sources:
  - https://restic.readthedocs.io/en/stable/080_examples.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup over a reverse SSH tunnel

Use this when the repository server is on an internal network that the remote host cannot reach directly.

## 1. Run the repository server locally

On the internal host:

```
rest-server --listen localhost:8000 --path /path/to/repo --no-auth
```

`--listen localhost:8000` makes the server accessible only from the internal host; `--no-auth` means no authentication is required to connect.

## 2. Open a reverse tunnel

Still on the internal host, forward a port on the remote host back to the server:

```
ssh -R 8000:localhost:8000 user@server
```

The tunnel lasts only as long as the SSH session.

## 3. Run restic on the remote host

```
restic -r rest:http://localhost:8000/ init
restic -r rest:http://localhost:8000/ backup /path/to/data
```

`snapshots` and `restore` work with the same URL.

## Alternative with rclone

Serve a local directory instead of `rest-server`:

```
rclone serve restic --addr localhost:8000 /path/to/repo
```

## Checked

Checked 2026-11-08 against the restic Examples page (080_examples), read in full. Confirmed: the idea of backing up to an internal rest-server through a reverse SSH tunnel, rest-server --listen localhost:8000 --path --no-auth, ssh -R 8000:localhost:8000, the rest:http://localhost:8000/ URL for init, backup, snapshots and restore, the tunnel lasting for the SSH session, and rclone serve restic --addr localhost:8000. Removed: the claim that the --no-auth setup is acceptable only because of the tunnel and the local-user exposure note, which the page does not state.

Method: documentation only; no commands were run.
