---
id: computing-software.firmware-embedded-development.device-driver-development.winusb-and-ms-os-descriptors
name: winusb-and-ms-os-descriptors
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [winusb, usb-device, ms-os-20-descriptor, bos-descriptor, libusb, firmware-embedded-development]
level: advanced
status: draft
description: "Make a vendor-class USB device install driverless on Windows with WinUSB via MS OS 2.0 descriptors (BOS platform capability), and talk to it from libusb or WinUSB APIs."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/usbcon/microsoft-defined-usb-descriptors
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/usbcon/automatic-installation-of-winusb
  - https://libusb.info/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WinUSB and Microsoft OS descriptors

A vendor-specific interface (class 0xFF) has no inbox driver on Windows; users would need Zadig or
an INF. MS OS descriptors tell Windows to bind **WinUSB** automatically, so libusb, WebUSB and
WinUSB API applications work out of the box.

## MS OS 2.0 (Windows 8.1+), preferred
1. Device descriptor `bcdUSB = 0x0201` (or higher) so Windows requests the **BOS descriptor**.
2. BOS contains a Platform Capability descriptor with the MS OS 2.0 UUID
   `{D8DD60DF-4589-4CC7-9CD2-659D9E648A9F}`, the total length of your MS OS 2.0 descriptor set,
   and a **vendor code** byte (`bMS_VendorCode`).
3. Windows sends a vendor request: `bmRequestType 0xC0, bRequest = vendor code, wIndex = 0x07`
   (MS_OS_20_DESCRIPTOR_INDEX); reply with the descriptor set:
```c
/* header (10) + [function subset header for composite] + compatible ID (20) + registry property */
0x0A,0x00, 0x00,0x00, 0x00,0x00,0x03,0x06, LEN_LO,LEN_HI,   /* set header, Windows 8.1 = 0x06030000 */
0x14,0x00, 0x03,0x00, 'W','I','N','U','S','B',0,0, 0,0,0,0,0,0,0,0,  /* compatible ID "WINUSB" */
/* registry property DeviceInterfaceGUIDs (REG_MULTI_SZ) = "{your-guid}\0\0" UTF-16LE */
```
For composite devices wrap the compatible ID in a **function subset header** naming the vendor
interface number, so CDC/HID interfaces keep their own drivers.

## MS OS 1.0 (legacy)
String descriptor at index 0xEE containing `"MSFT100"` + vendor code, then Extended Compat ID
(`wIndex 0x0004`) and Extended Properties (`wIndex 0x0005`) requests. Still needed for Windows 7.

## DeviceInterfaceGUIDs
Applications using the WinUSB API find the device by this GUID (`SetupDiGetClassDevs`). libusb
does not need it but it is required for WinUSB API users. Generate one GUID per product.

## Host side
```c
libusb_open_device_with_vid_pid(ctx, 0x1209, 0x0001);
libusb_claim_interface(h, 2);
libusb_bulk_transfer(h, 0x02, buf, 64, &n, 1000);   /* OUT EP2 */
```
Python: `pyusb` with the libusb backend. WebUSB adds a URL descriptor in the BOS as well.

## Windows caching (again)
Windows stores the "MS OS descriptor queried" result per VID/PID/bcdDevice in
`HKLM\SYSTEM\CurrentControlSet\Control\usbflags`. While iterating, bump `bcdDevice` or delete
that key, or Windows never asks again.

## Verify
- [ ] Device Manager shows the interface under "Universal Serial Bus devices" with driver WinUSB, no INF installed.
- [ ] libusb test program opens and transfers on a clean Windows machine.
