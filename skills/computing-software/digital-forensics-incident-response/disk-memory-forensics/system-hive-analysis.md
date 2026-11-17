---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.system-hive-analysis
name: system-hive-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [system-hive, windows-registry, controlset, timezone-analysis, services-registry, dfir]
level: practitioner
status: draft
description: "Analyse the SYSTEM hive: current ControlSet, computer name, time zone, network interfaces, services and drivers, shutdown time, mounted devices and USB keys."
sources: ["https://ericzimmerman.github.io/", "https://www.sans.org/posters/windows-forensic-analysis/", "https://github.com/keydet89/RegRipper3.0"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SYSTEM hive analysis

**Goal:** establish basic system facts needed to interpret every other artefact, and find
service-based persistence. Hive: `Windows\System32\config\SYSTEM`.

## First: which ControlSet
`SYSTEM\Select\Current` = N means `ControlSet00N` is live (`CurrentControlSet` does not
exist offline). Use that one; others may hold older configuration worth diffing.

## Key locations (under ControlSet00N)
| Fact | Key/value |
|---|---|
| Computer name | `Control\ComputerName\ComputerName` |
| Time zone | `Control\TimeZoneInformation` (`TimeZoneKeyName`, `Bias`, `ActiveTimeBias` in minutes) |
| Last shutdown | `Control\Windows\ShutdownTime` (FILETIME) |
| Network interfaces | `Services\Tcpip\Parameters\Interfaces\{GUID}` (IP, DHCP server, lease times, domain) |
| Services and drivers | `Services\<name>`: `ImagePath`, `Start` (2 auto, 3 manual, 4 disabled), `Type` (0x10 own process, 0x1 kernel driver), `ObjectName` |
| USB devices | `Enum\USBSTOR`, `Enum\USB`, plus `MountedDevices` at hive root |
| AppCompatCache | `Control\Session Manager\AppCompatCache` |
| BAM/DAM | `Services\bam\State\UserSettings\<SID>` |
| Prefetch enabled | `Control\Session Manager\Memory Management\PrefetchParameters` |
| Last access updates | `Control\FileSystem\NtfsDisableLastAccessUpdate` |
| RDP enabled | `Control\Terminal Server\fDenyTSConnections` |

## Tools
Registry Explorer bookmarks (Common, SYSTEM), RECmd batch (`Kroll_Batch`), RegRipper
plugins `compname`, `timezone`, `shutdown`, `nic2`, `services`, `usbstor`.

## What to look for
Services with `ImagePath` in user-writable paths, random names, `cmd /c` or PowerShell in
ImagePath; drivers loaded from unusual paths; RDP enabled during incident; last-access
updates disabled (affects interpretation).

## Verify
Time zone from SYSTEM is applied consistently in your timeline; service findings match 7045
events in System.evtx where those logs survive.
