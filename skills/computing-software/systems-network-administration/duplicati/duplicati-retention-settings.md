---
id: computing-software.systems-network-administration.duplicati.duplicati-retention-settings
name: duplicati-retention-settings
category: computing-software
field: systems-network-administration
product: duplicati
tags: [retention-policy, keep-versions, retention-buckets, smart-backup-retention, compact-process, delete-older-than]
level: practitioner
status: draft
description: "Configure Duplicati to delete old backup versions with a time limit, a version count or a bucketed retention policy such as the smart default."
sources: ["https://docs.duplicati.com/detailed-descriptions/configuration-and-management/retention-settings"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Duplicati retention settings

Stored data grows as new versions are added, so old versions need removal. Retention runs automatically at the end of each backup. After versions are deleted, Duplicati marks data that can no longer be referenced as waste and may occasionally compact, deleting unused volumes and writing new ones without waste. Duplicati never deletes the last version.

Three options:
- Delete older than: a period such as 7 days, 1 year or 5 years. Best for regular daily backups, for example keep three months.
- Keep versions: a count, for irregular backups triggered by external events, or when the source seldom changes (identical data does not create a new version).
- Retention policy: bucketed, in the format `bucket:interval`, comma separated. `7D:U,1Y:1W` means keep all backups (`U`, unlimited) for the newest 7 days, then one per week up to a year (roughly 52); anything older is deleted.

The UI default Smart backup retention is `1W:1D,4W:1W,12M:1M`: one backup per day for the last week, one per week for the last four weeks and one per month for the last twelve months. This resembles grandfather-father-son rotation. Bucket sizes use Duplicati's time format (for example D for days, W for weeks, M for months, Y for years).
