---
id: computing-software.cloud-infrastructure-engineering.azure.vm-sla-tiers-and-composite-availability
name: vm-sla-tiers-and-composite-availability
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vm-availability, vm-sla, sla-tiers, composite-sla, availability-zones]
level: practitioner
status: draft
description: "Map Azure VM deployment patterns to SLA tiers (single VM disk type, availability set, zones) and calculate composite availability."
sources: ["https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VM SLA tiers

**Goal:** pick the VM pattern whose published SLA meets the availability target, and compute the end-to-end number.

## Published tiers (verify against the current SLA document)
- Single VM using Premium SSD or Ultra Disk for all disks: 99.9%.
- Single VM with Standard SSD: 99.5%; Standard HDD: 95%.
- Two or more VMs in an availability set (different fault/update domains): 99.95%.
- Two or more VMs across availability zones: 99.99%.
- VM Scale Sets: SLA follows the same zone/availability-set deployment rules.

## Composite availability
Serial dependencies multiply: `A = A1 x A2 x ...`. Example: web 99.99% x database 99.99% x storage 99.9% = about 99.88%. Parallel redundancy: `1 - (1-A)^n` for independent copies. A higher VM SLA does not help if a single-region dependency (database, DNS, identity) is lower.

## Process
1. Define the target (for example 99.95%) and the user-journey dependency chain.
2. List each component's SLA from the SLA document; multiply along the chain.
3. Add redundancy to the weakest link (zones, paired region, replicas) and recompute.
4. Remember SLA is a credit mechanism, not a guarantee; design with failure testing (Chaos Studio) and measure real availability against SLOs.

## Gotchas
- SLA terms require meeting conditions (for example two or more instances, specific disk types).
- Planned maintenance on single VMs is excluded or reboots the VM; availability sets spread updates.
- Zones: all instances must be in different zones.

## Verify
Record the computed number beside the Azure Monitor availability measurement; reconcile quarterly.
