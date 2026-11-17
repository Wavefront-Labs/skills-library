---
id: computing-software.database-administration.postgresql.pg-hba-record-matching-order
name: pg-hba-record-matching-order
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, pg-hba-conf, client-authentication, pg-hba-file-rules, hostssl, access-control]
level: practitioner
status: verified
description: "Lay out pg_hba.conf so first-match-wins ordering does what you intend, using include files, groups (+role), @files and pg_hba_file_rules to check it."
sources:
  - https://www.postgresql.org/docs/current/auth-pg-hba-conf.html
  - https://www.postgresql.org/docs/current/view-pg-hba-file-rules.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pg_hba.conf record matching order

## The rule
For each connection, PostgreSQL scans records **top to bottom** and uses the **first record
whose connection type, database, user and address all match**. The auth method of that
record is final: if it fails there is no fall-through to later lines.

## Fields
```
# TYPE     DATABASE      USER          ADDRESS          METHOD          [OPTIONS]
local      all           postgres                       peer
hostssl    app           +app_users    10.0.0.0/16      scram-sha-256
hostnossl  all           all           0.0.0.0/0        reject
host       replication   replicator    10.0.5.0/24      scram-sha-256
```
- TYPE: `local` (Unix socket), `host` (TCP, TLS or not), `hostssl`, `hostnossl`,
  `hostgssenc`, `hostnogssenc`.
- DATABASE: name, `all`, `sameuser`, `samerole`, `replication` (physical replication only;
  logical replication connections match normal database names), `@file` list,
  or regex `/^tenant_` (PG16+).
- USER: name, `all`, `+group` (members of the role, including indirect), `@file`, regex.
- ADDRESS: CIDR, hostname (reverse+forward DNS checked, slow), `samehost`, `samenet`.

## A layout that stays correct
1. Local superuser/admin access (`peer`) first, so you cannot lock yourself out.
2. Explicit `reject` lines for things that must never happen (e.g. `postgres` over TCP).
3. Replication lines.
4. Application rules, most specific first, using `+role` groups instead of per-user lines.
5. `hostnossl all all 0.0.0.0/0 reject` near the end to force TLS.
6. Nothing permissive at the bottom; unmatched connections are rejected anyway.

PG16+ supports `include`, `include_if_exists` and `include_dir` in pg_hba.conf, so
generated per-tenant rules can live in a separate file that config management owns.

## Check before reloading
```sql
SELECT line_number, type, database, user_name, address, auth_method, options, error
FROM pg_hba_file_rules;           -- what the file parses to right now, with errors
SELECT pg_reload_conf();          -- only after error column is empty
```
On Unix, a file with errors is **not** loaded on reload (the postmaster keeps the old rules).
A broken file at startup stops the server: `FATAL: could not load .../pg_hba.conf`. On **Windows** every
new connection re-reads the file (docs), and with a bad line new logins failed with that same FATAL until it was fixed.

## Gotchas
- `host` matches both TLS and non-TLS; to force TLS for a range, put `hostssl ... scram`
  and a `hostnossl ... reject` for the same range.
- `trust` anywhere on TCP is a full bypass; never use it outside `local` on a dev box.

## Verify
Test each class of client (app, replica, admin, an outside address). A failed login logs
`DETAIL: Connection matched file ".../pg_hba.conf" line N: "<the line>"`; with `log_connections`
including `authentication`, a successful one logs `connection authenticated: identity="u" method=scram-sha-256 (.../pg_hba.conf:N)`.

## Checked
- PostgreSQL 18.6 (Windows): a file with a `reject` rule, a regex database rule (`/^tenant_.*`), md5 and SCRAM user lines, `replication`, `samehost` and CIDR lines parsed cleanly in `pg_hba_file_rules`; connecting as the reject user failed with `pg_hba.conf rejects connection for host "127.0.0.1", user "reject_me", database "postgres", no encryption`; with only `hostssl` plus a non-matching user the error was `no pg_hba.conf entry for host "127.0.0.1", user "lim", database "postgres", no encryption`; a SCRAM line refused a role holding an md5 verifier and logged `Connection matched file ... line 4: "host all scramuser 127.0.0.1/32 scram-sha-256"`; an md5 line accepted a role with a SCRAM verifier; success logged `connection authenticated: identity="md5user" method=md5 (.../pg_hba.conf:3)`. An invalid method (`scramx`) showed in `pg_hba_file_rules.error`, on reload new connections failed (`could not load`) on Windows, and the same file at startup made the server refuse to start.
- Docs (auth-pg-hba-conf): first match, no fall-through; `replication` matches physical only; `+` = directly or indirectly members; `samehost`/`samenet`; hostname reverse+forward lookup; `/regex` for database and user; `hostgssenc`/`hostnogssenc`; the Windows note about immediate re-read; PG16 release notes: `include`, `include_if_exists`, `include_dir` and regex tokens.
- Checked from the docs only, not run (Windows has no Unix sockets and this server had no TLS): `local`/`peer` lines and `hostssl`/`hostnossl` matching (auth-peer and auth-pg-hba-conf pages).
