---
id: computing-software.general-digital-literacy.basic-troubleshooting.hardware-and-peripheral-troubleshooting
name: hardware-and-peripheral-troubleshooting
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, hardware, peripherals, printer, printer-not-printing, usb, bluetooth, pairing, external-display, hdmi, no-signal, battery, device-manager, drivers, not-detected]
level: intro
status: docs-checked
description: "Diagnose printer, USB, Bluetooth and external-display problems by swapping one thing at a time, then check printers, drivers, pairing and displays."
sources:
  - https://support.microsoft.com/en-us/windows/hardware/printer/fix-printer-connection-and-printing-problems-in-windows
  - https://support.microsoft.com/en-us/windows/hardware/bluetooth/troubleshoot-bluetooth-not-connecting-in-windows
  - https://support.microsoft.com/en-us/windows/hardware/display-graphics/how-to-use-multiple-monitors-in-windows
  - https://support.microsoft.com/en-us/windows/hardware/camera/camera-doesn-t-work-in-windows
  - https://support.microsoft.com/en-us/windows/hardware/audio/fix-sound-or-audio-problems-in-windows
  - https://support.apple.com/guide/mac-help/connect-an-external-display-mchl7c7ebe08/mac
  - https://support.apple.com/guide/mac-help/connect-a-wireless-accessory-blth1004/mac
  - https://support.apple.com/guide/mac-help/optimize-your-mac-battery-life-mh35848/mac
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hardware and peripheral troubleshooting

**Goal:** get a printer, USB device, Bluetooth gadget or second monitor working without guessing, and know when the hardware itself is at fault. This is the companion to `everyday-troubleshooting-method` for anything with a plug, cable or battery.

## 1. Change one thing at a time
Check the cable and port first: a USB cable properly seated, a different cable, a different port, and testing the device on another computer. Microsoft also suggests testing an external camera on another device to rule out hardware.

## 2. Printer not printing
Follow Microsoft's order (Windows 11): run the printer troubleshooter in Get Help; power-cycle the printer (off, unplug, wait 30 seconds, plug in); check the USB cable or the printer's wireless connection (same network as the PC, and run the printer's wireless test); remove and re-add the printer (Settings > Bluetooth & devices > Printers & scanners > Remove, then Add device or Add manually); install the latest driver (Windows Update); clear and reset the print spooler (Services > Print Spooler > Stop, delete the files in the `%WINDIR%\System32\spool\PRINTERS` folder, Start). A status of "Printer in error state" may mean low paper or ink, an open cover, or a jam. See the printing skills for the offline and stuck-queue steps.

## 3. USB and other wired devices not detected
Windows: Device Manager (right-click Start) > expand the category > right-click the device > **Update driver** or **Uninstall device**, then restart so Windows reinstalls it; **Scan for hardware changes** looks for devices again. If a USB device is not recognised, Microsoft has an article on automatically diagnosing and fixing Windows USB problems.

## 4. Bluetooth pairing problems (Windows 11)
Run the Bluetooth troubleshooter in Get Help; make sure Bluetooth is on and the device is in pairing mode and close by; remove the device (Settings > Bluetooth & devices > ... > Remove device) and add it again; charge the device and switch it off and on; turn Bluetooth off for 10 seconds and on again; check for Windows updates; restart. On a Mac, hover over the device in System Settings > Bluetooth and click Disconnect, or Control-click and Forget, then Connect again.

## 5. External display: no picture
- Check cables are firmly connected to the PC or dock and check for Windows updates.
- Windows: `Win+P` for the display mode; Settings > System > Display > **Multiple displays > Detect** if a display is missing; **Identify** numbers the displays.
- Mac: System Settings > Displays, hold **Option** and click **Detect Displays**; unplug and replug the display, make sure it is on, check the cable, adapter and port, and sleep then wake the Mac. Check your Mac's tech specs for how many displays it supports (Help > your Mac's Specifications > Display Support).

## 6. Battery
On a Mac laptop, System Settings > **Battery** has Low Power Mode and **Battery Health** with Optimized Battery Charging. For an iPhone, Settings > Battery > Battery Health.

## Verify
- [ ] You changed one variable at a time (cable, port, device) before deciding the hardware is faulty.
- [ ] The printer shows ready, the device shows no warning in Device Manager, and the display shows a picture.

## Checked
Checked 2026-10-27 against Microsoft Support "Fix printer connection and printing problems in Windows", "Troubleshoot Bluetooth not connecting in Windows", "Camera doesn't work in Windows", "Fix sound or audio problems in Windows" (Device Manager steps) and "How to use multiple monitors in Windows", and the Apple Mac User Guide "Connect one or more external displays with your Mac", "Connect a Bluetooth device with your Mac" and "Save energy on your Mac". Confirmed: troubleshooting orders, menu paths and driver and display steps. Removed unconfirmed claims (shared USB-C and Thunderbolt bandwidth, USB-C cables that only carry power, System Report USB check, hub power advice, 2.4 GHz-only printers, Bluetooth and Wi-Fi interference, dock "No Signal" quirk, powercfg battery report, charging-port cleaning advice).
Method: documentation only; no commands were run.
