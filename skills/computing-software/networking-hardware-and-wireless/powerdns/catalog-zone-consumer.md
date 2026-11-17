---
id: computing-software.networking-hardware-and-wireless.powerdns.catalog-zone-consumer
name: catalog-zone-consumer
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, catalog-zone, consumer, create-secondary, change-primary, retrieve]
level: practitioner
status: docs-checked
description: "Run a PowerDNS catalog zone consumer: create-secondary then set-kind consumer, member zones inherit primaries, change-primary plus pdns_control retrieve, limits."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/catalog.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Catalog zone consumer

Setup:
```
pdnsutil zone create-secondary catalog.example 192.0.2.42
pdnsutil zone set-kind catalog.example consumer
```
(Before 5.0: `create-secondary-zone` and `set-kind`. API type is `CONSUMER`.)

New member zones listed in the catalog inherit their primaries from the consumer zone.

Move the primary (address or port) on a consumer using NOTIFY and AXFR:
```
pdnsutil zone change-primary catalog.example 192.0.2.45
pdns_control retrieve catalog.example
```
(Before 5.0: `change-secondary-zone-primary`.) This updates the primary details in every member zone of the catalog. Do both steps on each secondary.

Limits and advice:
- Requires 4.7.0+ and a catalog-capable backend (gmysql, gpgsql, gsqlite3, godbc, lmdb).
- Consumers read catalog v1 (ISC) and v2 (RFC 9432); on consumers there are no group templates and no custom extensions.
- Protecting catalog zones with TSIG is highly recommended.
- If you also use views, read the catalog zone section of the Views documentation.

## Checked

2026-11-04. Read catalog.rst in full and confirmed the 4.7.0 start, backend list, v1 and v2 consumer support, missing group templates and custom extensions, CONSUMER type, create-secondary and change-primary commands with pre-5.0 names, and member primaries inheritance. Removed a claim about views member variants that catalog.rst only points to the Views documentation for; kept a pointer instead.

Method: documentation only; no commands were run.
