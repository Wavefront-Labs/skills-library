---
id: computing-software.systems-network-administration.backup-and-recovery.fitting-the-backup-window
name: fitting-the-backup-window
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-strategy, backup-window, throughput, bottleneck-analysis, concurrent-tasks, change-rate, backup-performance, veeam]
level: practitioner
status: draft
description: "Make backups finish inside the window: calculate required throughput, find the bottleneck (source, proxy, network, target), parallelism, incremental-forever and snapshot offload."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fitting backups into the backup window

**Goal:** all backups (and their copies offsite) complete before business hours, with
headroom for growth.

## Do the arithmetic
Required throughput = data to move / window length.
- Daily incrementals: data ≈ total protected × daily change rate (often 2-5% for servers,
  more for databases with index rebuilds). 50 TB × 3% = 1.5 TB; in a 6 h window that's
  ~70 MB/s sustained, before dedupe/compression.
- Fulls (if any) and offsite copies add to this. Plan for 20-30% growth per year.

## Find the bottleneck
Backup products report stage load; Veeam shows **Bottleneck: Source / Proxy / Network /
Target** with percentages per job.
| Bottleneck | Typical causes | Fixes |
|---|---|---|
| Source | Production storage busy, NBD over 1 GbE management network | Storage snapshot integration, HotAdd/SAN mode, more streams per disk |
| Proxy | CPU (compression, encryption), too few task slots | More vCPU/proxies, lighter compression |
| Network | 1 GbE links, WAN to offsite | 10/25 GbE backup network, WAN acceleration, schedule copies separately |
| Target | Slow disks, dedupe appliance ingest, small block random writes | Faster repository, per-VM backup files, block clone filesystem, more repository task slots |

## Techniques
- **Forever-incremental with CBT/RCT** and synthetic fulls with block cloning: no read of
  unchanged data ever.
- **Parallelism:** more concurrent tasks (per proxy, per repository) until the next
  stage saturates; watch production latency.
- **Stagger** jobs by priority and size; long-running big VMs start first.
- **Storage snapshots** (array integration) shorten the VM snapshot lifetime and offload reads.
- Separate the backup window from the **copy window**: offsite copy can run during the day if
  it doesn't hit production.
- For very large file servers: file-level incremental (NAS backup with changed file tracking).

## Gotchas
- Increasing concurrency on the source side can hurt production; agree acceptable latency.
- A full rerun after CBT reset can take days; know which events reset CBT.

## Verify
Last 30 days: every job's end time inside the window with margin (e.g. ≥ 20%); trend of
duration vs data growth projected 12 months shows when you'll run out of window.
