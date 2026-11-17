---
id: computing-software.networking-hardware-and-wireless.powerdns.geoip-backend-settings
name: geoip-backend-settings
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, geoip, mmdb, maxmind, geoip-database-files, geoip-zones-file, edns-subnet]
level: practitioner
status: docs-checked
description: "Configure the PowerDNS geoip backend: geoip-database-files format with dat and mmdb drivers, geoip-zones-file, DNSSEC keydir, ECS requirement and build notes."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/geoip.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GeoIP backend settings

- `geoip-database-files`: comma, tab or space separated entries of the form `[driver:]path[;options]`.
- Drivers: `dat` (legacy libGeoIP; option `mode` of `standard`, `memory`, `index` or `mmap`) and `mmdb` (libmaxminddb; `mode` only `mmap`, and `language`, default `en`).
- `database-file` / `database-file6`: set to `""` to disable IPv4 or IPv6 lookups. Leaving them unset points at a default location, which stops startup if no file is there, so set paths explicitly.
- `geoip-zones-file`: full path of the YAML zone file; re-read by `pdns_control reload`.
- `geoip-dnssec-keydir`: full path; setting it enables DNSSEC, with keys managed by `pdnsutil`.
- `edns-subnet-processing` must be turned on for the backend to use EDNS Client Subnet in its decisions.

Notes:
- The backend API is read-only.
- Requires libyaml-cpp 0.5 or later. libgeoip and libmaxminddb are each optional since 4.2.0; without either, database-based placeholders are unavailable.
- Wildcard service records answer with CNAMEs, and a CNAME cannot share a label with NS or SOA (RFC 2181), so avoid such services at the zone apex.

## Checked

2026-11-04. Read backends/geoip.rst in full and confirmed the database-files format, dat and mmdb options, database-file unset warning, zones-file reload, dnssec-keydir, libyaml-cpp 0.5 and 4.2.0 optional libraries, read-only API and the RFC 2181 CNAME note. Corrected the setting name to edns-subnet-processing.

Method: documentation only; no commands were run.
