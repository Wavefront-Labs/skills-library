---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-rollback-after-upgrade
name: k3s-rollback-after-upgrade
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, rollback, downgrade, datastore-restore]
level: sme
status: docs-checked
description: "Roll back K3s after an upgrade by downgrading the binary and restoring a datastore snapshot taken on the older version."
sources:
  - https://docs.k3s.io/upgrades/roll-back
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rollback combines a binary downgrade with datastore restoration, for SQLite, external datastore or embedded etcd. For a previous Kubernetes minor version you must hold a datastore snapshot taken on that minor. Without a restorable database you cannot roll back a minor version.

Cautions: take backups before upgrading; k3s-killall.sh terminates processes forcefully and may lose data if applications are not shut down properly; verify versions before and after.

Embedded etcd steps:

1. Drain: `kubectl drain --ignore-daemonsets --delete-emptydir-data <NODE-ONE-NAME> <NODE-TWO-NAME> ...`
2. On each node run `k3s-killall.sh`.
3. Reinstall the old binary without starting, with `INSTALL_K3S_VERSION=vX.Y.Zk3s1 INSTALL_K3S_EXEC="server" INSTALL_K3S_SKIP_START="true"` (agent for agents).
4. On the first server run `k3s server --cluster-reset --cluster-reset-restore-path=<PATH-TO-SNAPSHOT>`. This overwrites all etcd data; verify the snapshot first.
5. `systemctl start k3s` on the first server.
6. On other servers `rm -rf /var/lib/rancher/k3s/server/db`, then start them.
7. Start agents.

SQLite: replace the .db file with your backup copy. External database: drain, killall, restore the dump (for PostgreSQL, `pg_restore -U <DB-USER> -d <DB-NAME> <BACKUP-FILE>`), reinstall the old version, start K3s.

Verify: `k3s --version`, `kubectl get nodes`, application behaviour and K3s logs.

## Checked

2026-11-03: read docs.k3s.io upgrades/roll-back. Confirmed: the snapshot-on-target-minor requirement, the embedded etcd steps with --cluster-reset-restore-path, the SQLite and external database variants, and the caution about k3s-killall.sh.

Method: documentation only; no commands were run.
