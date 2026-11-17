---
id: computing-software.systems-network-administration.active-directory.admt-installation-and-prerequisites
name: admt-installation-and-prerequisites
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-migration, admt-installation, admt, trusts]
level: advanced
status: draft
description: "Install ADMT 3.2 with SQL Express or SQL Server, set up trusts, DNS, audit and SID-history prerequisites, and the accounts and groups ADMT needs."
sources:
  - https://www.microsoft.com/en-us/download/details.aspx?id=56570
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ADMT installation and prerequisites

ADMT 3.2 (with its later update) is old but still the free tool for intra/inter-forest migrations.

## Where to install
A member server in the **target** domain (not a DC), 2012 R2-2019 commonly; needs SQL Server Express 2012+ or a full
SQL instance (create the DB with `admtdb create /s:<SQLSERVER\INSTANCE>` if installing against remote SQL).

## Trust and DNS
- Two-way trust between source and target (or one-way target trusts source + reverse for some tasks); external or
  forest trust.
- DNS conditional forwarders both ways.
- Disable SID filtering on the trust temporarily if migrated users need SID history to access source resources:
```cmd
netdom trust <TargetDomain> /domain:<SourceDomain> /quarantine:no
netdom trust <TargetForest> /domain:<SourceForest> /enablesidhistory:yes
```

## SID history prerequisites
- In the **source** domain: create local group `<SOURCEDOMAIN>$$$` (exactly, NetBIOS name + three dollar signs) in the
  domain, and enable auditing of account management (success/failure) on source and target DCs.
- On the source PDC: registry `HKLM\System\CurrentControlSet\Control\Lsa\TcpipClientSupport = 1`, reboot.
- Migration account: admin in the target (rights to create objects in target OUs), and member of source domain
  Administrators (or delegated), plus local admin on computers being migrated.

## Password migration
Install the Password Export Server on a source DC with a key generated on the ADMT server (`admt key /option:create`).

## Verify
- [ ] ADMT console opens; a test user migration with SID history succeeds; source user's SID appears in target
  user's `sIDHistory`.
