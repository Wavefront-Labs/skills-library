---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.startup-folder-and-winlogon-persistence
name: startup-folder-and-winlogon-persistence
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [winlogon, persistence, run-keys, autoruns, dfir]
level: practitioner
status: draft
description: "Check Startup folders and Winlogon persistence (Userinit, Shell, Notify, AppInit_DLLs, LSA packages) with locations, legitimate values and detection."
sources: ["https://attack.mitre.org/techniques/T1547/004/", "https://attack.mitre.org/techniques/T1547/001/", "https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Startup folder and Winlogon persistence

**Goal:** after Run keys, these are the most common logon-triggered persistence points.

## Startup folders (T1547.001)
- Per user: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`
- All users: `%ProgramData%\Microsoft\Windows\Start Menu\Programs\StartUp\`
- Items: LNK, EXE, BAT, VBS, JS, URL files. Check LNK targets/arguments (LECmd) and MFT creation times.
- Folder location can be redirected via `User Shell Folders` `Startup` value in NTUSER - check it.

## Winlogon (T1547.004)
Key `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon` (and HKCU equivalent for Shell):
| Value | Legitimate | Abuse |
|---|---|---|
| `Userinit` | `<SystemRoot>\system32\userinit.exe,` | extra comma-separated binaries appended |
| `Shell` | `explorer.exe` | `explorer.exe, evil.exe` or replaced |
| `Notify` subkeys (XP-era) | none on modern | DLL loaded by winlogon |
| `AppSetup`, `VMApplet` | rare | command execution |

## Related autostart points
- `AppInit_DLLs` (`...\Windows NT\CurrentVersion\Windows`, with `LoadAppInit_DLLs = 1`): DLL loaded into every user32 process (blocked with Secure Boot).
- LSA: `HKLM\SYSTEM\CurrentControlSet\Control\Lsa` `Authentication Packages`, `Notification Packages`,
  `Security Packages` - password filter DLLs (T1556.002) receive cleartext passwords at change.
- `Active Setup\Installed Components\<GUID>\StubPath` runs once per user at logon.

## Detection
- Autoruns (offline mode against the image hives: `autorunsc -a * -c -h -s -z <systemroot> <userprofile>`),
  RECmd batch, or Velociraptor `Windows.Sys.StartupItems` / `Windows.Persistence.*`.
- Unsigned or user-path binaries in any of these values; key last-write times inside the incident window.

## Gotchas
- Value data may use environment variables or short (8.3) paths to obfuscate.
- Malicious LSA packages need a reboot to load; check boot times vs key modification.

## Verify
Each value matches the known-good default or is explained, and startup folders of all profiles were checked.
