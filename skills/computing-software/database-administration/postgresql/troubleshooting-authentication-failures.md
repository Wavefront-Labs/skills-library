---
id: computing-software.database-administration.postgresql.troubleshooting-authentication-failures
name: troubleshooting-authentication-failures
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, client-authentication, pg-hba-conf, no-pg-hba-entry, authentication-failed, connection-refused, troubleshooting]
level: practitioner
status: verified
description: "Work out why a PostgreSQL login fails: connection refused, no pg_hba.conf entry, password or peer authentication failed, SSL off, role cannot log in."
sources:
  - https://www.postgresql.org/docs/current/client-authentication-problems.html
  - https://www.postgresql.org/docs/current/auth-pg-hba-conf.html
  - https://www.postgresql.org/docs/current/view-pg-hba-file-rules.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting authentication failures

The client message is deliberately vague; the **server log** has the detail
(`DETAIL: Connection matched file ".../pg_hba.conf" line 98: "host all all 0.0.0.0/0 scram-sha-256"`).
Always read it first.

## Error -> cause
| Client sees | Meaning | Fix |
|---|---|---|
| `connection to server at "host", port N failed: Connection refused` + `Is the server running on that host and accepting TCP/IP connections?` | nothing listening on that address:port | `listen_addresses = '*'` (restart), firewall/security group, right port |
| `timeout expired` | packets dropped (firewall, wrong IP) | network path, not PostgreSQL |
| `no pg_hba.conf entry for host "10.1.2.3", user "app", database "db", no encryption` | no line matched this (type, db, user, address) | add a line; note **"no encryption"**: a `hostssl`-only rule will not match a non-TLS attempt |
| `password authentication failed for user "app"` | wrong password, **or role does not exist**, or role has no password, or password `VALID UNTIL` passed | check `\du app`; reset with `\password app` |
| `Peer authentication failed for user "app"` | local socket + `peer` method, OS user name differs from DB role | connect with `-h localhost` (TCP rule), or map with pg_ident.conf |
| `role "app" is not permitted to log in` | role lacks `LOGIN` | `ALTER ROLE app LOGIN;` |
| `database "x" does not exist` | auth passed; db name wrong (defaults to user name) | pass `-d` |
| `too many connections for role "app"` | `CONNECTION LIMIT` | raise limit or pool |
| `FATAL: sorry, too many clients already` | `max_connections` exhausted | pool (PgBouncer), find idle sessions |
| `SCRAM authentication requires libpq version 10 or above` | old driver | upgrade client library |

## Checking the rules the server is actually using
```sql
SELECT line_number, type, database, user_name, address, netmask, auth_method, error
FROM pg_hba_file_rules ORDER BY line_number;
SHOW hba_file;
```
The file is read **top to bottom, first match wins, no fall-through**: a `reject` or a
`peer` line above your new rule wins even if auth then fails. Edits need
`SELECT pg_reload_conf();`, and `pg_hba_file_rules` shows parse errors before you reload.

## Password state
```sql
SELECT rolname, rolcanlogin, rolvaliduntil, rolpassword IS NOT NULL AS has_pw,
       left(rolpassword, 14) AS pw_type      -- needs superuser; 'SCRAM-SHA-256$' or 'md5...'
FROM pg_authid WHERE rolname = 'app';
```
A role whose password is stored as md5 cannot log in through a `scram-sha-256` rule; reset the
password with `password_encryption = 'scram-sha-256'` in effect.

## Gotchas
- Behind PgBouncer or a cloud proxy the server sees the proxy IP, not the client.
- `localhost` may resolve to `::1`; add both `127.0.0.1/32` and `::1/128` rules.
- Connection strings with `sslmode=disable` never match `hostssl` lines.

## Verify
`psql "host=... dbname=... user=... sslmode=require" -c 'select current_user, inet_server_addr()'`
succeeds, and the server log shows `connection authorized: user=app database=db application_name=psql` followed by ` SSL enabled (protocol=..., cipher=..., bits=...)`
(with `log_connections` including `authorization`; `on` still works).

## Checked
- PostgreSQL 18.6 (Windows, TCP rules only): each client message was reproduced: `role "nologin" is not permitted to log in`; `too many connections for role "lim"` (`CONNECTION LIMIT 0`); `password authentication failed for user "expired"` (`VALID UNTIL` in the past), `"nopw"` (log detail `User "nopw" has no password assigned.`) and `"ghost"` (log detail `Role "ghost" does not exist.`), each with `DETAIL: Connection matched file "...pg_hba.conf" line N: "<line>"`; `database "nodb" does not exist`; `Connection refused (0x0000274D/10061)` with `Is the server running on that host and accepting TCP/IP connections?` (the libpq text now starts `connection to server at "127.0.0.1", port N failed`); `no pg_hba.conf entry for host "127.0.0.1", user "lim", database "postgres", no encryption` when only a `hostssl` line existed for that address; a role with an md5 verifier was refused by a `scram-sha-256` line. `pg_hba_file_rules` and the pg_authid password-state query (`left(rolpassword, 14)`) ran; `log_connections = 'on'` logged `connection authorized: user=postgres database=postgres application_name=psql`. `sslmode=require` against this non-TLS server failed `server does not support SSL, but SSL was required`.
- Source (postgres REL_18_STABLE and REL9_6_STABLE on GitHub): `timeout expired` (libpq fe-misc.c), `sorry, too many clients already` (proc.c), `Peer authentication failed for user "%s"` (auth.c), `role "%s" is not permitted to log in` (miscinit.c), `connection authorized: user=%s` and ` SSL enabled (protocol=%s, cipher=%s, bits=%d)` (postinit.c), `SCRAM authentication requires libpq version 10 or above` (9.6 libpq only).
- Docs-only, not run (no Unix sockets, no old libpq, no TLS here): the Peer authentication row, the SCRAM libpq row, `sslmode=disable` never matching `hostssl`.
