---
id: computing-software.systems-network-administration.active-directory.sid-history-cleanup
name: sid-history-cleanup
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-migration, sidhistory-cleanup, sid-filtering, security-translation]
level: advanced
status: draft
description: "Remove SID history after an AD migration: inventory, find ACLs still relying on old SIDs, re-ACL with security translation, then clear sIDHistory safely."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-aduser
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SID history cleanup

SID history lets migrated users access resources ACLed to their old SIDs. It also inflates tokens and is an attack
vector (forged SID history). Remove it once resources are re-ACLed.

## Inventory
```powershell
Get-ADUser -Filter 'sIDHistory -like "*"' -Properties sIDHistory | Select Name,@{n='Count';e={$_.sIDHistory.Count}}
Get-ADGroup -Filter 'sIDHistory -like "*"' -Properties sIDHistory | Select Name
```
Group by source domain SID prefix to see which old domains still matter.

## Find who still depends on it
- File servers: scan ACLs for SIDs from the old domain (unresolvable ones show as raw SIDs). Tools: ADMT security
  translation reports, `icacls <path> /T /save acls.txt` and grep for the old domain SID.
- Access monitoring: on resource servers, 4624 logons include group SIDs; easier is to remove SID history for a pilot
  group and watch for access failures.

## Re-ACL
ADMT **Security Translation Wizard** in "Add" mode adds the new SID alongside the old on files, shares, registry,
local groups, user profiles; then "Remove" mode removes old SIDs. Or `SubInACL`-style tools / scripts that replace SID
A with SID B.

## Clear SID history
```powershell
Get-ADUser jdoe -Properties sIDHistory | ForEach-Object {
  Set-ADUser $_ -Remove @{sIDHistory = $_.sIDHistory.Value} }
```
Do it in waves; keep a CSV export of removed values so you can re-add (re-adding SID history requires ADMT/DsAddSidHistory,
not a simple write).

## Finish
- Re-enable SID filtering (quarantine) on the trust: `netdom trust ... /quarantine:yes`.
- Remove the trust when the source domain is decommissioned.

## Verify
- [ ] No users or groups with sIDHistory; SID filtering on; no access complaints after the waves.
