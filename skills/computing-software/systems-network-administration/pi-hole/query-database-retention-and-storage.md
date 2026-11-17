---
id: computing-software.systems-network-administration.pi-hole.query-database-retention-and-storage
name: query-database-retention-and-storage
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [maxdbdays, dbinterval, wal-mode]
level: advanced
status: docs-checked
description: "Control how long Pi-hole keeps queries, how often it writes them, and when to force disk storage or disable WAL."
sources: ["https://docs.pi-hole.net/ftldns/configfile/", "https://docs.pi-hole.net/database/query-database/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Query database retention and storage

FTL stores history in `/etc/pihole/pihole-FTL.db` (`files.database`).

| Option | Default | Meaning |
| --- | --- | --- |
| `database.maxDBdays` | `91` (configuration reference; the query database page says 365, so check the value on your install) | Days of queries to keep; `0` disables the database |
| `database.DBinterval` | `60` | Seconds between writes of queries to the database |
| `database.DBimport` | `true` | Load recent history from the database at startup |
| `database.useWAL` | `true` | Use Write-Ahead Log mode; leave on unless it causes problems, such as a database on a network share accessed from several hosts |
| `database.forceDisk` | `false` | Hold the history database on disk instead of in memory |

By default FTL uses an in-memory database for fast dashboard browsing. On systems with very limited RAM and occasional web use, `forceDisk` can help, but it reduces performance, especially on SD cards. The temporary database path is `files.tmp_db` (`/etc/pihole/pihole-tmp.db`), used only when `forceDisk` is true.

**Other files**

- `files.gravity`: `/etc/pihole/gravity.db`
- `files.macvendor`: `/etc/pihole/macvendor.db`

**Checklist**

1. Lower `maxDBdays` to save space.
2. Raise `DBinterval` to cut writes on flash storage.
3. Back up `pihole-FTL.db` before manual edits.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: FTL Configuration Reference (ftldns/configfile); Query Database (database/query-database). Nothing needed removing, but the two official pages disagree: the configuration reference gives `database.maxDBdays` default 91, the query database page says 365 days. The skill follows the reference and now says so.
Method: documentation only; no commands were run.
