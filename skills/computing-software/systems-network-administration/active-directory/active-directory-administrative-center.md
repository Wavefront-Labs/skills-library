---
id: computing-software.systems-network-administration.active-directory.active-directory-administrative-center
name: active-directory-administrative-center
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ou-delegation, active-directory-administrative-center, adac, powershell-history-viewer, dsac, recycle-bin-gui, fine-grained-password-policy-gui, global-search, rsat]
level: intro
status: docs-checked
description: "Use Active Directory Administrative Center well: PowerShell History Viewer to learn cmdlets, Recycle Bin and PSO GUIs, global search and multi-domain navigation."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/adac/advanced-ad-ds-management-using-active-directory-administrative-center--level-200-
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/adac/active-directory-recycle-bin
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/adac/fine-grained-password-policies
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/adac/use-active-directory-administrative-center-powershell-history
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active Directory Administrative Center (ADAC)

ADAC (`dsac.exe`) runs Windows PowerShell cmdlets for the actions you take in it, and its History Viewer shows each
cmdlet with its arguments, so every GUI action can be captured as a script.

## Features worth knowing
1. **Windows PowerShell History Viewer** (arrow at the bottom of the window): expand it, perform an action in the GUI,
   copy the generated cmdlet. Fastest way to learn the exact parameters for `New-ADUser` or `Restore-ADObject`.
   Create task notes to separate the cmdlets of one action.
2. **AD Recycle Bin GUI:** needs a Windows Server 2008 R2 or later forest functional level and Enterprise Admins
   membership, and cannot be disabled once enabled; it also grows NTDS.dit on every DC. Enable it from the domain
   node with **Tasks > Enable Recycle Bin**. Only objects deleted after enabling can be restored. Browse the
   *Deleted Objects* container and choose **Restore** (original location) or **Restore To** (pick a location).
   The Last Known Parent attribute shows where each object came from.
3. **Fine-grained password policies:** Tree View > domain > System > Password Settings Container > Tasks > New >
   Password Settings. Name and Precedence are required; add the groups or users under Directly Applies To.
4. **Navigation:** Manage > Add Navigation Nodes > Connect to other domains to add containers from another domain.

## Tips
- Start it with other credentials from a PAW or admin host, not from your daily workstation session:
  `runas /user:<domain\user> dsac`.

## Verify
- [ ] You can reproduce a GUI action by pasting the captured cmdlet from History Viewer.

## Checked
2026-10-27. Documentation: Microsoft Learn ADAC pages (Level 200, Recycle Bin, fine-grained password policies,
PowerShell history), current in the Windows Server documentation repository. Confirmed: History Viewer behaviour, Recycle
Bin prerequisites (2008 R2 forest functional level, Enterprise Admins, irreversible, database growth), Tasks > Enable
Recycle Bin, Restore and Restore To, Password Settings Container path and required fields, Add Navigation Nodes and
`runas ... dsac`. Removed as unconfirmed: authentication-policy node, Global Search, Dynamic Access Control claim,
attribute-editor and change-DC tips. Two earlier source URLs were dead and were replaced.
Method: documentation only; no commands were run.
