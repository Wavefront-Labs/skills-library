---
id: computing-software.networking-hardware-and-wireless.powerdns.lua-records-geo-helpers
name: lua-records-geo-helpers
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, lua-records, geoip, country, continent, asnum, netmask, createreverse, filterforward]
level: practitioner
status: docs-checked
description: "PowerDNS LUA location and reverse helpers: country, continent, asnum, netmask, geoiplookup, dblookup, createReverse, filterForward."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/lua-records/functions.rst
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/lua-records/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LUA geo and reverse helpers

Location (all judge `bestwho`; the geoip backend must be launched):
- `latlon()`: latitude and longitude text. `latlonloc()`: LOC format.
- `country(code|codes)`, `region(code|codes)`, `continent(code|codes)`, `asnum(number|numbers)`, `netmask(netmasks)`: booleans.
- `countryCode()` (two letters, or `--` if unknown), `regionCode()`, `continentCode()` (such as `EU`).
- `geoiplookup(address, attr)` with `GeoIPQueryAttribute.ASn`, `City`, `Continent`, `Country`, `Country2`, `Name`, `Region`, `Location`.
- `dblookup(name, type)` (4.9.0+): array of strings from the database; it does not evaluate LUA, and an empty result can break `ifurlup`.

Reverse DNS:
- `createReverse(format[, exceptions])` and `createReverse6(format[, exceptions])`: PTR names from IPv4 octets (`%1%` to `%6%`) or IPv6 nibbles and chunks (`%1%` to `%41%`).
- `createForward()` / `createForward6()`: the A or AAAA encoded in the queried name.
- `filterForward(address, masks[, fallback])` (4.5.0+): replaces addresses outside the NetmaskGroup with the fallback (default `0.0.0.0` or `::`); an empty fallback gives NODATA (4.9.0+), and that empty-fallback form cannot be combined with DNSSEC. The page recommends filtering `createForward` output this way so PowerDNS does not answer for addresses outside your network.

## Checked

2026-11-08. Read in full: PowerDNS docs lua-records/functions.rst and lua-records/index.rst. Confirmed all helper names and return shapes, the 5.0.0 GeoIPQueryAttribute constants, the 4.9.0 dblookup and filterForward notes, the 4.5.0 filterForward note, the createReverse format ranges and the geoip launch requirement. Narrowed the DNSSEC remark to the empty-fallback form.

Method: documentation only; no commands were run.
