---
id: computing-software.database-administration.sql.audit-log-triggers
name: audit-log-triggers
category: computing-software
field: database-administration
product: sql
tags: [sql, audit-log-triggers]
level: advanced
status: docs-checked
description: "Record row changes in a PostgreSQL audit table with an AFTER row trigger, using to_jsonb(OLD/NEW), TG_OP, current_user and a SET LOCAL session variable."
sources: ["https://www.postgresql.org/docs/current/plpgsql-trigger.html", "https://www.postgresql.org/docs/current/sql-createtrigger.html", "https://www.postgresql.org/docs/current/functions-json.html", "https://www.postgresql.org/docs/current/functions-info.html", "https://www.postgresql.org/docs/current/sql-set.html", "https://www.postgresql.org/docs/current/runtime-config-custom.html", "https://www.postgresql.org/docs/current/functions-admin.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audit and history tables via triggers

- Use an `AFTER INSERT OR UPDATE OR DELETE ... FOR EACH ROW` trigger: an AFTER trigger sees all changes, including those made by other triggers.
- In the PL/pgSQL trigger function, `TG_OP` and `TG_TABLE_NAME` give the operation and table; `NEW` is null for DELETE and `OLD` is null for INSERT.
- Store the rows with `to_jsonb(OLD)` and `to_jsonb(NEW)` (`to_jsonb` turns a composite value into a JSON object).
- `current_user` is the effective user; `session_user` is the session user's name.
- To record an application user, set a two-part custom setting with `SET LOCAL app.user_name = '...'` (it lasts until the end of the transaction) and read it with `current_setting('app.user_name', true)`; the second argument avoids an error when the setting is missing.
- Avoid `app.user` as the name: `USER` is a reserved key word.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
Read: the PL/pgSQL trigger page (NEW/OLD, TG_* variables, the audit example), CREATE TRIGGER (AFTER semantics), the to_jsonb entry on the JSON functions page, current_user/session_user on the system information page, SET LOCAL, custom options, and current_setting on the admin functions page (searched for the specific entries, not read end to end).
Corrected: the setting name `app.user` became `app.user_name`, because USER is reserved (key words appendix). Trimmed: the unsourced advice about trigger cost and partitioning or pruning the audit table, and the self-check.
