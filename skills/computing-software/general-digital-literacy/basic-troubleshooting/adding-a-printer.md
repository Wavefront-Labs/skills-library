---
id: computing-software.general-digital-literacy.basic-troubleshooting.adding-a-printer
name: adding-a-printer
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, printers, add-printer, printer-driver, usb-printer, airprint, default-printer]
level: intro
status: docs-checked
description: "Add a USB, Wi-Fi or network printer on Windows 11 and Mac using built-in drivers or AirPrint, add one manually or by IP address, and set the default printer."
sources:
  - https://support.microsoft.com/en-us/windows/hardware/printer/add-or-install-a-printer-in-windows
  - https://support.microsoft.com/en-us/windows/hardware/printer/fix-printer-connection-and-printing-problems-in-windows
  - https://support.apple.com/guide/mac-help/add-and-manage-printers-mh14004/mac
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Add a printer

**Goal:** the printer shows up in every app's Print dialog and prints a test page.

## Windows 11
1. Connect the printer (USB, or on the same network; for a wireless printer, the same wireless network as the PC) and switch it on. Most local printers install by themselves once plugged in and switched on.
2. If not, Settings > Bluetooth & devices > **Printers & scanners**. Check the printer is not already listed, then next to *Add a printer or scanner* select **Add device**. The list can take a few minutes to fill; select **Add device** next to your printer (it may also be added automatically).
3. After it installs, check Windows Update for updated drivers. A **Find drivers** button next to the printer means it may work with reduced functionality until a full driver set is installed; Microsoft says Windows Update is the best way to get printer drivers.
4. Not listed: next to *The printer that I want isn't listed* select **Add a new device manually** and follow the Add Printer window. It offers five "find a printer by other options" choices; for a USB printer use *Add a local printer or network printer with manual settings*.
5. Bluetooth printers have their own steps: Microsoft's "Pair a Bluetooth printer or scanner" article.
6. ARM PCs (for example Copilot+ PCs): Microsoft says a printer maker's own installer can fail there; use the Windows steps above instead, unless the maker says otherwise.
7. To remove a printer: Printers & scanners > select it > **Remove**.

## Mac
- With a document open, **File > Print** (`Cmd+P`) shows printers; or System Settings > **Printers & Scanners** > *Add Printer, Scanner, or Fax*, then pick it from the list and click Add. The Mac uses AirPrint, which needs no extra driver or app. If the printer is not AirPrint-compatible, install the maker's latest software.
- USB printer: connect the cable (a multiport adapter if the Mac has one USB-C port).
- Network printer not listed: add it by **IP address or host name** (the IP tab), choosing a protocol it supports: AirPrint, Internet Printing Protocol (IPP), Line Printer Daemon (LPD) or HP Jetdirect (Socket).
- Default printer: Printers & Scanners > *Default printer* pop-up menu (or *Last Printer Used*).
- Remove: Control-click the printer in the list > Remove Printer.

## Verify
- [ ] The printer appears in the list and a test page prints (Microsoft suggests printing a test page after install).

## Checked
Checked 2026-10-27 against Microsoft Support "Add or install a printer in Windows" and "Fix printer connection and printing problems in Windows" (Windows 11 and 10 sections) and the Apple Mac User Guide "Add and manage printers on Mac" (macOS 27 Golden Gate page set). Confirmed: Windows 11 menu path, Add device and manual add, Find drivers button, Windows Update for drivers, ARM PC note, Mac menu path, AirPrint behaviour, IP-printer protocols, default-printer setting. Removed unconfirmed claims (IPP class driver name, Windows default-printer toggle steps, ChromeOS and phone steps, router address reservation advice).
Method: documentation only; no commands were run.
