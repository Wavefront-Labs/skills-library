---
id: computing-software.systems-network-administration.wireshark.usb-capture-with-usbpcap-and-usbmon
name: usb-capture-with-usbpcap-and-usbmon
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, usb-capture, usbpcap, usbmon, capture-setup]
level: practitioner
status: docs-checked
description: "Capture USB traffic in Wireshark with USBPcap on Windows and usbmon on Linux, pick the right bus, filter one device and read URB transfers."
sources:
  - https://wiki.wireshark.org/CaptureSetup/USB
  - https://desowin.org/usbpcap/
  - https://www.kernel.org/doc/html/latest/usb/usbmon.html
  - https://www.wireshark.org/docs/dfref/u/usb.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# USB capture with USBPcap and usbmon

USB is captured at the host controller, not on a wire: you see USB Request Blocks (URBs) between
the OS driver and the device.

## Windows: USBPcap
USBPcap is an open-source USB sniffer for Windows; the Wireshark wiki points to it for raw USB
capture. Install it from the signed installer and restart the computer afterwards, as its page
requires. Wireshark has supported USBPcap since 1.10.0rc1. The Wireshark wiki warns that early
USBPcap versions had problems (for example USB buses not recognised after restart on Windows 7), so
read the issue history if you are affected.

## Linux: usbmon
```
sudo modprobe usbmon
lsusb                          # shows which bus the device is on
sudo dumpcap -i usbmon1 -w kbd.pcapng
```
- Capture interfaces are named `usbmonX` where X is the bus number (libpcap 1.1.0 or later); on
  Linux 2.6.22 and later `usbmon0` is a combined stream from all USB buses.
- First check normal capture privileges, then that the usbmonX devices are readable by your user.
  Some distributions (Fedora, RHEL) use a udev rule putting them in a `usbmon` group; otherwise add a
  rule under `/etc/udev/rules.d` and run `sudo udevadm trigger --subsystem-match=usbmon`, or grant
  access with an ACL: `sudo setfacl -m u:${USER}:r /dev/usbmon*`.
- The kernel usbmon documentation says device node `/dev/usbmon0` is special and means all buses.

## Filtering
Field names from the Wireshark usb reference:
```
usb.device_address == 4
usb.bus_id == 1 && usb.device_address == 4
usb.transfer_type
usb.endpoint_address.direction
```

## Gotchas
- The device address changes on each re-plug; re-check `lsusb`.
- The Wireshark wiki states no USB 3.x capture hardware with Wireshark support exists, so host
  capture cannot show link-layer problems.

## Verify
- [ ] Unplug and re-plug during capture and confirm the device and configuration descriptors decode.

## Checked
Method: docs-checked 2026-11-09 against the Wireshark CaptureSetup/USB wiki page (Linux and Windows sections), the USBPcap home page, the kernel usbmon documentation (usbmon0 grepped) and the usb display-filter reference (field names grepped). Dropped unconfirmed claims: USBPcapCMD options, extcap hub/device picker detail, transfer type value mapping, usbhid.data, isochronous snap-length advice, SuperSpeed bypass claim, and the "enumeration only if capture started before plug-in" statement.
