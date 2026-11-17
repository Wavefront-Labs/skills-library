---
id: computing-software.it-support-helpdesk.desktop-support.diagnosing-application-crashes
name: diagnosing-application-crashes
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, application-troubleshooting, application-crash, windows-error-reporting, wer, procdump, localdumps, crash-dump]
level: practitioner
status: docs-checked
description: "Capture user-mode crash dumps for a Windows app with WER LocalDumps registry settings, Task Manager live dumps and ProcDump, ready for a vendor or debugger."
sources:
  - "https://learn.microsoft.com/en-us/windows/win32/wer/collecting-user-mode-dumps"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# diagnosing-application-crashes

Goal: capture a usable dump of a crashing app for the vendor or a debugger.

## WER LocalDumps (off by default, needs administrator)
Registry key: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps`

| Value | Type | Default | Meaning |
|---|---|---|---|
| DumpFolder | REG_EXPAND_SZ | %LOCALAPPDATA%\CrashDumps | Where dumps go; a custom folder must let the crashing process write to it |
| DumpCount | REG_DWORD | 10 | Maximum dump files; oldest is replaced |
| DumpType | REG_DWORD | 1 | 0 custom, 1 mini, 2 full |
| CustomDumpFlags | REG_DWORD | 0x00000121 | Used only when DumpType is 0; MINIDUMP_TYPE flags |

- Per-application override: create a subkey named for the exe (for example `...\LocalDumps\MyApplication.exe`) and set values there; WER reads global settings, then the application's.
- Service crashes: dumps land in the service account profile folder (System: `%WINDIR%\System32\Config\SystemProfile`; Network and Local Service: `%WINDIR%\ServiceProfiles`).
- Not supported for apps that do their own crash reporting. No dump is collected if automatic debugging is set for application crashes.
- Works even if WER is disabled or the user cancels WER reporting. The dump is taken before the app terminates (and before any recovery callback).

## Other capture options (Windows 11)
- Task Manager: Processes or Details tab, right-click the process, Create live memory dump file.
- Sysinternals ProcDump supports triggers such as thread create/exit, performance counters and hung windows.
- WinDbg and CDB analyse full and mini dumps.

## Verify
After a crash, a .dmp file for the app appears in the configured DumpFolder.

## Checked
Date: 2026-11-09. Confirmed in the Microsoft Learn page Collecting User-Mode Dumps. Removed as unconfirmed (other sources were unreadable or 404): Event 1000/1002/1026 reading, faulting module table, exception codes, Reliability Monitor, Office safe-mode switches, ProcDump command line, clean boot and gotchas.
Method: docs-checked 2026-11-09 against the Microsoft Learn page listed in sources, downloaded and read in full.
