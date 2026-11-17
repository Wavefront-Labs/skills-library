---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.nalsd-bill-of-materials-and-cost-estimate
name: nalsd-bill-of-materials-and-cost-estimate
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, nalsd, nalsd-bill-of-materials, cost-estimate, capacity-estimation, back-of-the-envelope]
level: advanced
status: docs-checked
description: "Produce a NALSD resource estimate: translate requirements into machines, disks and network per component with explicit assumptions, then price it from your own cost data."
sources: ["https://sre.google/workbook/non-abstract-design/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NALSD bill of materials

**Goal:** turn a design into concrete resource counts, the step that makes a whiteboard design non-abstract. The
Workbook drives its exercise to discrete results such as the number of machines, while stressing that sound
reasoning and stated assumptions matter more than the final values.

## Inputs
- Quantified requirements: transaction rates, record sizes, daily volume, SLOs.
- Per-component unit capacities and the assumed machine shape.

## Method (Workbook AdWords example)
For each component compute the binding resource with scientific notation and explicit units:
```
disks (IOPS):  (5 x 10^5 writes/s) / (200 IOPS per disk) = 2,500 disks
RAM:           100 TB / (64 GB RAM per machine) = 1,563 machines
tasks:         (1.02 x 10^6 queries/s) / (40 operations/s) = 25,500 tasks
memory/task:   (4 x 10^12 bytes) / 25,500 tasks = 157 MB/task
tasks/machine: (6.4 x 10^10 bytes) / (1.57 x 10^8 bytes) = 408 tasks/machine
network:       (1.02 x 10^6 queries/s) x (2 x 10^3 bytes) = 2.04 GB/s = 16 Gbps
```
The final multi-datacenter design needs about 4 TB of RAM per datacenter, so 64 machines of 64 GB, using about 25%
of each machine's network bandwidth. Replicating work (two shards per record) doubles the transaction rates
downstream, so recompute after each design change.

## Then price it
- Multiply by datacenters and redundancy, and add growth headroom for the plan period.
- Price each line from your own cost data or the vendor's pricing page, and list the assumptions that most change
  the total.

## Sanity checks
- Which resource binds first: IOPS, capacity, RAM or network?
- Compare with similar existing systems.

## Verify
- [ ] Resource table reviewed with assumptions; the most cost-sensitive assumption is validated by measurement.

## Checked
2026-11-01. Confirmed against the SRE Workbook chapter "Introducing Non-Abstract Large System Design": 200 IOPS per disk, 2,500 disks, 64 GB machines, 1,563 machines, 25,500 tasks, 157 MB per task, 408 tasks per machine, 16 Gbps, about 4 TB RAM and 64 machines per datacenter, 25% network use.
Removed: the invented photo-storage figures, the price table, the 1 TB/3 TB/1.1 PB arithmetic, napkin-math and software-engineering-in-SRE sources, and the N+2 claim.
Method: documentation only; no commands were run.
