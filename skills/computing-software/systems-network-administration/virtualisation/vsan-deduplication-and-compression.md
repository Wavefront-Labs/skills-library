---
id: computing-software.systems-network-administration.virtualisation.vsan-deduplication-and-compression
name: vsan-deduplication-and-compression
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsan-deduplication, vsan-compression, vsan-space-efficiency, vsan, vmware, vsphere]
level: advanced
status: draft
description: "Choose and enable vSAN space efficiency (dedup and compression on OSA, compression-only, ESA per-policy compression), estimate savings, and know the rebuild costs."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsan/vsan/8-0/vsan-administration/increasing-space-efficiency-in-a-vsan-cluster.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSAN deduplication and compression

**Goal:** more usable capacity without surprising performance or long disk-group rebuilds.

## Options by architecture
| Architecture | Option | Scope | Notes |
|---|---|---|---|
| OSA (all-flash) | Deduplication and compression | disk group | dedup domain is the disk group; one capacity disk failure fails the whole disk group |
| OSA (all-flash) | Compression only (7.0U1+) | per capacity disk | a failed disk affects only that disk; usually the better choice |
| ESA | Compression | storage policy (default on) | done at ingest on the host; per-VM opt-out via policy *No compression* |
| ESA | Global dedup | 8.0U3+ select builds | check release notes |
Hybrid OSA clusters cannot use dedup/compression.

## Enable (OSA)
Cluster -> Configure -> vSAN -> Services -> Space efficiency -> Edit. Turning it on (or off) performs a **rolling disk-group reformat**: each disk group is evacuated and recreated. Needs free capacity (about one disk group's worth plus slack) and takes hours to days. Choose *Allow reduced redundancy* only on tiny clusters, and accept the risk window.

## Estimate and monitor
- Cluster -> Monitor -> vSAN -> Capacity: *Deduplication and compression savings* ratio and overhead.
- Typical ratios: VDI full clones 4-8x, general server VMs 1.5-2x, databases with encryption/compression inside ~1x (no gain, only CPU cost).
- RVC/CLI: `esxcli vsan storage list` shows *Deduplication: true/false* per disk.

## Gotchas
- In-guest encryption or already compressed data makes dedup pointless.
- Dedup metadata overhead is about 5% of raw capacity on OSA.
- Do not enable on a cluster above ~70% used; the reformat needs room.
- Space efficiency and vSAN encryption together: encryption happens after dedup, so both work.

## Verify
Capacity view shows the savings ratio; no resync backlog remains after the reformat; the vSAN health check *Space efficiency* is green.
