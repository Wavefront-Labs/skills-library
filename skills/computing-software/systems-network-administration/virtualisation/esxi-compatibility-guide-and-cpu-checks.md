---
id: computing-software.systems-network-administration.virtualisation.esxi-compatibility-guide-and-cpu-checks
name: esxi-compatibility-guide-and-cpu-checks
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmware-hcl, broadcom-compatibility-guide, esxi-installation, cpu-support, io-devices, vmware, esxi, vsphere]
level: practitioner
status: draft
description: "Check servers, CPUs, NICs and HBAs against the Broadcom Compatibility Guide before installing or upgrading ESXi, and match driver and firmware versions."
sources:
  - https://compatibilityguide.broadcom.com/
  - https://knowledge.broadcom.com/external/article?legacyId=82794
  - https://knowledge.broadcom.com/external/article/318697
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compatibility guide and CPU support checks

**Goal:** never install or upgrade onto hardware that ESXi will not support or will warn about at boot.

## What to check (in order)
1. **System/Server**: model and the ESXi release listed (compatibilityguide.broadcom.com, "Systems/Servers").
2. **CPU series**: listed for the target release. KB 318697 lists CPUs deprecated or unsupported in vSphere 8 (for example Intel Broadwell-DE and older Xeon families). Deprecated = warning at install; unsupported = blocked.
3. **IO devices**: NIC, HBA, RAID/BOSS, NVMe. Match by VID/DID/SVID/SSID, not marketing name.
4. **Driver and firmware pair**: the guide lists a supported driver version together with a firmware version. Drivers newer than the firmware support is a common cause of PSODs and path flaps.
5. **vSAN**: use the vSAN-specific lists (ReadyNode, controller and disk firmware).

## Get the IDs from a running host
```sh
esxcli hardware platform get                  # vendor, model, serial
esxcli hardware cpu global get; vim-cmd hostsvc/hosthardware | grep -i description
vmkchdev -l | grep vmnic                      # VID:DID SVID:SSID per device
esxcli network nic get -n vmnic0              # driver + firmware version
esxcli storage core adapter list
esxcli software vib list | grep -i <driver>
```
From PowerCLI, `Get-EsxCli -V2` then `$esxcli.hardware.pci.list.Invoke()` gives VendorID/DeviceID/SubVendorID/SubDeviceID for every device.

## Before an upgrade
- Run the vLCM hardware compatibility check (cluster -> Updates -> Hardware compatibility) which compares the HCL against the target image.
- The installer and `esxcli software profile update --dry-run` warn on unsupported CPUs; `allowLegacyCPU=true` bypasses it and is unsupported (labs only).

## Gotchas
- An OEM-rebranded NIC has a different SSID than the vendor's own card; check the exact SSID.
- "Certified" for a release does not mean every update; check the specific U-level.

## Verify
Every device, driver and firmware triple is listed for the exact ESXi build; findings are recorded in the change ticket.
