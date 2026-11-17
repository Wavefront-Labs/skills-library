---
id: computing-software.systems-network-administration.active-directory.admt-user-and-group-migration
name: admt-user-and-group-migration
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-migration, admt, admt-user-migration, admt-sid-history, sid-history, inter-forest-migration, group-migration]
level: advanced
status: draft
description: "Migrate users and groups between forests with ADMT and SID history: trusts, auditing and $$$ group prerequisites, migration order, and ADMT command-line options."
sources:
  - https://www.microsoft.com/en-us/download/details.aspx?id=56570
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-aduser
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migrate users and groups with ADMT and SID history

ADMT 3.2 is old and only partly supported on modern OS (installs on 2012 R2-2016 with
SQL Express; community-documented on 2019/2022). Commercial tools (Quest, Semperis)
replace it for large projects, but the mechanics are the same.

## Prerequisites for SID history
- Two-way trust (or one-way with source trusting target) and SID filtering disabled for
  the migration period on the trust (`netdom trust target /domain:source /quarantine:No`).
- Target domain: migration account is admin in both domains.
- Source domain: create local group `SOURCEDOMAIN$$$` (domain local), enable auditing
  of account management in both domains, and on the source PDC set
  `HKLM\System\CurrentControlSet\Control\Lsa\TcpipClientSupport=1`, reboot.
- ADMT installed in the target domain with its database.

## Order
1. Global groups (with SID history, no members) so ACLs keep working.
2. Users (with SID history, passwords via PES, "fix users' group memberships").
3. Re-run group migration to update membership; then computers; then translate
   security on servers.

## Command line
```
admt group /n "Finance-RW" /sd:old.example.com /td:corp.example.com /to:"Groups" /mss:yes /co:merge
admt user /n jsmith /sd:old.example.com /td:corp.example.com /to:"Users" /mss:yes /po:copy /ps:oldpdc /fgm:yes /uur:yes /co:merge
admt user /f users.txt ...      # include file
```
`/mss:yes` migrate SIDs, `/po:copy` passwords from PES server `/ps`, `/fgm` fix group
membership.

## After
- Users access old resources with SID history until security translation completes.
- Clean up SID history later (`Set-ADUser -Remove @{sidHistory=...}`) once resources
  are translated; re-enable SID filtering on the trust.

## Verify
- [ ] Migrated user token contains old SID (`whoami /groups` shows old domain groups by SID history).
