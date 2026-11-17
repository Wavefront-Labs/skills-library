---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.usrclass-dat-analysis
name: usrclass-dat-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [usrclass, windows-registry, registry, shellbags, ntuser, dfir]
level: practitioner
status: draft
description: "Analyse UsrClass.dat: location, shellbags (BagMRU), per-user COM registrations used for hijacking, MuiCache and file associations, with transaction logs."
sources: ["https://ericzimmerman.github.io/", "https://www.sans.org/posters/windows-forensic-analysis/", "https://learn.microsoft.com/en-us/windows/win32/sysinfo/hkey-classes-root-key"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UsrClass.dat analysis

**Goal:** `UsrClass.dat` is the per-user half of `HKEY_CLASSES_ROOT`, mounted at
`HKCU\Software\Classes`. It holds artefacts that are not in NTUSER.DAT.

## Location
`%LOCALAPPDATA%\Microsoft\Windows\UsrClass.dat` plus `UsrClass.dat.LOG1/.LOG2` - collect all three
per profile (KAPE `RegistryHives` target does).

## Key artefacts
| Key (under the hive root) | Value |
|---|---|
| `Local Settings\Software\Microsoft\Windows\Shell\BagMRU` and `Bags` | Shellbags for Windows 7+ (folders browsed in Explorer, including removable, network and deleted folders) |
| `Local Settings\Software\Microsoft\Windows\Shell\MuiCache` | Executables that ran with GUI resources (FriendlyAppName) - execution evidence |
| `CLSID\{...}\InprocServer32` / `LocalServer32` | Per-user COM registrations; HKCU overrides HKLM, the basis of COM hijacking persistence |
| `<.ext>` and `<ProgID>\shell\open\command` | Per-user file association changes (hijacking `ms-settings`, `exefile` for UAC bypass) |
| `Local Settings\...\AppContainer` / `Extensions\ContractId` | Store app data |

## Tools
```cmd
SBECmd.exe -d <profile_dir> --csv out\          :: ShellBags Explorer CLI
RECmd.exe -f UsrClass.dat --bn BatchExamples\Kroll_Batch.reb --csv out\
```
Registry Explorer replays LOG1/LOG2 when you open a dirty hive (it prompts); accept and save a clean copy for other tools.

## Hunting COM hijacks
- List CLSIDs in UsrClass.dat whose server path points to user-writable directories
  (`AppData`, `Temp`, `ProgramData`); compare the CLSID with the HKLM registration.
- Key last-write time dates the hijack.

## Gotchas
- Analysts parse NTUSER.DAT and forget UsrClass.dat, missing all post-Windows 7 shellbags.
- Without the transaction logs, recent changes (hours to days) may be missing.

## Verify
Shellbag entries and COM registrations are reported with key last-write times after log replay.
