---
id: computing-software.digital-forensics-incident-response.incident-response-process.active-directory-forest-recovery
name: active-directory-forest-recovery
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [ad-forest-recovery, incident-recovery, active-directory, krbtgt-reset, dfir]
level: sme
status: docs-checked
description: "Recover an AD forest after compromise or ransomware: trusted backup, isolated restore of one writeable DC per domain, FSMO seizure, metadata cleanup, RID pool, krbtgt resets."
sources: ["https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-guide", "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-perform-initial-recovery"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active Directory forest recovery

**Goal:** bring back a trustworthy AD after DCs were encrypted or the directory was tampered with,
following Microsoft's AD Forest Recovery Guide.

## Decide
- Restore one writeable DC per domain from a backup whose database was not influenced by whatever
  caused the failure. Microsoft stresses a trusted backup that is thoroughly tested before it
  enters production. If the DC data proves damaged after restore, repeat with a different backup.
- Start with the forest root domain and recover a parent domain before its children. Several
  domains can be recovered at the same time.

## Initial recovery (per domain, isolated network)
1. Keep the target DC off the production network: unplug the cable of a physical server; for a VM
   remove the adapter or attach it to an isolated network.
2. On the first writeable DC in the domain do a nonauthoritative restore of AD DS and an
   authoritative restore of SYSVOL, using an AD-aware backup tool (Windows Server Backup is
   recommended). Do the authoritative SYSVOL restore only on the first DC; doing it elsewhere
   causes SYSVOL replication conflicts.
3. Verify the restored data. If the failure was an intrusion, reset all administrative account
   passwords (Enterprise Admins, Domain Admins, Schema Admins, Server Operators, Account
   Operators and so on) before installing more DCs, and replace gMSA passwords. Plan a user
   password reset if user accounts may be compromised.
4. Seize all domain-wide and forest-wide FSMO roles on the first restored DC (forest root); seize
   domain-wide roles in each child domain.
5. Clean up metadata of every other writeable DC you are not restoring. Deleting the DC object in
   ADUC or Sites and Services (Windows Server 2012 or later tools) performs the cleanup. Until it is
   done a restored RID master will not issue new RIDs (event ID 16650, then 16648 on success).
6. Ensure DNS is running on the restored DC (point the forest root DC at itself), delete NS and
   SRV records of removed DCs, and optionally run `nltest.exe /dsderegdns:server.domain.tld`.
7. **Raise the available RID pool by 100,000** and **invalidate the current RID pool**, to stop
   SIDs of post-backup principals being reissued with their stale access rights.
8. Reset the DC's **computer account password twice** and the **krbtgt password twice** (the
   krbtgt password history holds two passwords). After a breach you may also reset trust passwords.
9. In a multidomain forest, if the restored DC was a global catalog, clear the global catalog
   option on it to avoid lingering objects (single-domain forest: not required).
10. Configure the PDC emulator in the forest root to sync time from an external source.

## Then
- Join the restored DCs (one per domain) to a common isolated network, run `repadmin /replsum`
  and `DCDiag /v`, then add the global catalog to a forest root DC; it advertises once fully
  synchronised (Directory Service event ID 1119). Take a fresh backup of each restored DC.
- Redeploy the remaining DCs by installing AD DS (not by restoring them).
- Treat reconnection to production as gated on an IOC sweep and EDR on the DCs (team practice, not
  from the Microsoft guide).

## Gotchas
- A VM snapshot can be used for the nonauthoritative restore only if the host supports
  Hypervisor Generation ID.
- If the restored DC holds an operations master role, the guide notes you may need the registry
  value `Repl Perform Initial Synchronizations` set to 0 under `NTDS\Parameters`, and back to 1
  after the forest is fully recovered.

## Verify
`repadmin /replsum` clean, `DCDiag /v` passing, test logons, and no attacker principals present.

## Checked
Date: 2026-11-08. Confirmed against Microsoft Learn "Active Directory Forest Recovery Guide" and
"AD Forest Recovery - Perform initial recovery": backup trust, isolation, authoritative SYSVOL on the
first DC only, FSMO seizure, metadata cleanup, DNS, RID pool +100,000 and invalidation, double
computer-account and krbtgt resets, GC handling, replication checks, snapshot/Generation ID. Removed
as unsupported: the msDFSR-Options value, ntdsutil and rIDAvailablePool specifics, DSRM and Entra
Connect gotchas, and the FSMO-software backup preference. The linked sub-procedures were not read.
Method: documentation only; no commands were run.
