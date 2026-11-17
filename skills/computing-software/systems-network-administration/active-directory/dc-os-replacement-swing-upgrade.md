---
id: computing-software.systems-network-administration.active-directory.dc-os-replacement-swing-upgrade
name: dc-os-replacement-swing-upgrade
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, dc-upgrade, dc-replacement, dc-swing-upgrade, functional-level, frs-to-dfsr, ip-reuse, decommission, windows-server-2025]
level: practitioner
status: docs-checked
description: "Upgrade DCs by replacement, not in-place: build new DCs, move FSMO and DNS dependencies, demote the old ones, then raise functional levels."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/upgrade-domain-controllers
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/active-directory-functional-levels
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/dfsrmig
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/ldap-signing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replace DCs with a new OS (swing upgrade)

**Goal:** move the domain to a new DC OS with no downtime. Microsoft's guidance is that the recommended way to
upgrade is a clean OS install: promote new servers on the newer Windows Server and demote the older DCs as needed. It
prefers this to an in-place upgrade, because a clean install gets the full performance improvements of the new version.

## Plan
1. Inventory DCs, roles, site placement, and everything that points at a DC by IP or name:
   DHCP option 006, static DNS on servers, LDAP binds in apps/appliances, RADIUS/NPS clients,
   firewall rules, time clients, SIEM collectors, backup jobs.
2. Check SYSVOL replication uses **DFSR**: on the PDC emulator `dfsrmig /getglobalstate` should report the
   Eliminated state (state 3, irreversible, so only when committed to DFSR). FRS is listed as a removed feature; DFS
   Replication replaces it, so migrate SYSVOL first.
3. Run adprep explicitly (see the adprep skill) and confirm the schema version.
4. Check forest functional level against the new OS: Windows Server 2019 or later needs at least Windows Server 2008,
   and the old DCs that set the floor must be removed first.

## Execute per site
1. Build the new server(s), promote as additional DCs/GCs/DNS in the same site.
2. Wait for full replication; verify with `repadmin /replsummary` and `dcdiag`.
3. Move FSMO roles to new DCs (transfer).
4. Re-point dependencies (DHCP 006, server NIC DNS, apps). If you want the new DC to take over the old DC's address,
   plan the address change and DNS re-registration explicitly and check that the DC's records updated.
5. Demote old DCs one at a time (see demote-dc-and-metadata-cleanup). Before demoting, watch for clients still using the
   old DCs; for LDAP, Directory Service events 2887 and 2889 identify unsigned and clear-text binds (2889 needs the
   16 LDAP Interface Events diagnostic level set to 2 and should be turned off afterwards).
6. After the last old DC is gone, raise domain and forest functional levels.

## Gotchas
- Windows Server 2025 DCs: review the changed defaults (LDAP signing required by default for new deployments, 32k
  database page option, Kerberos RC4 TGT change) against legacy apps before go-live; see the windows-server-2025-ad-features
  skill.
- Do not demote a DC that is the only GC in a site with Exchange or the only DNS server for a site.

## Verify
- [ ] No old-OS DC objects remain (`Get-ADDomainController -Filter *`).
- [ ] DNS NS records in every AD zone list only the new DCs.
- [ ] Functional levels raised and replication clean.

## Checked

Date: 2026-10-27. Documentation: Upgrade domain controllers, AD DS functional levels (updated 2025-10), dfsrmig
reference, Features removed or no longer developed in Windows Server, LDAP signing for AD DS, What's new in Windows
Server 2025 (MicrosoftDocs/windowsserverdocs, main branch).
Confirmed: clean-install-then-demote recommendation, `dfsrmig /getglobalstate` on the PDC emulator and the Eliminated
state, FRS listed as removed, 2008 forest-level floor for 2019+, LDAP events 2887/2889 and the diagnostic setting,
2025 default changes.
Removed unconfirmed claims: "FRS not supported on 2019+ DCs" as worded, the IP-swap recipe, the one-week waiting period,
the 1644 diagnostic, the NTP reconfiguration step and the certificate-authority-on-DC remark.

Method: documentation only; no commands were run.
