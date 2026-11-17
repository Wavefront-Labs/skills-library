---
id: computing-software.systems-network-administration.virtualisation.vsan-esa-vs-osa-architecture
name: vsan-esa-vs-osa-architecture
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsan, vsan-esa, vsan-osa, disk-group, storage-pool, cache-tier, capacity-tier, vsan-hcl, readynode, vmware, vsphere]
level: advanced
status: draft
description: "Choose and build vSAN OSA (cache+capacity disk groups) or ESA (single-tier NVMe storage pool): hardware rules, network speed, capacity maths and what cannot be converted."
sources:
  - https://core.vmware.com/resource/vsan-esa-frequently-asked-questions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSAN ESA vs OSA

**Goal:** pick the right vSAN architecture for the hardware you have, and lay out disks so
a single device failure does not take out more than you planned.

## Original Storage Architecture (OSA)
- **Disk groups:** 1 cache device (SSD/NVMe) + 1-7 capacity devices; up to 5 disk groups
  per host. The cache device failing takes its **whole disk group** offline.
- Cache sizing: hybrid uses 70% read cache / 30% write buffer; all-flash uses cache only
  as write buffer (max 600 GB used per cache device in older versions, larger in 8.x).
- 10 GbE minimum for all-flash (25 GbE recommended).
- More, smaller disk groups = smaller failure domain and more parallelism.

## Express Storage Architecture (ESA, vSAN 8+)
- **Storage pool:** all devices are NVMe TLC, each contributes capacity and performance;
  no cache tier, so one device failure only affects that device.
- Requires ESA-certified **ReadyNodes** (or approved hardware), 25 GbE minimum
  (100 GbE recommended for larger nodes), and vSAN Advanced/Enterprise-class licensing
  (now bundled in VCF/VVF).
- Log-structured file system: RAID-5/6 erasure coding at RAID-1-like performance, so
  RAID-5 becomes the default efficient choice; compression on by default.

## Capacity maths (rule of thumb)
Usable ≈ raw × policy efficiency × (1 − slack). Efficiency: RAID-1 FTT=1 50%, RAID-5
(4+1 ESA / 3+1 OSA) 75-80%, RAID-6 (4+2) 67%. Keep **slack ~25-30%** (OSA) or follow
ESA's operations reserve + host rebuild reserve settings so rebuilds and policy changes
can complete.

## Things you cannot do
- Convert a cluster in place from OSA to ESA: build a new cluster and migrate VMs.
- Mix OSA and ESA hosts in one cluster.
- Use non-HCL controllers or firmware: the health service will flag it and support will
  ask you to fix it first. Check the vSAN HCL for controller, driver **and** firmware.

## Verify
Cluster → Monitor → vSAN → Skyline Health: hardware compatibility green; Configure →
vSAN → Disk Management shows expected disk groups (OSA) or pool devices (ESA) per host
with equal capacity across hosts.
