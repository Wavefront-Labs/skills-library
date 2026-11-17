---
id: computing-software.cloud-infrastructure-engineering.minio.hardware-checklist
name: hardware-checklist
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, hardware-checklist, network-throughput, memory-sizing, xfs, jbod, das, nfs, drive-selection, capacity-planning]
level: practitioner
status: docs-checked
description: "Plan MinIO production hardware with the documented NIC throughput table, per-request memory formula, host memory by capacity, flash and XFS storage guidance and the no-NFS rule."
sources: ["https://github.com/minio/docs/blob/main/source/operations/checklists/hardware.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO hardware checklist

Use identical hardware and software across all nodes of a server pool; mixed configurations give unpredictable performance. Data that can live on cheaper hardware belongs in a separate warm or cold deployment reached by tiering. Capacity planning inputs: data at launch, two years of growth, object count by average size, retention, number of sites and buckets.

## Priorities
Order of performance impact: network, storage controller, then drives. Secure those before CPU.

## Network
| NIC | Aggregate storage throughput |
|---|---|
| 10 Gbps | 1.25 GBps |
| 25 Gbps | 3.125 GBps |
| 50 Gbps | 6.25 GBps |
| 100 Gbps | 12.5 GBps |
With ~100 MB/s spinning disks, 1 GbE supports about one disk, 10 GbE roughly 10-12, 25 GbE about 30.

## Memory
Memory limits concurrent requests per node: `totalRam / ramPerRequest`, where RAM per request is `((2MiB + 128KiB) * driveCount) + (2 * 10MiB) + (2 * 1MiB)`. Example (free RAM, 16 drives): 585 requests at 32 GiB, 1,170 at 64 GiB. Host memory by storage: up to 1 Ti 8 GiB, 10 Ti 16 GiB, 100 Ti 32 GiB, 1 Pi 64 GiB, over 1 Pi 128 GiB. Since RELEASE.2024-01-28T22-35-53Z MinIO preallocates 2 GiB per node (distributed) or 1 GiB (single node).

## Storage
- Baremetal: flash (NVMe preferred, else SSD); HDD is not recommended for production.
- Prefer direct-attached JBOD with no RAID or pooling layer; use thick LUNs only if virtual volumes are unavoidable.
- Kubernetes: one storage class per tenant, consistent media and equal PV size (the smallest PV caps every PV in the pool), XFS formatting, CSI such as DirectPV that presents local storage.
- NFS and similar network filesystems break the read-after-write and list-after-write guarantees.
- Give MinIO exclusive access to its drives; external changes or remounts risk data loss.

## Checked

2026-11-03. Confirmed against the MinIO docs source: hardware checklist page: NIC throughput table, RAM per request formula and the 585 and 1,170 request example, host memory by storage, drive and network filesystem guidance. Removed or fixed: nothing.

Method: documentation only; no commands were run.
