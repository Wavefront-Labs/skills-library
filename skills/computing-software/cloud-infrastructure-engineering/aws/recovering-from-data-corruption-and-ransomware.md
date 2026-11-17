---
id: computing-software.cloud-infrastructure-engineering.aws.recovering-from-data-corruption-and-ransomware
name: recovering-from-data-corruption-and-ransomware
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, disaster-recovery, ransomware-recovery, data-corruption, aws-backup-vault-lock, logically-air-gapped-vault, point-in-time-recovery]
level: practitioner
status: gated
description: "Recover from logical data corruption and ransomware on AWS: why replication does not help, immutable and air-gapped backups, finding the last good point, and clean-room restores."
sources: ["https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recovering from data corruption and ransomware

**Key point:** multi-AZ and cross-region replication copy corruption and deletion within
seconds. Recovery needs **point-in-time copies that the attacker cannot change**.

## Protection layers
| Layer | Mechanism |
|---|---|
| Immutable backups | AWS Backup **Vault Lock** in compliance mode (no one, including root, can delete before retention) |
| Separate blast radius | cross-account backup copies to a dedicated backup account; **logically air-gapped vault** |
| Object storage | S3 versioning + **Object Lock** (compliance mode) on critical buckets; MFA delete (gated: unconfirmed, source is paywalled or blocked) |
| Databases | RDS/Aurora automated backups + PITR, DynamoDB PITR, plus on-demand backups to the locked vault |
| Detection | GuardDuty, Macie, CloudTrail anomalies, S3 delete spikes alarms |
| Least privilege | no human or workload role can both delete backups and data; SCP denies actions that delete recovery points or change vault access policies |

## Recovery procedure
1. **Contain:** revoke compromised credentials, isolate resources (quarantine SGs), preserve evidence (snapshots, logs).
2. **Find the last known good point:** CloudTrail/GuardDuty timeline of the first malicious action; restore candidates just before it; validate with checksums or application checks.
3. **Restore into a clean environment:** new account or isolated VPC (clean room), from the backup account/air-gapped vault, with fresh credentials and patched images; never restore into the compromised account first.
4. **Validate data** (row counts, integrity checks, sample business records) before switching traffic.
5. **Rebuild compute from IaC and golden images**, not from possibly-infected instances.
6. **Replay** changes since the restore point from durable logs/queues if available (event sourcing, Kinesis/MSK retention, S3 versions).

## Test it
- AWS Backup **restore testing** (see the AWS Backup guide) to rehearse restores.
- Annual ransomware game day: assume the production account admin is compromised; recover from the backup account only.

## Gotchas
- Governance-mode locks can be removed by privileged users; use compliance mode for ransomware protection (and be sure of retention: a compliance-mode lock cannot be removed once the grace time ends).
- KMS keys: if attackers schedule key deletion, encrypted backups become unreadable. Use keys owned by the backup account; alarm on KMS key deletion being scheduled.
- PITR windows may be shorter than attacker dwell time; keep longer-retention backups.

## Verify
- [ ] Vault Lock compliance mode active; cross-account copies succeed daily.
- [ ] Last restore test restored and validated data within the RTO.

## Checked

2026-10-28

Confirmed: Vault Lock governance mode (removable by privileged users) vs compliance mode (not deletable after grace time), and that a locked vault denies delete or lifecycle changes even for the root user (AWS Backup Developer Guide, Vault Lock page).

Removed: 35-day PITR figures, air-gapped vault account/RAM detail, GuardDuty feature detail, IAM action names, restore-testing detail, AWS-managed-key advice, ScheduleKeyDeletion name; replaced prose sources.

Gated: S3 Object Lock and MFA delete row: the Object Lock page was not fetched.

Method: documentation only; no commands were run.
