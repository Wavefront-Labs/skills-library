---
id: computing-software.database-administration.pgbouncer.hba-file-format
name: hba-file-format
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, hba, auth-hba-file, peer, pg-hba]
level: advanced
status: docs-checked
description: "auth_type hba and auth_hba_file: supported record types, field support and unsupported pg_hba.conf features."
sources:
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write an HBA file PgBouncer accepts.

Set `auth_type = hba` and `auth_hba_file = /path/to/hba.conf`. The file follows the PostgreSQL pg_hba.conf format with these supports:

- Record types: local, host, hostssl, hostnossl.
- Database field: all, replication, sameuser, @file, multiple names. Not supported: samerole, samegroup.
- User field: all, @file, multiple names. Not supported: +groupname.
- Address field: all, IPv4, IPv6. Not supported: samehost, samenet, DNS names, domain prefixes.
- Auth-method field: only methods supported by PgBouncer's auth_type, plus peer and reject. The methods any and pam work only globally, not in the HBA file.
- The user name map (`map=`) parameter is supported when the method is cert or peer.

Example intent: Unix-socket connections use peer, TCP connections must use TLS.

RELOAD re-reads auth_hba_file along with the main config.

Ident maps: `auth_ident_file` is loaded only when auth_type is hba and a user map is defined. Lines are only `map-name system-username database-username`. No include directives. The system-username field cannot be a regular expression. The database-username field accepts `all` or a single Postgres user name; +groupname and regular expressions are unsupported.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: an unstated claim that auth_file is still needed.

Method: documentation only; no commands were run.
