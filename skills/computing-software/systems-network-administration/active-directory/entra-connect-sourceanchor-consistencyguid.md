---
id: computing-software.systems-network-administration.active-directory.entra-connect-sourceanchor-consistencyguid
name: entra-connect-sourceanchor-consistencyguid
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-connect, sourceanchor, consistencyguid, hard-match, immutableid]
level: advanced
status: docs-checked
description: "Understand sourceAnchor with ms-DS-ConsistencyGuid: how immutableId is derived, switching from objectGUID, cross-forest moves and hard-match recovery."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/plan-connect-design-concepts
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-install-existing-tenant
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sourceAnchor and ms-DS-ConsistencyGuid

The sourceAnchor uniquely identifies an object as the same object on-premises and in Entra ID. In Entra it appears as
**immutableId**. Its value cannot change after the object is created in Entra and synchronized; if it changes after
export, Connect throws an error and blocks further changes to that object until it is changed back.

## How it is set
- Connect 1.1.524.0 and later can use `ms-DS-ConsistencyGuid` for **user** objects; `objectGUID` is used for other object
  types. For a user whose `ms-DS-ConsistencyGuid` is empty, Connect writes the `objectGUID` value back into it and then
  uses it.
- Express install logic: reuse the attribute the previous Connect installation recorded in the tenant; otherwise use
  `ms-DS-ConsistencyGuid` if no object in AD uses it; otherwise fall back to `objectGUID`.
- `objectGUID` is system-generated and changes if a user is moved to another forest, which is why `ms-DS-ConsistencyGuid`
  (which can be moved with the user) is preferred when users move between forests or domains.
- The source anchor can only be chosen at first installation; a second Connect server must use the same attribute, and a
  DirSync migration must use `objectGUID`.
- The AD DS connector account needs write permission on `ms-DS-ConsistencyGuid` (`Set-ADSyncMsDsConsistencyGuidPermissions`).

## Switch an existing objectGUID deployment
Connect 1.1.552.0 and later: run the wizard > **Configure** > **Configure Source Anchor**. The wizard checks that no object
in AD already has `ms-DS-ConsistencyGuid` populated and stops with an error if one does (this also happens when you repeat
the task on a staging server after the primary). If you are certain no other application uses the attribute, restart the
wizard (`AzureADConnect.exe`) with `/SkipLdapSearch`.

## Compute immutableId from AD
```powershell
$g = (Get-ADUser jdoe -Properties 'mS-DS-ConsistencyGuid').'mS-DS-ConsistencyGuid'
[Convert]::ToBase64String($g)
```
The sourceAnchor is the Base64 form of the attribute (non-string attributes are Base64-encoded).

## Hard match
If Entra finds an object whose `ImmutableId` equals the incoming sourceAnchor, Connect takes it over (hard match); otherwise
Entra tries a soft match on UPN or primary SMTP address. To fix an orphaned or recreated user, set the on-premises
`mS-DS-ConsistencyGuid` to the cloud user's existing ImmutableId.
Since 2026-07-01 Entra blocks a hard match when the target cloud account already has `onPremisesObjectIdentifier` set,
holds or is eligible for a privileged Entra role, or the tenant flag `BlockCloudObjectTakeoverThroughHardMatchEnabled`
is on. The safe recovery is to confirm the intended mapping, temporarily remove the role, complete the match, then restore
the role; to remap an object with `onPremisesObjectIdentifier` set, clear it to `null` through Graph first. Microsoft
advises against syncing on-premises accounts onto existing administrative accounts.

## Gotchas
- Clearing `ms-DS-ConsistencyGuid` on an AD object breaks the link on the next sync.
- If sourceAnchor changed after reinstalling Connect with a different attribute, objects fail with InvalidSoftMatch.

## Verify
- [ ] immutableId in Entra equals base64 of the on-premises sourceAnchor attribute for sampled users.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): Connect design concepts (sourceAnchor and ConsistencyGuid),
existing-tenant matching (hard match protections effective 2026-07-01) and sync-error troubleshooting pages. Corrected: only
users use `ms-DS-ConsistencyGuid`, the switch is the Configure Source Anchor task (not "customize options"), and
hard-match blocks now include privileged-role and `onPremisesObjectIdentifier` cases (the old "blocked since 2023"
statement was unconfirmed). Removed the `Get-ADSyncGlobalSettings` check and the backup-restore claim.
Method: documentation only; no commands were run.
