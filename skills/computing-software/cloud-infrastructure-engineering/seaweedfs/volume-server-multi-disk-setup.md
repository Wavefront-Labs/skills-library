---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.volume-server-multi-disk-setup
name: volume-server-multi-disk-setup
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [weed-volume, datacenter-rack, multi-disk, max-volumes]
level: practitioner
status: docs-checked
description: "Add volume servers with weed volume: -dir lists, -max=0 auto volume count, -dataCenter/-rack, leveldb index and compaction throttling."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Production-Setup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# volume server multi disk setup

Single disk:
```bash
weed volume -master=ip1:9333,ip2:9333,ip3:9333 -dataCenter=dc1 -rack=rack1 -dir=/data/seaweedfs/volume -ip=x.x.x.x -max=0
```
Multiple disks: give a comma list and a matching `-max` list.
```bash
weed volume -master=ip1:9333,ip2:9333,ip3:9333 -dataCenter=dc1 -rack=rack1 -ip=x.x.x.x   -dir=/data/seaweedfs/volume1,/data/seaweedfs/volume2 -max=0,0
```
Or run one volume server per disk on different `-port` values.

Rules and gotchas:
- Without `-max=0` the volume count is limited to 8; set a non-zero value only to manage disk space explicitly.
- Never put multiple directories on the same disk: the automatic volume count limit double-counts capacity.
- Huge disks with many volumes: `-index=leveldb` reduces memory load.
- `-compactionMBps` throttles background jobs (compaction, balancing, encoding/decoding) on busy volume servers.
- After adding volume servers there is no data rebalancing; data goes to new servers once new volumes are created on them. `volume.balance -force` in `weed shell` balances manually.
- Several volume servers on one physical host count as separate servers for replication, so `001` does not guarantee that each copy lands on a different physical host.

Verify: visit `http://<master>:9333/` and check the free volume count is not zero.

## Checked

2026-11-08. Confirmed against the Production Setup wiki page (volume server section and notes). Reworded the rebalancing and replication notes to match the page and replaced the master UI check with the page's free volume count check.

Method: documentation only; no commands were run.
