---
id: computing-software.cloud-infrastructure-engineering.talos-linux.etcd-space-quota-and-defrag
name: etcd-space-quota-and-defrag
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [etcd, quota-backend-bytes, defrag, alarm, nospace, talosctl-etcd, database-size]
level: practitioner
status: docs-checked
description: "Handle etcd NOSPACE alarms and fragmentation on Talos: check status and alarms, raise quota-backend-bytes, disarm, and defragment one control plane node at a time."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/build-and-extend-talos/cluster-operations-and-maintenance/etcd-maintenance.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`talosctl etcd` commands work only on control plane nodes. The etcd space quota defaults to 2 GiB; past it etcd stops operating until resolved. Check with:

```bash
talosctl -n <IP> etcd alarm list
```

A tripped quota shows `NOSPACE`. For a large Kubernetes database raise the quota (recommended maximum 8 GiB) in the machine configuration:

```yaml
cluster:
  etcd:
    extraArgs:
      quota-backend-bytes: 4294967296 # 4 GiB
```

After the node reboots with the new configuration, run `talosctl etcd alarm disarm` to clear the alarm.

Fragmentation: the API server compacts etcd, which marks deleted space reusable, but disk space is not returned until the database is defragmented. Compare DB SIZE with IN USE:

```bash
talosctl -n <IP1>,<IP2>,<IP3> etcd status
```

If the in use ratio is under 0.5 defragmentation may improve performance, and if the database is over quota while the real data is small it is required. Run it on one node at a time:

```bash
talosctl -n <IP1> etcd defrag
```

Defragmentation is resource-intensive and blocks reads and writes on a live member while it rebuilds. Afterwards DB SIZE should closely match IN USE. Any node over quota prints alarms in the `ERRORS` column of `etcd status`.

## Checked

2026-11-04. Quota default, recommended maximum, YAML, alarm and defrag commands and the one-node-at-a-time warning confirmed on the etcd Maintenance page.

Method: documentation only; no commands were run.
