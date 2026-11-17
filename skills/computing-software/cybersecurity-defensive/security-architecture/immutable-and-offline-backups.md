---
id: computing-software.cybersecurity-defensive.security-architecture.immutable-and-offline-backups
name: immutable-and-offline-backups
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [resilience, immutable-backups, backup-strategy, 3-2-1-1-0, object-lock, air-gapped-backups, ransomware-resilience, backup-credentials, worm-storage]
level: practitioner
status: draft
description: "Design ransomware-resilient backups: 3-2-1-1-0 rule, immutability (object lock, hardened repositories), separate credentials and monitoring of the backup plane."
sources: ["CIS Control 11 (data recovery, 11.4 isolated recovery data)", "CISA StopRansomware Guide (backups)", "AWS Docs - S3 Object Lock", "NIST SP 800-209 Security guidelines for storage infrastructure"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Immutable and offline backups

**Goal:** after a ransomware attacker gains domain admin, you still have clean, restorable
backups they could not delete or encrypt.

## The rule: 3-2-1-1-0
3 copies, on 2 media types, 1 offsite, 1 **immutable or offline**, 0 errors in restore tests.

## Immutability options
| Option | Notes |
|---|---|
| S3 Object Lock (compliance mode) | Not even root can delete before retention expires. Governance mode can be bypassed by privileged users. Requires versioning. |
| Azure Blob immutable storage (locked time-based policy) | Locked policies cannot be shortened. |
| Hardened Linux repository (e.g. Veeam hardened repo, XFS immutability) | Single-use credentials, no SSH, separate from the domain. |
| Backup appliance with retention lock (Data Domain, etc.) | Lock mode requires security officer for changes. |
| Tape / offline disk rotation | True air gap; slow restores. |

## Isolate the backup plane
- Backup servers and repositories **not joined** to the production domain, or in a separate admin forest.
- Separate admin accounts with phishing-resistant MFA; no password reuse with production.
- Backup console reachable only from a management network / PAW.
- Separate cloud account/subscription for backup copies, with restricted cross-account roles.
- Encrypt backups; store keys outside the production environment.

## Monitor the backup system as a target
Alert on: job deletions, retention reductions, disabled jobs, new admin users on the backup
console, unusual restore activity, failed immutability. Ransomware operators target backups
first, often days before encryption.

## Gotchas
- Retention shorter than attacker dwell time restores already-infected systems: keep at least 30-90 days of immutable points.
- Snapshots on the same storage array as production are not backups.
- SaaS data (Microsoft 365, Google Workspace, Salesforce) needs its own backup; native retention is not a backup.
- Compliance-mode object lock with a wrong (long) retention cannot be undone and costs money.

## Verify
- [ ] Attempt to delete an immutable backup with admin credentials fails (test it).
- [ ] Backup admin credentials are not present in production AD.
- [ ] Restore tests pass (see restore testing).
