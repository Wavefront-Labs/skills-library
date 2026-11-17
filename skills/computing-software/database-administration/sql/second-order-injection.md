---
id: computing-software.database-administration.sql.second-order-injection
name: second-order-injection
category: computing-software
field: database-administration
product: sql
tags: [sql, second-order-injection]
level: advanced
status: draft
description: "Find injection where stored data is reused in later queries."
sources: ["https://www.postgresql.org/docs/current/", "https://www.sqlite.org/lang.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Second-order and stored injection

- Data inserted safely (parameterised) but later concatenated into SQL, reports or dynamic SQL is still exploitable.
- Treat database values as untrusted when building queries; parameterise everywhere including admin tools and ETL.
- Review stored procedures that use `EXECUTE` or `sp_executesql` with string building.
- Defensive checks: static analysis (semgrep rules), least-privilege roles, query logging for anomalies.
- Self-check: grep for string-built SQL in jobs, not only request handlers.
