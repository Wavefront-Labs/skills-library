---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-hardware-requirements
name: grafana-mimir-hardware-requirements
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [hardware, disk, iops, nfs, capacity]
level: practitioner
status: docs-checked
description: "Summarises Mimir hardware guidance: CPU to memory ratio, SSD disk and IOPS needs, unsupported network filesystems and network bandwidth."
sources: ["https://grafana.com/docs/mimir/latest/set-up/hardware-requirements/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mimir hardware requirements

Actual CPU and memory depend on active series, ingested samples per second and query load; per-component sizing is in the capacity planning guide.

## Compute

As a general guide provision at least a 1:4 CPU to memory ratio (an 8-core node with at least 32 GB). Ingesters and store-gateways are the most memory-intensive.

## Disk

Ingesters, store-gateways and compactors need fast persistent local disks for the WAL, TSDB blocks and temporary data. Requirements: low latency (SSD strongly recommended), at least 50 IOPS per GB for ingester disks (compactors benefit from high IOPS too), and POSIX semantics including `mmap`, `fsync` and file locking.

Examples: AWS EBS `io1` or `gp3`; GCP `pd-ssd`; Azure Premium SSD managed disks (`managed-csi-premium`).

## Unsupported filesystems

NFS (including Azure NFS shares), Amazon EFS, FUSE-based network filesystems, and anything without full POSIX `mmap` consistency. They can cause component crashes and silent data corruption.

## Network

Components talk over gRPC and HTTP. For high throughput, 10 Gbit/s or faster between nodes is recommended; keep latency low, ideally sub-millisecond inside a zone.

## Object storage

Required for long-term blocks, ruler configuration and Alertmanager state; see the object storage skill for supported services.

## Checked

Confirmed against the page: 1:4 CPU to memory ratio and the 8-core example, memory-heavy components, disk needs, 50 IOPS per GB, POSIX requirements, cloud disk examples, unsupported filesystems and failure modes, 10 Gbit/s network guidance, object storage. Nothing removed.

Method: docs-checked 2026-11-09 against the raw markdown of the Mimir set-up hardware-requirements page (grafana/mimir main), read in full.
