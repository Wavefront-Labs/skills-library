---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.backups-vs-archives
name: backups-vs-archives
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [backups-vs-archives, archive-strategy, data-integrity, backup-strategy, object-lock, retention]
level: practitioner
status: docs-checked
description: "Separate backups (for fast recovery, RTO-driven) from archives (long-term retention for compliance), and design retention, storage class and immutability for each."
sources: ["https://sre.google/sre-book/data-integrity/", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html", "https://cloud.google.com/storage/docs/storage-classes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backups vs archives

SRE Book "Data Integrity": the most important difference is that backups can be loaded back into an
application, while archives cannot. **Archives** safekeep data for long periods to meet auditing, discovery
and compliance needs; recovery generally need not complete within the service's uptime requirements (the
book's example: seven years of financial data, where a week to retrieve logs during an audit may be
acceptable). **Backups** exist so data can be recovered quickly, preferably well within the service's uptime
needs. "No one really wants to make backups; what people really want are restores."

## Compare
| | Backup | Archive |
|---|---|---|
| Purpose | recover service after loss/corruption | retain records for auditing, discovery, compliance |
| Driven by | how quickly you must recover and how much recent data you can lose (RTO, RPO) | retention policy, regulation |
| Schedule | the most recent data is at risk until backed up: daily, hourly or more often, full plus incremental or streaming | for example moved to long-term offsite storage periodically |
| Restore speed | quick, tested | slower is acceptable |
| Storage | tiered: fastest and most local first, nearline or offline later | long-term storage classes |
| Immutability | protect copies from deletion | WORM / legal hold where required |

## Backup design (SRE Book, "Second Layer: Backups")
- Let the recovery scenarios drive: which methods, how often to take full or incremental backups, where to
  store them and how long to retain them.
- The less recent data you can afford to lose, the more serious you should be about incremental backups;
  frequent fulls load the live datastore, so take fulls off-peak and incrementals when busy.
- The faster users must be rescued, the more local the backup. A tiered strategy keeps quick-to-restore
  copies close for a short time, and moves later copies to nearline or offsite storage that protects against site-level failures.
- Backups can be replicated or staggered across independent sites so a lost backup does not defeat recovery.
- Restore tests are part of the backup (see `restore-drills-and-restore-slos`).

## Archive design
- S3 Object Lock uses a write-once-read-many (WORM) model, with retention periods and legal holds. In
  compliance mode no user, including the root user, can overwrite or delete a protected version, and the retention mode
  and period cannot be shortened. Governance mode lets users with special permission change settings, and
  the S3 documentation says you can use it to test retention settings first.
- Google Cloud Storage's Archive class is documented for archiving, online backup and disaster recovery,
  with data available within milliseconds and a 365-day minimum storage duration. So class names do not by
  themselves tell you retrieval time: read each provider's documentation.
- Store schema or format documentation with the data so it can be read later.

## Gotchas
- Using archives as backups: check the actual retrieval time against your recovery objective.
- Using backups as archives: rotating retention deletes data you may be required to keep.
- Compliance-mode locks cannot be shortened even by root; test with governance mode first.
- Deletion requests (privacy law) vs immutable archives: design for it up front and ask your legal team.

## Verify
- [ ] Each dataset has documented recovery objectives (backup) and retention period (archive), separately.
- [ ] Archive readability test: restore and parse a year-old archive.

## Checked
2026-11-01. Confirmed against the SRE Book "Data Integrity" chapter (backups versus archives, backup
scheduling, tiering, replication), the S3 Object Lock page (WORM, legal holds, compliance versus
governance mode) and the Cloud Storage storage-classes page (Archive class access and minimum duration).
Removed: the AWS CLI example, the 12-48 h retrieval claim (contradicted by Cloud Storage Archive), named cold tiers
of other vendors, the 7-year lock and 30-day lifecycle example, format recommendations and the
copy-in-another-account advice (no fetched page states them).
Method: documentation only; no commands were run.
