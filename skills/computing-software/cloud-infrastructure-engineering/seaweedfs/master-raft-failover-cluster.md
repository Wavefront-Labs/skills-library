---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.master-raft-failover-cluster
name: master-raft-failover-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [weed-master, quorum, raft, peers, failover]
level: practitioner
status: docs-checked
description: "Run 3 or 5 SeaweedFS masters with -peers, keep -ip consistent with peer names, and point volume servers at all masters for failover."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Failover-Master-Server
  - https://github.com/seaweedfs/seaweedfs/wiki/Production-Setup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# master raft failover cluster

Masters coordinate via Raft; the leader assigns file ids and volumes, others forward to it.

```bash
weed master -ip=ip1 -mdir=/data/seaweedfs/master -peers=ip1:9333,ip2:9333,ip3:9333
# repeat on ip2, ip3 with their own -ip
weed volume -dir=/data/vol -master=ip1:9333,ip2:9333,ip3:9333
```
Or all-in-one: `weed server -master.peers=...`.

Rules:
- Usually start 3 or 5 masters. A single master is also fine for many clusters, but two machines cannot reach consensus (Production Setup page).
- Peers are identified by hostname/IP plus port; the value should be consistent with the master's own `-ip`.
- Give volume servers as many masters as possible so they can switch when one fails; listing any one master also works.
- After a leader change, volume servers send heartbeats with their volume information to the new leader; those that have not yet reported are temporarily not writable.
- Adding a master to a running cluster means stopping all existing masters and starting the new set with the new master list; adding volume servers can keep using the existing masters.
- Add `-volumeSizeLimitMB=1024` if volume servers have small disks.
- For production, `-metrics.address=<Prometheus gateway address>` is suggested.

Verify: stop the leader and confirm another master takes over and volume servers heartbeat to it.

## Checked

2026-11-08. Confirmed against the Failover Master Server and Production Setup wiki pages. Removed the unsupported "odd number" rule, the `cluster.raft.ps` command and the master UI leader check; added the add-a-master procedure and the two-machine consensus note.

Method: documentation only; no commands were run.
