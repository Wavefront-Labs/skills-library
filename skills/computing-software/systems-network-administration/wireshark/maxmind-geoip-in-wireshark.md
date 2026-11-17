---
id: computing-software.systems-network-administration.wireshark.maxmind-geoip-in-wireshark
name: maxmind-geoip-in-wireshark
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, geoip, maxmind, asn-lookup, endpoints, ip-geolocation, threat-hunting]
level: practitioner
status: docs-checked
description: "Add country, city and ASN data to packets with MaxMind .mmdb databases: configure the path, filter on ip.geoip fields, and map endpoints in Statistics."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChMaxMindDbPaths.html
  - https://www.wireshark.org/docs/dfref/i/ip.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatEndpoints.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MaxMind GeoIP in Wireshark

## Get the databases
Wireshark needs a build with the MaxMindDB library. MaxMind offers some databases free to registered
users (GeoLite2) and others for a fee. Any file ending in `.mmdb` in a configured directory is loaded
automatically, so drop the Country, City and ASN databases in one folder. The old GeoIP Legacy `.dat`
format is no longer supported.

## Point Wireshark at them
Wireshark always searches `/usr/share/GeoIP` and `/var/lib/GeoIP` on non-Windows platforms, and the
ProgramData GeoIP folder and a top-level GeoIP folder on the C drive on Windows. Add any other folder
as an entry in the MaxMind database paths user table in the preferences. The default
paths are not listed in that table; see Help > About Wireshark > Folders.

## Fields and filters
IP packets gain a GeoIP subtree. Field names listed in the ip protocol reference include
`ip.geoip.country`, `ip.geoip.country_iso`, `ip.geoip.city`, `ip.geoip.asnum`, `ip.geoip.org`,
`ip.geoip.isp`, `ip.geoip.lat`/`lon`, and src_ and dst_ variants of each (for example
`ip.geoip.dst_country_iso`, `ip.geoip.dst_asnum`).
```
ip.geoip.country == "Russia"
ip.geoip.dst_country_iso == "CN"
ip.geoip.asnum == 13335
ip.geoip.org contains "Amazon"
```
Add `ip.geoip.dst_country` and `ip.geoip.dst_asnum` as columns.

## Endpoints map
Statistics > Endpoints lists IPv4 endpoints; the Map button shows the endpoints mapped in your web
browser.

## Uses
- Quick triage of outbound connections to unexpected countries/ASNs.
- Separating CDN/cloud traffic (ASN) from the rest.
- Checking where a DDoS or scan originates.

## Gotchas
- Geolocation is approximate; cloud and VPN egress addresses mislead. ASN is more reliable than
  city.
- Databases go stale; refresh them on a schedule.
- Check the database licence terms before redistributing.

## Verify
- [ ] Public addresses in the packet details show a GeoIP subtree with country and AS number.

## Checked
Method: docs-checked 2026-11-09 against the Wireshark User's Guide MaxMind Database Paths and Endpoints pages and the ip display-filter reference (geoip field names), all read in full or grepped. Dropped: geoipupdate commands, the exact preferences menu path, OpenStreetMap and version claims, the tshark note, and attribution wording, none of which the pages confirm.
