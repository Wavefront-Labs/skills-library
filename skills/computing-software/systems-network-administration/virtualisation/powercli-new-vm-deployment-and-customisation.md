---
id: computing-software.systems-network-administration.virtualisation.powercli-new-vm-deployment-and-customisation
name: powercli-new-vm-deployment-and-customisation
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [new-vm-powercli, powercli, guest-customization, vm-deployment, vmware, vsphere]
level: practitioner
status: docs-checked
description: "PowerCLI New-VM from a template or content library item with an OS customisation spec, and Set-OSCustomizationNicMapping static IP parameters, per the reference pages."
sources:
  - https://developer.broadcom.com/powercli/latest/vmware.vimautomation.core/commands/new-vm
  - https://developer.broadcom.com/powercli/latest/vmware.vimautomation.core/commands/set-oscustomizationnicmapping
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# New-VM with a customisation spec (PowerCLI reference)

**Goal:** deploy a VM from a template or content library item and give it a static IP
through an OS customisation spec.

## New-VM
`New-VM` has separate parameter sets; the ones used here:
- From a template: `-Template <Template>` (required, position 1). Passing it through the
  pipeline is deprecated and will be deactivated in a future release.
- From a content library item: `-ContentLibraryItem <ContentLibraryItem>` (required,
  position 1, accepts pipeline input).
- Common optional parameters on these sets: `-Name`, `-Datastore`, `-VMHost`, `-Location`,
  `-ResourcePool`, `-OSCustomizationSpec` (a customisation specification applied to the new
  VM) and `-DiskStorageFormat`.
- `-ResourcePool` accepts VMHost, Cluster, ResourcePool and VApp objects; if omitted the VM is
  added to the resource pool of its host.
- `-DiskStorageFormat` accepts `Thin`, `Thick` and `EagerZeroedThick`.
- `-RunAsync` returns immediately with a Task object instead of waiting for completion.

## Set-OSCustomizationNicMapping
Pipe a spec's mapping into it, as in the page's examples:
```powershell
Get-OSCustomizationSpec Spec | Get-OSCustomizationNicMapping | Set-OSCustomizationNicMapping -IpMode UseStaticIp -IpAddress 10.10.0.1 -SubnetMask 255.255.255.0 -DefaultGateway 10.10.0.1 -Dns 10.10.150.1
```
- `-IpAddress`: using it automatically sets `-IpMode` to UseStaticIp.
- `-IpMode` valid values: UseDhcp, PromptUser, UseVCApplication, UseStaticIP.
- `-SubnetMask` (position 1), `-DefaultGateway` (position 2) and `-Dns` (position 3, string
  array) are positional; `-Dns` applies only to Windows operating systems.
- `-Position` selects which mapping to modify; `-OSCustomizationNicMapping` takes the
  mapping object(s) directly.

## Checked
Date: 2026-11-07. Read the New-VM and Set-OSCustomizationNicMapping reference pages and
searched them for the parameters above; the full New-VM description text and examples were
not read line by line. Removed as not on those pages: the CSV driven loop,
`New-OSCustomizationSpec -Type NonPersistent`, `Set-VM`, `Set-NetworkAdapter` and `Start-VM`
steps, the `Get-VIEvent` wait for `CustomizationSucceeded`/`CustomizationFailed`, the
VMware Tools, Sysprep and cloud-init notes, the 5 to 10 concurrent clones advice and the
Verify step.
Method: documentation only; no commands were run.
