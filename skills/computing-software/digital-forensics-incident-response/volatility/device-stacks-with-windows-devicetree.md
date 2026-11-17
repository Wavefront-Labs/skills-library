---
id: computing-software.digital-forensics-incident-response.volatility.device-stacks-with-windows-devicetree
name: device-stacks-with-windows-devicetree
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [devicetree, volatility3, rootkit-detection, filter-drivers, kernel-memory, dfir]
level: advanced
status: docs-checked
description: "Use Volatility 3 windows.devicetree and driverirp to find unexpected filter drivers attached to Windows device stacks in memory and corroborate them."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.devicetree.html", "https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.driverirp.html", "https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/device-objects-and-device-stacks", "https://learn.microsoft.com/en-us/windows-hardware/drivers/ifs/allocated-altitudes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Device stacks with windows.devicetree

Windows represents a device with one or more device objects organised into a device stack, one per driver
in the stack that handles I/O requests. An IRP goes to the top device object, and each driver handles it or
passes it to the next lower one. A driver that inserts itself into a stack (a filter) therefore sees the
I/O, which is why rootkits and keyloggers abuse it. `windows.devicetree` lists a tree of drivers and their
attached devices in a memory image, so unexpected attachments stand out; `windows.driverirp` lists IRPs
for drivers.

## Run
```bash
vol -f mem.raw windows.devicetree > devtree.txt
vol -f mem.raw windows.driverirp > irp.txt
```

## What to look for
- A device attached to a keyboard, disk, volume, file system or network driver stack by a driver that is not
  part of the normal set for that build (unnamed or odd driver names).
- Legitimate attachments exist: endpoint security, encryption, backup, DLP and virtualisation software all
  add filters, so compare against a clean baseline image of the same build.

## Corroborate
- `windows.driverirp` for IRP handlers that point outside the owning driver's module (hooking).
- File-system minifilters are identified by altitude; compare against Microsoft's allocated filter
  altitudes table (minifilter, altitude, company).
- Dump and statically analyse the suspicious driver, and check its signature.

## Gotchas
- Device names are often empty; identify by driver and type instead.

## Verify
Each suspicious attachment is tied to a driver module whose file, signature and IRP handlers have been
examined, and benign attachments are matched to known software.

## Checked
2026-11-08. Read: devicetree and driverirp plugin reference pages, Microsoft "Introduction to device
objects" (device stacks, IRP flow) and the allocated filter altitudes page (table of minifilter, altitude,
company). Removed unconfirmed claims: DRV/DEV/ATT output labels, FILE_DEVICE_* type names, specific
driver names to watch (kbdclass, i8042prt, Disk, volmgr, Ntfs, Tcpip, AFD, NDIS), the modules cross-check and
unlinked-driver plugin advice, and the module dump command details.
Method: documentation only; no commands were run.
