---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-etcd-snapshot-scheduled
name: k3s-etcd-snapshot-scheduled
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, etcd-snapshot, etcd-snapshot-schedule-cron, etcd-snapshot-retention]
level: practitioner
status: docs-checked
description: "Configure the default twice-daily embedded etcd snapshots: schedule, retention, directory, name and compression."
sources:
  - https://docs.k3s.io/cli/etcd-snapshot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune automatic etcd backups.

Scheduled snapshots are on by default at 00:00 and 12:00 system time, keeping 5 snapshots per server node on local disk. Names start with etcd-snapshot, followed by node name and timestamp.

Server flags (config-file keys use the same names):

- --etcd-disable-snapshots: disable scheduled snapshots
- --etcd-snapshot-name: base name (default etcd-snapshot)
- --etcd-snapshot-compress: compress snapshots
- --etcd-snapshot-dir: directory (default ${data-dir}/db/snapshots)
- --etcd-snapshot-retention: local snapshots kept per server node (default 5)
- --etcd-snapshot-schedule-cron: cron spec (default `0 */12 * * *`; every 5 hours is `0 */5 * * *`)

data-dir defaults to /var/lib/rancher/k3s and is changed with --data-dir.

Retention is applied per server node for local snapshots, deleting the oldest first, as soon as the count exceeds the limit.

Example config:

```
etcd-snapshot-schedule-cron: "0 */6 * * *"
etcd-snapshot-retention: 10
etcd-snapshot-compress: true
```

To replicate snapshots off the node, enable the S3 options (see the S3 skill). Snapshots are also required for rollback after an upgrade, and the server token must be saved with them.

## Checked

2026-11-03: read docs.k3s.io cli/etcd-snapshot. Confirmed: the 00:00 and 12:00 default schedule, retention of 5 per server node, all six scheduling flags and their defaults, the 5-hour cron example, and oldest-first per-node retention.

Method: documentation only; no commands were run.
