---
id: computing-software.systems-network-administration.virtualisation.vmx-advanced-configuration-parameters
name: vmx-advanced-configuration-parameters
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmx-advanced-settings, vsphere-vm-administration, advanced-configuration, disk-enableuuid, powercli, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Set and audit VM advanced configuration (VMX) parameters safely: common keys like disk.EnableUUID, hardening and tools keys, PowerCLI New-AdvancedSetting and pitfalls."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-virtual-machine-administration-guide-8-0.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/tools/13-1-0/vmware-tools-administration/configuring-vmware-tools-components/using-vmware-tools-configuration-file/security-considerations-to-configure-vmware-tools.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage/getting-started-with-cloud-native-storage-in-vsphere/cloud-native-storage-for-vsphere-administrators/configure-kubernetes-cluster-in-vsphere-virtual-machines.html
  - https://developer.broadcom.com/powercli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VMX advanced configuration parameters

Edit Settings → VM Options → Advanced → **Edit Configuration** adds `key = "value"` lines to
the .vmx. Most changes require the VM **powered off** (or take effect at next power-on).

## Frequently needed keys
| Key | Value | Purpose |
|---|---|---|
| `disk.EnableUUID` | TRUE | Guest sees consistent disk serials; required by Kubernetes CSI, some backup VSS, and Linux `/dev/disk/by-id` |
| `isolation.tools.copy.disable` / `paste.disable` | TRUE | Hardening: clipboard copy/paste and drag-and-drop are deactivated by default; these keep it that way |
| `isolation.device.connectable.disable` | TRUE | Device connect/disconnect is deactivated by default; this keeps non-admin users from reconnecting devices |

## PowerCLI
```powershell
$vm = Get-VM app01
New-AdvancedSetting -Entity $vm -Name disk.EnableUUID -Value TRUE -Confirm:$false
Get-AdvancedSetting -Entity $vm -Name disk.EnableUUID
Get-VM | Get-AdvancedSetting -Name isolation.tools.copy.disable | ? Value -ne 'TRUE'   # audit
Get-AdvancedSetting -Entity $vm -Name log.keepOld | Set-AdvancedSetting -Value 10 -Confirm:$false
```

## Gotchas
- Keys are case-insensitive but values are strings; a typo is silently stored and does
  nothing. Check vmware.log at power-on for unrecognised keys.
- Templates and content-library items carry the settings; fix the template.
- Some keys are reserved and rejected by vCenter while the VM is powered on.
- Do not hand-edit the .vmx while the VM is registered and on: hostd overwrites it. If
  you must, unregister, edit, re-register.

## Verify
Settings visible under Configuration Parameters; behaviour confirmed in the guest (the
guest sees consistent disk identifiers after disk.EnableUUID).

## Checked
2026-10-31: Confirmed `disk.EnableUUID` (for Kubernetes node VMs) against the vSphere 8.0
Cloud Native Storage "Configure Kubernetes Cluster" page, and the isolation.tools copy /
paste and device-connectable hardening parameters plus their deactivated-by-default
behaviour against the VMware Tools 13.1 "Security Considerations to Configure VMware
Tools" page. Removed the table rows for ctkEnabled, numa.vcpu.preferHT,
tools.guest.desktop.autolock, RemoteDisplay.maxConnections, log.keepOld, log.rotateSize,
vmotion.maxSwitchoverSeconds, hypervisor.cpuid.v0 and svga.present (not confirmable in
fetched documentation), and the uuid.bios example.
Method: documentation only; no commands were run.
