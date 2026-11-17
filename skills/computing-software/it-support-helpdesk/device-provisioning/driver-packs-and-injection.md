---
id: computing-software.it-support-helpdesk.device-provisioning.driver-packs-and-injection
name: driver-packs-and-injection
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, driver-injection, driver-packs, dism, pnputil, winpe, osd]
level: practitioner
status: draft
description: "Handle drivers for OS builds: vendor driver packs by model, WinPE-only NIC/storage drivers, offline DISM and online pnputil injection, model detection and VMD storage gotchas."
sources:
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/add-and-remove-drivers-to-an-offline-windows-image"
  - "https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/pnputil-command-syntax"
  - "https://www.dell.com/support/kbdoc/en-us/000124139/dell-command-deploy-driver-packs-for-enterprise-client-os-deployment"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# driver-packs-and-injection

## Sources
Use enterprise driver packs, not consumer installers: Dell Driver Packs (Dell Command |
Deploy), HP driver packs / HP Image Assistant, Lenovo SCCM packages / Update Retriever.
They are INF-based and match the model's supported OS build.

## Model detection
```powershell
(Get-CimInstance Win32_ComputerSystem).Model              # Dell, HP
(Get-CimInstance Win32_ComputerSystemProduct).Version     # Lenovo friendly name
(Get-CimInstance Win32_ComputerSystem).Model              # Lenovo returns machine type, e.g. 21HD
```
Use these values in task sequence WMI conditions or naming of driver packages.

## WinPE: only what boot needs
Add NIC and storage drivers to the boot image, nothing else. Missing storage driver = no
disks visible; on Intel 11th gen and later, VMD/RST mode is the usual cause (add the
Intel RST VMD driver or switch to AHCI before imaging if policy allows).

## Offline injection
```cmd
DISM /Image:<MOUNT_DIR> /Add-Driver /Driver:<DRIVERS>\Model-21HD /Recurse
DISM /Image:<MOUNT_DIR> /Get-Drivers
```

## Online injection (running OS)
```cmd
pnputil /add-driver "<DRIVERS>\*.inf" /subdirs /install
pnputil /enum-drivers
```

## In a task sequence
- **Apply Driver Package** per model (condition on model) is predictable; avoid Auto Apply
  Drivers with a huge catalogue (wrong matches, slow).
- After deployment, keep drivers current with Windows Update for Business driver policies
  or vendor tools rather than re-imaging.

## Gotchas
- Driver packs for the wrong OS build install but cause yellow bangs or BSODs.
- Firmware (BIOS, Thunderbolt, dock) updates are separate from driver packs.
- Duplicate INFs from several packs make Windows pick by date/rank, not the one you meant.

## Verify
Device Manager shows no unknown devices after build, `pnputil /enum-drivers` lists the
intended versions, and the model boots and sleeps/wakes cleanly.
