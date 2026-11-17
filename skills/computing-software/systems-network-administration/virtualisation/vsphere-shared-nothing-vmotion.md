---
id: computing-software.systems-network-administration.virtualisation.vsphere-shared-nothing-vmotion
name: vsphere-shared-nothing-vmotion
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [shared-nothing-vmotion, vmotion, storage-vmotion, vmware, vsphere]
level: practitioner
status: draft
description: "Migrate a running VM between hosts or clusters that share no storage by changing compute and storage together, with sizing limits and network mapping."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
  - https://knowledge.broadcom.com/external/article?legacyId=2046091
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shared-nothing vMotion (compute and storage together)

**Goal:** move a powered-on VM to a host that cannot see its datastore, for example between clusters or from local disk to a SAN.

## Requirements
- Both hosts managed by the same vCenter (cross-vCenter is a separate workflow), vMotion vmkernel adapters on both with L3 reachability.
- Licence that includes vMotion and Storage vMotion.
- Destination datastore space for all disks plus swap.

## Run it
- vSphere Client: VM -> **Migrate** -> *Change both compute resource and storage* -> pick host/cluster, datastore (optionally per disk), network mapping, vMotion priority.
- PowerCLI:
```powershell
$vm = Get-VM web01
$dst = Get-VMHost esx21.example.com
$pg = Get-VDPortgroup -Name 'pg-web-b'
Move-VM -VM $vm -Destination $dst -Datastore (Get-Datastore local-esx21) `
  -NetworkAdapter (Get-NetworkAdapter -VM $vm) -PortGroup $pg -DiskStorageFormat Thin
```

## How the data moves
Disk blocks are copied over the **vMotion network** (or the *provisioning* TCP/IP stack if a vmk is tagged for it), then memory is pre-copied, then switchover. Duration scales with disk size, so plan bandwidth: 1 TB on 10 GbE is roughly 15-25 minutes.

## Gotchas
- It counts against both vMotion and Storage vMotion concurrency limits on the host.
- Different vDS on source and destination: map each adapter to a destination port group or the task fails validation.
- EVC/CPU compatibility still applies; validation errors are the same as plain vMotion.
- Large writes during copy extend mirror time; avoid during backup windows.

## Verify
Task completes, `Get-VM web01 | Select VMHost, @{n='DS';e={(Get-Datastore -RelatedObject $_).Name}}` shows the new host and datastore, and the guest kept its network session.
