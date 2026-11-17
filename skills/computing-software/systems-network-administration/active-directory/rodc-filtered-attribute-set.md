---
id: computing-software.systems-network-administration.active-directory.rodc-filtered-attribute-set
name: rodc-filtered-attribute-set
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, rodc, read-only-domain-controller, filtered-attribute-set, rodc-cached-credentials, searchflags, confidential-attributes, schema, fas, bitlocker-recovery, laps]
level: advanced
status: gated
description: "Keep sensitive application attributes off RODCs with the RODC filtered attribute set (searchFlags 0x200), and check what credentials an RODC has cached."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/adschema/a-searchflags
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-addomaincontrollerpasswordreplicationpolicyusage
  - https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RODC filtered attribute set (FAS)

**Goal:** stop secret-bearing attributes that applications store in AD (custom keys,
passwords in extension attributes) from replicating to RODCs.

## How it works
An attribute whose schema `searchFlags` has bit **0x200** (512) set is not replicated to RODCs (gated: unconfirmed, source is paywalled or blocked). The
public searchFlags page confirms the neighbouring bits (for example 128 / 0x80 marks an attribute confidential, ignored for
base schema attributes with systemFlags 0x10) but does not list bit 512. The filtered-attribute flag is documented in the
Active Directory technical specification (MS-ADTS), which the GitHub-hosted docs used for this check do not include.
System-critical attributes cannot be added to the set (gated: unconfirmed, source is paywalled or blocked).

## Add an attribute to the FAS
Requires Schema Admins and a forest functional level that has no pre-RODC DCs (gated: unconfirmed, source is paywalled or blocked).
```powershell
$schema = (Get-ADRootDSE).schemaNamingContext
$attr = Get-ADObject -SearchBase $schema -Filter "lDAPDisplayName -eq 'extensionAttribute15'" -Properties searchFlags
$attr.searchFlags                                    # current value
Set-ADObject $attr -Replace @{searchFlags = ($attr.searchFlags -bor 0x200)}
```
Marking the attribute confidential as well sets bit 0x80 (128); combined with 0x200 the value is `-bor 0x280`.
Check the 0x200 bit (gated: unconfirmed, source is paywalled or blocked) before changing a production schema.

## List what is filtered
```powershell
Get-ADObject -SearchBase $schema -LDAPFilter '(searchFlags:1.2.840.113556.1.4.803:=512)' -Properties lDAPDisplayName |
  Select -Expand lDAPDisplayName
```

## Check cached credentials on an RODC
```powershell
Get-ADDomainControllerPasswordReplicationPolicyUsage -Identity BR01-RODC -RevealedAccounts
```
`-RevealedAccounts` returns accounts in the RODC's revealed list; compare against the intended allow list, and treat any
privileged account in it as a finding.

## Gotchas
- Changing schema flags is forest-wide; test in a lab forest first.
- Whether Windows LAPS or BitLocker recovery attributes replicate to RODCs is not confirmed here (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] The filtered-attribute query lists the attribute you added.
- [ ] A writable DC still returns the value to an authorised reader.

## Checked

Documentation: Microsoft Learn "Search-Flags attribute" (win32 docs repository, latest commit 2026-10-08) and the
Get-ADDomainControllerPasswordReplicationPolicyUsage reference, from the public GitHub sources.
Confirmed: searchFlags bit 128 (0x80) marks an attribute confidential and is ignored for base schema attributes, the
`-RevealedAccounts` parameter. Not confirmed (marked gated): bit 0x200 as the RODC filtered-attribute flag, the
system-critical-attribute restriction, the Schema Admins and functional-level prerequisite, and LAPS/BitLocker behaviour.
Removed: `repadmin /prp view`, `repadmin /showattr` checks and the "irreversible in practice" claim.

Method: documentation only; no commands were run.
