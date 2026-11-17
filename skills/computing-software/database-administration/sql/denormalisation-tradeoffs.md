---
id: computing-software.database-administration.sql.denormalisation-tradeoffs
name: denormalisation-tradeoffs
category: computing-software
field: database-administration
product: sql
tags: [sql, denormalisation-tradeoffs]
level: advanced
status: draft
description: "Denormalise deliberately for read performance while keeping a source of truth."
sources: ["https://www.postgresql.org/docs/current/", "https://www.sqlite.org/lang.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# When and how to denormalise

- Start normalised (3NF); denormalise only with measured read cost: summary tables, counters, copied columns.
- Keep derived data consistent via triggers, generated columns, materialised views or application writes in one transaction.
- Document which table is authoritative and how drift is detected (a reconciliation query).
- Avoid storing arrays or delimited lists of ids where joins are needed.
- Self-check: a periodic query comparing derived to computed values returns zero rows.
