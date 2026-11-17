---
id: computing-software.systems-network-administration.backup-and-recovery.immutability-period-planning
name: immutability-period-planning
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [immutability-period, retention, object-lock, hardened-repository]
level: practitioner
status: docs-checked
description: "Plan immutability periods: how the Veeam hardened repository counts the lock, S3 Object Lock governance vs compliance modes, timeshift protection."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/hardened_repository_immutability.html
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Immutability period planning

## Inputs to decide
- How long it takes you to detect an attack, plus margin: the lock has to outlast it. Estimate this from your own monitoring, not a generic figure.
- Retention: data stays until its lock expires, so the lock cannot exceed what you are willing to store.
- Compliance: regulated records may need WORM storage for the full retention period.

## Veeam hardened repository (Linux)
- Backup files become immutable for the configured period: minimum 7 days.
- For image-level VM and physical machine backups, the period is counted from the moment the last restore point in the active chain is created, and it is extended automatically for all files in the active chain. Inactive chains are not extended. Veeam's example: a 10-day period with the last restore point on 14 January keeps the files immutable until 24 January.
- The Veeam Immutability Service checks file attributes every 20 minutes and sets or removes the immutable attribute.
- Timeshift detection guards against clock tampering: if the detected shift exceeds 86400 seconds (24 hours), retention operations are blocked with a warning in the job session. Shutting the repository down for more than 24 hours also blocks retention operations, and while blocked the service neither sets nor removes the immutable attribute on existing or new files. For precise detection, set the RTC to UTC. A Reset time shift protection option exists in the Host configuration menu of the Veeam Host Management console on a Hardened Repository or Software Appliance.
- Veeam states this architecture prevents deletion or modification even if an attacker compromises the Data Mover service or the NTP server.

## S3 Object Lock modes
- Governance mode: users with `s3:BypassGovernanceRetention` can bypass it, so it is weaker.
- Compliance mode: no user, including the account root user, can delete or overwrite a protected version or shorten its period.
- A legal hold is separate from retention periods and has no expiry.
- A longer compliance period costs storage for the whole period if set wrongly; trial settings in governance mode first.

## Gotchas
- Immutability stops deletion, not backing up data that is already encrypted; detection and enough history still matter.
- Forecast capacity with lock overlap included (locked data cannot be freed early).

## Verify
Try to delete the newest and oldest locked points: deletion is refused until expiry, and capacity forecasts include the lock overlap.

## Checked

2026-11-09. Confirmed against Veeam "How Immutability Works" (minimum 7 days, counting from last restore point of the active chain, extension and 10-day example, 20-minute check, timeshift detection, 24-hour blocks, RTC to UTC, reset option) and the S3 Object Lock page (modes, root user, bypass permission, legal hold). Partial read of the Veeam page (image-level section; the "maximum 9999" value and other backup types were not relied on). Removed: CISA source (403), dwell time of "days to weeks", the retention and immutability table, GFS locking claim, Veeam object storage block-generation padding of 10 days, 20-30% headroom advice and NTP authentication advice.

Method: documentation only; no commands were run.
