---
id: computing-software.systems-network-administration.coredns.coredns-geoip-plugin
name: coredns-geoip-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, geoip, maxmind, metadata, mmdb]
level: advanced
status: docs-checked
description: "Enrich queries with city, country and ASN data from a MaxMind mmdb database via the geoip plugin, optionally using EDNS0 client subnet."
sources:
  - https://coredns.io/plugins/geoip/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expose client geography to later plugins through metadata.

geoip looks up the client IP in an `.mmdb` database and stores the result with the metadata plugin, so other plugins can read it.

```
geoip [DBFILE] {
    [edns-subnet]
}
```

- DBFILE is the mmdb path. Update it periodically for accuracy.
- `edns-subnet` uses the EDNS0 subnet (if present) instead of the packet source IP. This identifies the real client behind an intermediary resolver and helps testing.
- Resolvers may mask some bits of the client address, which can reduce accuracy. RFC 7871 conceals the last 72 bits of an IPv6 source address in its example.

Databases: those following the city schema (ASN, City, Enterprise) are supported when their field names map to the metadata labels. Other schemas are not supported yet.

Labels (all values are stored as strings, so convert numbers back; numerics are base 10): `geoip/city/name`, `geoip/country/code`, `geoip/country/name`, `geoip/country/is_in_european_union`, `geoip/continent/code`, `geoip/continent/name`, `geoip/latitude`, `geoip/longitude`, `geoip/timezone`, `geoip/postalcode`, `geoip/subdivisions/code` (comma separated), `geoip/asn/number`, `geoip/asn/org`. Plugin code reads them with `metadata.ValueFunc(ctx, "geoip/city/name")`.

The metadata plugin must be enabled as well. Example, with the db path as a placeholder:

```
. {
    geoip <path-to>/GeoLite2-City.mmdb {
        edns-subnet
    }
    metadata
}
```

GSLB with view: put a block with `view` and `expr metadata('geoip/city/name') == 'Exampleshire'` first, then geoip, metadata and its own zone file, and a viewless block for the same zone last; the viewless block must be last.

Note: since CoreDNS v1.13.2 the geoip library upgrade means missing latitude and longitude now come back as an empty string instead of "0".

## Checked

2026-11-08. Checked in full against the geoip plugin README. Removed two unsupported claims (rewrite using metadata labels; metadata label naming rules); listed all exported labels with string typing, a placeholder-path example, the view GSLB ordering rule and the v1.13.2 empty-coordinate change.

Method: documentation only; no commands were run.
