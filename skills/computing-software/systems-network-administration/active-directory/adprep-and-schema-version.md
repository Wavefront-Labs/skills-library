---
id: computing-software.systems-network-administration.active-directory.adprep-and-schema-version
name: adprep-and-schema-version
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, adprep, schema-version, forestprep, domainprep, objectversion, schema-update, dc-upgrade, schema-admins, functional-level]
level: practitioner
status: docs-checked
description: "Check the AD schema version and run adprep forestprep/domainprep before the first DC on a new OS: rights, FSMO connectivity, and the objectVersion table."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/upgrade-domain-controllers
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/schema-updates
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/rodc/forest-wide-updates
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/domain-wide-updates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# adprep and the schema version

**Goal:** prepare the forest and domains for a newer DC OS in a controlled change, not as a
side effect of the first promotion.

## Read the current schema version
```powershell
Get-ADObject (Get-ADRootDSE).schemaNamingContext -Property objectVersion | Select objectVersion
```
| objectVersion | Schema update from |
|---|---|
| 47 | Windows Server 2008 R2 |
| 56 | 2012 |
| 69 | 2012 R2 |
| 87 | 2016 |
| 88 | 2019 (the only new schema file for 2019; the schema-updates article lists none for 2022) |
| 91 | 2025 (new schema files sch89, sch90, sch91) |
Check from several DCs; a mismatch means schema replication has not converged.

## Run adprep explicitly (recommended for change control)
Promoting a new server to a DC runs adprep automatically (it is built into the PowerShell and Server Manager
experiences). For an in-place upgrade of an existing DC you must run `adprep /forestprep` and `adprep /domainprep`
manually. Run `/forestprep` once per forest and `/domainprep` once per domain for each newer Windows Server version.
```cmd
adprep /forestprep      REM needs the schema master; Schema Admins + Enterprise Admins + Domain Admins
adprep /domainprep      REM needs the infrastructure master; Domain Admins, once per domain
adprep /rodcprep        REM Enterprise Admins; only if you will deploy RODCs
```
Only 64-bit upgrades are supported. A new DC install also needs connectivity to the RID master, and a new domain
needs the domain naming master.

## Before you run
- Verify security settings and application compatibility; take a full backup of the schema master and confirm
  replication is healthy (`repadmin /replsummary`).
- Check what the target version needs: Windows Server 2019 and later need at least Windows Server 2008 forest
  functional level, and new Windows Server 2025 forests need 2016 or later.

## Verify
- [ ] `objectVersion` shows the new value on every DC.
- [ ] The `revision` attribute of `CN=ActiveDirectoryUpdate,CN=ForestUpdates,CN=Configuration,<forest root DN>` and of
  `CN=ActiveDirectoryUpdate,CN=DomainUpdates,CN=System,<domain DN>` reflects the new operations (the forest-wide and
  domain-wide update articles list the revision numbers per release).

## Checked

Date: 2026-10-27. Documentation: Upgrade domain controllers (FSMO connectivity, rights table, in-place upgrade rule),
Windows Server Active Directory schema updates (objectVersion values and files per release), Forest-wide updates and
Domain-wide updates (revision attributes), What's new in Windows Server 2025 (schema files sch89-sch91)
(MicrosoftDocs/windowsserverdocs, main branch).
Confirmed: objectVersion 47, 56, 69, 87, 88 and 91 with their release, rights and FSMO needs for each adprep switch,
ForestUpdates/DomainUpdates `ActiveDirectoryUpdate` objects and their `revision` attribute, 64-bit-only upgrades,
functional-level minimums.
Removed unconfirmed claims: the `\support\adprep` media path, the adprep log folder, "idempotent" re-run wording,
schema-extension conflict warnings and the out-of-hours advice.

Method: documentation only; no commands were run.
