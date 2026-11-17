---
id: computing-software.systems-network-administration.backup-and-recovery.ransomware-clean-restore-point
name: ransomware-clean-restore-point
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [ransomware-recovery, clean-restore-point, dwell-time, malware-scan, secure-restore, indicators-of-compromise, isolated-recovery-environment, incident-response]
level: advanced
status: draft
description: "Pick a restore point that predates the attacker after ransomware: establish the intrusion timeline, scan restore points for IOCs, restore into isolation, and avoid reinfection."
sources:
  - https://www.cisa.gov/stopransomware/ransomware-guide
  - https://www.nccoe.nist.gov/data-integrity
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding a clean restore point after ransomware

**Goal:** restore systems from backups taken before the attacker had a foothold, so you
don't restore the backdoor along with the data.

## Why the latest backup is often wrong
Attackers typically spend days to weeks inside (dwell time) before encrypting: persistence
(scheduled tasks, services, web shells, new accounts) is already in recent backups. Restoring
the newest point reinfects you.

## Procedure
1. **Timeline first** (with incident response): earliest malicious activity per system from
   EDR telemetry, logs (authentication, PowerShell, remote tools), and threat intel on the
   ransomware group's typical tooling.
2. **Candidate points:** for each system, restore points before that earliest time. Balance
   data loss (older = more loss) against confidence.
3. **Scan before trusting:**
   - Mount restore points read-only and scan with updated AV/EDR and YARA/IOC sets (Veeam
     Secure Restore / scan backup, Rubrik/Cohesity threat hunting, or mount + scanner).
   - Look for IOCs: known file hashes, persistence keys, unknown services, unexpected admin
     accounts, scheduled tasks.
4. **Restore into an isolated recovery environment** (no route to production or internet
   except controlled), validate, patch, rotate credentials.
5. **Recover data separately** when the system point must be old: restore a clean system
   image, then bring newer *data* (files, DB exports) forward after scanning, rather than the
   newer full system.
6. Promote to production only after identity (AD) is clean and the entry vector is closed.

## Rebuild vs restore
Domain controllers and internet-facing systems used in the intrusion are often **rebuilt**
from clean media rather than restored; stateless servers are rebuilt from configuration
management; data-heavy servers are restored then hardened.

## Gotchas
- Immutable backups protect the backup copies, not their cleanliness.
- Backup system credentials may be compromised: rebuild the backup server or rotate all its
  credentials before using it in recovery.
- Encrypted-but-unnoticed files from early encryption stages may exist in "clean" points;
  check file entropy/extension changes.

## Verify
Each restored system has a documented restore point, the evidence it predates the
intrusion, scan results, and sign-off from incident response before reconnection.
