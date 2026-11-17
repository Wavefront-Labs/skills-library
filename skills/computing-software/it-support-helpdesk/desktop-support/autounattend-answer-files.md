---
id: computing-software.it-support-helpdesk.desktop-support.autounattend-answer-files
name: autounattend-answer-files
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, unattend-xml, autounattend, windows-sim, configuration-passes, windows-installation, oobe]
level: advanced
status: gated
description: "Automate Windows installs with autounattend.xml: configuration passes, Windows SIM, disk layout, OOBE skips, local admin, placing the file on media, and debugging setup logs."
sources:
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/update-windows-settings-and-scripts-create-your-own-answer-file-sxs"
  - "https://learn.microsoft.com/en-us/windows-hardware/customize/desktop/unattend/"
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/windows-setup-automation-overview"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# autounattend-answer-files

An answer file lets Windows Setup run without prompts: useful for lab builds, VMs, and
small shops without MDT/ConfigMgr/Autopilot.

## Configuration passes (in order)
| Pass | Runs | Typical settings |
|---|---|---|
| windowsPE | Setup from media | Language, disk partitioning, image selection, product key |
| offlineServicing | Applies to offline image | Drivers, packages |
| specialize | First boot, before OOBE | Computer name, time zone, domain join (`Microsoft-Windows-UnattendedJoin`) |
| oobeSystem | OOBE | Skip screens, local accounts, AutoLogon, FirstLogonCommands |
| generalize / auditSystem / auditUser | Sysprep and audit mode | Imaging workflows |

## Build it
- Use **Windows System Image Manager** (Windows ADK) with the `install.wim` catalog for the
  exact edition/build; it validates component names and passes.
- Architecture attribute `processorArchitecture="amd64"` and the correct component
  `publicKeyToken="31bf3856ad364e35"` must match or Setup ignores the component.

## Key snippets
- Disk (UEFI/GPT): `DiskConfiguration` creating EFI (FAT32, 100-260 MB), MSR (16 MB),
  Windows (NTFS, extend) and Recovery partitions; `ImageInstall/OSImage/InstallTo` disk 0
  partition 3. **Wipes disk 0**; double-check on multi-disk machines.
- OOBE (`Microsoft-Windows-Shell-Setup/OOBE`): `HideEULAPage`, `HideOnlineAccountScreens`,
  `HideWirelessSetupInOOBE`, `ProtectYourPC` = 3.
- Local account: `UserAccounts/LocalAccounts/LocalAccount` with group Administrators;
  password stored base64-obfuscated (`PlainText false`), *not* encrypted: treat the file as
  sensitive and delete it after use (Setup copies it to `%WINDIR%\Panther\unattend.xml`).
- `FirstLogonCommands` for scripts that must run as the user at first sign-in.

## Placement
- `autounattend.xml` at the root of the USB/ISO is picked up automatically by Setup.
- For a captured image, `unattend.xml` in `%WINDIR%\Panther` or passed to Sysprep with
  `/unattend:`.

## Debugging
- Setup logs: `\Windows\Panther\setupact.log` on the WinPE RAM disk (drive X) during windowsPE,
  then `%WINDIR%\Panther\setupact.log` and `UnattendGC\setupact.log` for specialize/OOBE.
  Search for "unattend" and the component name.
- "Windows could not parse or process unattend answer file" names the pass/component.

## Gotchas
- Windows 11 OOBE network requirement: answer files that skip online accounts still need
  a supported path (local account in `oobeSystem`); behaviours change between releases;
  test each new build.
- Domain join credentials in the file are plain text; use a join account with only
  join rights in one OU.

## Verify
A VM boots from the media and reaches the desktop with the intended name, time zone,
partitions and accounts without any prompts; Panther logs show no component errors.

## Checked

- Date: 2026-11-02.
- Confirmed against: Autounattend.xml discovery on removable media, /unattend:<filename>, the %WINDIR%\Panther cache, oobeSystem pass, FirstLogonCommands (Microsoft Learn windows-setup-automation-overview and answer-file pages).
- Not confirmed: component and OOBE element names (HideEULAPage, ProtectYourPC), the 260 MB figure and the setupact.log paths (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
