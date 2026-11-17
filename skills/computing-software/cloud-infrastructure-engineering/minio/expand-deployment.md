---
id: computing-software.cloud-infrastructure-engineering.minio.expand-deployment
name: expand-deployment
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, expand-deployment, server-pool, expansion, sequential-hostnames, pool-write-weighting, mc-admin-rebalance, non-disruptive-restart]
level: advanced
status: docs-checked
description: "Expand a distributed MinIO deployment with a new server pool: sequential hostnames, 2 x EC:N drive minimum, no auto-rebalance, free-space write weighting and all-node restart."
sources: ["https://github.com/minio/docs/blob/main/source/operations/deployments/baremetal-expand-minio-deployment.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expanding a distributed MinIO deployment

Expansion adds a **server pool**, increasing capacity. It is not BC/DR: each pool has its own erasure sets, but losing a whole pool stops I/O for every pool, and an erasure set that loses quorum loses data regardless of other sets. For BC/DR use site replication. Single-node single-drive topologies cannot be expanded.

## Prerequisites
- Full bidirectional connectivity between nodes, one listen port across all servers, and a load balancer using **least connections** (NGINX and HAProxy are named as known to work).
- Sequentially numbered hostnames using `{x...y}` expansion, with DNS created beforehand, e.g. `minio{5...8}.example.com`.
- The pool must offer at least `2 x EC:N` drives per erasure set, where EC:N is the deployment's Standard parity. The pool need not match existing hardware, but drives inside the new pool should be alike.
- Synchronised time on all nodes (ntp, timedatectl or timesyncd).
- Back up first with `mc admin cluster bucket export` and `mc admin cluster iam export`.

## Procedure
Install the binary, TLS certificates and systemd unit on each new node, then edit the environment file on **all** nodes. A space separates pools in `MINIO_VOLUMES`:
```
MINIO_VOLUMES="https://minio{1...4}.example.net:9000/mnt/disk{1...4}/minio https://minio{5...12}.example.net:9000/mnt/disk{1...8}/minio"
```
Restart all server processes at about the same time (non-disruptive).

## Behaviour after expansion
- No automatic rebalance. New writes pick a pool with probability FreeSpaceOnPool / FreeSpaceOnAllPools (3, 2 and 5 TiB free gives 30, 20 and 50 percent). A pool is skipped if a write would take a drive above 99 percent usage or below 1000 free inodes. Pools being decommissioned get no writes.
- Rebalance manually with `mc admin rebalance`.
- Plan capacity for at least 2 years of data before reaching 70 percent usage; frequent just-in-time expansion signals a planning issue.

Removing a pool: `computing-software.cloud-infrastructure-engineering.minio.decommission-pool`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Expand a Distributed MinIO Deployment page (baremetal-expand-minio-deployment.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
