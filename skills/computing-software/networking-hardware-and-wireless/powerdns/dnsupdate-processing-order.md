---
id: computing-software.networking-hardware-and-wireless.powerdns.dnsupdate-processing-order
name: dnsupdate-processing-order
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, dnsupdate, dhcpd, rcode, tsig, ddns, troubleshooting]
level: practitioner
status: docs-checked
description: "Understand how PowerDNS processes a DNS UPDATE, which check returns which rcode, and the dhcpd dynamic DNS example with TSIG key and per-zone metadata."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnsupdate.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS UPDATE processing order

Order of checks (use it to read the rcode you get):
1. TSIG validated against known keys; invalid signature is refused.
2. Zone must be valid, else ServFail.
3. `dnsupdate` must be enabled, else Refused.
4. With a Lua policy, jump to step 7.
5. Source IP must match `ALLOW-DNSUPDATE-FROM` (global or zone), else Refused.
6. TSIG key name must match `TSIG-ALLOW-DNSUPDATE`, else Refused.
7. Find the zone's backend.
8. On a secondary, forward to the masters if enabled; ServFail if all fail.
9. Every record must be in the zone, else NotZone.
10. Open a backend transaction; check RFC 2136 section 3.2 prerequisites and return the matching rcode.
11. Apply each update; ServFail on backend failure.
12. If records changed and the SOA was not itself updated, bump the serial.
13. Commit (ServFail on failure), then NoError.

The served SOA may differ from the one just written because SOA-EDIT applies when serving.

dhcpd example:
1. `dnssec-keygen -a hmac-md5 -b 128 -n USER dhcpdupdate`
2. In `dhcpd.conf` add the `key` block, `ddns-updates on`, `ddns-update-style interim`, `update-static-leases on`, `ddns-domainname`, `ddns-rev-domainname`, and `zone { primary <server>; key <name>; }` blocks.
3. In `pdns.conf`: `dnsupdate=yes` and `allow-dnsupdate-from=`.
4. `pdnsutil tsigkey import dhcpdupdate hmac-md5 <secret>`.
5. For each forward and reverse zone set `ALLOW-DNSUPDATE-FROM` to the dhcpd host and `TSIG-ALLOW-DNSUPDATE` to the key name; restart.

## Checked

2026-11-04. Read dnsupdate.rst in full and confirmed the 13-step order and rcodes (against the page's 15-step list), SOA-EDIT note and every step of the dhcpd example including settings and pdnsutil tsigkey import. Nothing removed.

Method: documentation only; no commands were run.
