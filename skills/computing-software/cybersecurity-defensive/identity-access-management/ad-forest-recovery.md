---
id: computing-software.cybersecurity-defensive.identity-access-management.ad-forest-recovery
name: ad-forest-recovery
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [ad-forest-recovery, active-directory-recovery, dc-restore, krbtgt-reset, authoritative-restore, ransomware-recovery, tier-0]
level: sme
status: gated
description: "Recover an Active Directory forest after compromise or ransomware: backups to use, isolated restore of one DC per domain, metadata cleanup, password resets and re-promotion."
sources: ["https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-guide", "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-procedures", "https://www.ncsc.gov.uk/collection/incident-management"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active Directory forest recovery

Follow the Microsoft AD Forest Recovery Guide; this is the condensed operational shape.

## Before you need it
- System state / bare-metal backups of at least two DCs per domain, offline/immutable, tested; backup age within the forest's tombstone lifetime (check your value).
- Know which backups predate the compromise (attacker dwell time!). Malware-scanned restore points.
- Isolated recovery network (no connection to production), documented DSRM passwords in a vault, recovery runbook with forest topology.

## Procedure (per domain, root domain first)
1. Shut down/isolate all DCs. Decide the restore point (before compromise).
2. Restore one writable DC per domain from backup in the isolated network, ideally the one holding FSMO roles. Start in DSRM, perform **non-authoritative restore of AD DS + authoritative synchronisation of DFSR-replicated SYSVOL** (see the guide's procedure).
3. Boot normally; if it was not a GC, make it one temporarily.
4. Clean up metadata of all other DCs (`ntdsutil metadata cleanup` or ADUC delete DC object), seize FSMO roles if needed (`ntdsutil roles seize`) (gated: unconfirmed, source is paywalled or blocked).
5. Raise the RID pool and invalidate the current RID pool as the guide describes.
6. Reset: computer account password of the DC twice, **krbtgt twice** (with replication-wait gaps - here single DC so immediate), trust passwords twice, all tier-0 admin passwords, DSRM password.
7. Remove attacker persistence: rogue admins, GPOs, AdminSDHolder ACL changes, SID history, scheduled tasks, DCShadow artefacts.
8. Re-promote additional DCs fresh (do not restore them), then reconnect to production in stages.

## Gotchas
- Restoring from a backup taken after the attacker achieved domain admin restores their persistence.
- Virtual DC snapshots restored without VM-GenerationID support cause USN rollback (gated: unconfirmed, source is paywalled or blocked).
- Recovery needs DNS, time and identities of the recovery team that do not depend on the failed AD; pre-stage local accounts.

## Verify
- [ ] Annual recovery drill in an isolated lab using real backups, timed.
- [ ] Post-recovery: `repadmin /replsummary` clean, `dcdiag /e` passes, no unknown privileged members.

## Checked

2026-10-28. Confirmed against the AD Forest Recovery Guide procedures page: nonauthoritative restore of AD DS and authoritative synchronisation of DFSR-replicated SYSVOL. Gated: ntdsutil metadata cleanup and role seizure, USN rollback and VM-GenerationID. Removed: 180-day tombstone figure, msDFSR-Options value, 100,000 RID pool figure and rIDAvailablePool, netdom resetpwd.

Method: documentation only; no commands were run.
