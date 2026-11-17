---
id: computing-software.database-administration.vitess.vitess-backup-include-binlogs
name: vitess-backup-include-binlogs
category: computing-software
field: database-administration
product: vitess
tags: [backup, binary-logs, include-binlogs, builtin-engine, point-in-time-recovery, vstream]
level: advanced
status: docs-checked
description: "Keep binary log history in a Vitess full backup with --include-binlogs: effect on restored servers, the builtin-engine requirement and why xtrabackup or mysqlshell do not qualify."
sources:
  - https://vitess.io/docs/25.0/user-guides/operating-vitess/backup-and-restore/creating-a-backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A server restored from a normal full backup starts with an empty binary log history, so it cannot serve binlog streams (replication or VStreams) for transactions from before the backup. Pass `--include-binlogs` to `vtctldclient Backup`, `vtctldclient BackupShard` or `vtbackup` to keep that history:

```sh
vtctldclient --server=<vtctld_host>:<vtctld_port> Backup --include-binlogs <tablet-alias>
```

The backup then contains every binary log listed in the source's binary log index. Restores need no extra flag: the logs are written under the target tablet's own `log-bin` basename and added to the binary log index before mysqld starts. Vitess does not reset or purge them afterward. Point-in-time recovery from such a backup works as usual.

Requirement: use the `builtin` engine. It stops mysqld before copying files, so the binary logs end exactly at the position of the backed-up data. `xtrabackup` and `mysqlshell` back up a running server, so logs copied alongside the data could include transactions the data lacks. Incremental backups, by contrast, always copy binary logs regardless of the configured engine.

## Checked

2026-11-08. Re-read the full Creating a Backup page (v25.0). Flag, restore behaviour and builtin-engine rationale confirmed in the Include binary logs in a full backup section; incremental statement confirmed in Choosing the backup type, Creating a Backup page.

Method: documentation only; no commands were run.
