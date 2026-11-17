---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.usb-device-connection-timestamps
name: usb-device-connection-timestamps
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [usb-device-timestamps, usb-forensics, setupapi, kernel-pnp, removable-media, dfir]
level: practitioner
status: draft
description: "Establish first, last connected and last removal times for USB devices from registry Properties keys, setupapi.dev.log and Kernel-PnP/Partition event logs."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://ericzimmerman.github.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USB device connection timestamps

**Goal:** a defensible timeline of when a device was first plugged in, each later
connection where logs allow, and when it was last removed.

## Registry
`SYSTEM\ControlSet00N\Enum\USBSTOR\<device>\<serial>\Properties\{83da6326-97a6-4088-9453-a1923f573b29}\`
- `0064`: first install date (UTC FILETIME)
- `0065`: install date (often equal to 0064 or last driver install)
- `0066`: **last arrival** (last connected)
- `0067`: **last removal**
Registry Explorer and USB Detective decode these; also check `Enum\USB\VID_..\<serial>`
equivalent properties.

## Logs
- `Windows\INF\setupapi.dev.log`: `>>> [Device Install (Hardware initiated) - USBSTOR\Disk&Ven_...\<serial>]` followed by `>>> Section start 2026/09/02 10:14:22.123`
  = first connection (local time).
- `Microsoft-Windows-Partition/Diagnostic.evtx` Event **1006**: every connection on Win10+
  with serial, model, capacity, and partition table/VBR bytes (gives volume serial).
- `Microsoft-Windows-Kernel-PnP/Configuration` Events 400/410/420 (device configured/started),
  `Microsoft-Windows-DriverFrameworks-UserMode/Operational` 2003/2100/2102 (if enabled).
- Security 6416 (new external device recognised) with "Audit PNP Activity" enabled.

## Build the timeline
First connect: min(0064, setupapi). Each connection: Partition 1006 events.
Last connect/remove: 0066/0067. Map to user sessions (4624/4634, 4800/4801 lock/unlock)
to argue who was present.

## Gotchas
- setupapi log is local time, registry is UTC: convert.
- Driver updates can reset install times; Windows feature updates may rewrite keys.
- Partition/Diagnostic log size limited; older connections roll off.

## Verify
Registry last-arrival time matches the latest Partition 1006 event for that serial within
seconds.
