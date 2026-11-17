---
id: computing-software.database-administration.postgresql.analyze-in-stages-after-upgrade
name: analyze-in-stages-after-upgrade
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-upgrade, major-version-upgrade, analyze-in-stages, vacuumdb, planner-statistics, post-upgrade, default-statistics-target]
level: practitioner
status: docs-checked
description: "Rebuild PostgreSQL planner statistics after pg_upgrade or a logical restore with vacuumdb --analyze-in-stages, so the first hours after cutover don't run on terrible plans."
sources:
  - https://www.postgresql.org/docs/18/app-vacuumdb.html
  - https://www.postgresql.org/docs/18/pgupgrade.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Statistics after an upgrade or restore

**Goal:** after pg_upgrade or a restore, the planner has usable statistics within
minutes, and complete ones soon after.

## Why
From PG18, pg_upgrade transfers most optimizer statistics (unless `--no-statistics`),
but not all of them, and the statistics of a release without that feature (or of a
restore that skipped them) must be rebuilt. Until ANALYZE runs, the planner works
from default estimates and can pick poor plans. Autovacuum will analyze eventually,
but not necessarily fast enough for production traffic.

## Command
```bash
vacuumdb --all --analyze-in-stages --jobs=8
```
Runs three stages: the first uses the lowest possible statistics target (see
`default_statistics_target`) to produce usable statistics faster, and the
later stages build the full statistics. Traffic can be let in after stage 1 if
the downtime budget is tight, and the remaining stages complete in the background.
`--analyze-only` (single full pass) is better when you can wait for it.
`--jobs` runs commands in parallel and increases the load on the server.

## PG18+
pg_upgrade transfers most optimizer statistics (not those from `CREATE STATISTICS`,
extension statistics or the cumulative statistics system). The upgrade docs say to run
`vacuumdb --all --analyze-in-stages --missing-stats-only` first, then
`vacuumdb --all --analyze-only` so cumulative statistics exist for triggering
vacuum and analyze; `--missing-stats-only` also stops stage 1 from replacing
existing statistics with lower-target ones. It needs SELECT on `pg_statistic` and
`pg_statistic_ext_data`, which are superuser-only by default.

## Gotchas
- Without `--missing-stats-only`, the early stages can temporarily replace existing
  statistics with lower-target ones and give transiently worse plans; don't
  benchmark until the last stage finishes.

## Verify
```sql
SELECT relname, last_analyze, last_autoanalyze FROM pg_stat_user_tables ORDER BY greatest(last_analyze,last_autoanalyze) NULLS FIRST LIMIT 20;
```
No large table without an analyze timestamp after the upgrade.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): vacuumdb reference (`--analyze-in-stages` runs three stages, the first with the lowest possible statistics target; `--missing-stats-only` semantics, privilege note and restriction to the analyze options; `--jobs`), pg_upgrade reference (statistics transfer from PG18, `--no-statistics`, the documented post-upgrade vacuumdb commands) and pg_dump reference (`--statistics-only`, `--no-statistics`). Removed unconfirmed details: per-stage targets beyond the first, the visibility-map VACUUM advice and the partitioned-table remark.
Method: documentation only; no commands were run.
