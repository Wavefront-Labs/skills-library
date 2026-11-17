---
id: computing-software.general-digital-literacy.basic-troubleshooting.printer-shows-offline
name: printer-shows-offline
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, printers, printer-offline, use-printer-offline, print-spooler, default-printer]
level: intro
status: docs-checked
description: "Bring a printer back online on Windows: power-cycle, same network, default printer, clear the queue, restart the Print Spooler, remove and re-add it."
sources:
  - https://support.microsoft.com/en-us/windows/hardware/printer/troubleshooting-offline-printer-problems-in-windows
  - https://support.microsoft.com/en-us/windows/hardware/printer/fix-printer-connection-and-printing-problems-in-windows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Printer shows offline

**Goal:** the printer's status changes from Offline to Ready, even though it is on and connected.

## Windows 11 (Microsoft's order)
0. Run the printer troubleshooter in the **Get Help** app first; if it cannot fix it, continue.
1. Unplug the printer, wait 30 seconds, plug it back in and switch it on.
2. Wireless printer: check on the printer's own menu that it is on the same Wi-Fi network as your PC (with extenders or several routers with separate network names, make sure both are on the same one).
3. Set it as default: Settings > Bluetooth & devices > **Printers & scanners** > your printer > **Set as default**. If that option is missing, **Let Windows manage my default printer** is on; turn it off first.
4. Check the queue: select the printer > **Open print queue** > the ... menu > **Cancel all** if jobs are waiting.
5. Restart the spooler: search for `services`, open Services, right-click **Print Spooler** > **Restart**.
6. Remove and re-add: select the printer > **Remove** > Yes; then next to *Add a printer or scanner* choose **Add device** and follow the prompts.
7. Restart the PC.

## Windows 10 (support ended 14 Oct 2025)
Settings > Devices > Printers & scanners > printer > **Open queue** > Printer menu > **Set As Default Printer**, and clear **Pause Printing** and **Use Printer Offline** if ticked. Then queue, spooler, reinstall and restart as above.

## Mac
Microsoft's article covers Windows only. For Mac printers use System Settings > Printers & Scanners and confirm the printer is on the same Wi-Fi network (Apple's AirPrint steps say to wait a minute or two after switching the printer on).

## Verify
- [ ] Status reads Ready or Idle and a test page prints.

## Checked
Checked 2026-10-27 against Microsoft Support "Troubleshooting offline printer problems in Windows" and "Fix printer connection and printing problems in Windows", and the Apple Mac User Guide "Add and manage printers on Mac". Confirmed: the seven-step Windows 11 order, the Windows 10 "Use Printer Offline" step (it appears only in the Windows 10 steps), the default-printer toggle, spooler restart. Removed unconfirmed claims (port IP and SNMP settings, duplicate "Copy 1" printers, VPN and firmware advice, Mac Printer Queue, Resume and Reset printing system).
Method: documentation only; no commands were run.
