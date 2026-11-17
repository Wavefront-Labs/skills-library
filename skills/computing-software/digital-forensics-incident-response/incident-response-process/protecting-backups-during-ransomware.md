---
id: computing-software.digital-forensics-incident-response.incident-response-process.protecting-backups-during-ransomware
name: protecting-backups-during-ransomware
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [immutable-backups, backup-integrity, ransomware, backup-recovery, containment, dfir]
level: practitioner
status: draft
description: "Protect and validate backups during a ransomware event: isolate backup infrastructure, lock immutable copies, check for tampering and confirm restorability."
sources: ["https://www.cisa.gov/stopransomware/ransomware-guide", "https://www.veeam.com/blog/immutable-backup-solutions.html", "https://csrc.nist.gov/pubs/sp/800/209/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Protecting backups during ransomware

**Goal:** the backups survive the attack and can actually restore. Ransomware operators
target backups first (deleting jobs, wiping repositories, encrypting backup servers).

## Immediately on suspicion
1. **Isolate backup infrastructure**: disconnect backup servers/repositories from the
   domain network; disable domain-joined backup admin accounts the attacker may hold.
2. Pause automatic retention/pruning jobs so older clean restore points are not aged out
   during the incident.
3. Ensure offline/immutable copies stay out of reach: tape out of library, object-lock
   buckets (S3 Object Lock compliance mode), hardened Linux repositories, vendor immutable
   vaults.
4. Rotate backup console credentials and enable MFA; check for attacker-created backup
   admins and changed encryption passwords.

## Check for tampering
- Backup job history: deleted jobs, changed retention, disabled jobs, failed jobs from the
  intrusion window.
- Repository contents vs catalogue (missing restore points).
- Cloud backups: deletion/lifecycle-policy changes in audit logs.
- Snapshots on storage arrays and hypervisors: deletion events.

## Confirm restorability
- Test-restore a sample of critical systems into an isolated network; time the restore to
  estimate total recovery time.
- Scan restored data for incident IOCs before using it.

## Gotchas
- Backup servers joined to the production domain with domain admin service accounts are the
  most common reason backups are lost.
- Immutable in name only: governance-mode object lock can be bypassed by privileged users.
- Encryption keys for backups stored only on the encrypted system.

## Verify
Document, for each critical system, the newest clean restore point, its location, and a
completed test restore. Without that list, recovery time estimates are guesses.
