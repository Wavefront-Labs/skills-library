---
id: computing-software.networking-hardware-and-wireless.powerdns.catalog-zone-producer
name: catalog-zone-producer
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, catalog-zone, producer, pdnsutil, coo, group, catalog-hash]
level: practitioner
status: docs-checked
description: "Create a PowerDNS catalog zone producer: SOA/NS-only zone, set-kind producer, pdnsutil catalog set members, coo/group/unique options, CATALOG-HASH, version support."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/catalog.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Catalog zone producer

Needs Authoritative 4.7.0+. Backends: gmysql, gpgsql, gsqlite3, godbc, lmdb. Catalog v1 (ISC) is consumer-only; v2 (RFC 9432) supports producer and consumer. There are no configuration options.

Steps:
1. Make a zone with only SOA and NS at the apex (other records are ignored for the catalog). Its initial SOA serial must be at or below the epoch; it is raised to EPOCH after each relevant member change.
2. Load it and set the kind:
```
pdnsutil zone load catalog.example ZONEFILE
pdnsutil zone set-kind catalog.example producer
```
(Before 5.0: `load-zone`, `set-kind`. API type is `PRODUCER`.)
3. Add members:
```
pdnsutil catalog set example.com catalog.example
pdnsutil zone set-kind example.com primary
```
Via the API, set the zone's `catalog` property; an empty string removes membership. Since 5.1.0 a catalog zone may itself be a member of another catalog.
4. Member properties:
```
pdnsutil zone set-option example.com producer coo other-catalog.example
pdnsutil zone set-option example.com producer group pdns-group-x pdns-group-y
pdnsutil zone set-option example.com producer unique 123
```
`coo` is one DNS name, `group` may repeat, `unique` is a single label that tells consumers to reset state. These cannot be set via the API.

`CATALOG-HASH` metadata on producer zones is server-managed; changing or deleting it bumps the serial and regenerates it.

Use TSIG on catalog zones.

## Checked

2026-11-04. Read catalog.rst in full and confirmed the version table, backend list, SOA/NS-only producer zone, serial at or below epoch, PRODUCER type, catalog set, coo/group/unique options, API limits, 5.1.0 nested catalogs and CATALOG-HASH behaviour. Nothing removed.

Method: documentation only; no commands were run.
