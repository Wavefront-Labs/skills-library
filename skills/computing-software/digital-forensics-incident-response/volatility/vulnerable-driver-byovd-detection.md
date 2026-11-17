---
id: computing-software.digital-forensics-incident-response.volatility.vulnerable-driver-byovd-detection
name: vulnerable-driver-byovd-detection
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [byovd, rootkit, driver-scan, kernel-memory, edr-tampering, dfir]
level: advanced
status: draft
description: "Detect bring-your-own-vulnerable-driver attacks used to kill EDR: loaded and unloaded driver lists, loldrivers matching, service events and memory evidence."
sources: ["https://www.loldrivers.io/", "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/microsoft-recommended-driver-block-rules", "https://attack.mitre.org/techniques/T1068/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vulnerable driver (BYOVD) detection

**Goal:** ransomware operators load a legitimately signed but vulnerable driver (e.g. old versions
of `RTCore64.sys`, `gdrv.sys`, `procexp152.sys`, `aswArPot.sys`, `zamguard64.sys`) to gain kernel
access and terminate EDR/AV processes.

## Disk and log evidence
- **System 7045** service installed with `Kernel Mode Driver` type and an image path in Temp/ProgramData/user folders.
- Sysmon **6** (driver loaded) with hash and signature status; Code Integrity events 3023/3033 if blocked.
- Driver file: hash and compare with loldrivers.io (`loldrivers` CSV/JSON has SHA256 and Authentihash) and Microsoft's vulnerable driver blocklist.
- EDR/AV logs or crash events shortly after driver load (security service stopped, 7034/7036).

## Memory evidence (Volatility 3)
```bash
vol -f mem.raw windows.modules          # loaded drivers (list)
vol -f mem.raw windows.modscan          # pool scan: includes hidden/unlinked
vol -f mem.raw windows.unloadedmodules  # recently unloaded drivers: attackers often unload after use
vol -f mem.raw windows.driverscan
vol -f mem.raw windows.callbacks        # removed or replaced EDR callbacks indicate kernel tampering
vol -f mem.raw windows.modules --dump   # hash dumped drivers and match loldrivers
```
- Missing EDR kernel callbacks (`PsSetCreateProcessNotifyRoutine` entries for the EDR driver gone) while the EDR driver is loaded = callback removal via BYOVD.

## Hunting at scale
- Velociraptor/osquery: list drivers (`Windows.Sys.Drivers`, `drivers` table) and hash-match against loldrivers.
- Enable Microsoft vulnerable driver blocklist (default on in Windows 11 22H2+ with HVCI) and report hosts where it was disabled.

## Gotchas
- Some vulnerable drivers belong to legitimate installed tools (hardware utilities, old AV); context matters.
- Attackers rename driver files; match by hash/Authentihash, not name.

## Verify
Each suspicious driver is hash-matched, load time placed on the timeline, and its effect (killed processes, removed callbacks) shown.
