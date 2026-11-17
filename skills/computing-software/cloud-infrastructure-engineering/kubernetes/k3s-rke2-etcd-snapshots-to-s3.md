---
id: computing-software.cloud-infrastructure-engineering.kubernetes.k3s-rke2-etcd-snapshots-to-s3
name: k3s-rke2-etcd-snapshots-to-s3
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, k3s, rke2, k3s-etcd-snapshot, rke2-etcd-snapshot, etcd-backup, s3]
level: practitioner
status: docs-checked
description: "Take, schedule, list and restore embedded-etcd snapshots on k3s and rke2, including S3 targets, retention and the cluster-reset restore procedure."
sources: ["https://docs.k3s.io/cli/etcd-snapshot", "https://docs.rke2.io/datastore/backup_restore", "https://docs.k3s.io/datastore/backup-restore"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# k3s and rke2 etcd snapshots

The commands are the same for both; replace `k3s` with `rke2` (the RKE2 docs use the same flags and restore steps).
Local path: `/var/lib/rancher/k3s/server/db/snapshots` (rke2: `/var/lib/rancher/rke2/server/db/snapshots`).

## Scheduled snapshots with S3 (config.yaml on every server)
```yaml
etcd-snapshot-schedule-cron: "0 */6 * * *"
etcd-snapshot-retention: 20      # local, per server node (default 5); also sets etcd-s3-retention unless that is set
etcd-s3-retention: 20            # S3: counted cluster-wide for the bucket+folder, not per node
etcd-s3: true
etcd-s3-endpoint: s3.eu-west-1.amazonaws.com
etcd-s3-region: eu-west-1
etcd-s3-bucket: acme-k3s-backups
etcd-s3-folder: prod-cluster
etcd-s3-access-key: <key>        # or etcd-s3-config-secret (a Secret in kube-system)
etcd-s3-secret-key: <secret>
```
Restart the service after editing. Scheduled snapshots default to 00:00 and 12:00 system time with 5 retained per server node; snapshot names include the node name. Each etcd node uploads, so with N nodes keep roughly N times the number of cycles you want in `etcd-s3-retention`.

## On demand
```bash
k3s etcd-snapshot save --name pre-upgrade
k3s etcd-snapshot list                      # local and S3
kubectl get etcdsnapshotfile                # cluster-scoped ETCDSnapshotFile resources track snapshots on all members
k3s etcd-snapshot prune --snapshot-retention 10
```
S3 flags (`--s3`, `--s3-bucket`, ...) can be given on the command line. On-demand snapshots have no retention: delete them with `etcd-snapshot delete` or `prune`.

## Restore
```bash
systemctl stop k3s                     # on ALL servers
k3s server --cluster-reset --cluster-reset-restore-path=<snapshot-file-or-name>
# with S3: add --etcd-s3 --etcd-s3-bucket=... and pass only the snapshot file name as the restore path
systemctl start k3s                    # first server
# other servers: rm -rf /var/lib/rancher/k3s/server/db, then start k3s to rejoin
```

## Gotchas
- The node token must match the one used when the snapshot was taken; keep
  `/var/lib/rancher/k3s/server/token` with the backups.
- Snapshots only exist with embedded etcd; SQLite or external datastore clusters need their own backups.
- Local retention is per server node; S3 retention (`etcd-s3-retention`) is cluster-wide for the bucket and folder.
- The S3 config Secret cannot be used for a restore; pass S3 settings on the command line.
- A restore creates `/var/lib/rancher/k3s/server/db/reset-flag` to block repeated cluster resets; it is deleted on a normal start.
- Snapshots hold CA keys and cluster data; anyone with a snapshot and the server token can read encrypted resources.

## Checked

2026-10-26, against k3s-io/docs and rancher/rke2-docs on main (latest commits 2026-10-23/24; docs mention RKE2 v1.37 and containerd 2.0 era releases). Confirmed: config keys and defaults, `etcd-s3-retention` scope, config-secret restriction, `save`/`list`/`prune`/`delete` subcommands, ETCDSnapshotFile resources, cluster-reset restore procedure, reset-flag, token requirement. Wrong: retention was described as counted separately per location per node (S3 retention is cluster-wide and has its own flag).

Method: documentation only; no commands were run.
