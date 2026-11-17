---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.malicious-service-persistence
name: malicious-service-persistence
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [service-persistence, persistence, 7045, services-registry, windows-forensics, dfir]
level: practitioner
status: draft
description: "Find and analyse malicious Windows services used for persistence: registry Services keys, ImagePath and ServiceDll, 7045 events, svchost groups and unsigned binaries."
sources: ["https://attack.mitre.org/techniques/T1543/003/", "https://www.sans.org/posters/hunt-evil/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Malicious service persistence

**Goal:** identify services created or modified by an attacker to run code at boot as SYSTEM.

## Where to look
- Registry `SYSTEM\ControlSet00N\Services\<name>`: `ImagePath`, `Start` (2 = automatic),
  `Type` (0x10 own process, 0x20 shared svchost, 0x1/0x2 driver), `ObjectName` (account),
  `Parameters\ServiceDll` for svchost-hosted DLL services, `Description`, `DisplayName`, key
  last write time.
- System.evtx **7045** (service installed) and 7040 (start type changed); Security 4697
  (service installed, if audited).
- `SOFTWARE\Microsoft\Windows NT\CurrentVersion\Svchost` group lists (attacker adds a new
  service name to an existing group like `netsvcs`).

## Red flags
- ImagePath in user-writable or unusual paths (`ProgramData`, `Users\Public`, `Temp`,
  `Windows\Temp`), or `cmd.exe /c`, `powershell -enc`, `rundll32`, `mshta`.
- Random or lookalike names (`WindowsUpdateSvc`, `MicrosoftEdgeUpdateSrv`), missing
  description, binary unsigned or signed by an unexpected publisher.
- ServiceDll changed on a legitimate service (hijack) or pointing outside System32.
- Services created by remote logons around incident time.
- Kernel drivers with odd names (BYOVD: vulnerable signed drivers like `RTCore64.sys`,
  `gdrv.sys` used to kill EDR).

## Tools
Autoruns (`autorunsc -a s -h -s -c`), Velociraptor `Windows.System.Services`, RECmd batch
for Services, RegRipper `services`/`svc`, `sc qc <name>` live.

## Stacking
Across the fleet, stack services by ImagePath and hash; rare entries on few hosts are
candidates.

## Verify
Service key last-write and 7045 time agree; the binary's creation time ($MFT) precedes it;
the service ran (7036 state change, Prefetch for the binary).
