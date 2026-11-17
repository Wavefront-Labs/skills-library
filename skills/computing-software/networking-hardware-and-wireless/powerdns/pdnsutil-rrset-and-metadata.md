---
id: computing-software.networking-hardware-and-wireless.powerdns.pdnsutil-rrset-and-metadata
name: pdnsutil-rrset-and-metadata
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, pdnsutil, rrset, metadata, rectify, nsec3-hash, catalog-list-members]
level: practitioner
status: docs-checked
description: "pdnsutil rrset add, replace, delete and hash, the --rectify flag, plus metadata add/get/set semantics and catalog list-members and set."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/manpages/pdnsutil.1.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pdnsutil rrset and metadata

RRsets (alias `record`); NAME must be absolute:
- `rrset add ZONE NAME TYPE [TTL] CONTENT`: uses `default-ttl` if TTL is omitted.
- `rrset replace ZONE NAME TYPE [TTL] CONTENT [CONTENT]...`
- `rrset delete ZONE NAME TYPE`
- `rrset hash ZONE RNAME`: NSEC3 hash of RNAME with the zone's NSEC3 settings; fails if NSEC3 is not configured.

These do not rectify the zone unless you pass `--rectify`.

Metadata:
- `metadata get ZONE [KIND]...`: all known kinds if none given.
- `metadata set ZONE KIND [VALUE]...`: replaces all values; no values clears the kind.
- `metadata add ZONE KIND VALUE [VALUE]...`: appends; errors if the kind holds only a single value.

Catalog:
- `catalog list-members CATALOG`
- `catalog set ZONE [CATALOG]`: moves the zone into the catalog; omit CATALOG to remove it.

## Checked

2026-11-08. Read the catalog zone, zone metadata and zone record sections of the PowerDNS pdnsutil manpage (docs/manpages/pdnsutil.1.rst on master) and confirmed every command form, the `record` alias, the `--rectify` note, `default-ttl`, absolute names and NSEC3 hash behaviour. Removed the claim about `set-meta` and `set-catalog` before 5.0, which the page does not state.

Method: documentation only; no commands were run.
