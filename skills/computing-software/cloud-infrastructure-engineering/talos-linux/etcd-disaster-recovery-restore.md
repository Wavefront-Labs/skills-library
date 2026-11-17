---
id: computing-software.cloud-infrastructure-engineering.talos-linux.etcd-disaster-recovery-restore
name: etcd-disaster-recovery-restore
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [etcd, disaster-recovery, bootstrap, recover-from, ephemeral, wipe, quorum]
level: sme
status: docs-checked
description: "Restore a Talos control plane from an etcd snapshot: confirm quorum is unrecoverable, remove init nodes, wipe EPHEMERAL, then bootstrap with --recover-from and verify the logs."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/build-and-extend-talos/cluster-operations-and-maintenance/disaster-recovery.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
First prove etcd cannot be recovered normally: compare `talosctl -n IP etcd members` across all healthy control plane nodes and check `talosctl -n IP service etcd`. If quorum can be restored, that might be better than full recovery. Then get the freshest snapshot (take one even from an unhealthy cluster).

Make sure no node has the deprecated machine type `init`, which is incompatible with recovery:

```bash
talosctl -n <IP1>,<IP2>,... get machinetype
```

Convert an init node with `talosctl edit mc --mode=staged` and `talosctl reboot`. Replace failed hardware using the saved machine configuration, and repoint the control plane endpoint if addresses changed. If a node is up but etcd is not, wipe its EPHEMERAL partition after taking a snapshot:

```bash
talosctl -n <IP> reset --graceful=false --reboot --system-labels-to-wipe=EPHEMERAL
```

All control plane nodes should then boot with `etcd` in the `Preparing` state (`talosctl -n <IP> service etcd`). Run bootstrap against any one control plane node:

```bash
talosctl -n <IP> bootstrap --recover-from=./db.snapshot
```

If the snapshot came from `talosctl cp` of the data directory, add `--recover-skip-hash-check`. The node kernel log prints the matching hash, revision and key count ("recovering etcd from snapshot"). etcd then turns healthy on the bootstrap node, control plane components start, and the other control plane nodes join once the endpoint is up.

## Checked

2026-11-04. Recovery preconditions, init node check, EPHEMERAL wipe, bootstrap with --recover-from and the skip-hash flag confirmed on the Disaster Recovery page.

Method: documentation only; no commands were run.
