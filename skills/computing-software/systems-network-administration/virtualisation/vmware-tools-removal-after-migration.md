---
id: computing-software.systems-network-administration.virtualisation.vmware-tools-removal-after-migration
name: vmware-tools-removal-after-migration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmware-tools-removal, v2v, open-vm-tools, vmware-to-hyper-v, proxmox, hyper-v]
level: practitioner
status: draft
description: "Remove VMware Tools from Windows and Linux guests when leaving vSphere: uninstall before cutover, handle the installer refusing off-VMware, clean leftovers, and ghost NICs."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/tools/12-5-0.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Removing VMware Tools after leaving vSphere

## Best practice: uninstall on the source, just before final shutdown
Windows:
```powershell
$p = Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\* | ? DisplayName -eq 'VMware Tools'
Start-Process msiexec.exe -ArgumentList "/x $($p.PSChildName) /qn /norestart" -Wait
```
Then install target drivers if not already present (virtio-win guest tools for Proxmox/KVM;
Hyper-V drivers are in-box on supported Windows), shut down, migrate.

Linux:
```sh
dnf remove open-vm-tools open-vm-tools-desktop     # RHEL family
apt purge open-vm-tools open-vm-tools-desktop      # Debian/Ubuntu
# legacy tarball installs:
/usr/bin/vmware-uninstall-tools.pl
```

## Already migrated and the MSI refuses
Older VMware Tools installers check they run on VMware and abort ("This setup is intended
for VMware virtual machines"); newer 12.x releases allow uninstall off-platform. Options:
- Upgrade path: install a current VMware Tools MSI's uninstall (download the 12.x x64 MSI,
  `msiexec /x <msi> /qn`).
- Clean up manually as last resort: stop and delete services `VMTools`, `VGAuthService`,
  `vm3dservice`, `VMware Physical Disk Helper Service`; remove drivers via
  `pnputil /enum-drivers` → `pnputil /delete-driver oemNN.inf /uninstall` for vmxnet3,
  pvscsi, vmci, vsock, vm3d; delete the program folder and uninstall registry key.
  Snapshot first.

## Ghost hardware (Windows)
Old VMXNET3 adapters keep the static IP config; the new NIC can't take the same IP
("already assigned to another adapter").
```powershell
$env:devmgr_show_nonpresent_devices = 1
Get-PnpDevice -Class Net | ? Status -eq 'Unknown' | Select FriendlyName, InstanceId
Get-PnpDevice -Class Net | ? { $_.Status -eq 'Unknown' -and $_.FriendlyName -like '*vmxnet3*' } |
  ForEach-Object { pnputil /remove-device $_.InstanceId }
```
Then set the IP on the new adapter.

## Verify
No VMware services/drivers (`Get-Service *vm*`, `driverquery | findstr /i vm`), no ghost NICs,
target guest agent running and reporting IPs to the new hypervisor.
