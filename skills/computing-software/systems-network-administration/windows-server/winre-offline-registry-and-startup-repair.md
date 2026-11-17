---
id: computing-software.systems-network-administration.windows-server.winre-offline-registry-and-startup-repair
name: winre-offline-registry-and-startup-repair
category: computing-software
field: systems-network-administration
product: windows-server
tags: [boot-troubleshooting, offline-registry, startup-repair, winre, reg-load]
level: advanced
status: docs-checked
description: "Repair unbootable servers from WinRE: use the WinRE command prompt to load the offline SYSTEM hive with reg load and disable a bad driver or service."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/windows-recovery-environment--windows-re--technical-reference
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/windows-re-troubleshooting-features
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/reg-load
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/install/hklm-system-currentcontrolset-services-registry-tree
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Offline registry edits from WinRE

## Get to a command prompt
Boot WinRE (or install media) and open a Command Prompt. All Windows PE command-line tools are
available from cmd.exe in WinRE, including Registry Editor with its command-line switches and
Chkdsk. The Windows volume letter in WinRE is often not C:; find it with `dir <WinDrive>\Windows`
before editing anything.

## Load the offline SYSTEM hive
`reg load <keyname> <filename>` loads a hive file under a temporary key; `reg unload <keyname>`
removes it again.
```cmd
reg load HKLM\OFFSYS <WinDrive>\Windows\System32\config\SYSTEM
reg query HKLM\OFFSYS\Select
```
`Current` under `Select` names the ControlSet in use. A driver or service lives in
`HKLM\SYSTEM\CurrentControlSet\Services\<DriverName>`; offline that is
`HKLM\OFFSYS\ControlSet00x\Services\<DriverName>`. Disable a bad one by setting its `Start` value:
```cmd
reg add HKLM\OFFSYS\ControlSet001\Services\BadDriver /v Start /t REG_DWORD /d 4 /f
reg unload HKLM\OFFSYS
```
`Start` values: 0 boot (loaded by the boot loader), 1 system (loaded by the I/O subsystem), 2 automatic
(loaded by the Service Control Manager), 3 demand (loaded by PnP when needed), 4 disabled. Always
unload the hive before rebooting. Back up the hive file first (copy it) so the edit can be undone.
Replace the driver or service properly once the server boots.

## Verify
- [ ] Server boots; the disabled driver/service is fixed properly (updated or removed) afterwards.

## Checked
2026-10-28. Confirmed against the Learn pages "Windows RE technical reference" and "Windows RE troubleshooting features" (command prompt tools incl. Registry Editor and Chkdsk), the `reg load` and `reg unload` references, and the "Services registry tree" page (Start values 0-4 and their meanings). Removed as unconfirmed: Startup Repair log path, `bcdedit | find osdevice`, UpperFilters/LowerFilters note, other hives, RegBack statement and the Azure rescue-VM advice (see the Azure boot diagnostics skill).
Method: documentation only; no commands were run.
