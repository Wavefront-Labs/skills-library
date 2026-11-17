---
id: computing-software.it-support-helpdesk.desktop-support.windows-sandbox-for-safe-testing
name: windows-sandbox-for-safe-testing
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, virtualization, client-virtualization, windows-sandbox, wsb-config, disposable-vm, suspicious-file-testing, installer-testing]
level: practitioner
status: docs-checked
description: "Use Windows Sandbox to test installers, scripts and suspicious attachments safely: enabling it, .wsb configs with mapped folders, networking off, logon commands, and limits."
sources:
  - "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/"
  - "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-install"
  - "https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# windows-sandbox-for-safe-testing

Goal: try something risky on a disposable Windows in 30 seconds, and lose
nothing when you close it.

## Enable
Requirements: Windows Pro, Enterprise or Education (not supported on Home),
virtualization capabilities enabled in the BIOS or UEFI, at least 4 GB of RAM
(8 GB recommended) and 1 GB of free disk space.
```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Containers-DisposableClientVM -All
```
Reboot, then launch "Windows Sandbox" from Start. Nothing persists on the
device: everything is discarded when the user closes the application (from
Windows 11 22H2 data survives restarts initiated inside the sandbox).

## Configure with a .wsb file
Configuration files work on Windows 10 build 18342 or later and Windows 11.
By default networking is **enabled** (via the Hyper-V default switch), which
can expose untrusted software to the internal network; use a .wsb file to
turn it off.
```xml
<Configuration>
  <Networking>Disable</Networking>
  <vGPU>Disable</vGPU>
  <ClipboardRedirection>Disable</ClipboardRedirection>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>%USERPROFILE%\Downloads\to-test</HostFolder>
      <SandboxFolder>%SystemDrive%\Users\WDAGUtilityAccount\Desktop\to-test</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
  </MappedFolders>
  <LogonCommand>
    <Command>explorer.exe %SystemDrive%\Users\WDAGUtilityAccount\Desktop\to-test</Command>
  </LogonCommand>
  <MemoryInMB>4096</MemoryInMB>
</Configuration>
```
Save as `test.wsb` and double-click. Details from Microsoft: environment
variables in mapped-folder paths work from Windows 11 version 23H2 (use
literal paths on older builds); the sandbox user is `WDAGUtilityAccount`;
mapped folders are mapped before the logon command runs; `ReadOnly` defaults
to false; with vGPU disabled the sandbox uses software rendering (WARP).

## Good uses for support
- Test an installer or a silent-install command line before packaging it.
- Check whether a problem reproduces on a clean Windows.
- Open a suspicious attachment with Networking disabled and a read-only
  mapping, but report suspected malware to security rather than analysing it
  yourself unless that is your role.

## Limits
- Multiple instances cannot run at the same time.
- Not a security analysis lab; copy results out through a writable mapped
  folder if you need them.

## Verify
The sandbox launches, the mapped folder is read-only (creating a file is
denied), there is no network when disabled, and closing it leaves no trace on
the host.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn Windows Sandbox overview, install and .wsb configuration pages, as published October 2026. Confirmed: editions and Home exclusion, BIOS virtualization, 4 GB RAM and 1 GB disk, Enable-WindowsOptionalFeature feature name, disposable behaviour and the Windows 11 22H2 restart persistence, no simultaneous instances, networking on by default via the Hyper-V default switch, .wsb support from build 18342, environment variables from Windows 11 23H2, WDAGUtilityAccount, ReadOnly default, vGPU/WARP behaviour. Removed: WindowsSandbox CSP name and the 'no persistent state' blanket claim.

Method: documentation only; no commands were run.
