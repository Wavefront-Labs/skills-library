---
id: computing-software.systems-network-administration.patch-management.out-of-band-update-handling
name: out-of-band-update-handling
category: computing-software
field: systems-network-administration
product: patch-management
tags: [out-of-band-update, emergency-patching, microsoft-update-catalog, wsus-import, release-health, patch-acquisition]
level: practitioner
status: docs-checked
description: "Handle out-of-band vendor releases: detect them, decide urgency, import catalog-only updates into WSUS with the supported script, and expedite deployment outside the normal cycle."
sources:
  - https://learn.microsoft.com/en-us/windows/release-health/
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-server-update-services/manage/wsus-and-the-catalog-site
  - https://learn.microsoft.com/en-us/mem/intune/protect/windows-10-expedite-updates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Out-of-band vendor releases

**Goal:** apply urgent fixes that vendors ship outside their regular cadence, quickly and with the same control as routine patches.

## Detect
- Microsoft: Windows release health lists known and resolved issues per release and a Message center feed; subscribe the triage rota to it.
- Other vendors: their security advisory (PSIRT) feeds and mailing lists, and CISA alerts. Alert on new CISA Known Exploited Vulnerabilities entries.

## Decide
- Security out-of-band release for an exploited vulnerability on exposed systems: emergency change path.
- Regression fix: deploy only to affected systems (the release notes list symptoms and affected builds).

## Acquire (Microsoft catalog-only updates into WSUS)
The Microsoft Update Catalog lists updates that can be distributed over a corporate network. The old WSUS Import Updates action was built on ActiveX, which is deprecated, and has been replaced by a PowerShell script.
1. Find the update in the Microsoft Update Catalog and copy its UpdateID from the update details page.
2. Run the Microsoft-published script `ImportUpdateToWSUS.ps1` (full text on the WSUS and the Microsoft Update Catalog page) from an elevated PowerShell console on a computer with the WSUS administrative console installed, for example:
```powershell
.\ImportUpdateToWSUS.ps1 -WsusServer WSUSServer.contoso.com -PortNumber 8530 -UpdateId 12345678-90ab-cdef-1234-567890abcdef
.\ImportUpdateToWSUS.ps1 -WsusServer WSUSServer.contoso.com -PortNumber 8531 -UseSsl -UpdateIdFilePath <path>\UpdateIDs.txt
```
Parameters: `-WsusServer` (default localhost), `-PortNumber` (80, 443, 8530 or 8531; default 8530), `-UseSsl` (use port 443 or 8531), `-UpdateId` or `-UpdateIdFilePath` (one ID per line), not both.
- A `.msu` downloaded from the catalog's download button cannot be imported into WSUS.
- Update files download according to your Update files settings (for example only when approved).
- On errors, enable TLS 1.2 and check `%ProgramFiles%\Update Services\LogFiles\SoftwareDistribution.log` on the WSUS server.
- Intune: an expedite policy overrides deferral settings to push a specific security or critical quality update quickly; it needs devices that meet the Intune requirements (see the Intune page).

## Deploy
Short pilot (hours, not days), then broad. Record whether the out-of-band update supersedes or must coexist with the monthly update.

## Gotchas
- Imported catalog updates still need approval for the right target groups.
- Match WSUS languages to the update's languages, or the update is not deployed to clients.
- Imported updates that are Not Approved or Declined can be removed by the Server Cleanup Wizard and re-imported later.

## Verify
Affected systems show the update installed, and the original symptom or vulnerability is resolved.

## Checked
Date: 2026-11-07. Read in full: WSUS and the Microsoft Update Catalog (ActiveX deprecation, ImportUpdateToWSUS.ps1 syntax, parameters and defaults, `.msu` not importable, log path, languages, cleanup wizard note), Intune "Manage Windows quality updates" (expedite policies accelerate installation of a specific update, prerequisites), Windows release health landing page (Message center, per-release known issues). Corrected: the draft's WSUS console "Updates > Import Updates" path is the deprecated ActiveX route, and `ImportUpdateFromCatalogSite('<GUID>', '<.msu path>')` is wrong (the script passes the UpdateID and an empty file list; `.msu` files cannot be imported). Removed as unconfirmed: ConfigMgr catalog import steps, the `wusa.exe` command line, known issue rollback (KIR) group policy advice, vendor PSIRT product names. The MSRC update guide page returned no readable text, so it was dropped from sources and from the text.
Method: documentation only; no commands were run.
