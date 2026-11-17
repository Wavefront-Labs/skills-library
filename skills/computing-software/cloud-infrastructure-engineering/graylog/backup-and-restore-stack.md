---
id: computing-software.cloud-infrastructure-engineering.graylog.backup-and-restore-stack
name: backup-and-restore-stack
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [backup, mongodump, mongorestore, snapshots, disaster-recovery]
level: advanced
status: docs-checked
description: "Back up every Graylog stack component: server config, MongoDB, Data Node snapshots and Data Lake, and restore safely."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/backup_considerations.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# backup and restore stack

Do not rely on virtual machine snapshots as a backup method.

Components to back up:
- **Graylog**: `/etc/graylog/server/server.conf`, custom config files, plugins and custom scripts on each node.
- **Data Node**: snapshots of message data plus configuration files. This is the core of the backup; incremental snapshots work well.
- **MongoDB**: database dump holding users, dashboards, alerts and stream definitions. Use `mongodump` and `mongorestore`.
- **Data Lake**: stored log data.
- TLS certificates and keys if TLS is enabled.

Backup types: minimal, full, incremental and archive. Schedule backups, use remote storage, encrypt sensitive data, apply access controls and keep multiple versions. Test restores regularly and document the recovery process.

Restore order and compatibility: keep versions consistent across Graylog, MongoDB and Data Node. Restore MongoDB, Data Node and Data Lake to the same point in time.

## Checked

2026-11-04. Confirmed against the Backup Considerations page. Added its warning on restoring components to the same point in time.

Method: documentation only; no commands were run.
