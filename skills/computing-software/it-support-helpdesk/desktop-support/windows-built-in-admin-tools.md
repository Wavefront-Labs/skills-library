---
id: computing-software.it-support-helpdesk.desktop-support.windows-built-in-admin-tools
name: windows-built-in-admin-tools
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, clean-boot-msconfig, resmon, local-group-policy, control-panel, systeminfo, msinfo32, windows-tools]
level: practitioner
status: draft
description: "Use the built-in Windows admin consoles well: msconfig clean boot, Resource Monitor, Local Group Policy Editor, Control Panel applets vs Settings, and systeminfo/msinfo32."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/perform-clean-boot-windows"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/systeminfo"
  - "https://learn.microsoft.com/en-us/windows/client-management/client-tools/administrative-tools-in-windows"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# windows-built-in-admin-tools

## msconfig and clean boot
Clean boot isolates third-party services and startup apps as the cause of a fault.
1. `msconfig` > Services > tick **Hide all Microsoft services** > Disable all.
2. Task Manager > Startup apps > disable each.
3. Restart and test. If fixed, re-enable half the services, restart, test (half-split)
   until the culprit is found.
4. Return to normal: msconfig > General > **Normal startup**, re-enable startup apps.
- Don't use "Disable all" without hiding Microsoft services; it breaks networking,
  sign-in and more.
- msconfig Boot tab: Safe boot options (Minimal, Network); remember to untick or the PC
  keeps booting into safe mode.

## Resource Monitor (`resmon`)
- Deeper than Task Manager: per-process disk I/O by file, network by process and
  remote address, listening ports, memory hard faults/sec, and **Associated handles**
  search (CPU tab) to find which process locks a file ("file in use" errors).
- Disk tab sorted by Total (B/sec) finds the process hammering the disk.

## Local Group Policy Editor (`gpedit.msc`)
- Pro/Enterprise/Education only. Sets local policy; domain GPOs and MDM override local.
- Use for testing a setting on one machine before building a GPO/Intune profile, or
  standalone devices. Changes apply on `gpupdate /force`; check with `gpresult /h`.
- Settings land in `%SystemRoot%\System32\GroupPolicy` (machine/user `Registry.pol`).
  Resetting a broken local policy: rename that folder and run `gpupdate /force`.

## Control Panel vs Settings
- Settings is the primary UI; many Control Panel applets still exist and remain the
  only place for some tasks: `ncpa.cpl` (network adapters), `appwiz.cpl` (programs and
  features, Windows features via `optionalfeatures`), `sysdm.cpl` (system properties:
  computer name, remote, environment variables, performance options), `mmsys.cpl`
  (sound devices), `inetcpl.cpl` (internet options/proxy), `powercfg.cpl`,
  `control printers`.
- Run from Win+R; faster than navigating the menus on a remote session.

## systeminfo and msinfo32
- `systeminfo` (works remotely: `systeminfo /s <PC>`): OS build, install date, last
  boot time, domain, hotfixes, RAM, Hyper-V requirements. `systeminfo /fo csv` for
  parsing.
- `msinfo32`: hardware resources, components, software environment (drivers, services,
  startup programs); File > Export to save a report for a ticket. `msinfo32 /report
  <file>.txt` from the command line.

## Verify
Clean boot test results are recorded with the culprit found; settings tested in gpedit
show in `gpresult`; the ticket carries an msinfo32 or systeminfo export where hardware or
build questions arise.
