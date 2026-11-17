---
id: computing-software.firmware-embedded-development.device-driver-development.usb-descriptors-and-enumeration
name: usb-descriptors-and-enumeration
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [usb-device, usb-descriptors, enumeration, device-descriptor, configuration-descriptor, interface-association-descriptor, vid-pid, bcd-device, usb-chapter-9, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write correct USB device, configuration, interface, endpoint and string descriptors: field meanings, wTotalLength, power fields, endpoint attributes, IAD class codes."
sources:
  - https://www.beyondlogic.org/usbnutshell/usb5.shtml
  - https://www.usb.org/sites/default/files/iadclasscode_r10.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# USB descriptors

**Goal:** descriptors that describe exactly what the firmware implements, so the host binds the
right drivers. Descriptor layouts below are from the USB in a NutShell descriptor chapter and the
USB-IF Interface Association Descriptor document; confirm class-specific details in each class
specification.

## Device descriptor (18 bytes, type 0x01)
- `bcdUSB`: highest USB version supported, BCD in the form 0xJJMN, so USB 2.0 is 0x0200 and
  USB 1.1 is 0x0110.
- `bDeviceClass`, `bDeviceSubClass`, `bDeviceProtocol`: used by the host to find a class driver.
  0 in `bDeviceClass` means each interface specifies its own class (the usual choice, which lets one
  device support several classes); 0xFF means vendor-specific.
- `bMaxPacketSize` (endpoint 0): valid sizes are 8, 16, 32 or 64.
- `idVendor` is assigned by the USB-IF; `idProduct` is assigned by the manufacturer. The host uses
  them to find a driver.
- `bcdDevice`: device release number, assigned by the developer, same format as `bcdUSB`.
- `iManufacturer`, `iProduct`, `iSerialNumber`: string descriptor indexes; 0 means no string.
- `bNumConfigurations`: configurations supported at the current speed.

## Composite devices with an IAD
The USB-IF IAD document says devices that use the Interface Association Descriptor must use
`bDeviceClass` 0xEF (Miscellaneous), `bDeviceSubClass` 0x02 (Common Class) and
`bDeviceProtocol` 0x01 (Interface Association Descriptor). An IAD groups the interfaces of one
function (and their alternate settings) so they bind to the same driver instance:
- Place the IAD before the first interface of the function. A single-interface function does not
  need an IAD.
- `bFirstInterface` is the first interface number N, and `bInterfaceCount` is (M - N) + 1 for
  interfaces N through M. Interfaces in an association must be numbered contiguously, and alternate
  settings do not count towards `bInterfaceCount`.
- Hosts build hardware IDs from `idVendor`, `idProduct` and the IAD's `bFirstInterface`, and
  compatibility IDs from the IAD's `bFunctionClass`, `bFunctionSubClass` and `bFunctionProtocol`.
- Descriptors between the configuration descriptor and the first interface or IAD are treated as
  global and delivered to every function driver.
- Hosts whose USB software does not understand the IAD ignore it and may not bind the interfaces
  correctly.

## Configuration descriptor (type 0x02)
- `wTotalLength`: bytes of the whole hierarchy returned when the configuration is read (the
  configuration descriptor plus all interface and endpoint descriptors). Getting this wrong is a
  common bug, so derive it from the descriptor structures rather than counting by hand.
- `bNumInterfaces`; `bConfigurationValue` is what the host passes in SetConfiguration (non-zero);
  `iConfiguration` is a string index.
- `bmAttributes`: D7 reserved, set to 1; D6 self-powered; D5 remote wakeup; D4 to D0 reserved, 0.
- `bMaxPower`: maximum bus current in 2 mA units, so roughly 500 mA is the maximum that can be
  declared. Report it whenever the device draws any power from the bus. If external power is lost
  the device must not draw more than `bMaxPower`.

## Interface descriptor
`bInterfaceNumber` is zero-based and incremented per interface; `bAlternateSetting` selects
alternate interfaces via Set Interface; `bNumEndpoints` excludes endpoint zero; class, subclass and
protocol codes select class drivers; `iInterface` is a string index.

## Endpoint descriptor (7 bytes, type 0x05)
- `bEndpointAddress`: bits 0 to 3 endpoint number, bits 4 to 6 zero, bit 7 direction (0 = OUT,
  1 = IN; ignored for control endpoints). So 0x81 is endpoint 1 IN.
- `bmAttributes`: bits 0 to 1 transfer type (00 control, 01 isochronous, 10 bulk, 11 interrupt).
  For isochronous endpoints, bits 3..2 give the synchronisation type and bits 5..4 the usage type.
- `wMaxPacketSize`: maximum payload for the endpoint.
- `bInterval`: polling interval in frames (1 ms for low and full speed, 125 us for high speed);
  ignored for bulk and control endpoints; 1 to 255 for interrupt endpoints; isochronous must be 1.

## String descriptors (type 0x03)
Strings are optional; an unused index field must be 0. String index 0 returns a list of 16-bit
supported language IDs (for example 0x0409 English United States). Other strings are Unicode
encoded; the host asks for a language by putting its ID in `wIndex` of Get Descriptor (String).

## Verify
- [ ] Every length field is derived from the structures (`wTotalLength`, each `bLength`).
- [ ] Interfaces of each IAD function are contiguous and `bInterfaceCount` matches.
- [ ] A descriptor dump tool decodes the whole configuration with no warnings.
- [ ] Re-test on each OS after changing the composition of a composite device.

## Checked
2026-11-09. Read: USB in a NutShell chapter 5 (device, configuration, interface, endpoint and
string descriptor tables and notes) and the USB-IF Interface Association Descriptor Class Code and
Use Model Rev 1.0 (device class codes, IAD use model, bFirstInterface and bInterfaceCount rule,
hardware and compatibility ID construction). Removed: the enumeration sequence and the
SET_ADDRESS timing, Windows error symptoms and descriptor caching per VID/PID/bcdDevice, the MS
OS 2.0 and WINUSB advice, pid.codes and VID sourcing advice, the 64-byte-at-full-speed packet
size rule, the UTF-16LE and bLength formula, serial-number COM port behaviour, and the debug
tool list. The usb.org and Microsoft sources were not used.
Method: docs-checked 2026-11-09 against USB in a NutShell chapter 5 and the USB-IF IAD document Rev 1.0.
