---
id: computing-software.it-support-helpdesk.device-provisioning.removing-bloatware-and-provisioned-apps
name: removing-bloatware-and-provisioned-apps
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, standard-build, debloat, remove-appxprovisionedpackage, oem-bloatware, consumer-features, windows-spotlight, start-menu-layout, intune-remove-apps]
level: practitioner
status: draft
description: "Strip consumer and OEM apps from corporate Windows builds safely: provisioned vs installed Appx, OEM software, turning off consumer experiences, and not breaking Windows."
sources:
  - "https://learn.microsoft.com/en-us/powershell/module/dism/remove-appxprovisionedpackage"
  - "https://learn.microsoft.com/en-us/windows/configuration/store/remove-provisioned-apps"
  - "https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-experience"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# removing-bloatware-and-provisioned-apps

Goal: a clean, quick-to-sign-in build without games, trials and vendor
nag-ware — without removing something Windows needs.

## Two kinds of Store apps
- **Provisioned** (in the image, installed for each new user at first
  sign-in): remove with `Remove-AppxProvisionedPackage -Online`.
- **Installed for an existing user**: `Remove-AppxPackage` (per user, or
  `-AllUsers`).
Remove the provisioned copy or it comes back for every new profile.
```powershell
$remove = 'Microsoft.BingNews','Microsoft.GamingApp','Microsoft.XboxGamingOverlay',
          'Microsoft.MicrosoftSolitaireCollection','Microsoft.ZuneMusic','Clipchamp.Clipchamp'
Get-AppxProvisionedPackage -Online | Where DisplayName -in $remove |
  Remove-AppxProvisionedPackage -Online
Get-AppxPackage -AllUsers | Where Name -in $remove | Remove-AppxPackage -AllUsers
```
Run as SYSTEM early in provisioning (Autopilot platform script / task
sequence step), log what was removed.

## Never remove
Microsoft.WindowsStore (breaks app updates, winget sources), Desktop App
Installer (winget), VCLibs/UI.Xaml/.NET frameworks, Windows Security, Edge,
ShellExperienceHost/StartMenuExperienceHost, Photos/Calculator/Notepad
unless replaced. Community "debloat" scripts often remove too much —
review every line.

## Stop them coming back
- Policy: **Turn off Microsoft consumer experiences** (Experience CSP
  `AllowWindowsConsumerFeatures=0`; Enterprise/Education honour it fully)
  stops suggested app installs and Start pins.
- Start layout / pinned apps via Intune (Start CSP `ConfigureStartPins`).
- Intune "Microsoft Store app (new)" uninstall assignments for specific
  apps.

## OEM software
Uninstall OEM trialware (AV trials, "app assist" tools) but **keep** OEM
driver/firmware utilities you use (Dell Command | Update, HP Image Assistant,
Lenovo System Update) — or remove them only if updates are handled by
Windows Update/Intune driver policy. Simplest: start from a clean
Microsoft image or OEM "corporate ready" image.

## Gotchas
- Feature updates can reinstall some inbox apps — re-run removal after
  upgrades (detection script/remediation).
- Removing Teams (personal) vs Teams (work): different packages
  (`MicrosoftTeams` consumer vs `MSTeams` work).

## Verify
New user profile on a fresh build has no listed apps
(`Get-AppxPackage | Where Name -in $remove` empty), Store and winget still
work, Start menu shows the corporate layout.
