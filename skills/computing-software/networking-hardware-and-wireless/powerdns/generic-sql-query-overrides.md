---
id: computing-software.networking-hardware-and-wireless.powerdns.generic-sql-query-overrides
name: generic-sql-query-overrides
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, generic-sql, basic-query, query-override, prepared-statements, xfr-cycle-interval]
level: advanced
status: docs-checked
description: "Override PowerDNS generic SQL backend queries such as gmysql-basic-query: naming pattern, positional placeholders, column order, query families and how to print defaults."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/generic-sql.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic SQL query overrides

Every generic SQL backend (gmysql, gpgsql, gsqlite3, godbc) lets you replace its queries with settings named `<backend>-<name>`, for example `gmysql-basic-query`. Print the defaults with `pdns_server --launch=BACKEND --config=default`.

- `backend-dnssec=yes` (for example `gmysql-dnssec`) enables DNSSEC.
- Since 4.0.0 queries are prepared statements with positional `?` placeholders; earlier releases used `%` snprintf placeholders.
- Column names do not matter, order does. A regular lookup returns `content, ttl, prio, type, domain_id, disabled, name, auth`. The default basic query is `SELECT content,ttl,prio,type,domain_id,disabled,name,auth FROM records WHERE disabled=0 and type=? and name=?`.
- Long queries may continue across lines by ending a line with `\`.

Query families:
- Lookup: `basic-query` (the most used), `id-query`, `any-query`, `any-id-query`, `list-query` (AXFR), `list-subzone-query`, `search-records-query`.
- DNSSEC: `get-order-first/before/after/last-query`, `update-ordername-and-auth-query`, and the empty-non-terminal queries.
- Zone: `is-our-domain-query`, `insert-zone-query`, `delete-zone-query`, `get-all-domains-query`, `insert-record-query`.
- Metadata, keys, TSIG, comments, and primary/secondary queries (`info-all-primary-query`, `update-serial-query`, `autoprimary-query`).

`xfr-cycle-interval` (default 60 s) sets how often secondary domains are checked. Avoid raw SQL for changes; use the REST API or `pdnsutil`.

## Checked

2026-11-04. Read backends/generic-sql.rst in full and confirmed prepared statements since 4.0.0, the --config=default command, column order, the basic-query example, line continuation, query names and the 60 second xfr-cycle-interval default. gmysql-dnssec confirmed on the gmysql page. Nothing removed.

Method: documentation only; no commands were run.
