---
id: computing-software.cloud-infrastructure-engineering.minio.scanner
name: scanner
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, scanner, object-scanner, mc-admin-scanner-info, scan-cycle, lifecycle, heal-check, usage-metrics]
level: practitioner
status: docs-checked
description: "Understand the MinIO object scanner tasks, cluster and bucket level scanning with 16 scan passes, factors that affect scan length and how to read mc admin scanner info output."
sources: ["https://github.com/minio/docs/blob/main/source/operations/concepts/scanner.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO object scanner

The scanner is MinIO's built-in background process that checks objects and applies scheduled actions:
- calculate data usage on drives
- evaluate and apply lifecycle and object retention rules
- perform bucket and site replication
- check for missing or corrupted data or parity shards and heal them

## How it scans
- Cluster level: buckets are split into groups scanned one group at a time. New buckets since the last scan go first; the rest are randomised. All groups finish before a new round starts.
- Bucket level: items are grouped and selected by a hash of the object name. Across 16 scans every object in the namespace is checked. Prefixes known to be new are fully scanned.

## Scan length and performance
The scanner yields to client read and write requests. By default it waits a factor of `10.0` times the length of each operation before the next one; the factor depends on the scanner speed setting. Duration depends on drive type, IOPS and throughput, object count and size, other activity, node resources, cluster size, erasure set count versus drive count (one 16 drive set scans slower than two 8 drive sets) and bucket hierarchy complexity.

## Inspecting
Run `mc admin scanner info` for status and time since the last full scan. Output includes "Last full scan time", "Current cycle", "Active drives" and per-minute statistics such as Objects Scanned, ILM checks, Check Replication and Yield. Usage metrics reflect the last completed scan, so recent `PUT` or `DELETE` operations show only after the next scan of that bucket.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Object Scanner page (scanner.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
