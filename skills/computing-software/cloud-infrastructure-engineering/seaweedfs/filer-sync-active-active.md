---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.filer-sync-active-active
name: filer-sync-active-active
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [active-passive, cross-cluster, disaster-recovery, filer-sync, active-active]
level: advanced
status: docs-checked
description: "Replicate two SeaweedFS clusters with weed filer.sync in active-active or active-passive mode, per-path, resumable, including a Kubernetes sidecar."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Filer-Active-Active-cross-cluster-continuous-synchronization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# filer sync active active

Run from any machine that can reach both clusters' filers and volume servers:
```bash
weed filer.sync -a filer1:8888 -b filer2:8888                       # active-active
weed filer.sync -a filer1:8888 -b filer2:8888 -a.path /filer1/path1 -b.path /filer2/path2
weed filer.sync -a filer1:8888 -b filer2:8888 -isActivePassive      # a to b only
```
It bootstraps from the beginning, or resumes from the last checkpoint, then runs continuously. Checkpoints and per-filer signatures are persisted, so stopping and restarting is safe; the signatures prevent changes from bouncing back and forth.

Mechanism: each filer has local change logs; `filer.sync` reads them and replays them in the other cluster.

Kubernetes with the SeaweedFS Operator: add a sidecar to the filer spec running `weed filer.sync -a=localhost:8888 -b=remote-filer.dr.svc.cluster.local:8888 -isActivePassive`. The sidecar runs on every filer replica, so for active-passive keep a single sync process (pin it to one replica or a separate single-replica filer).

Verify: write on cluster A, read the same path from cluster B.

## Checked

Method: docs-checked 2026-11-09 against the SeaweedFS wiki page Filer Active-Active cross-cluster continuous synchronization (raw markdown, read in full).
