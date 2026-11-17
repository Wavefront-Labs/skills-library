---
id: computing-software.firmware-embedded-development.device-driver-development.usb-composite-devices-and-iad
name: usb-composite-devices-and-iad
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [usb-iad-composite, usb-device, interface-association-descriptor, composite-device, endpoint-budget, firmware-embedded-development]
level: advanced
status: gated
description: "Build a USB composite device (CDC-ACM + HID + MSC): Interface Association Descriptors, class 0xEF/0x02/0x01, interface and endpoint numbering, Windows binding."
sources:
  - https://github.com/hathach/tinyusb/blob/master/src/device/usbd.h
  - https://github.com/hathach/tinyusb/blob/master/src/common/tusb_types.h
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/usbcon/usb-common-class-generic-parent-driver
  - https://www.usb.org/sites/default/files/iadclasscode_r10.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composite devices and IADs

A composite device exposes several functions (virtual COM port, keyboard, disk) in one
configuration. The host's composite driver (Windows `usbccgp`, Linux core) splits interfaces into
separate functions.

## Device descriptor for IAD-based composites
```c
.bDeviceClass    = 0xEF,   /* Miscellaneous */
.bDeviceSubClass = 0x02,   /* Common Class */
.bDeviceProtocol = 0x01,   /* Interface Association Descriptor */
```
Used whenever a function spans **more than one interface** (CDC-ACM uses two: communication +
data; USB audio uses control + streaming) (gated: unconfirmed, source is paywalled or blocked). TinyUSB's `TUSB_CLASS_MISC` is 0xEF,
`MISC_SUBCLASS_COMMON` is 2 and `MISC_PROTOCOL_IAD` is 1, and the IAD descriptor type is 0x0B.

## IAD placement
Each multi-interface function is preceded by an IAD in the configuration descriptor:
```c
/* IAD for CDC: interfaces 0-1 */
0x08, 0x0B,  /* bLength, bDescriptorType = INTERFACE_ASSOCIATION */
0x00,        /* bFirstInterface */
0x02,        /* bInterfaceCount */
0x02, 0x02, 0x00,  /* function class/subclass/protocol = CDC, ACM */
0x00,        /* iFunction string */
/* then interface 0 (CDC comm, 1 interrupt IN endpoint), CDC functional descriptors, interface 1 (data, bulk IN/OUT) */
/* then HID interface 2 (no IAD needed for single-interface functions, but adding one is allowed) */
```
The CDC Union functional descriptor must reference the actual interface numbers (`bMasterInterface`
= 0, `bSlaveInterface0` = 1); renumbering interfaces without updating it breaks enumeration.

## Endpoint budget
Count endpoints per direction: CDC = 1 notification IN + 1 bulk OUT + 1 bulk IN, HID = 1 IN
(`TUD_HID_INOUT_DESCRIPTOR` adds an OUT), MSC = 1 bulk OUT + 1 bulk IN. Check your controller's
reference manual for its endpoint count and packet-memory size, which must fit all buffers.
`wTotalLength` (the `_total_len` argument of `TUD_CONFIG_DESCRIPTOR`) must equal the full
configuration descriptor size.

## Windows details
- Microsoft provides the generic parent driver `Usbccgp.sys` for composite devices; it exposes each
  interface (or each interface collection) as a separate device, and Microsoft's in-box `Usbser.sys`
  serves CDC control devices.
- Whether Windows caches descriptors per VID/PID/bcdDevice, and the symptoms of a missing IAD, were
  not confirmed (gated: unconfirmed, source is paywalled or blocked); bumping `bcdDevice` when you change the composition is a cheap precaution.

## With TinyUSB
Set `CFG_TUD_CDC 1`, `CFG_TUD_HID 1`, `CFG_TUD_MSC 1`; write the configuration descriptor with
`TUD_CDC_DESCRIPTOR(...)`, `TUD_HID_DESCRIPTOR(...)`, `TUD_MSC_DESCRIPTOR(...)` macros (the CDC macro
includes the IAD, a 66-byte block `TUD_CDC_DESC_LEN`) inside `TUD_CONFIG_DESCRIPTOR(...)`, and keep
interface/endpoint numbers in an enum.

## Verify
- [ ] `lsusb -v` (Linux) or USB Device Tree Viewer (Windows) shows each function bound to its driver.
- [ ] The USB-IF Chapter 9 compliance test passes for the composite descriptor.

## Checked

TinyUSB master sources (hathach/tinyusb), Microsoft driver documentation (MicrosoftDocs/windows-driver-docs, staging), STM32 CMSIS device headers and Linux kernel Documentation, read 2026-10-27.
Confirmed in TinyUSB: `TUSB_CLASS_MISC = 0xEF`, `MISC_SUBCLASS_COMMON = 2`, `MISC_PROTOCOL_IAD = 1`, `TUSB_DESC_INTERFACE_ASSOCIATION = 0x0B`; `TUD_CDC_DESCRIPTOR` starts with an 8-byte IAD (class CDC, abstract control model) followed by the control interface, header, call-management and union functional descriptors, a notification endpoint and the data interface with OUT and IN endpoints; `TUD_HID_DESCRIPTOR`, `TUD_HID_INOUT_DESCRIPTOR`, `TUD_MSC_DESCRIPTOR`, `TUD_CONFIG_DESCRIPTOR(... _total_len ...)`, `CFG_TUD_CDC/HID/MSC`. Confirmed in Microsoft's documentation: Usbccgp.sys exposes each interface or interface collection of a composite device as a separate device, and Usbser.sys is the in-box CDC driver.
Gated: the rule that an IAD is required for multi-interface functions comes from the USB-IF IAD class-code document, which was not read in this review. Removed: the STM32 endpoint and packet-memory figures, the "code 10" symptom, the descriptor-caching claim and the USBDeview remark.

Method: documentation only; no commands were run.
