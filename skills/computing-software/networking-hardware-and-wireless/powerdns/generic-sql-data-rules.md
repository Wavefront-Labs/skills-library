---
id: computing-software.networking-hardware-and-wireless.powerdns.generic-sql-data-rules
name: generic-sql-data-rules
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, generic-sql, records-table, auth, ordername, disabled, empty-non-terminals]
level: advanced
status: docs-checked
description: "Data rules for PowerDNS generic SQL tables: names without trailing dot, disabled, auth values, ordername per NSEC/NSEC3 mode, empty non-terminals, type, ttl and domain_id."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/generic-sql.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic SQL data rules

Rules to respect when rows are written outside the API:
- Record and zone names never end in `.`; only the root zone is named `.`.
- `disabled` is `1` (`true` in PostgreSQL). A disabled SOA disables the whole zone; `pdnsutil` cannot set it.
- `auth` is `1` for zone data, including the SOA and the zone's own NS records, and `0` for delegation NS and glue. A secure delegation's DS record should be authoritative.
- `ordername` depends on the mode:
  - NSEC3 narrow: ignored, best left empty.
  - NSEC: relative labels, reversed, dots replaced by spaces.
  - NSEC3 non-narrow: lowercase base32hex of the salted, iterated hash (see `pdnsutil rrset hash`).
- Empty non-terminals need a row whose `type` is SQL NULL; rectify inserts them and NSEC3 needs them.
- `type` must match exactly, so use VARCHAR, not CHAR.
- `ttl` is a positive integer. `domain_id` is a positive integer unique across all backends.

Prefer the REST API or `pdnsutil` over raw SQL.

## Checked

2026-11-04. Read backends/generic-sql.rst in full and confirmed trailing-dot rule, disabled data, auth, ordername per mode, empty non-terminals with SQL NULL type, VARCHAR advice and positive ttl and domain_id. Nothing removed.

Method: documentation only; no commands were run.
