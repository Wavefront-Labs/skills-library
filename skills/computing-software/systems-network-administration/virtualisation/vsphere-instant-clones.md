---
id: computing-software.systems-network-administration.virtualisation.vsphere-instant-clones
name: vsphere-instant-clones
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [instant-clone, vm-cloning, vmware, vsphere, govc]
level: advanced
status: draft
description: "Create instant clones of a running VM with the vSphere API, govc or PowerCLI, and handle guest identity refresh, memory sharing and lifecycle limits."
sources:
  - https://github.com/vmware/govmomi/blob/main/govc/USAGE.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instant clones

**Goal:** spin up identical VMs in seconds from a running parent, for VDI pools, CI runners or lab environments.

## How they work
An instant clone forks the parent's running state: memory pages are shared copy-on-write and the disk is a delta on the parent's disk. The clone starts already running.

## Create one
- govc:
```bash
govc vm.instantclone -vm parent01 -folder /DC1/vm/clones clone01
```
- PowerCLI (API call):
```powershell
$parent = Get-VM parent01
$spec = New-Object VMware.Vim.VirtualMachineInstantCloneSpec
$spec.Name = 'clone01'
$spec.Location = New-Object VMware.Vim.VirtualMachineRelocateSpec
$spec.Config = New-Object VMware.Vim.VirtualMachineConfigSpec
$opt = New-Object VMware.Vim.OptionValue
$opt.Key = 'guestinfo.ipaddress'; $opt.Value = '10.0.5.51'
$spec.Config.ExtraConfig = @($opt)
$parent.ExtensionData.InstantClone_Task($spec)
```

## Guest identity
The clone wakes with the parent's MAC-derived settings and hostname cached in the OS. Give it a new MAC (the API assigns one) and pass identity in `guestinfo.*` keys; a script in the parent reads them with `vmtoolsd --cmd "info-get guestinfo.ipaddress"` and reconfigures the NIC and hostname. VMware Tools must be running in the parent.

## Limits and gotchas
- Clone and parent must be on the same host type and the delta lives on the parent's datastore unless relocated.
- Memory sharing breaks as clones diverge; size host RAM for divergence, not for the fresh state.
- Windows domain identity is not handled for you; Horizon uses ClonePrep for that.
- The parent cannot be deleted while clones depend on its disk.
- Snapshots and vMotion of clones are supported; Storage vMotion inflates them.

## Verify
`govc vm.info clone01` shows it powered on; the guest reports its new IP after the identity script runs.
