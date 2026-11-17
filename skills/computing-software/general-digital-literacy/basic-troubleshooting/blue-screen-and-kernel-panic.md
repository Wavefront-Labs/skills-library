---
id: computing-software.general-digital-literacy.basic-troubleshooting.blue-screen-and-kernel-panic
name: blue-screen-and-kernel-panic
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-method, blue-screen, bsod, stop-code, kernel-panic]
level: intro
status: draft
description: "Respond to a Windows blue screen or Mac kernel panic: read the stop code, undo the recent driver or update, test memory and disk, and know when it is hardware."
sources:
  - https://support.microsoft.com/en-us/windows/resolving-blue-screen-errors-in-windows-60b01860-58f2-be66-7516-5c45a66ae3c6
  - https://support.apple.com/en-us/102580
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Blue screen and kernel panic errors

## Windows blue (or black) screen
1. Note the **stop code** (`CRITICAL_PROCESS_DIED`, `IRQL_NOT_LESS_OR_EQUAL`, `PAGE_FAULT_IN_NONPAGED_AREA`, `VIDEO_TDR_FAILURE`) and any file named (`What failed: nvlddmkm.sys`). Photograph the QR code screen.
2. One-off after months of stability: restart and carry on. Repeated: keep going.
3. **What changed?** New driver, update, hardware or app (especially antivirus, VPN, overclocking tools). Uninstall it; Device Manager › device › Driver › **Roll Back Driver**; Settings › Windows Update › Update history › Uninstall updates.
4. Can't boot: after 2 failed starts Windows opens **Recovery** › Troubleshoot › Advanced › Startup Settings › **Safe Mode**, or *Uninstall Updates*, or *System Restore*.
5. Check hardware: **Windows Memory Diagnostic** (`mdsched`); disk health with `chkdsk /scan` and the maker's SSD tool; reseat RAM on desktops; check temperatures.
6. Repair system files: `sfc /scannow` then `DISM /Online /Cleanup-Image /RestoreHealth` in an admin terminal.
7. Find the culprit later: Reliability Monitor, or Event Viewer ID 1001 (BugCheck).

## Mac kernel panic ("Your computer restarted because of a problem")
1. Click **Report** to see the panic log; it may name an extension (kext) or device.
2. Unplug all accessories and restart; add back one at a time.
3. Update macOS and apps; remove old system extensions/security software.
4. **Safe Mode** (Apple silicon: hold power › select disk › hold Shift › Continue in Safe Mode). Panics stop in Safe Mode → third-party software.
5. Apple Diagnostics (hold power on Apple silicon, then `Cmd+D`) for hardware.

## Hardware signs
- Different stop codes each time, crashes under load, crashes in Safe Mode too → RAM, disk, PSU or overheating. Back up now and book a repair.

## Verify
- [ ] A week of normal use with no further crash in Reliability Monitor / no panic reports.
