---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.office-add-in-and-template-persistence
name: office-add-in-and-template-persistence
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [office-addin-persistence, persistence, maldoc, windows-registry, dfir]
level: advanced
status: draft
description: "Find Office persistence via Normal.dotm macros, XLSTART/STARTUP folders, WLL/XLL/COM/VSTO add-ins and Office test registry keys."
sources: ["https://attack.mitre.org/techniques/T1137/", "https://learn.microsoft.com/en-us/office/vba/library-reference/concepts/getting-started-with-vba-in-office", "https://www.mdsec.co.uk/2019/05/persistence-the-continued-or-prolonged-existence-of-something-part-1-microsoft-office/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Office add-in and template persistence

**Goal:** Office loads code every time an application starts from several locations
(ATT&CK T1137). Each is a persistence point that survives reboots and runs as the user.

## Locations
| Mechanism | Where |
|---|---|
| Word global template macros | `%APPDATA%\Microsoft\Templates\Normal.dotm` (AutoExec/AutoOpen in VBA) |
| Word startup add-ins (.dotm, .wll) | `%APPDATA%\Microsoft\Word\STARTUP\` |
| Excel startup (.xlsb/.xlam, Personal.xlsb) | `%APPDATA%\Microsoft\Excel\XLSTART\` |
| Excel XLL add-ins | `HKCU\Software\Microsoft\Office\<ver>\Excel\Options` values `OPEN`, `OPEN1`... (`/R "path.xll"`) |
| COM add-ins | `HKCU/HKLM\Software\Microsoft\Office\<App>\Addins\<ProgID>` (`LoadBehavior = 3`) -> CLSID InprocServer32 |
| VSTO add-ins | same Addins key with `Manifest` value pointing to `.vsto` |
| "Office Test" key | `HKCU\Software\Microsoft\Office test\Special\Perf` default value = DLL loaded at start |
| Outlook | `VbaProject.OTM` in `%APPDATA%\Microsoft\Outlook\`, Outlook rules/forms/home page (T1137.003-005) |

## Investigate
- Hash and analyse each file (olevba for templates, PE analysis for WLL/XLL which are DLLs).
- Normal.dotm normally has no or few macros; modified time recent = suspicious.
- Registry key last-write times date add-in registration.
- Trust Center: `Security\Trusted Locations` additions (attacker adds a folder to bypass macro blocking).

## Fleet hunt
- Velociraptor/osquery: list files in STARTUP/XLSTART across users; registry Addins with LoadBehavior 3 and unknown ProgIDs; any `Office test` key (should not exist).

## Gotchas
- Users legitimately keep Personal.xlsb macros; review content, not just presence.
- XLL files must match Office bitness; dropped mismatched XLLs crash Excel (WER entries may reveal them).

## Verify
All Office auto-load locations reviewed for every profile, with suspicious items hashed and analysed.
