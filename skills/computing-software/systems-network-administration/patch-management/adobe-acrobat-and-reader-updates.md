---
id: computing-software.systems-network-administration.patch-management.adobe-acrobat-and-reader-updates
name: adobe-acrobat-and-reader-updates
category: computing-software
field: systems-network-administration
product: patch-management
tags: [adobe-updates, acrobat, acrobat-reader, third-party-patching, patch-management]
level: practitioner
status: draft
description: "Patch Adobe Acrobat and Reader at scale: continuous vs classic tracks, Customization Wizard, disabling the updater or using it, MSP/MSI deployment and version verification."
sources:
  - https://www.adobe.com/devnet-docs/acrobatetk/tools/ReleaseNotesDC/index.html
  - https://www.adobe.com/devnet-docs/acrobatetk/tools/AdminGuide/updates.html
  - https://helpx.adobe.com/security/security-bulletin.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Adobe Acrobat and Reader updates

## Tracks
- **Continuous** (Acrobat DC / Reader DC / Acrobat Reader 64-bit): frequent updates (monthly-ish security on Patch Tuesday), version like `24.004.20220`.
- **Classic** (Acrobat 2020 / 2024): quarterly-ish security-only, fixed EOL date.
Security bulletins (APSB) publish on Microsoft Patch Tuesday.

## Updater strategy
Choose one:
1. **Let Adobe updater auto-install** (default `Automatically install updates`) - fine for unmanaged-ish fleets; check it actually runs (Adobe Acrobat Update Service).
2. **Manage centrally** - disable the updater and deploy updates through ConfigMgr/Intune/third-party catalog:
```text
HKLM\SOFTWARE\Policies\Adobe\Adobe Acrobat\DC\FeatureLockDown  bUpdater (DWORD) = 0
HKLM\SOFTWARE\Policies\Adobe\Acrobat Reader\DC\FeatureLockDown bUpdater (DWORD) = 0
```
Or set in the Acrobat Customization Wizard (Online and Acrobat.com features > Disable all updates).

## Deploy
- Base installer + cumulative MSP: `msiexec /i AcroPro.msi /update AcrobatDCUpd2400420220.msp /qn` (Reader: `AcroRdrDC*.exe -sfx_nu /sAll /rs /msi EULA_ACCEPT=YES`).
- Continuous updates are cumulative; one latest MSP covers all older.
- Intune: Win32 app with supersedence, or catalog-based.

## Version check
```powershell
Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*','HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*' |
  Where-Object DisplayName -match 'Adobe Acrobat' | Select-Object DisplayName, DisplayVersion
```

## Gotchas
- 32-bit Reader and 64-bit unified Acrobat installer coexist confusingly; Adobe now ships a unified 64-bit app that runs as Reader or Acrobat depending on licence.
- Updates fail while Acrobat or browsers with the PDF plugin are open; schedule or force-close.
- Classic track reaches EOL on a fixed date; plan migration.

## Verify
DisplayVersion at or above the latest APSB fixed version across inventory; scanner Acrobat findings closed.
