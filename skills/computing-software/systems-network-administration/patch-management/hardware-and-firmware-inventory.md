---
id: computing-software.systems-network-administration.patch-management.hardware-and-firmware-inventory
name: hardware-and-firmware-inventory
category: computing-software
field: systems-network-administration
product: patch-management
tags: [hardware-inventory, firmware-inventory, redfish, bios-version, patch-management]
level: practitioner
status: draft
description: "Collect a hardware and firmware inventory for patching: model, serial, BIOS/BMC/NIC/disk firmware versions via Redfish, dmidecode, fwupd and PowerShell CIM."
sources:
  - https://www.dmtf.org/standards/redfish
  - https://fwupd.github.io/libfwupdplugin/
  - https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-bios
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hardware and firmware inventory

**Goal:** know every server and endpoint's model and firmware component versions so firmware advisories (BMC, BIOS, NIC, drive) can be matched like software CVEs.

## What to capture per device
Manufacturer, model, serial/service tag, BIOS/UEFI version and date, BMC (iDRAC/iLO/XCC) version, NIC and HBA firmware, drive model + firmware, CPU microcode revision, TPM version, warranty end.

## Out-of-band via Redfish (no OS needed)
```sh
BMC=https://10.0.10.21
curl -sk -u "$U:$P" $BMC/redfish/v1/Systems/System.Embedded.1 | jq '{Model,SerialNumber,BiosVersion}'
curl -sk -u "$U:$P" "$BMC/redfish/v1/UpdateService/FirmwareInventory?\$expand=*" \
  | jq -r '.Members[] | [.Name, .Version, .Updateable] | @tsv'
```
FirmwareInventory lists every updatable component with its version; the URI under Systems varies by vendor (`System.Embedded.1` Dell, `1` HPE, `Self` some others), so read `/redfish/v1/Systems` first.

## In-band Linux
```sh
sudo dmidecode -s system-product-name; sudo dmidecode -s system-serial-number; sudo dmidecode -s bios-version
fwupdmgr get-devices --json | jq -r '.Devices[] | [.Name, .Version] | @tsv'
ethtool -i eno1 | grep -E 'driver|firmware-version'
sudo smartctl -i /dev/sda | grep -E 'Model|Firmware'
grep -m1 microcode /proc/cpuinfo
```

## In-band Windows
```powershell
Get-CimInstance Win32_BIOS | Select SMBIOSBIOSVersion, ReleaseDate, SerialNumber
Get-CimInstance Win32_ComputerSystem | Select Manufacturer, Model
Get-CimInstance Win32_DiskDrive | Select Model, FirmwareRevision
Get-NetAdapter | Select Name, DriverVersion, DriverDate
Get-Tpm | Select ManufacturerVersion
```
At scale: ConfigMgr hardware inventory classes, Intune device hardware report, or vendor consoles (OpenManage Enterprise, HPE OneView, XClarity) which export CSV of all component versions.

## Normalise and store
Write to the CMDB or a table keyed on serial, with `component, version, collected_at, source`. Compare against the vendor's current catalog to flag out-of-date firmware.

## Gotchas
- BIOS versions are vendor-formatted (Dell `2.19.1`, HPE `U46 v2.80`), so compare within vendor only.
- VMs report the hypervisor's virtual BIOS; exclude them from firmware compliance.
- BMC credentials for inventory should be a read-only role.

## Verify
Spot-check three servers: console/BMC page versions equal the inventory row; record age (collected_at) is under 7 days for all active devices.
