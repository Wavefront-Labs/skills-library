---
id: computing-software.cybersecurity-defensive.security-architecture.backup-restore-testing
name: backup-restore-testing
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [resilience, restore-testing, backup-verification, recovery-testing, isolated-recovery-environment, clean-room-recovery, malware-scan-before-restore, rto-validation]
level: practitioner
status: draft
description: "Test restores on a schedule: file, system and full-environment recovery, measured against RTO/RPO, in an isolated environment with malware checks."
sources: ["CIS Control 11.5 (test data recovery)", "NIST SP 800-34 Rev. 1 Contingency planning (testing)", "CISA StopRansomware Guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backup restore testing

**Goal:** proof, not hope, that you can restore the systems that matter within the agreed time,
from backups that are clean.

## Test levels and cadence
| Test | Cadence | Pass criteria |
|---|---|---|
| Automated backup verification (checksum, boot test like Veeam SureBackup) | Every job / daily | Job integrity and VM boots |
| File/object restore sample | Monthly | Random files restored and opened |
| Full system restore (e.g. a database server) | Quarterly per tier-1 system | Application works, data current to RPO, time within RTO |
| Full environment / ransomware scenario (AD, identity, core apps) | Annually | Business processes validated by owners |

## Ransomware-scenario restore
1. Restore into an **isolated recovery environment** (separate network, no trust to production).
2. Restore identity first: Active Directory from a known-good backup (forest recovery
   procedure), or rebuild; reset krbtgt twice and all privileged credentials.
3. Scan restored systems for malware and persistence (EDR, YARA, IOC sweep) before reconnecting.
4. Choose a restore point before the earliest known attacker activity, not just before encryption.
5. Bring up in dependency order (DNS, identity, databases, applications).

## Measure
Record actual times per step against RTO, data loss against RPO, and blockers (missing
passwords, licences, documentation, staff knowledge). The blockers list is the value of the test.

## Gotchas
- Backups that "succeeded" but excluded open files, new volumes or new servers: check scope against the asset inventory.
- Restore requires the backup server, which requires AD, which is encrypted: plan the bootstrap order.
- Encryption keys and backup console credentials stored only in the production password vault.
- Bandwidth: restoring 50 TB from cloud takes days unless you planned for bulk restore.

## Verify
- [ ] Test reports with measured RTO/RPO per tier-1 system from the last quarter.
- [ ] Blockers from the last test have owners and are closed.
