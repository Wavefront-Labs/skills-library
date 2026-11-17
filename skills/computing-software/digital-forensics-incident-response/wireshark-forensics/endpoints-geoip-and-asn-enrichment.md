---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.endpoints-geoip-and-asn-enrichment
name: endpoints-geoip-and-asn-enrichment
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [geoip, wireshark, pcap-triage, statistics-conversations, dfir]
level: practitioner
status: draft
description: "Enrich Wireshark endpoints and conversations with MaxMind GeoIP/ASN databases, filter by country or ASN, and avoid over-trusting geolocation."
sources: ["https://www.wireshark.org/docs/wsug_html_chunked/ChMaxMindDbPaths.html", "https://www.wireshark.org/docs/wsug_html_chunked/ChStatEndpoints.html", "https://dev.maxmind.com/geoip/geolite2-free-geolocation-data"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Endpoints, GeoIP and ASN enrichment

**Goal:** quickly see which external networks a capture talks to, flag unusual countries/hosting
providers, and filter by them.

## Configure
1. Download MaxMind GeoLite2 City and ASN `.mmdb` files (free account) or commercial GeoIP2.
2. Wireshark: Edit > Preferences > Name Resolution > **MaxMind database directories** > add the folder.
3. Enable "Enable IP geolocation" in Name Resolution preferences.

## Use
- Statistics > **Endpoints** > IPv4/IPv6 tab: columns Country, City, AS Number, AS Organization,
  plus packets/bytes; sort by bytes to find top talkers; "Map" button plots endpoints (OpenStreetMap HTML).
- Statistics > Conversations for pair-level volume and duration.
- Display filters on GeoIP fields:
```text
ip.geoip.dst_country == "Russia"
ip.geoip.asnum == 14061            # e.g. a hosting provider ASN
!ip.geoip.country and !(ip.dst == 10.0.0.0/8 or ip.dst == 172.16.0.0/12 or ip.dst == 192.168.0.0/16)
ip.geoip.dst_org contains "Hosting"
```
- tshark: `tshark -r cap.pcapng -o "maxmind.db_paths:<dir>" -T fields -e ip.dst -e ip.geoip.dst_asnum -e ip.geoip.dst_org -Y "ip" | sort | uniq -c | sort -rn`

## Interpretation
- ASN/organisation is more useful than country: VPS/hosting ASNs, bulletproof hosters, residential
  proxy ranges are more telling than a country flag.
- Cloud/CDN IPs (AWS, Azure, Cloudflare, Akamai) host both legitimate and malicious services; pivot on SNI/Host instead.

## Gotchas
- GeoIP accuracy is limited (country usually right, city often wrong); VPNs and proxies mask origin. State it as "registered/geolocated to".
- Database age matters: use one dated close to the capture date for historic cases and record its version.

## Verify
Record the database edition/date used, and corroborate any key IP with WHOIS/RDAP and passive DNS.
