---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.ifeo-and-accessibility-feature-backdoors
name: ifeo-and-accessibility-feature-backdoors
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [ifeo, persistence, windows-registry, sticky-keys, dfir]
level: advanced
status: docs-checked
description: "Detect Image File Execution Options debugger hijacks, SilentProcessExit monitoring and accessibility backdoors (sethc, utilman) used for persistence (T1546.012, T1546.008)."
sources: ["https://attack.mitre.org/techniques/T1546/012/", "https://attack.mitre.org/techniques/T1546/008/", "https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/gflags-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IFEO and accessibility-feature backdoors

**Goal:** two classic persistence and privilege tricks: make Windows start the attacker's program when a given program launches (IFEO, T1546.012), or replace or redirect the accessibility tools reachable from the logon screen (T1546.008) for SYSTEM-level access without credentials.

## IFEO
- Debuggers are `Debugger` values under `HKLM\SOFTWARE{\Wow6432Node}\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\<executable>`. When the process is created, the debugger is prepended to the application name, so the new process launches under it (ATT&CK example: an `ntsd.exe -g notepad.exe` debugger command).
- IFEO can be set directly in the registry or through GFlags. GFlags stores per-program settings in a `GlobalFlag` entry under the same `Image File Execution Options\<ImageFileName>` key, and has a "Silent process exit" feature (monitor and report silent exits, with notification, event logging and dump creation).
- IFEO can also launch an arbitrary monitor program when a program silently exits (prematurely terminated by itself or by a non-kernel-mode process); that is configured through GFlags and/or registry values under `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SilentProcessExit\`.
- Abuses named by ATT&CK: persistence by continuous triggered invocation, privilege escalation, and impairing defences by registering invalid debuggers for system and security applications.
- Hunt: enumerate every IFEO subkey (both registry views) for `Debugger` or `GlobalFlag` values, and the SilentProcessExit key; investigate any without a documented business reason.

## Accessibility binaries
- Two common programs: `sethc.exe` (Shift five times, "sticky keys") and `utilman.exe` (Windows + U), both in System32. Others listed: `osk.exe`, `Magnify.exe`, `Narrator.exe`, `DisplaySwitch.exe`, `AtBroker.exe`.
- Methods: replacing the binary (for example with `cmd.exe`) or replacing pointers to it in the registry; the key combination at the login screen, at the keyboard or over RDP, then runs it as SYSTEM. On newer x64 Windows a replaced binary must be digitally signed, reside in the system directory and be protected by WFP/WRP, which is why the IFEO debugger route was likely found as a workaround that needs no binary replacement.
- Check: compare the file against the known OS copy (hash, signature, size) and look at the registry for an IFEO `Debugger` on each of the programs above.

## Gotchas
- Debuggers legitimately exist for developer workflows; judge by value content (a shell or unknown binary on an accessibility program is not legitimate).
- Examine offline hives from images as well as the live registry.

## Verify
No IFEO `Debugger` or SilentProcessExit entries without a documented reason, and the accessibility binaries match known OS files.

## Checked
2026-11-08. Confirmed against ATT&CK T1546.012, T1546.008 and Microsoft Learn GFlags Overview: IFEO registry path and debugger behaviour, SilentProcessExit registry path, GlobalFlag per-image location, accessibility program list, replacement methods and x64 signing/WFP requirement. Removed as unconfirmed: the 0x200 flag value, ReportingMode/MonitorProcess details, MFT timestamp advice, parent-process heuristics, event 4624 claims, CBS.log and NLA/UserAuthentication notes, and the Autoruns claim.
Method: documentation only; no commands were run.
