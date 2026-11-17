---
id: computing-software.database-administration.database-backup-recovery.ransomware-recovery-planning
name: ransomware-recovery-planning
category: computing-software
field: database-administration
product: database-backup-recovery
tags: [database-administration, database-backup-recovery, backup-strategy, ransomware-recovery, immutable-backup, isolated-recovery, clean-restore-point]
level: advanced
status: draft
description: "Plan database recovery from ransomware: backups attackers cannot delete, credential separation, finding a clean restore point, isolated recovery environments, and drills."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
  - https://www.cisa.gov/stopransomware/ransomware-guide
  - https://csrc.nist.gov/pubs/sp/1800/25/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ransomware recovery planning for databases

Ransomware operators look for backups first: they delete snapshots, wipe backup servers and
encrypt database files, often weeks after gaining access. Normal HA (replicas) replicates the
damage. Plan specifically for an attacker with admin credentials.

## 1. Backups that cannot be deleted or altered
- **Immutable** storage: S3 Object Lock (compliance mode), Azure immutable blob policies, GCS
  bucket lock, WORM tape, backup appliances with retention lock.
- **Separate credentials and control plane**: the backup account/vault is in a different
  account/tenant, without trust from the production domain; production admins cannot shorten
  retention. MFA and break-glass for the backup admin.
- At least one copy **offline or logically air-gapped** (3-2-1-1-0: 3 copies, 2 media, 1 offsite,
  1 immutable/offline, 0 errors on verification).
- Keep retention long enough to predate a long dwell time (30-90+ days of restore points).

## 2. Protect what you need to restore
Backups are useless without: encryption keys (TDE wallets/certificates, KMS keys with deletion
protection), backup catalogs (RMAN catalog, pgBackRest repo info), configuration (pg_hba, my.cnf,
logins/users scripts), runbooks, and installation media, all stored outside the blast radius.

## 3. Find a clean restore point
- Determine when the attacker got in (incident response), not only when encryption started.
- Restore candidate backups into an **isolated recovery environment** (no network path to
  production or the internet), scan for persistence (malicious stored procedures, new users,
  jobs, triggers, extensions/modules, altered binaries), check integrity (`DBCC CHECKDB`,
  `pg_amcheck`, RMAN validate), and compare data with known-good checks.
- PITR can roll forward close to the attack only if log backups from before encryption are intact
  and the logs themselves are not tampered with.

## 4. Recovery order and time
Identity (AD/IdP) and infrastructure first, then the databases in dependency order. Measure real
restore throughput: restoring 50 TB from object storage can take days. That number, not the
backup schedule, is your RTO; tiered recovery (critical systems first) and pre-staged hardware or
cloud capacity shorten it.

## 5. Drills
At least yearly: simulate "all production and primary backups gone", restore from the immutable
copy into the isolated environment with only documented credentials, and time it.

## Verify
Attempt to delete or overwrite a backup object with production admin credentials (must fail);
the last drill restored the critical databases within the target RTO from immutable copies.
