---
id: computing-software.database-administration.vitess.vitess-xtrabackup-engine-setup
name: vitess-xtrabackup-engine-setup
category: computing-software
field: database-administration
product: vitess
tags: [backup, xtrabackup, xbstream, backup-engine, vtctldclient, vttablet]
level: practitioner
status: docs-checked
description: "Configure and troubleshoot the xtrabackup backup engine in Vitess: required flags, MySQL 8.0 xbstream mode, vtctldclient Backup and BackupShard, and the documented common errors."
sources:
  - https://vitess.io/docs/25.0/user-guides/operating-vitess/backup-and-restore/creating-a-backup/
  - https://vitess.io/docs/25.0/user-guides/operating-vitess/backup-and-restore/overview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The default backup engine is `builtin`, but the docs strongly recommend `xtrabackup` because it is more robust and allows non-blocking backups. Restores always use whichever engine created the backup. A compatible `xtrabackup` and, if needed, `xbstream` must be in `$PATH` before running `Backup` or `BackupShard`; the supported version listed is MySQL 8.0.

Required flags on Vitess components that run backups (vtbackup, vttablet, vtctld):
- `--backup-engine-implementation=xtrabackup`
- `--xtrabackup-user string`: the user xtrabackup connects as; it needs the Percona-documented privileges and must be able to connect locally without a password via auth_socket.
- For MySQL 8.0 also `--xtrabackup-stream-mode=xbstream`.

Commands:
```sh
vtctldclient --server=<vtctld_host>:<vtctld_port> Backup [--upgrade-safe=false] <tablet-alias>
vtctldclient --server=<vtctld_host>:<vtctld_port> BackupShard [--allow-primary=false] [--upgrade-safe=false] <keyspace/shard>
```
With `builtin`, replication is stopped before mysqld is shut down for the backup; with `xtrabackup` the tablet keeps serving traffic.

Documented errors and fixes:
- `xtrabackupUser must be specified`: set `--xtrabackup-user` on vtctld and vttablet.
- `executable file not found in $PATH`: put the binary in the PATH of the user running vttablet, or set `--xtrabackup-root-path` on vtctld and vttablet.
- `Streaming in tar format is no longer supported in 8.0`: set `--xtrabackup-stream-mode` to xbstream on vttablets and vtctlds.
- `Unsupported server version`: continue at your own risk with `--xtrabackup-backup-flags=--no-server-version-check`.

## Checked

2026-11-04. Engine choice, prerequisites, flags, commands and the four error cases confirmed in the Creating a Backup page (Using xtrabackup, Create a full backup with vtctl, Common Errors and Resolutions).

Method: documentation only; no commands were run.
