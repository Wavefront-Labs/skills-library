---
id: computing-software.it-support-helpdesk.desktop-support.label-and-thermal-printers
name: label-and-thermal-printers
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, label-printer, thermal-printer, zebra, zpl, barcode-printing]
level: practitioner
status: draft
description: "Support label and thermal printers: direct thermal vs transfer, media calibration, Zebra ZPL and drivers, print darkness and speed, and fixing skipped or faded labels."
sources:
  - https://supportcommunity.zebra.com/s/article/Calibrating-Zebra-Printers
  - https://docs.zebra.com/us/en/printers/software/zpl-pg/c-zpl-zpl-commands.html
  - https://www.zebra.com/us/en/support-downloads/software/drivers/zebradesigner-driver.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Label and thermal printers

Common in warehouses, shipping, labs and retail (Zebra, Brother QL, DYMO, TSC, Honeywell).

## Basics
- **Direct thermal**: heat-sensitive labels, no ribbon; fade in sun/heat; shipping labels.
- **Thermal transfer**: ribbon melts ink onto labels; durable; ribbon type must match (wax, wax-resin, resin) and wind (coated side in/out).
- Media sensing: **gap/notch** (die-cut labels), **black mark**, or **continuous**. Wrong sensor setting causes skipped labels or printing across gaps.

## Install
- Use the vendor driver (ZDesigner for Zebra) or send raw ZPL/EPL from the application. Many apps (shipping, ERP, label software like BarTender, NiceLabel) need a specific driver name.
- Set label size and DPI (203 or 300 dpi) in the driver to match the media; mismatched DPI shrinks or enlarges barcodes.
- Network models: static IP or DHCP reservation, raw port 9100.

## Calibrate (Zebra)
- Load media, then hold the FEED button until it flashes (two flashes on many models) or send `~JC`; the printer feeds labels and learns the gap length.
- Print a configuration label (hold FEED/cancel, or `~WC`) to confirm settings.
- Reset to factory defaults with `^JUF` if settings are corrupt (then recalibrate).

## Quick ZPL test
```
^XA^FO50,50^ADN,36,20^FDTest label^FS^FO50,120^BY2^BCN,80,Y,N,N^FD12345678^FS^XZ
```
Send with `copy /b test.zpl \\server\ZebraShare` or `nc printer-ip 9100 < test.zpl`.

## Troubleshooting
| Symptom | Fix |
|---|---|
| Blank labels | Direct thermal media upside down, or ribbon missing/inside-out |
| Faded print | Increase darkness (`~SD`), slow speed, clean printhead with isopropyl pen |
| Skips a label / red light | Recalibrate; check sensor setting |
| Barcodes not scanning | DPI/size mismatch, darkness too high (bars bleed) |
| Vertical white lines | Damaged printhead elements; replace head |

## Verify
Configuration label shows correct media type and size; test barcode scans with the site scanner.
