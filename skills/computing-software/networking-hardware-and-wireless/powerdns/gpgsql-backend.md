---
id: computing-software.networking-hardware-and-wireless.powerdns.gpgsql-backend
name: gpgsql-backend
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, gpgsql, postgresql, backend, tls, prepared-statements]
level: practitioner
status: docs-checked
description: "Configure the PowerDNS gpgsql backend for PostgreSQL: host, dbname and TLS parameters, prepared statements with poolers, schema load, and CockroachDB changes."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/generic-postgresql.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gpgsql backend

Settings:
- `gpgsql-host`: IP to connect to; a value starting with `/` is a Unix socket directory.
- `gpgsql-port`, `gpgsql-dbname`, `gpgsql-user`, `gpgsql-password`.
- `gpgsql-dnssec` (default no): enable DNSSEC for this backend.
- `gpgsql-extra-connection-parameters` (default empty): extra libpq parameters. To pin a CA, use `sslmode=verify-full` plus `sslrootcert=/path/to/ca.pem`.
- `gpgsql-prepared-statements` (default yes, since 4.4.0): may break behind connection poolers; set it to no there.

Setup:
1. `createdb pdns` (you may need to).
2. `psql pdns`, then load the schema `modules/gpgsqlbackend/schema.pgsql.sql` (the 4.7 schema by default).
3. For migrations use `zone2sql --gpgsql`, which assumes that schema.

Use an IP rather than a hostname in `gpgsql-host`, so the database is not needed to resolve its own address.

CockroachDB:
- Make an explicit sequence with `MAXVALUE 2147483648` for each SERIAL column: `domain_id`, `record_id`, `comment_id`, `meta_id`, `key_id`, `tsig_id`, and use `DEFAULT nextval('domain_id')` style defaults (for example `id INT DEFAULT nextval('domain_id') PRIMARY KEY`).
- Skip the `recordorder` index on `records`, because `text_pattern_ops` is unsupported.
- Override `gpgsql-get-order-first-query`, `-before-query`, `-after-query` and `-last-query` with the generic MySQL style queries, since the defaults use unsupported range operators.

## Checked

2026-11-04. Read backends/generic-postgresql.rst in full and confirmed settings and defaults, 4.4.0 prepared statements, pooler caveat, the extra-connection-parameters TLS example, setup commands and the CockroachDB sequence, index and query changes. Nothing removed.

Method: documentation only; no commands were run.
