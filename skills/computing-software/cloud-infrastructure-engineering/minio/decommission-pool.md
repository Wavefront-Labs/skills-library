---
id: computing-software.cloud-infrastructure-engineering.minio.decommission-pool
name: decommission-pool
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, decommission-pool, mc-admin-decommission, draining, pool-removal, irreversible, decommission-status, tiering-decommission]
level: sme
status: docs-checked
description: "Decommission a MinIO server pool with mc admin decommission start and status: permanence, capacity needs, resumability, ignored expired objects and the final listing check."
sources: ["https://github.com/minio/docs/blob/main/source/operations/deployments/baremetal-decommission-server-pool.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decommissioning a MinIO server pool

Needs two or more pools, with enough free space elsewhere to absorb the target's data. Data migrates to the remaining pools by ratio of their free space. During draining GET, LIST and HEAD are served normally while PUT and versioned DELETE go to active pools; versioned objects keep their order. Since RELEASE.2023-01-18T04-36-38Z several pools can be queued in one command: all go read-only immediately but drain one at a time.

> **Permanent.** Once started the pool is marked inactive ("draining") and never returns to active, even if cancelled or interrupted. Verify the pool before running the command.

## Prerequisites and planning
- Back up with `mc admin cluster bucket export` and `mc admin cluster iam export`.
- Total free capacity must exceed the pool's used data. With three 200 TB pools each 100 TB used, removing pool 1 fits; if it were full it would fill the others.
- When replacing hardware, expand first and decommission afterwards, never both in one step; topology must stay stable while draining.

## Procedure
```
mc admin decommission status myminio
mc admin decommission start myminio/ https://minio-{01...04}.example.net:9000/mnt/disk{1...4}/minio
mc admin decommission status myminio
mc admin decommission status myminio POOL_DESCRIPTION
```
Give the full pool description (hosts, disks, paths). Status shows `Active` or `Draining`, and the detail view reports the rate and elapsed time. It reads `Complete` when done. Load balancers need no change at start.

## Behaviour
- Resumable: transient restarts or network failures resume automatically; manually cancelled or failed runs resume only when you start it again.
- At the end MinIO lists the pool; an empty listing marks success, any objects returns failure.
- Ignored data: objects whose only version is a delete marker (since RELEASE.2023-05-27T05-56-19Z) and versions expired by lifecycle rules (since RELEASE.2023-06-23T20-26-00Z). Watch them with `mc admin trace --call decommission` (since RELEASE.2023-06-29T05-12-28Z).
- With tiering active (since RELEASE.2023-03-20T20-16-18Z) object references move and GET keeps working via the remote tier.
- Removing the finished pool from `MINIO_VOLUMES` requires restarting all nodes at about the same time.

## Checked

2026-11-03. Confirmed against the MinIO docs source: decommission-server-pool page: commands, status values, draining behaviour, release-gated behaviours. Removed or fixed: nothing.

Method: documentation only; no commands were run.
