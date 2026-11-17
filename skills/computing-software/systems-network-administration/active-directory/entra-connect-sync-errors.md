---
id: computing-software.systems-network-administration.active-directory.entra-connect-sync-errors
name: entra-connect-sync-errors
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-connect, sync-errors, hard-match, soft-match, duplicate-attribute, attributevaluemustbeunique, invalidsoftmatch, immutableid, ms-ds-consistencyguid, upn-mismatch, idfix]
level: advanced
status: docs-checked
description: "Fix Entra Connect export errors: duplicate proxyAddresses/UPN, InvalidSoftMatch, hard-matching a cloud user to AD via ImmutableId, and UPN suffix mismatches."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/tshoot-connect-sync-errors
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-install-existing-tenant
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra Connect sync errors

Find them in: Entra admin center > Connect Health > Sync services > sync errors (not uploaded if Connect uses a
non-default configuration such as changed attribute filtering), or Synchronization Service Manager > Operations > the export
run on the Entra connector (named like `<tenant>.onmicrosoft.com - AAD`).

## AttributeValueMustBeUnique
Two objects with different sourceAnchor values claim the same `proxyAddresses` or `userPrincipalName`.
- Find the conflicting objects (the error names them). Often an old cloud-only user, a contact, or a group with the
  same SMTP address.
- Fix it in the source of authority (on-premises AD for synced objects), remove the duplicate, wait for a delta sync.
- Duplicate attribute resiliency is on by default for tenants: it avoids failing the whole object for a duplicate value,
  and you see fewer InvalidSoftMatch errors. Still fix the duplicate (see the resiliency page for the exact behaviour).

## Soft match vs hard match
- **Hard match:** Entra finds an object whose ImmutableId equals the incoming sourceAnchor (the base64 of
  `ms-DS-ConsistencyGuid`, or `objectGUID` depending on configuration) and Connect takes it over.
- **Soft match:** if no hard match, Entra tries the UPN or primary SMTP address. The target must have no ImmutableId.
- **InvalidSoftMatch:** the soft match found an object that already has a different ImmutableId, meaning it was synced
  from another object. Typical causes: two on-premises objects with the same `proxyAddresses`/UPN, or a reinstall with a
  different source anchor.
- **ObjectTypeMismatch:** two objects of different types (user, group, contact) share `proxyAddresses`.
- **InvalidHardMatch:** Entra blocks the hard match because the target cloud user has `onPremisesObjectIdentifier` set or
  holds or is eligible for a privileged Entra role (error 103: "The cloud user with privileged roles is not allowed to be
  taken over."). Fix: confirm the mapping is intended, temporarily remove the role or eligibility (restore the user from
  the Entra recycle bin first if soft-deleted), rerun sync, then restore the role. If `onPremisesObjectIdentifier` is set,
  clear it to `null` through Microsoft Graph (needs `User-OnPremisesSyncBehavior.ReadWrite.All` and Global Administrator or
  Hybrid Identity Administrator), then rerun sync.
- Tenant switches `BlockCloudObjectTakeoverThroughHardMatchEnabled` and `BlockSoftMatchEnabled` (set through
  `Update-MgDirectoryOnPremiseSynchronization`) disable matching for the whole tenant; use them only outside planned
  matching windows.

To hard match a cloud user to an AD user, make the on-premises `mS-DS-ConsistencyGuid` equal the cloud user's
ImmutableId, or set the cloud user's `onPremisesImmutableId` to the base64 of the on-premises value:
```powershell
$g = (Get-ADUser jsmith -Properties 'mS-DS-ConsistencyGuid').'mS-DS-ConsistencyGuid'
[Convert]::ToBase64String($g)
```
Then ensure the AD user is in sync scope and run a delta sync. Microsoft strongly recommends against syncing
on-premises accounts onto existing administrative accounts.

## Other frequent ones
- **IdentityDataValidationFailed / DataValidationFailed**: unsupported characters or format in `userPrincipalName` or
  another attribute; run IdFix.
- **LargeObject / ExceededAllowedLength**: attribute too large. `userCertificate` has a hard limit of 15 certificates;
  `proxyAddresses` is also a common culprit. Clean the attribute on-premises.

## Verify
- [ ] Sync error count is zero in Connect Health (or the export run shows no errors).
- [ ] The affected user is one object in Entra, synced from on-premises.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): Connect sync-error troubleshooting and the existing-tenant
matching page (hard-match protections effective 2026-07-01). Confirmed error names, the soft/hard-match rules, the
InvalidHardMatch behaviour, the `userCertificate` limit and the tenant block switches. Removed the quarantined-UPN example,
`SynchronizeUpnForManagedUsers` and `FederatedDomainChangeError` guidance, and the `Update-MgUser` hard-match command, none
of which appear on the cited pages.
Method: documentation only; no commands were run.
