---
id: computing-software.firmware-embedded-development.device-driver-development.usb-vid-pid-and-compliance-testing
name: usb-vid-pid-and-compliance-testing
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [usb-compliance, usb-device, vid-pid, usb3cv, usb-if-logo, firmware-embedded-development]
level: advanced
status: draft
description: "Get a legitimate USB VID/PID (USB-IF, vendor sub-licence, pid.codes) and pass compliance: USB3CV Chapter 9 and class tests, electrical tests, and the logo programme."
sources:
  - https://www.usb.org/getting-vendor-id
  - https://www.usb.org/compliancetools
  - https://pid.codes/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VID/PID and USB-IF compliance testing

## Getting IDs
| Source | Cost | Notes |
|---|---|---|
| USB-IF vendor ID | USD 6,000 one-time (or included with membership) | 65,536 PIDs, required for the USB logo |
| MCU vendor PID sub-licence | free (application) | ST, NXP, Microchip, Espressif, Raspberry Pi grant PIDs under their VID for products using their chips; terms forbid use with other chips |
| pid.codes | free | PIDs under VID 0x1209 for open-source hardware |
| Test/demo PIDs from vendor examples | free | **Not for products**: conflicts with every other product using the same IDs; Windows driver binding collides |
Never invent a VID. Unique `iSerialNumber` per device prevents Windows assigning a new COM port
per USB socket (when no serial is given, Windows keys device instances by port location).

## Compliance testing
Required for the logo and expected by many OEM customers; useful regardless.
1. **USB3CV** (Windows tool from USB-IF, despite the name covers USB 2.0): Chapter 9 tests
   (descriptors, standard requests, address/configured states, suspend/resume) and class tests
   (HID, MSC, UVC...).
2. **USBCV legacy** for older stacks, **HID descriptor tool**.
3. **Electrical tests**: signal quality eye diagram, inrush current (bus-powered devices must
   limit inrush to 10 uF equivalent + 50 uC), drop/droop, back-voltage (no VBUS/D+ driven when
   host is off). Needs a test fixture and scope; usually done at an independent test lab.
4. **Interoperability**: enumerate on several host controllers (Intel, AMD, Renesas xHCI, hubs,
   macOS, Linux).
Registration in the Integrators List after passing at a USB-IF workshop or authorised lab.

## Common Chapter 9 failures
- `GET_STATUS` on interface/endpoint not implemented or wrong length.
- Not STALLing unsupported requests (must STALL EP0, not ignore).
- `wTotalLength` mismatch, string descriptor 0 missing LANGID 0x0409.
- `bMaxPower` lower than actual consumption.
- Endpoint halt (`SET_FEATURE ENDPOINT_HALT`/`CLEAR_FEATURE`) not resetting data toggle.

## Verify
- [ ] VID/PID documented with its licence source; serial number unique per unit (from MCU UID).
- [ ] USB3CV Chapter 9 and relevant class tests pass with zero failures.
