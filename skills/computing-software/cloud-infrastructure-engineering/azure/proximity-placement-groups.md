---
id: computing-software.cloud-infrastructure-engineering.azure.proximity-placement-groups
name: proximity-placement-groups
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vm-availability, ppg, proximity-placement, low-latency, allocation-failure]
level: practitioner
status: docs-checked
description: "Use Azure proximity placement groups for low-latency VM colocation, intent VM sizes, deployment order, alignment checks and how to avoid allocation failures."
sources: ["https://learn.microsoft.com/en-us/azure/virtual-machines/co-location", "https://learn.microsoft.com/en-us/cli/azure/ppg"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proximity placement groups (PPG)

**Goal:** keep VMs physically close (lowest latency) for chatty tiers such as app-to-database.

A proximity placement group is a logical grouping that makes sure Azure compute resources are physically located close to each other. It is a colocation constraint, not a pinning mechanism: it is pinned to a specific data center when the first resource that uses it is deployed, and is no longer pinned once all resources using it have been stopped (deallocated) or deleted.

## Create and use
```bash
az ppg create -g rg -n ppg1 -l westeurope --type Standard
az vm create -g rg -n vm1 --image Ubuntu2204 --size Standard_D4s_v5 --ppg ppg1
az vmss create ... --ppg ppg1
az vm availability-set create -g rg -n avset1 --ppg ppg1
```
- A PPG can be used with VMs, availability sets and scale sets. For availability sets and scale sets, set the PPG at the resource level rather than on individual VMs.
- To move an existing resource into a PPG, deallocate it first (it may be redeployed to a different data center).
- A single PPG cannot span availability zones. For lowest latency, put the PPG and the whole solution in one zone; for resiliency, spread instances across zones instead.

## Intent (VM sizes) and zone
```bash
az ppg create -g rg -n ppg1 --intent-vm-sizes Standard_E64s_v4 Standard_M416ms_v2 --zone 1
```
- The intent lists the VM sizes you plan to use; creation or update succeeds only if at least one data center supports all of them, otherwise it fails with `OverconstrainedAllocationRequest`. Intent gives no capacity reservation or guarantee.
- The zone parameter can only be given at creation, only together with intent, and only one zone. Intent needs API version 2021-11-01 or higher. Intent can be changed on update after deallocating all VMs.
- With intent, VMs need not be deployed in any particular order or in one ARM template.

## Avoid allocation errors (without intent)
1. Specify all required VM types upfront in one template, or follow a deployment sequence.
2. If a deployment fails, restart it with the VM size that failed as the first size deployed.
3. A second VM of a different size can fail with `OverconstrainedAllocationRequest` if that size doesn't exist in the data center chosen for the first.
4. Elastic workloads (adding and removing instances) and deallocate/start cycles can fail with `AllocationFailure`, since capacity isn't kept once a VM is deallocated.
5. When reusing a PPG from which VMs were deleted, wait for the deletion to complete before adding VMs.

## Alignment
`az ppg show -g rg -n ppg1 --include-colocation-status true` returns the colocation status: Aligned, Unknown (at least one VM deallocated) or Not aligned. To realign, deallocate and restart the affected resources; for an availability set or scale set, deallocate all its VMs first. After an allocation failure you may need to deallocate every resource in the PPG (including aligned ones) and restart them.

## Tradeoffs
Planned maintenance such as datacenter hardware decommissioning can move resources and break alignment. Use accelerated networking together with a PPG for the lowest latency.

## Checked
Date: 2026-11-07
Read in full: Learn "Proximity placement groups" (colocation constraint, intent and zone rules, allocation failure cases, alignment status, best practices) and the `az ppg` reference page's `az ppg create` section (`--intent-vm-sizes`, `--zone`, `--ppg-type --type {Standard, Ultra}`; `--include-colocation-status` found by searching the page, not read in its parameter text). `--ppg` on `az vm create`, `az vmss create` and `az vm availability-set create` was verified against the CLI references by the review tooling, not read by me.
Removed as unconfirmed: "one availability zone" phrasing that implied a PPG can be combined with a zone without intent, the capacity-reservation advice, "put the scarcest SKU first" rule, the "stop and start together resets placement" shortcut (replaced with the page's own realign steps), and the invented sockperf/ping Verify step.
Method: documentation only; no commands were run.
