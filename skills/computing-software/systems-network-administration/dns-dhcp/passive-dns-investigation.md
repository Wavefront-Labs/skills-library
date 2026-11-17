---
id: computing-software.systems-network-administration.dns-dhcp.passive-dns-investigation
name: passive-dns-investigation
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, passive-dns, threat-intelligence, dns-history, incident-response]
level: practitioner
status: draft
description: "Use passive DNS data (commercial feeds, own sensors) to see historical resolutions, pivot on IPs and name servers, and support incident and takeover investigations."
sources:
  - https://www.farsightsecurity.com/technical/passive-dns/
  - https://datatracker.ietf.org/doc/html/draft-dulaunoy-dnsop-passive-dns-cof
  - https://github.com/gamelinux/passivedns
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Passive DNS

Passive DNS collects resolver-to-authoritative answers observed by sensors and stores which name
resolved to which data, first/last seen and counts. It answers "what did this name point to last
March?" and "what else lives on this IP?".

## Sources
- Commercial/community: DomainTools/Farsight DNSDB, SecurityTrails, Cisco Umbrella Investigate,
  VirusTotal relations, CIRCL pDNS (for CSIRTs).
- Your own: `passivedns` sensor on resolver egress, dnstap from your resolvers into a database, or
  Zeek `dns.log` aggregated.

## Typical queries
- Name history: all A/CNAME/NS for `login-example.com` over time (phishing infrastructure rotation).
- Reverse pivot: every name seen on 203.0.113.50 (shared hosting, C2 clusters).
- NS pivot: domains using the same unusual name server (registrant grouping).
- Your own domains: verify a dangling CNAME existed and when it was pointed at an attacker's resource.
CIRCL format (common output):
```
{"rrname":"evil.example","rrtype":"A","rdata":"203.0.113.50","time_first":1700000000,"time_last":1700500000,"count":42}
```

## Caveats
- Sensor coverage is partial; absence does not prove non-existence.
- Shared IPs (CDNs, hosting) produce huge noisy pivots: filter by time window and count.
- Privacy: your own pDNS sensors must not store client IPs unless justified (only resolver egress data).

## Use in incidents
Combine with WHOIS history, certificate transparency (crt.sh) and malware sandboxes to build an
infrastructure timeline.

## Verify
- [ ] Findings cite source, time_first/time_last and are corroborated by a second source (CT logs, WHOIS, own logs).
