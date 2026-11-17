---
id: computing-software.email-administration.dovecot.sql-passdb-query-bind-parameters
name: sql-passdb-query-bind-parameters
category: computing-software
field: email-administration
product: dovecot
tags: [sql-passdb, passdb-sql-query, bind-parameters, concat-filter, sql-injection, userdb-sql-iterate-query]
level: advanced
status: docs-checked
description: "Write passdb_sql_query and userdb queries safely: variables become bind parameters, quoting rules, the concat filter, and constructs Dovecot rejects."
sources:
  - https://doc.dovecot.org/main/core/config/auth/databases/sql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Auth SQL queries (`passdb_sql_query`, `userdb_sql_query`, `userdb_sql_iterate_query`) can use any settings variable such as `%{user}`. Dovecot never pastes the value into the SQL text. Each `%{variable}` becomes a bind parameter sent separately, so a value cannot change the query structure and there is no injection risk or need to escape. Debug logs show values filled in, but `%{password}` stays hidden unless `auth_debug_passwords = yes`.

Because each variable is exactly one bind parameter, it must stand for one whole SQL value:
- Use it bare (`userid = %{user}`) or in single quotes (`'%{user}'`); both mean the same. Double quotes are not accepted.
- Never mix it with other text inside quotes. Build the value with the `concat` filter instead, for example `%{user | username | concat('@example.com')}` or `%{user | concat('%')}` for a LIKE prefix. The filter works on every database, unlike `CONCAT()` (SQLite has it only from 3.44; Cassandra has none).
- Other filters such as `%{user | lower}` apply before binding.

Queries fail with an error if they contain SQL comments outside strings, a literal `?` outside a string (including PostgreSQL jsonb operators), dollar-quoted strings or `$1` parameters, or a backslash inside single quotes (write `''`).

The passdb query must return a field named `password` (use `AS`). Without `passdb_default_password_scheme`, prefix each stored value with `{scheme}`. Only one statement is allowed per query, but a stored procedure works. If all passdb and userdb SQL settings are equal, one connection is shared.

## Checked
2026-11-09. Read the Dovecot SQL authentication database page (main documentation) in full. Confirmed each statement:
bind parameters, quoting rules, the concat filter and its portability note, filters applied before binding, the four
rejected constructs, the `password` field with `AS`, scheme prefix, single statement with stored procedure, and the
shared connection. Nothing removed.
Method: documentation only; no commands were run.
