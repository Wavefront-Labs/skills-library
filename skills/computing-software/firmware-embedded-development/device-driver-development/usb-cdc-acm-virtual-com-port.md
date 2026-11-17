---
id: computing-software.firmware-embedded-development.device-driver-development.usb-cdc-acm-virtual-com-port
name: usb-cdc-acm-virtual-com-port
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [usb-device, usb-cdc-acm, virtual-com-port, dtr, set-line-coding, zero-length-packet, bulk-endpoint, flow-control-usb, firmware-embedded-development]
level: practitioner
status: gated
description: "Implement a USB CDC-ACM serial port that never drops data or hangs: DTR-based connection detection, ZLP handling, TX when no host is listening and throughput."
sources:
  - https://github.com/hathach/tinyusb/blob/master/src/device/usbd.h
  - https://github.com/hathach/tinyusb/blob/master/src/class/cdc/cdc_device.h
  - https://github.com/hathach/tinyusb/blob/master/src/class/cdc/cdc_device.c
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/usbcon/usb-driver-installation-based-on-compatible-ids
  - https://www.usb.org/document-library/class-definitions-communication-devices-12
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# USB CDC-ACM virtual COM port

**Goal:** a USB serial port for logs, CLIs and data streaming that works with every terminal
program and doesn't block firmware when nobody is connected.

## Structure
Two interfaces grouped with an IAD: a Communication interface (one notification endpoint) and a
Data interface (bulk OUT + bulk IN); TinyUSB's `TUD_CDC_DESCRIPTOR` builds exactly this. Full-speed
bulk packets are 64 bytes (gated: unconfirmed, source is paywalled or blocked).
Class requests on EP0: `SET_LINE_CODING`/`GET_LINE_CODING` (TinyUSB reports changes through
`tud_cdc_line_coding_cb`) and `SET_CONTROL_LINE_STATE` (DTR bit 0, RTS bit 1).

## Connection detection
The host's port being open is usually signalled by **DTR**; TinyUSB's `tud_cdc_connected()` treats DTR
(bit 0) active as connected. Use it to decide whether to send:
```c
if (tud_cdc_connected()) {            /* TinyUSB: DTR set */
    tud_cdc_write(buf, n);
    tud_cdc_write_flush();
}
```
Writing when nobody reads fills the TX FIFO; a blocking write then hangs the firmware. Drop
or ring-buffer data when not connected, and never block a high-priority task on USB TX.

## Zero-length packets
A bulk transfer ends with a short packet. If the data is an exact multiple of the endpoint packet
size, the device must send a zero-length packet or the host keeps waiting for more (the "last line
appears only when the next line arrives" symptom) (gated: unconfirmed, source is paywalled or blocked). TinyUSB has a
`CFG_TUD_CDC_RX_NEED_ZLP` option for the receive side; check how your stack terminates transmit
transfers.

## Throughput
Full-speed bulk throughput is bounded by the bus (about 1.2 MB/s at most) (gated: unconfirmed, source is paywalled or blocked) and real
figures are lower. Write in large chunks (fill whole packets, double-buffer endpoints), not per
character. The line-coding "baud rate" is not a link speed.

## OS notes
- Windows: Microsoft ships the in-box USB serial driver `Usbser.sys` for communications/CDC control
  devices; whether it binds without an INF on a given Windows version (gated: unconfirmed, source is paywalled or blocked).
- Linux: devices appear as `/dev/ttyACM*` (gated: unconfirmed, source is paywalled or blocked). ModemManager may probe new ACM devices with AT
  commands; a udev rule setting `ID_MM_DEVICE_IGNORE` for your VID/PID is the usual fix
  (gated: unconfirmed, source is paywalled or blocked).
- macOS device names were not confirmed.

## Common bugs
- Not handling `SET_LINE_CODING`/`GET_LINE_CODING`: some host programs fail to open the port.
- Reading OUT data only when a full buffer arrives: interactive CLIs feel laggy; process
  partial reads.
- Resetting the MCU on DTR toggle (Arduino-style 1200-baud touch) when you didn't mean to.

## Verify
- [ ] Send exactly 64, 128 and 1000 bytes: host receives all immediately.
- [ ] Unplug/close terminal for an hour while firmware logs: no hang, no watchdog reset.
- [ ] Sustained throughput measured with a host script.

## Checked

TinyUSB master sources (hathach/tinyusb), Microsoft driver documentation (MicrosoftDocs/windows-driver-docs, staging), STM32 CMSIS device headers and Linux kernel Documentation, read 2026-10-27.
Confirmed in TinyUSB: `TUD_CDC_DESCRIPTOR` emits an Interface Association Descriptor, a control interface with a notification endpoint and a data interface with OUT and IN endpoints; `tud_cdc_connected()` tests DTR (bit 0); line state bit 0 is DTR and bit 1 is RTS; `tud_cdc_write()` and `tud_cdc_write_flush()`; `tud_cdc_line_coding_cb` and `tud_cdc_line_state_cb`; `CFG_TUD_CDC_RX_NEED_ZLP`. Confirmed in Microsoft's documentation: the in-box Usbser.sys driver for CDC control devices.
Gated: USB packet sizes, zero-length-packet rules and bus throughput come from the USB 2.0 and CDC specifications, and the Linux, ModemManager and macOS behaviours were not found in a readable source. The USB-IF specification documents were not read in this review. Removed: the Windows 10 auto-binding wording, the macOS device name, the PuTTY remark and the 500-900 KB/s measurements.

Method: documentation only; no commands were run.
