---
id: computing-software.systems-network-administration.backup-and-recovery.legal-hold-and-regulatory-retention
name: legal-hold-and-regulatory-retention
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [legal-hold, regulatory-retention, s3-object-lock, worm, ediscovery, retention-policy, backup-vs-archive]
level: advanced
status: docs-checked
description: "Apply legal holds and regulatory retention to backup and archive data: scoping, suspending deletion, Object Lock legal holds, mailbox holds, release and review."
sources:
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html
  - https://learn.microsoft.com/en-us/purview/ediscovery-create-a-litigation-hold
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Legal hold and regulatory retention

**Goal:** preserve data that law or litigation requires, without keeping all backups forever.

## Legal hold
A legal hold suspends normal deletion for data relevant to actual or anticipated litigation or investigation, on instruction from legal counsel.
1. **Scope** with counsel: custodians, systems, date ranges, data types.
2. **Preserve at the source first** (for example mailbox Litigation Hold, or application-level holds). Backups are a fallback.
   - Exchange Server Litigation Hold (Microsoft documents it for Exchange 2016, 2019 and Subscription Edition) preserves all mailbox content including deleted items and original versions of modified items, and also holds the archive mailbox if enabled. It can take up to 60 minutes to take effect, holds items indefinitely unless you set a duration in days, and preserves items in the Recoverable Items folder (default size 30 GB), so monitor held mailboxes weekly against quota.
3. If backups must be preserved: copy the relevant restore points to a separate repository or tag them so retention does not expire them.
   - S3 Object Lock legal hold: a legal hold gives the same protection as a retention period but has no expiry; it stays until explicitly removed, is placed on individual object versions, is independent of retention periods, and can be placed or removed by any user with the `s3:PutObjectLegalHold` permission. Example: `aws s3api put-object-legal-hold --bucket <BUCKET> --key <KEY> --legal-hold Status=ON`
   - Check your backup tool's documentation for a per-restore-point "keep" or "exclude from retention" feature.
4. **Document**: hold notice, scope, what was preserved where, who has access (chain of custody).
5. **Release** only on written instruction; then return data to normal retention.

## Regulatory retention
- Map each regulation to data types and periods. Get the list from compliance/legal, not from IT guesses.
- S3 Object Lock uses a write-once-read-many (WORM) model and AWS says it has been assessed by Cohasset Associates for SEC 17a-4, CFTC and FINRA environments. In compliance mode no user, including the account root user, can delete or overwrite a protected version or shorten its period; governance mode can be bypassed by users with `s3:BypassGovernanceRetention`.
- Backups are not archives: restoring an old full system backup to find one record is slow and costly. Consider an indexed archive for long retention and keep backup retention short.
- Conflicting obligations (privacy minimisation vs retention) need a documented legal decision.

## Gotchas
- Holds on repositories with immutability can block legitimate deletion; track hold scope precisely.
- Forgotten holds become indefinite retention; review open holds regularly with counsel.

## Verify
For each open hold, you can show the preserved data, its location, access log and the instruction that created it.

## Checked

2026-11-09. Confirmed against the S3 Object Lock page (WORM, retention vs legal hold, `s3:PutObjectLegalHold`, compliance/governance modes, Cohasset assessment) and the Microsoft "Place a mailbox on Litigation Hold" page (applies to Exchange Server; 60 minutes, duration, Recoverable Items 30 GB default, archive mailbox). Partial read of both pages. The `put-object-legal-hold` command is checked by tools/review/check_commands.py in this batch. Removed: Google Vault and Microsoft 365 hold claims, specific SEC Rule 17a-4 audit-trail requirements and broker-dealer detail (SEC page was blocked, so unconfirmed), healthcare and tax period claims.

Method: documentation only; no commands were run.
