---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.usb-connection-events-in-windows-logs
name: usb-connection-events-in-windows-logs
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [kernel-pnp-events, usb-forensics, removable-media, windows-event-logs, dfir]
level: practitioner
status: draft
description: "Reconstruct USB connect/disconnect history from Kernel-PnP, DriverFrameworks-UserMode, Partition/Diagnostic and StorSvc events, beyond registry first/last times."
sources: ["https://learn.microsoft.com/en-us/windows-hardware/drivers/install/", "https://www.sans.org/posters/windows-forensic-analysis/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USB connection events in Windows logs

**Goal:** registry keys give first, last connected and last removed times. Event logs can give
**every** connection session (while retained).

## Event sources
| Log | Event IDs | Notes |
|---|---|---|
| `Microsoft-Windows-Kernel-PnP/Configuration` | 400 (device configured), 410 (device started), 420 (deleted) | Device instance ID incl. serial; 400 is often first install, 410 each start |
| `Microsoft-Windows-DriverFrameworks-UserMode/Operational` | 2003, 2004, 2006, 2010, 2100, 2101, 2105, 2106 | Connect/disconnect lifecycle per session (disabled by default on newer Windows) |
| `Microsoft-Windows-Partition/Diagnostic` | 1006 | Each attach: disk serial, model, size, partition table and raw VBR bytes (VSN!) - Windows 10 1709+ |
| `Microsoft-Windows-Storsvc/Diagnostic` | 1001 | Storage device arrival with model/serial |
| `System` | 20001/20003 (UserPnp) | Driver installation for new device |
| `Security` | 6416 | "A new external device was recognized" (requires Audit PNP Activity) |

## Workflow
```powershell
Get-WinEvent -LogName 'Microsoft-Windows-Partition/Diagnostic' | ? Id -eq 1006 |
  % { $x=[xml]$_.ToXml(); [pscustomobject]@{Time=$_.TimeCreated; Data=($x.Event.EventData.Data | % { "$($_.Name)=$($_.'#text')" }) -join ';'} }
```
- Parse 1006 with EvtxECmd maps (they extract serial, model, VBR-derived VSN).
- Build a session table: connect time, disconnect time, device serial, VSN, user logged on.

## Gotchas
- Event 1006 also fires on disconnect with zeroed partition data; the pairs give session length.
- Logs roll over; Partition/Diagnostic is often retained longer because it is low volume.
- Times are system UTC; compare with registry device timestamps (DEVPKEY 0064/0066/0067 properties).

## Verify
Event-derived sessions include the registry first/last times for the same serial.
