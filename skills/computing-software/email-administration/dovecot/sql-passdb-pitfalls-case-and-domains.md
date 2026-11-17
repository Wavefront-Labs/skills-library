---
id: computing-software.email-administration.dovecot.sql-passdb-pitfalls-case-and-domains
name: sql-passdb-pitfalls-case-and-domains
category: computing-software
field: email-administration
product: dovecot
tags: [sql-case-sensitivity, username-return, extra-fields, virtual-domain, mysql-collation, user-at-domain]
level: practitioner
status: docs-checked
description: "Avoid two common SQL passdb mistakes: case-insensitive usernames from MySQL and returning only the user part so the domain is lost."
sources:
  - https://doc.dovecot.org/main/core/config/auth/databases/sql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two recurring SQL problems come from what the query returns, not from the query syntax.

Case mismatch. MySQL compares strings case-insensitively by default, so users may log in as `user`, `User` and `uSer`. The fix is to have the database return a `user` extra field, which makes Dovecot modify the username to the returned value.

Lost domain. If your table has separate user and domain columns and the query returns only the user column, Dovecot drops the domain from the username. Return either a concatenated `user@domain` string or the `username` and `domain` fields separately. Remember the `concat` filter rule for building the value when you filter on it, because bind parameters cannot be embedded inside quoted strings.

The passdb query must return a field named `password`; use SQL `AS` if the column has another name. Other returned fields can be passdb extra fields with special meaning.

Keep the table's password column in a single format and set `passdb_default_password_scheme`, or prefix each value with `{scheme}`. When all SQL settings for passdb and userdb are equal, only one SQL connection is used for both.

## Checked
2026-11-09. Read the Dovecot SQL authentication database page (main documentation) in full. Confirmed: MySQL
case-insensitive comparison and the `user` extra field fix, the lost-domain problem and the user@domain or
username/domain fix, the concat filter and bind-parameter rule, the `password` field and `AS`, scheme prefix and
`passdb_default_password_scheme`, and the shared connection. Removed as unconfirmed: cache and mail-path splitting, the
userdb advice, `nologin`/`nodelay` examples, and the second-connection inference.
Method: documentation only; no commands were run.
