---
id: computing-software.systems-network-administration.backup-and-recovery.restic-rclone-backend
name: restic-rclone-backend
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restic-rclone, restic, rclone, cloud-backup, restic-backends, backup-to-cloud]
level: practitioner
status: docs-checked
description: "Use rclone as a restic backend to reach Google Drive, OneDrive, SFTP variants and other clouds: rclone remotes, options, append-only serve mode, and failure handling."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html#other-services-via-rclone
  - https://rclone.org/commands/rclone_serve_restic/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# restic via rclone

**Goal:** back up with restic to any storage rclone supports, including ones restic has no native backend for.

## Set up
```sh
rclone config                          # create remote "gdrive" (OAuth) or "b2" etc.
restic -r rclone:gdrive:restic/host01 init
restic -r rclone:gdrive:restic/host01 backup /home
```
restic launches `rclone serve restic --stdio` as a child process and talks to it over stdin/stdout. Restic builds the command line from `rclone.program`, `rclone.args` and the text after `rclone:` in the repository string.

## Options
```sh
restic -o rclone.program=/usr/local/bin/rclone \
       -o rclone.args="serve restic --stdio --b2-hard-delete" \
       -r rclone:b2:bucket/path snapshots
```
- Defaults: `rclone.program` is `rclone`, `rclone.args` is `serve restic --stdio --b2-hard-delete`, and `-o rclone.timeout` (wait for the repository to open) is `1m`.
- If you override `rclone.args`, keep `serve restic --stdio` and keep `--b2-hard-delete` for B2 remotes (the reason is restic issue 1657, referenced in the restic manual).
- `rclone.program` may be a wrapper such as `ssh user@remotehost rclone`, which runs rclone (and its credentials) on the remote host.
- Restic documents B2 via its S3-compatible API as the recommended route over the native B2 backend.

## Append-only server
On a storage host you control, rclone can act as a rest-server that refuses deletes:
```sh
rclone serve restic --addr :8000 --append-only --htpasswd /etc/rclone/htpasswd --cert server.pem --key server.key remote:restic
```
`--append-only` disallows deletion of repository data; `--htpasswd` enables authentication (without it none is done); `--cert` and `--key` enable TLS; `--addr` defaults to 127.0.0.1:8080. Clients use `-r rest:https://user:pass@host:8000/`. Run `forget --prune` only from a trusted admin host with full access.

## Gotchas
- Restic exits non-zero when the backend fails, so alert on job exit codes.
- Restic encrypts the repository itself; no extra encryption layer is needed for confidentiality.

## Verify
`restic -r rclone:remote:path check` succeeds and a restored file matches the original checksum.

## Checked

2026-10-26. Documentation checked: restic/restic doc/ sources on master (last commit 2026-10-18; latest release v0.19.1) and the generated man pages in doc/man. rclone docs: docs/content/commands/rclone_serve_restic.md on master. Confirmed: rclone.program, rclone.args default (serve restic --stdio --b2-hard-delete) and rclone.timeout default 1m, how restic joins arguments, ssh wrapper example, rclone serve restic flags (--addr default, --append-only, --htpasswd, --cert, --key, --private-repos, --stdio). Removed unconfirmed rclone.connections, --drive-use-trash and --config advice.

Method: documentation only; no commands were run.
