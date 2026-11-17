---
id: computing-software.networking-hardware-and-wireless.opnsense.alias-geoip
name: alias-geoip
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [aliases, geoip, ipinfo, maxmind]
level: practitioner
status: docs-checked
description: "Set up GeoIP aliases in OPNsense: IPinfo gzip and MaxMind zip sources, table size increase, and Business Edition mirror behaviour."
sources: ["https://docs.opnsense.org/manual/aliases.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GeoIP aliases

A GeoIP alias selects one or more countries or whole continents to allow or block; a "toggle all" checkbox selects every country in a region. Outside the Business Edition you must first define a data source on the Firewall > Aliases > GeoIP settings tab. OPNsense understands the formats offered by IPinfo and MaxMind, and there are dedicated how-tos for each provider. On the Business Edition you can leave the Url field empty and the firewall downloads the IPinfo database from the vendor's mirrors automatically.

IPinfo format: a gzip-compressed CSV whose header names the columns. The full column order is network, country, country_code, continent, continent_code, asn, as_name, as_domain, but only network and country_code are used and must appear in the header.

MaxMind format: a zip containing CSV files: %prefix%-locations-en.csv (maps geoname_id to country_iso_code, e.g. 1,,,,NL) and %prefix%-IPv4.csv (network,geoname_id, e.g. 2.21.241.0/28,1), with a matching IPv6 file for IPv6 data.

Sizing: IPinfo's dataset is much larger and more detailed, roughly 7 million entries in total at the time of writing. When selecting many countries, raise Firewall > Settings > Advanced > Firewall Maximum Table Entries, otherwise the table will not load completely. The Loaded# column on the alias overview helps spot an overflow.

GeoIP aliases are used like any other alias in rule source or destination fields.

## Checked

2026-11-03. Read the Aliases manual page (aliases.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
