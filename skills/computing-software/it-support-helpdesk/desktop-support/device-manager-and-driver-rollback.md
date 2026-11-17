---
id: computing-software.it-support-helpdesk.desktop-support.device-manager-and-driver-rollback
name: device-manager-and-driver-rollback
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, device-manager-driver-rollback, device-manager, pnputil, driver-store, error-codes, hardware-ids, driver-installation]
level: practitioner
status: docs-checked
description: "Use Device Manager and pnputil for driver faults: reading device error codes, hardware IDs, roll back vs uninstall, driver store cleanup, and blocking a bad driver from returning."
sources:
  - "https://support.microsoft.com/en-us/windows/hardware/drivers/error-codes-in-device-manager-in-windows"
  - "https://support.microsoft.com/en-us/windows/update-drivers-through-device-manager-in-windows-ec62f46c-ff14-c91d-eead-d7126dc1f7b6"
  - "https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/pnputil-command-syntax"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# device-manager-and-driver-rollback

`devmgmt.msc` (or right-click Start, Device Manager). A yellow triangle means
a problem; open the device, General tab, to read the error code.

## Common error codes
| Code | Microsoft's meaning | Action |
|---|---|---|
| 10 | This device cannot start | Update or roll back the driver |
| 28 | The drivers for this device are not installed | Find the driver by hardware ID |
| 31 | Windows cannot load the drivers required for this device | Reinstall the driver |
| 39 | Windows cannot load the device driver; it may be corrupted or missing | Uninstall the driver package, reinstall |
| 43 | Windows has stopped this device because it has reported problems | Reseat, try another port, update firmware/driver |
| 45 | This hardware device is not connected to the computer | Reconnect it, or remove the ghost device |
| 52 | Windows cannot verify the digital signature for the drivers | Install a correctly signed driver |

## Identify the device
Details tab, **Hardware Ids** property; search the vendor site or Microsoft
Update Catalog with it.
`pnputil /enum-devices /problem` lists devices with a problem (use
`/problem <code>` for one code).

## Roll back vs uninstall vs update
- **Roll Back Driver** (device Properties, Driver tab): needs administrator
  permission and a previously installed driver; the first thing to try when the
  issue began after a driver update.
- **Uninstall device**, restart: Windows attempts to reinstall the driver.
  Some devices such as printers may need reinstalling manually.
- To remove a package from the driver store, use pnputil (below).

## pnputil (driver store; Windows 10 1607 and later)
```
pnputil /enum-drivers                      # third-party packages (oemNN.inf)
pnputil /delete-driver oem42.inf /uninstall /force
pnputil /add-driver <DRIVERS_DIR>\*.inf /subdirs /install
```
Run elevated; use the real path to the extracted driver.

## Gotchas
- Back up or note the current driver version before removing it with
  `/force`; the device stops working until a replacement is installed.
- Windows Update can re-offer a driver after you roll back; for managed
  fleets control driver updates in your update management policy.

## Verify
No entries in `pnputil /enum-devices /problem`; the device works; the Driver
tab version matches the intended one after a reboot.


## Checked

Date 2026-10-27. Documentation release: Microsoft Support Device Manager error codes and driver update pages, pnputil command syntax, as published October 2026. Confirmed: codes 10, 28, 31, 39, 43, 45, 52 and their messages, Roll Back Driver steps and admin requirement, uninstall-and-restart behaviour, pnputil /enum-drivers, /delete-driver with /uninstall and /force, /add-driver with /subdirs and /install, /enum-devices /problem. Removed: Show or hide updates troubleshooter, vendor ID list, Intune driver policy, GPO device-ID, hidden-devices and Basic Display Adapter notes, and the 'Attempt to remove the driver' checkbox that the current page does not show.

Method: documentation only; no commands were run.
