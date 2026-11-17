---
id: computing-software.firmware-embedded-development.device-driver-development.usb-host-mode-on-mcus
name: usb-host-mode-on-mcus
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [usb-host, usb-device, usb-otg, vbus-switch, host-class-driver, firmware-embedded-development]
level: advanced
status: draft
description: "Run an MCU as a USB host (flash drives, keyboards, CDC devices): VBUS power switching, enumeration in the host stack, class drivers, hubs, and overcurrent handling."
sources:
  - https://docs.tinyusb.org/en/latest/reference/index.html
  - https://www.st.com/resource/en/user_manual/um1720-stm32cube-usb-host-library-stmicroelectronics.pdf
  - https://www.usb.org/document-library/usb-20-specification
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USB host mode

## Hardware
- An OTG or host-capable controller (STM32 OTG_FS/HS, RP2040 native USB, ESP32-S2/S3 OTG).
- **VBUS supply**: the host must provide 5 V at up to 500 mA (USB 2.0) through a current-limited
  power switch (e.g. STMPS2151, TPS2051) with an overcurrent fault output to a GPIO. Never connect
  VBUS directly to a regulator without limiting: a shorted cable resets your board.
- 15 kOhm pull-downs on D+/D- (internal in OTG PHYs when in host mode).
- For OTG with micro-AB/Type-C: ID pin or CC logic decides the role; for host-only designs force
  host mode (`OTG_GUSBCFG.FHMOD` on STM32).

## Host stack flow
1. Detect connect (D+ or D- pulled up by the device: full vs low speed).
2. Bus reset (10-20 ms), read 8 bytes of device descriptor at address 0 (learn EP0 max packet).
3. `SET_ADDRESS`, read full device and configuration descriptors.
4. Select a class driver by interface class (0x08 MSC, 0x03 HID, 0x02/0x0A CDC), `SET_CONFIGURATION`.
5. Class driver opens pipes (host channels) for the endpoints and runs transfers.

STM32Cube USB Host library: `USBH_Init`, `USBH_RegisterClass(&hUsbHost, USBH_MSC_CLASS)`,
`USBH_Start`, then call `USBH_Process()` from a loop or task; application callback gets
`HOST_USER_CLASS_ACTIVE`. TinyUSB: `CFG_TUH_ENABLED 1`, `tuh_task()` in the loop, callbacks like
`tuh_msc_mount_cb`, `tuh_hid_report_received_cb`.

## Class specifics
- **MSC**: SCSI over Bulk-Only Transport; pair with FatFS (`diskio.c` -> `USBH_MSC_Read`).
  Many cheap drives need longer timeouts and retries on `TEST UNIT READY`.
- **HID boot protocol** (`SET_PROTOCOL` 0) gives fixed 8-byte keyboard reports without parsing the
  report descriptor; report protocol needs a descriptor parser.
- **CDC/vendor serial** (FTDI, CP210x, CH340) each need vendor-specific drivers; CDC-ACM is generic.

## Hubs and limits
Hub support multiplies complexity (split transactions for FS/LS devices behind HS hubs). MCU host
controllers have few channels (STM32 OTG_FS: 8-12), limiting simultaneous endpoints.

## Overcurrent
Handle the power-switch fault pin: switch VBUS off, report, retry after a delay. Also handle
devices that draw more than the configured `bMaxPower` at enumeration.

## Verify
- [ ] A selection of flash drives, keyboards and a hub enumerate; hot-plug and unplug repeatedly without leaks or hangs.
- [ ] Short VBUS to ground: fault detected, board keeps running, recovers after removal.
