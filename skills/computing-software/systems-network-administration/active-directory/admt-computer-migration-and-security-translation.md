---
id: computing-software.systems-network-administration.active-directory.admt-computer-migration-and-security-translation
name: admt-computer-migration-and-security-translation
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-migration, admt, security-translation, computer-migration, profile-translation, re-acl, admt-agent]
level: advanced
status: draft
description: "Migrate member computers with ADMT and translate security: agent deployment, computer migration and reboot, security translation modes for files, shares, profiles."
sources:
  - https://www.microsoft.com/en-us/download/details.aspx?id=56570
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migrate computers and translate security

## Computer migration
ADMT installs an agent on each computer, joins it to the target domain and reboots it.
Requirements: ADMT account is local admin on the computers (add target group to local
Administrators via GPO first), File and Printer Sharing and RPC open, computers online.
```
admt computer /n PC001 /sd:old.example.com /td:corp.example.com /to:"Computers" /rdl:5
```
`/rdl` restart delay in minutes. Check `Agent Monitor` and the per-computer logs on the
ADMT server.

## Security translation
Rewrites ACLs (and other references) from source SIDs to the migrated target SIDs,
using the ADMT database mapping (or a SID mapping file for objects migrated otherwise).
Objects: files and folders, shares, printers, local groups, user rights, registry,
**user profiles**.
Modes:
| Mode | Effect |
|---|---|
| Add | adds target SID next to source SID (safest, reversible) |
| Replace | replaces source SID with target SID |
| Remove | removes source SID (after cutover, cleanup) |
```
admt security /n FS01 /sd:old.example.com /td:corp.example.com /tot:add /tsf:yes /tss:yes /tlg:yes /tup:yes
```
Run Add during migration, Remove at the end once SID history is to be cleaned.

## Profiles
Workstations: translate user profiles (`/tup:yes`) with Replace or Add so users keep
their profile under the new account. For modern Windows, profile translation in ADMT is
unreliable; tools like ForensiT User Profile Wizard are commonly used.

## Gotchas
- Servers with huge file trees: translation takes hours; run per volume and outside
  business hours.
- Services running as source-domain accounts must be reconfigured separately.

## Verify
- [ ] Computer in target domain, users log on with target accounts and keep access
  without relying on SID history (test with SID filtering enabled in a pilot).
