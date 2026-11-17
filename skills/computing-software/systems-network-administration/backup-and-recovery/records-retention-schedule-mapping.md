---
id: computing-software.systems-network-administration.backup-and-recovery.records-retention-schedule-mapping
name: records-retention-schedule-mapping
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [records-retention-schedule, retention-policy, records-management, data-retention, compliance, backup-retention]
level: practitioner
status: draft
description: "Map an organisation's records retention schedule onto backup and archive retention: record classes, legal minimums and maximums, backups vs archives, and defensible deletion."
sources:
  - https://www.archives.gov/records-mgmt/grs
  - https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mapping the records retention schedule to backups

**Goal:** backup and archive retention that satisfies legal minimums without keeping personal data longer than allowed.

## Know the difference
- **Records retention schedule** (owned by records/legal): how long each *record class* must be kept, and when it must be destroyed. Example classes: financial transactions 7 years, HR files employment + 6 years, CCTV 30 days.
- **Backups** exist for operational recovery. They are not the system of record; long backup retention is not a substitute for archiving.
- **Archives** hold records for their retention period in a searchable, managed store.

## Mapping steps
1. Get the current schedule (in the US federal space, NARA General Records Schedules plus agency schedules; elsewhere the legal/records team).
2. For each system, list which record classes it holds.
3. Choose:
   - Operational backup retention: driven by RPO and detection window (e.g. 30-90 days daily, 12 monthlies).
   - Archive: records with multi-year retention go to an archive/WORM tier with per-record lifecycle, not 7-year backups of the whole VM.
4. Check **maximums**: GDPR storage limitation and schedules that say "destroy after". Backups holding data past the limit need justification (documented in the RoPA) or shorter retention.
5. Document the mapping table: system, record classes, backup retention, archive location/retention, deletion method, legal hold process.

## Gotchas
- Erasure requests: you usually cannot edit backups; document that restored data is re-scrubbed against a deletion log before use.
- "Keep everything forever" is an e-discovery liability.
- Legal hold suspends deletion for affected data only; it should not freeze all expiry.

## Verify
Records/legal sign the mapping; backup job retention settings and archive lifecycle rules match it on spot-check.
