---
id: computing-software.systems-network-administration.backup-and-recovery.backup-deletion-and-anomaly-alerting
name: backup-deletion-and-anomaly-alerting
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-anomaly-detection, ransomware-detection, backup-deletion-alert, siem, audit-logs]
level: advanced
status: draft
description: "Alert on attacks against backups: deletions, retention or encryption changes, job disabling, unusual change rates and malware detection, forwarded to the SIEM."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/malware_detection.html
  - https://www.cisa.gov/stopransomware/ransomware-guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alerting on backup deletion and anomalies

Attackers disable or delete backups before encrypting. These events must page someone, not sit in a console.

## High-priority events (alert immediately)
- Restore points or backup files deleted; repository removed; retention shortened.
- Jobs disabled or deleted in bulk; encryption turned off; immutability settings changed.
- New admin users or role changes in the backup software; MFA disabled.
- Configuration backup disabled.
- Cloud: S3 `DeleteObject`/`PutBucketPolicy`/`PutObjectRetention` from unusual principals; Azure vault soft delete disabled; AWS Backup vault lock changes.

## Anomaly signals
- **Change rate spike**: incremental size suddenly 5-10x normal (mass encryption).
- **Data reduction drop**: compression ratio collapses (encrypted data does not compress).
- **Inline malware/entropy detection**: Veeam v12.1+ inline entropy and file-index analysis marks restore points as suspicious; Rubrik/Cohesity have similar.
- Job duration or failure spikes across many systems at once.

## Plumbing
- Forward backup server events via **syslog** (Veeam v12.1+ supports syslog servers in General Options) and Windows event logs to the SIEM.
- Cloud trails (CloudTrail, Azure Activity Log) into the SIEM with rules for the APIs above.
- SIEM rules with severity "page", routed to the security on-call, not only the backup team.

## Response playbook
Treat as a possible intrusion: verify with the person who made the change (out of band), lock accounts, check immutable copies are intact, preserve logs.

## Verify
Quarterly test: delete a test restore point and disable a test job; confirm the SIEM alert and the on-call page within minutes.
