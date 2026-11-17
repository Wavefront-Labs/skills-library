---
id: computing-software.cloud-infrastructure-engineering.etcd.hardware-recommendations
name: hardware-recommendations
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [hardware, cpu, memory, disk, network, iops, ssd, cluster-sizing, recommendations]
level: practitioner
status: docs-checked
description: "Hardware guidance for etcd members: CPU, RAM, SSD disk IOPS, network and the small, medium, large and xlarge cluster profiles."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/hardware/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

From the hardware recommendations page.

Principles: fast disks are the most critical factor for performance and stability; network latency and enough memory matter too. These are starting points, not hard rules, and the page says to test with a simulated workload before production. The example setups assume machines dedicated to etcd.

- CPUs: a few cores for light clusters; typical clusters use 2 to 4 cores; heavy clusters (thousands of clients, tens of thousands of requests per second) need 8 to 16 cores.
- Memory: typically 8 GB; heavy deployments with thousands of watchers and millions of keys need 16 GB to 64 GB.
- Disk: typically 50 sequential IOPS (for example a 7200 RPM disk) is required; heavily loaded clusters should have 500 sequential IOPS (a typical local SSD or high-performance virtualized block device). Cloud providers usually publish concurrent IOPS, which can be 10x the sequential figure. Back storage with an SSD where possible; measure with a benchmark tool such as `fio`. About 10 MB/s of disk bandwidth recovers 100 MB in 15 seconds; 100 MB/s or more is suggested for large clusters.
- Network: a 1 GbE link suffices for common deployments and 10 GbE reduces mean recovery times in large clusters. Deploy members within a single data center when possible; for cross data center deployments read the tuning page.

Example profiles in the guide: small (fewer than 100 clients, fewer than 200 requests per second, no more than 100 MB of data; example 2 vCPU, 8 GB), medium (fewer than 500 clients, fewer than 1,000 requests per second, up to 500 MB), large (fewer than 1,500 clients, fewer than 10,000 requests per second, up to 1 GB), xLarge (more than 1,500 clients, more than 10,000 requests per second, more than 1 GB; example 16 vCPU, 64 GB). Each has AWS and GCE example machine types on the page.

## Checked

2026-11-03. Confirmed on the v3.5 hardware recommendations page: CPU (2-4 cores typical, 8-16 heavy), memory (8 GB typical, 16-64 GB heavy), disk IOPS 50 and 500 sequential with the concurrent-IOPS caveat, SSD and fio, bandwidth for recovery, 1GbE and 10GbE, single data center advice, and the small, medium, large and xLarge profiles. Corrected: the small profile data size (100 MB, not 5 MB), the xLarge profile (more than 1,500 clients and 10,000 requests per second, 3,000-node Kubernetes example). Removed: memory-mapped file, shared network disk and WAL-on-own-device claims.

Method: documentation only; no commands were run.
