---
id: computing-software.firmware-embedded-development.device-driver-development.usb-hid-report-descriptors
name: usb-hid-report-descriptors
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [usb-device, usb-hid, report-descriptor, hid-usage-tables, vendor-defined-hid, boot-protocol, report-id, interrupt-endpoint, driverless-usb, firmware-embedded-development]
level: advanced
status: draft
description: "Build USB HID devices: write report descriptors (keyboard, gamepad, vendor-defined), use report IDs, and use HID as a driverless data channel to a host app."
sources:
  - https://www.usb.org/hid
  - https://www.usb.org/document-library/hid-usage-tables-15
  - https://github.com/libusb/hidapi
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USB HID and report descriptors

**Goal:** a HID device every OS supports without drivers: keyboard/mouse/gamepad, or a
vendor-defined HID for a configuration tool.

## The report descriptor
A byte-coded description of every field in each report. Items: Usage Page, Usage, Logical
Min/Max, Report Size (bits), Report Count, Input/Output/Feature, Collection/End Collection.
Vendor-defined 64-byte in/out:
```c
0x06, 0x00, 0xFF,  /* Usage Page (Vendor Defined 0xFF00) */
0x09, 0x01,        /* Usage (0x01) */
0xA1, 0x01,        /* Collection (Application) */
0x15, 0x00,        /*   Logical Minimum (0) */
0x26, 0xFF, 0x00,  /*   Logical Maximum (255) */
0x75, 0x08,        /*   Report Size (8) */
0x95, 0x40,        /*   Report Count (64) */
0x09, 0x01,        /*   Usage (0x01) */
0x81, 0x02,        /*   Input (Data,Var,Abs) */
0x95, 0x40,
0x09, 0x01,
0x91, 0x02,        /*   Output (Data,Var,Abs) */
0xC0               /* End Collection */
```
Validate with the USB-IF HID Descriptor Tool or an online parser; a malformed descriptor
makes Windows show Code 10 with no further explanation.

## Report IDs
With more than one report type, prefix each with `Report ID` (0x85 nn). Then **every report
starts with the ID byte** on the wire, and the endpoint max packet size must hold ID + data.
Without report IDs, the first byte is data: mixing the two conventions between firmware and
host app is a classic off-by-one.

## Standard devices
- Keyboard/mouse: support **boot protocol** (interface subclass 1, protocol 1/2) so BIOS/UEFI
  and some KVMs work; the 8-byte keyboard boot report is fixed.
- Gamepads: Usage Page Generic Desktop, Usage Game Pad; axes with Logical Min/Max and buttons
  as 1-bit fields.

## Vendor HID as a data channel
- Driverless on Windows/macOS/Linux; host side with `hidapi` (`hid_open(vid, pid, NULL)`,
  `hid_write`, `hid_read_timeout`). On Windows, `hid_write` buffers must include the report ID
  byte (0 if none).
- Throughput: interrupt endpoint at full speed = one 64-byte packet per `bInterval` ms
  (1 ms min) = 64 KB/s max. Use CDC or vendor bulk for more.
- Linux needs a udev rule for non-root access (`KERNEL=="hidraw*", ATTRS{idVendor}=="1209",
  MODE="0660", GROUP="plugdev"`).

## Verify
- [ ] Descriptor parses cleanly; device appears in OS HID lists with no driver install.
- [ ] Host app round-trips 64-byte reports at the expected rate.
- [ ] Keyboard works in BIOS setup (boot protocol).
