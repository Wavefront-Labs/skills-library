---
id: computing-software.systems-network-administration.virtualisation.vds-config-export-and-restore
name: vds-config-export-and-restore
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vds-export, vds-config-backup, distributed-switch, vsphere-networking, powercli, vmware, vsphere]
level: practitioner
status: draft
description: "Back up and restore vSphere Distributed Switch and port group configuration with export/import, including preserving identifiers, and when restore is the right tool."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking-8-0.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Export, import and restore a vDS

vCenter file-based backup includes the vDS, but restoring all of vCenter to undo one
port-group mistake is overkill. Keep per-switch exports.

## Export (before every change, and on a schedule)
UI: Networking → right-click vDS → Settings → Export Configuration → "Distributed switch
and all port groups" → zip.
```powershell
Get-VDSwitch | ForEach-Object {
  Export-VDSwitch -VDSwitch $_ -Destination "<BACKUP_DIR>\vds-$($_.Name)-$(Get-Date -f yyyyMMdd).zip" -Force }
Get-VDPortgroup -Name "App-VLAN20" | Export-VDPortGroup -Destination "<BACKUP_DIR>\pg-app20.zip"
```

## Three different operations
| Operation | Use when | Identifiers |
|---|---|---|
| **Restore** (right-click vDS → Settings → Restore Configuration) | Roll back settings of the *existing* switch | keeps the switch; host/VM attachments untouched |
| **Import** with "Preserve original distributed switch and port group identifiers" | Rebuilding vCenter from scratch, hosts still have the old vDS | reattaches existing hosts/VMs cleanly |
| **Import** without preserve | Clone a design to another vCenter/lab | new UUIDs; hosts must be migrated |

PowerCLI equivalents: `New-VDSwitch -BackupPath x.zip -KeepIdentifiers -Location (Get-Datacenter dc1)`
for import; `Set-VDSwitch -VDSwitch $vds -BackupPath x.zip` for restore;
`Set-VDPortgroup -BackupPath` for one port group.

## Gotchas
- Export contains config only: not host uplink-to-vmnic mapping and not VMkernel IPs.
  Document those separately (`Get-VMHostNetworkAdapter -VMKernel | Export-Csv`).
- Restoring a port group with a different VLAN immediately moves every VM on it.
- Version: an export from a newer vDS version cannot be imported into an older vCenter.
- After a vCenter rebuild, import with preserve **before** adding hosts back, otherwise
  hosts show the switch as out of sync and you migrate everything by hand.

## Verify
Unzip and confirm `data.bin` and `META-INF` present; in a lab, import with
"preserve identifiers" into a test vCenter at least once per major version.
