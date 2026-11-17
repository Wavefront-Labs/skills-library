---
id: computing-software.general-digital-literacy.basic-troubleshooting.connecting-a-wireless-printer
name: connecting-a-wireless-printer
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, printers, wireless-printer, wifi-printer, airprint]
level: intro
status: docs-checked
description: "Get a wireless printer onto the same Wi-Fi network as your computer, test its wireless connection, and add it on Windows or Mac with AirPrint."
sources:
  - https://support.microsoft.com/en-us/windows/hardware/printer/add-or-install-a-printer-in-windows
  - https://support.microsoft.com/en-us/windows/hardware/printer/fix-printer-connection-and-printing-problems-in-windows
  - https://support.apple.com/guide/mac-help/add-and-manage-printers-mh14004/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connect a wireless printer

**Goal:** computers can print over Wi-Fi without a cable.

## Get the printer on Wi-Fi
- Follow the instructions that came with the printer, or the maker's website, to join it to your Wi-Fi network. Many printers have a button that shows a blue wireless icon when wireless is available.
- Run the printer's own **wireless connectivity test** (many printers have a menu option for it) to confirm it is connected.
- On a Mac, some Wi-Fi printers must first be connected to the Mac by USB cable so the maker's software and setup assistant can pass on the Wi-Fi details; after setup the cable can be removed.

## Add it to computers
- **Windows 11:** Settings > Bluetooth & devices > Printers & scanners > *Add a printer or scanner* > **Add device**, then select your printer. The printer and PC must be on the same wireless network; with access points, extenders or several routers using separate network names, join the one the printer uses.
- **Mac:** make sure the printer is on the same Wi-Fi network, then File > Print and choose the AirPrint printer, or System Settings > Printers & Scanners > Add Printer, Scanner, or Fax. After switching the printer on, wait a minute or two before printing; some printers need that long to join the network.

## If it will not connect
- Not found: confirm both devices are on the same network, then use *Add a new device manually* (Windows) or add it by IP address or host name (Mac).
- Some printers need a configuration profile (an *AirPrint Profile*) from your network administrator before a Mac can see them.
- Install the maker's latest software or driver (Windows Update for Windows).

## Verify
- [ ] The wireless test reports connected, and a test page prints from each computer.

## Checked
Checked 2026-10-27 against Microsoft Support "Add or install a printer in Windows" and "Fix printer connection and printing problems in Windows", and the Apple Mac User Guide "Add and manage printers on Mac". Confirmed: wireless icon button and connectivity test, same-network requirement, Windows and Mac add paths, USB-assisted setup, wait of a minute or two, configuration profiles. Removed unconfirmed claims (WPS timing, 2.4 GHz and WPA3 limits, Wi-Fi Direct, guest-network isolation, phone steps, maker app names, router IP reservation).
Method: documentation only; no commands were run.
