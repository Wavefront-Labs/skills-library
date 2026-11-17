---
id: computing-software.collaboration-platform-administration.matrix-synapse.postgres-auth-and-locale-troubleshooting
name: postgres-auth-and-locale-troubleshooting
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, postgresql, pg-hba, ident, collate, ctype, allow-unsafe-locale, reindex]
level: advanced
status: docs-checked
description: "Fix Synapse Postgres failures: Ident authentication failed via pg_hba.conf md5, scram-sha-256 or trust lines and ordering, and the refusal to start on incorrect COLLATE or CTYPE."
sources:
  - https://element-hq.github.io/synapse/latest/postgres.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two Postgres problems are covered in the troubleshooting section.

**Ident authentication failed.** If you see `FATAL:  Ident authentication failed for user "synapse_user"`, use another auth method in `pg_hba.conf`. If the role has a password, put it in the `database:` section of `homeserver.yaml` and add:

```
host    synapse     synapse_user    ::1/128     md5  # or `scram-sha-256` instead of `md5` if you use that
```

If the role has no password, none is needed in `homeserver.yaml`, but `pg_hba.conf` needs:

```
host    synapse     synapse_user    ::1/128     trust
```

Line order matters in `pg_hba.conf`: a new line must come before the default

```
host    all         all             ::1/128     ident
```

for it to apply.

**Incorrect COLLATE or CTYPE.** Synapse refuses to start on a database whose `COLLATE` and `CTYPE` are wrong, unless `allow_unsafe_locale` in the `database` section is set to true. The reason given is that different locales cause trouble if the locale library is updated under the database, or a replica uses a different locale version.

The safest fix is to dump the database and recreate it with the correct locale (`--locale=C`, as in the setup commands). Changing the parameters on a live database and running `REINDEX` on the whole database is possible but needs extreme care to avoid corruption. If corruption has already occurred, the reindex can fail with a duplicate-rows error, and those duplicates must be removed manually.

See the database setup skill for the correct `createdb` command.

## Checked

2026-11-04. Confirmed against the Synapse Using Postgres page (Troubleshooting): ident error, md5, scram-sha-256 and trust lines, line ordering, allow_unsafe_locale, dump-and-recreate fix, REINDEX caveat. Reworded the ordering sentence.
Method: documentation only; no commands were run.
