---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-wan-accelerators
name: veeam-wan-accelerators
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [wan-accelerator, veeam, global-cache, backup-copy, replication, wan-optimization, high-bandwidth-mode]
level: advanced
status: docs-checked
description: "Use Veeam WAN accelerators for copy and replication over slow links: source and target roles, global cache sizing and population, high bandwidth mode, and when not to bother."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/wan_acceleration.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/wan_global_cache.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Veeam WAN accelerators

**Goal:** reduce the data sent over a WAN by off-site backup copy and replication jobs.

## What it is
WAN acceleration is specific to off-site backup copy jobs and replication jobs. You deploy a pair of WAN accelerators (source and target). It combines network traffic compression, multistreaming upload, global data deduplication and variable block size deduplication. Availability depends on the licence; see the Veeam Data Platform Feature Comparison.

## Global cache
- It is a folder on the target WAN accelerator. By default it is the VeeamWAN folder on the disk with the most free space; you can choose another folder when configuring the target accelerator.
- Default size is 100 GB; at least 40 GB is recommended. More space lets more repeating blocks be cached and makes acceleration more efficient.
- The size is specified per source WAN accelerator: one target serving several sources allocates that amount for each source, so the cache grows proportionally.
- It is populated during the first job cycle, so acceleration is minimal at first and improves with each backup copy interval. Frequently sent blocks are added; blocks not sent or reused for a period are removed; periodic consistency checks remove corrupted blocks.
- You can populate it manually before the first run so WAN traffic is minimal from the first session (see "Manual Population of Global Cache" in the Veeam guide).

## High bandwidth mode
- Recommended for WAN links faster than 100 Mbps.
- It does not use the global cache (the cache is not used when both accelerators in the pair run in this mode); it uses a faster compression method, optimised digest processing and an alternative deduplication mechanism.
- Enable it on the accelerators at both the source and target sites. A target with it enabled can serve different source accelerators in different modes, each per its own setting.

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center pages "WAN Acceleration" and "WAN Global Cache" (build 13.x).
Removed (not on those pages): the "start around 100 GB" sizing rule beyond the documented default, digest-space percentage, "1 Gbps+ direct mode is often faster", the 100 Mbps lower bound for usefulness, "high bandwidth is default on newer versions", cache corruption/clear-and-repopulate advice, IOPS remarks, the Populate cache menu path and the Verify section.
Method: documentation only; no commands were run.
