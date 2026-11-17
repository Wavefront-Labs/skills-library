---
id: computing-software.systems-network-administration.dns-dhcp.catalog-zones-and-hidden-primary
name: catalog-zones-and-hidden-primary
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, zone-transfer, axfr, catalog-zones, hidden-primary, secondaries, rfc9432, also-notify, provisioning, knot-dns, nsd]
level: advanced
status: docs-checked
description: "Scale authoritative DNS with a hidden primary and catalog zones (RFC 9432): secondaries auto-provision member zones from a catalog, with BIND configuration examples."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter6.html#catalog-zones
  - https://datatracker.ietf.org/doc/html/rfc9432
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Catalog zones and the hidden primary

## Hidden primary
The primary (where edits and signing happen) is not listed in the public NS records; only the
secondaries are. The primary can then sit on a management network while secondaries serve
queries.
```
// primary
zone "example.org" { type primary; file "example.org.db";
    notify explicit; also-notify { 192.0.2.11; 192.0.2.12; };
    allow-transfer { key xfr-key; }; };
```

## Catalog zones (RFC 9432)
The format and behaviour of catalog zones are specified in RFC 9432. Instead of configuring
every new zone on every secondary, the primary publishes a catalog zone listing the member
zones, and consumers configure them from it.

Catalog zone content, per RFC 9432:
```
version.catalog.example.        0 IN TXT "2"
<unique-1>.zones.catalog.example. 0 IN PTR example.org.
<unique-2>.zones.catalog.example. 0 IN PTR example.net.
```
- The catalog needs a TXT RRset named `version.$CATZ` with exactly one RR, value "2".
- Each member zone is a PTR in the `zones` sub-domain; the label can be any unique label. Two
  labels pointing to the same member zone make the catalog broken (it must not be processed).
- A catalog zone also needs at least one NS RR to be a valid zone; a single NS with the
  absolute name `invalid.` is recommended. The TTL carries no meaning.

Secondary (BIND `named.conf`):
```
options {
    catalog-zones {
        zone "catalog.example" default-primaries { 10.0.0.10 key xfr-key; } zone-directory "catz";
    };
};
zone "catalog.example" { type secondary; primaries { 10.0.0.10 key xfr-key; }; file "catalog.example.db"; };
```
`default-primaries` supplies the primaries for member zones, and `zone-directory` is where
local copies of member zone files are stored (unless `in-memory` is yes). To add a member
zone, add a PTR record to the catalog zone on the primary.

## Verify
- [ ] Adding a member PTR provisions the zone on the secondaries.
- [ ] Public NS records do not reveal the hidden primary.

## Checked
2026-11-01: confirmed against RFC 9432 (version TXT "2", PTR members under zones, unique labels, NS "invalid.") and the BIND 9 Administrator Reference Manual (Catalog Zones: catalog-zones grammar, default-primaries, zone-directory, in-memory, PTR to add members). Removed: BIND version gates, SOA field values, hash-label advice, member removal behaviour, rndc/dig checks, Knot/NSD support claim.
Method: documentation only; no commands were run.
