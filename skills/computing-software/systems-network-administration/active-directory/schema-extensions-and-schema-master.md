---
id: computing-software.systems-network-administration.active-directory.schema-extensions-and-schema-master
name: schema-extensions-and-schema-master
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, fsmo-roles, schema-extension, schema-admins, ldifde, schmmgmt]
level: advanced
status: docs-checked
description: "Plan, test and apply AD schema extensions safely: Schema Admins membership on demand, ldifde imports, version checks and why schema changes are irreversible."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/ad/extending-the-schema
  - https://learn.microsoft.com/en-us/windows/win32/ad/disabling-existing-classes-and-attributes
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc731033(v=ws.11)
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/reducing-the-active-directory-attack-surface
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema extensions and the schema master

Schema additions are permanent: you can disable classes and attributes, but you can never remove them. Treat a
schema change like a production database migration.

## Before
- Get the vendor's LDIF and read it: every `objectClass: attributeSchema` add and its OID. Microsoft recommends that no
  attribute value exceed 500 KB and no object exceed 1 MB, and an attribute added to `user` multiplies across every user.
- Test in an isolated lab copy of the forest at the same schema version.
- Confirm forest replication is healthy and know the schema master:
  `Get-ADForest | Select SchemaMaster`.
- Take a system-state backup of the schema master.

## Grant Schema Admins only for the change window
Schema Admins is the only group that can modify the schema and is intended to be populated only temporarily and
occasionally. Add the account, do the change, remove it, and alert on any membership outside change windows.
```powershell
Add-ADGroupMember 'Schema Admins' -Members ops-schema-admin -MemberTimeToLive (New-TimeSpan -Hours 2)
```
`-MemberTimeToLive` sets a time-to-live on the new member (it relies on the time-bound membership feature; see the
time-bound membership skill for prerequisites). Without it, remove the member manually.

## Apply
```cmd
ldifde -i -f vendor-schema.ldf -s <SchemaMasterFQDN> -c "DC=X" "DC=corp,DC=example,DC=com" -k -j <LOG_DIR>
```
- `-i` import mode; `-f` import file; `-s` the DC to run against; `-c` replaces every occurrence of the first string
  with the second; `-k` ignores errors such as "object already exists" so reruns continue; `-j` sets the log file
  location.
- Run against the schema master directly, then confirm on other DCs after replication. Application installers that
  extend the schema ship their own tool; follow the vendor's documentation (Windows LAPS uses `Update-LapsADSchema`, a
  one-time forest-wide operation).

## Deactivate a bad attribute (cannot delete)
Set `isDefunct` to `TRUE` on the attributeSchema (or classSchema) object with ADSI Edit in the Schema partition.
New instances can no longer be created; existing values are not cleaned up, and setting it back to `FALSE` re-enables
the attribute. You cannot disable a Category 1 object, or an attribute that is still a member of an enabled class.

## Verify
```powershell
Get-ADObject -SearchBase (Get-ADRootDSE).schemaNamingContext -Filter 'lDAPDisplayName -eq "vendorAttr"' -Properties *
```
- [ ] New classes and attributes visible on every DC.
- [ ] Schema Admins is empty again.
- [ ] Change recorded with the LDIF in source control.

## Checked
2026-10-27. Documentation: Microsoft Learn "Extending the Schema" and "Disabling Existing Classes and Attributes"
(Win32 AD reference), ldifde reference (2012 R2 library), Appendix B/Reducing the AD Attack Surface and the Windows LAPS
schema article. Confirmed: schema additions are permanent and only disableable; `isDefunct` behaviour, reversibility and the
Category 1 and class-membership restrictions; the 500 KB and 1 MB size guidance; ldifde `-i -f -s -c -k -j` meanings;
Schema Admins is the only group that can modify the schema and is populated only temporarily; `Update-LapsADSchema` is a
one-time forest operation; `Add-ADGroupMember -MemberTimeToLive` exists. Removed as unconfirmed: the claim that every
schema change replicates to all DCs as stated, the partial-attribute-set cost note, the name/OID reservation remark, the
Exchange `/PrepareSchema` mention, the claim that vendor tools always go to the schema master, and the repadmin
objectVersion check.
Method: documentation only; no commands were run.
