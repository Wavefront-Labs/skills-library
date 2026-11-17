---
id: computing-software.data-engineering.metabase.database-sync-and-scan
name: database-sync-and-scan
category: computing-software
field: data-engineering
product: metabase
tags: [sync, scan, fingerprinting, refingerprint, field-values, hidden-tables]
level: practitioner
status: docs-checked
description: "Understand and schedule Metabase database sync, scan and fingerprinting: what each reads, default frequencies, setting locations, manual triggers and 14-day behaviour."
sources:
  - https://www.metabase.com/docs/latest/databases/sync-scan
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three jobs:
- **Sync** reads table and view names, column names, data types and primary and foreign keys, and deactivates deleted tables. Hourly by default and cannot be turned off.
- **Scan** caches distinct column values for filter dropdowns: the first 1,000 distinct values per column in ascending order, caching only the first 100 KB of text (so long values such as addresses may yield fewer than 1,000 cached values). Daily by default.
- **Fingerprinting** samples the first 10,000 rows of each table for statistics (distinct counts, min and max, null ratios). It runs only on first connection unless periodic refingerprinting is enabled, which adds database load.

Settings: Admin, Databases, your database, Connection and sync, Edit connection details, Show advanced options, "Choose when syncs and scans happen". Sync frequency is hourly or daily at a time in the server timezone. Scan runs on a schedule, only when a filter widget is added, or never. "Periodically refingerprint tables" is off by default.

Manual triggers: Admin, Databases, "Sync database schema"; Table Metadata gear menu for "Re-scan this table/field" or "Discard cached field values"; API endpoints for sync, rescan and notify (the notify endpoint needs the `MB_API_KEY` environment variable, which differs from standard API keys).

Gotchas:
- Only fields used in the last 14 days are scanned, and cached values last 14 days.
- Hidden tables skip syncs and scans and vanish from the query builder but stay queryable in SQL.
- If someone types in a filter search box for values outside the cached first 1,000 distinct values or 100 KB, Metabase queries the database on the fly.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Corrected the 100 KB cache cap and the live-query condition to match the page. Otherwise unchanged.
