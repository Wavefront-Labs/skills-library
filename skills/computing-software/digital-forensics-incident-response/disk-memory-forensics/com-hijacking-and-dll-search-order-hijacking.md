---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.com-hijacking-and-dll-search-order-hijacking
name: com-hijacking-and-dll-search-order-hijacking
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [com-hijacking, dll-search-order-hijacking, dll-sideloading, persistence, inprocserver32, dfir]
level: advanced
status: draft
description: "Detect COM object hijacking and DLL search-order hijacking or side-loading used for persistence and execution: HKCU CLSID overrides, phantom DLLs and signed loaders."
sources: ["https://attack.mitre.org/techniques/T1546/015/", "https://attack.mitre.org/techniques/T1574/001/", "https://attack.mitre.org/techniques/T1574/002/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# COM hijacking and DLL search-order hijacking

**Goal:** find persistence that abuses how Windows resolves COM objects and DLLs, which
leaves no obvious autostart entry.

## COM hijacking (T1546.015)
- Windows checks `HKCU\Software\Classes\CLSID\{CLSID}` before `HKLM`. An attacker registers
  an `InprocServer32` (DLL) or `LocalServer32` under HKCU for a CLSID that a frequently used
  process loads (Explorer, Task Scheduler ComHandler tasks), with no admin rights needed.
- Hunt: enumerate `NTUSER.DAT`/`UsrClass.dat` `Software\Classes\CLSID\*\InprocServer32`
  default values; any HKCU CLSID entry that also exists in HKLM with a different path is a
  hijack candidate. Also `TreatAs` and `ScriptletURL`/`scrobj.dll` entries.
- Autoruns covers some; Velociraptor `Windows.Persistence.ComHijacking`-style artifacts or
  a RECmd query over UsrClass hives.

## DLL search-order hijacking and side-loading (T1574.001/.002)
- **Side-loading**: a legitimate signed EXE copied to a writable folder with a malicious DLL
  named like one it imports (e.g. `version.dll`, `dbghelp.dll`, vendor DLLs). Very common in
  APT and ransomware loaders.
- **Phantom DLLs**: services load DLLs that do not exist on disk (e.g. historically
  `wlbsctrl.dll` for IKEEXT); placing one gives persistence.
- Hunt: signed EXEs running from unusual paths (`ProgramData`, `AppData`, `Temp`) with an
  unsigned DLL in the same folder loaded (Sysmon 7 `Signed=false`, EDR image load events);
  stack image loads of system-named DLLs from non-System32 paths.
```kusto
DeviceImageLoadEvents
| where FileName in~ ("version.dll","dbghelp.dll","wtsapi32.dll","winmm.dll")
| where FolderPath !contains @":\Windows\System32\" and FolderPath !contains @":\Windows\SysWOW64\"
```

## Gotchas
- Legitimate software ships private DLL copies; validate signer and hash.
- KnownDLLs are protected from search-order hijacking; target is usually a non-KnownDLL.

## Verify
Malicious DLL creation time precedes first load event; removing the hijack and rebooting
stops the load events.
