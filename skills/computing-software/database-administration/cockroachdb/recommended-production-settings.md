---
id: computing-software.database-administration.cockroachdb.recommended-production-settings
name: recommended-production-settings
category: computing-software
field: database-administration
product: cockroachdb
tags: [production-settings, sizing, hardware, cache, max-sql-memory, load-balancing]
level: practitioner
status: docs-checked
description: "Apply CockroachDB production recommendations: vCPU sizing, RAM and storage ratios, replication factor, cache and SQL memory, load balancing and networking flags."
sources:
  - https://www.cockroachlabs.com/docs/stable/recommended-production-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: provision a self-hosted cluster to the documented baseline before go-live.

Sizing: size by total vCPUs, then prefer the largest possible nodes and smallest possible cluster that meets fault-tolerance goals. Hardware ratios on the page: provision at least 4 GiB RAM per vCPU (2 GiB per vCPU is the minimum and suitable only for testing). Maximum recommended storage per node is 10 TiB regardless of vCPUs. Keep some disk free; CockroachDB creates an emergency ballast file at startup that you can delete to restart a node that ran out of disk.

Storage and replication:
- Use zone configs to raise replication factor from 3 to 5 (across at least 5 nodes), especially with local disks rather than replicated network disks.
- Do not use distributed file systems such as CephFS or GlusterFS for store volumes.
- Disable swap, or provision enough RAM; benchmark IOPS with sysbench and watch IOPS in the DB Console and `iostat`.
- AWS `gp3` volumes default to 3,000 IOPS and 125 MiB/s; on Azure use Premium Storage or local SSD with a Linux filesystem such as ext4, not ntfs.

Memory: the defaults are meant for development. Production should set `--cache` and `--max-sql-memory`; default SQL memory is 25%, and you can experiment up to 35%:
```shell
cockroach start --cache=.35 --max-sql-memory=.35 {other start flags}
```
Running out of SQL memory raises `memory budget exceeded` and risks an OOM crash.

Networking: understand `--listen-addr` versus `--advertise-addr`; with a private network, listen on the private IP and omit advertise.

Load balancing: every node is a valid SQL gateway; use a load balancer with CockroachDB's readiness health check (HAProxy on-premises, managed LBs on cloud) and make the balancer itself redundant. Size connection pools carefully; too many connections raises latency.

## Checked

2026-11-03. Confirmed against the production checklist page: RAM per vCPU, 10 TiB storage, ballast file, replication factor 3 to 5 across at least 5 nodes, CephFS/GlusterFS, swap, sysbench/iostat, `gp3` figures, Azure guidance, cache and SQL memory defaults, listen versus advertise address, load balancing. Removed: invented verification step.
Method: documentation only; no commands were run.
