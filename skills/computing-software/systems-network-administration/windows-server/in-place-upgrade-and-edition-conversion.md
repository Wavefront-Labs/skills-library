---
id: computing-software.systems-network-administration.windows-server.in-place-upgrade-and-edition-conversion
name: in-place-upgrade-and-edition-conversion
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-server-installation, in-place-upgrade, set-edition, dism, evaluation-to-retail, feature-upgrade, setup-exe, upgrade-paths, compat-scan]
level: practitioner
status: docs-checked
description: "Upgrade Windows Server in place (supported paths, compat scan, rollback) and convert editions with DISM /Set-Edition, including Evaluation to retail."
sources:
  - https://learn.microsoft.com/en-us/windows-server/get-started/upgrade-overview
  - https://learn.microsoft.com/en-us/windows-server/get-started/upgrade-conversion-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# In-place upgrade and edition conversion

## In-place OS upgrade
Check the supported upgrade paths and edition rules on Microsoft's upgrade overview page before planning; do not assume a
path from memory. Clusters use their own rolling-upgrade process.
Run Setup from the media of the target version; its command-line switches (including a compatibility-scan-only mode)
are listed in Microsoft's Windows Setup command-line options.
- Snapshot/backup first (Hyper-V checkpoint is fine for a member server; not for DCs, see
  virtual DC guidance; DCs are better replaced).
- Remove/upgrade incompatible agents (AV, backup, old drivers) and read the Setup logs for blockers.

## Edition conversion (Standard to Datacenter, Evaluation to retail)
```cmd
DISM /Online /Get-CurrentEdition
DISM /Online /Get-TargetEditions
DISM /Online /Set-Edition:ServerDatacenter /ProductKey:<KEY> /AcceptEula
```
- Run `DISM /online /Get-TargetEditions` first: it lists which editions you can convert to; Learn notes some conversions
  are only to specific retail editions (for example Datacenter Core, not Standard Core).
- Supply the corresponding retail key for the target edition.

## Verify
- [ ] `Get-ComputerInfo | Select OsName,OsVersion,WindowsEditionId` shows the target.
- [ ] Licensing shows Licensed with the new edition.
- [ ] Roles/services/apps tested after upgrade; rollback path documented.

## Checked
2026-10-28. Confirmed on the Learn upgrade-conversion pages: `DISM /online /Get-TargetEditions` and `/Set-Edition:<target edition>`
workflow and the Core retail-conversion limit. Removed as unconfirmed: the two-versions-per-hop rule, the Setup switch
lines, Panther log paths, the feature-update claim, the evaluation/KMS/DC/Datacenter-to-Standard statements, slmgr step.
Method: documentation only; no commands were run.
