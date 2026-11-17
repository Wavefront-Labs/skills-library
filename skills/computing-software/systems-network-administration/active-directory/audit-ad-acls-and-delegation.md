---
id: computing-software.systems-network-administration.active-directory.audit-ad-acls-and-delegation
name: audit-ad-acls-and-delegation
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ou-delegation, delegation-of-control, ad-acl-audit, ou-permissions-audit, get-acl, ad-drive, genericall, writedacl, dcsync, bloodhound, attack-paths, attack-path-analysis]
level: advanced
status: docs-checked
description: "Audit who can do what in AD: dump OU ACLs with Get-Acl on the AD: drive, flag GenericAll/WriteDacl/DCSync rights held by non-admins, and clean up."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/implementing-least-privilege-administrative-models
  - https://learn.microsoft.com/en-us/dotnet/api/system.directoryservices.activedirectoryrights
  - https://learn.microsoft.com/en-us/windows/win32/adschema/r-ds-replication-get-changes
  - https://learn.microsoft.com/en-us/windows/win32/adschema/r-ds-replication-get-changes-all
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Audit AD ACLs and over-delegation

**Goal:** find non-admin principals with rights that amount to admin, so they can be removed.

## Dump explicit ACEs on OUs and the domain root
```powershell
Import-Module ActiveDirectory
$targets = @((Get-ADDomain).DistinguishedName) + (Get-ADOrganizationalUnit -Filter *).DistinguishedName
$risky = 'GenericAll|GenericWrite|WriteDacl|WriteOwner|CreateChild|ExtendedRight|WriteProperty'
$rows = foreach ($dn in $targets) {
  (Get-Acl "AD:$dn").Access | ? { -not $_.IsInherited -and $_.ActiveDirectoryRights -match $risky } |
    Select @{n='Target';e={$dn}}, IdentityReference, ActiveDirectoryRights, ObjectType, InheritedObjectType, InheritanceType }
$rows | ? { $_.IdentityReference -notmatch 'Domain Admins|Enterprise Admins|SYSTEM|Administrators|ENTERPRISE DOMAIN CONTROLLERS|Domain Controllers' } |
  Export-Csv ad-acl-audit.csv -NoTypeInformation
```
The flag names are members of the .NET `ActiveDirectoryRights` enumeration. `ObjectType` GUIDs map to attributes and
extended rights: resolve them via the schema (`schemaIDGUID`) and `CN=Extended-Rights` (`rightsGuid`) to read the CSV.

## High-risk findings
- **Directory replication rights**: `Replicating Directory Changes` (`DS-Replication-Get-Changes`,
  `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2`) together with `Replicating Directory Changes All`
  (`1131f6ad-9c07-11d1-f79f-00c04fc2dcd2`) on the domain root, held by anything that is not a domain controller or an
  approved, documented sync account.
- `GenericAll`/`WriteDacl`/`WriteOwner` on the domain root, AdminSDHolder, the Domain Controllers OU, or GPOs linked there.
- `Everyone`/`Authenticated Users` with write rights anywhere.
- Write access to `msDS-AllowedToActOnBehalfOfOtherIdentity` on servers.
- Owners of privileged groups or GPOs who are not Tier 0.

## Clean up
Remove with `dsacls <DN> /R <principal>` or by editing in ADUC Advanced Security; replace with scoped delegation
per the delegation skill. Record each removal, and check the application vendor's documentation first because some
products add their own ACEs.

## Verify
- [ ] Re-run produces only approved delegation groups.
- [ ] No non-DC principal holds the replication rights except documented sync accounts.

## Checked
2026-10-27. Documentation: Microsoft Learn AD schema reference (extended rights) and the .NET
`ActiveDirectoryRights` enumeration. Confirmed: the two replication rights are `DS-Replication-Get-Changes` (display name
Replicating Directory Changes, GUID 1131f6aa-...) and `DS-Replication-Get-Changes-All` (GUID 1131f6ad-...); `GenericAll`,
`WriteDacl` and `ExtendedRight` are enum members; `msDS-AllowedToActOnBehalfOfOtherIdentity` is a documented attribute; the
dsacls `/R` behaviour. Removed as unconfirmed: the named Entra Connect account statement and the third-party tooling
section.
Method: documentation only; no commands were run.
