---
id: computing-software.systems-network-administration.virtualisation.encrypted-vmotion
name: encrypted-vmotion
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmotion, encrypted-vmotion, vsphere-security, opportunistic, required, migration-encryption, vmware, vsphere]
level: practitioner
status: draft
description: "Control vMotion encryption per VM: disabled, opportunistic (default) or required; what it costs, how it interacts with encrypted VMs and cross-vCenter moves."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypted vMotion

**Goal:** VM memory contents (passwords, keys, data) are never sent across the vMotion
network in clear text where policy requires it.

## Settings (VM → Edit Settings → VM Options → Encryption → Encrypted vMotion)
| Value | Behaviour |
|---|---|
| Disabled | Never encrypt |
| **Opportunistic** (default) | Encrypt when both source and destination hosts support it (ESXi 6.5+); otherwise plain |
| Required | Only migrate to hosts that support encryption; otherwise fail |
Encrypted VMs (VM encryption with a key provider) always use encrypted vMotion; the
setting is forced to Required.

## How it works
vCenter generates a one-time 256-bit key and nonce per migration and passes them to both
hosts over the management channel; vMotion traffic is AES-GCM encrypted. No KMS needed
for encrypted vMotion of unencrypted VMs.

## Cost
CPU on source and destination for the crypto (AES-NI makes it modest); throughput on
25 GbE+ links may drop measurably for very large memory VMs. Test with a large VM before
setting Required everywhere.

## PowerCLI
```powershell
$spec = New-Object VMware.Vim.VirtualMachineConfigSpec
$spec.MigrateEncryption = 'required'     # disabled | opportunistic | required
(Get-VM app01).ExtensionData.ReconfigVM($spec)
Get-VM | Select Name, @{n='vMotionEnc';e={$_.ExtensionData.Config.MigrateEncryption}}
```

## Gotchas
- Cross-vCenter moves of **encrypted** VMs need both vCenters to share the key provider
  (same KMS cluster name) or the move fails.
- Storage vMotion data is not covered by this setting; disk encryption is VM encryption's
  job.
- Physical isolation of the vMotion VLAN is still recommended; encryption complements it.

## Verify
Report shows Required on VMs in scope (PCI, regulated); a migration of such a VM to an
old host fails at compatibility check rather than migrating in clear text.
