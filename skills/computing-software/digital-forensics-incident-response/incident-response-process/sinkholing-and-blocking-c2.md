---
id: computing-software.digital-forensics-incident-response.incident-response-process.sinkholing-and-blocking-c2
name: sinkholing-and-blocking-c2
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [dns-sinkhole, c2-blocking, containment, dns-rpz, firewall, dfir]
level: practitioner
status: draft
description: "Block and sinkhole command-and-control domains and IPs with DNS RPZ, firewall and proxy rules, and use sinkhole hits to find additional infected hosts."
sources: ["https://www.isc.org/rpz/", "https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://learn.microsoft.com/en-us/windows-server/networking/dns/deploy/dns-policies-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sinkholing and blocking C2

**Goal:** sever command-and-control and exfiltration channels in a coordinated moment, and
turn the block into a detector for hosts you have not found yet.

## Where to block
| Layer | Mechanism | Notes |
|---|---|---|
| Internal DNS | BIND/Unbound **RPZ** zone, Windows DNS policy/zone, Infoblox RPZ | Point domain to an internal sinkhole IP that logs connections |
| Egress firewall | Deny rules for C2 IPs/ranges | Log hits; IPs change, so keep updating |
| Proxy / SWG | URL/domain category block | Catches HTTP(S) C2 by SNI/host |
| EDR | Custom IOC block (domain/IP/hash) | Per-host enforcement, works off-network |

## RPZ example (BIND)
```
$TTL 60
@ IN SOA localhost. root.localhost. 1 3600 600 86400 60
  IN NS localhost.
evil-c2.example      CNAME .            ; NXDOMAIN
*.evil-c2.example    A     10.99.99.99  ; or redirect to sinkhole
```
`options { response-policy { zone "rpz.local"; }; };` then `rndc reload`.

## Sinkhole as sensor
Run a listener on the sinkhole IP (web server plus packet capture). Every host that
connects is infected or configured with the C2; feed them into the affected-asset register.

## Gotchas
- Hosts using DoH/DoT or hard-coded DNS bypass internal DNS; block known DoH endpoints and
  outbound 53/853 except from resolvers.
- Blocking before scoping tips off the attacker; time the block with coordinated containment.
- Do not sinkhole shared infrastructure (CDNs, cloud storage) by IP; block by full URL/domain.
- Domain fronting and legitimate SaaS C2 (Slack, Telegram, OneDrive) require proxy-level or
  tenant restrictions.

## Verify
Resolve the domain from a client (`nslookup evil-c2.example`) and confirm sinkhole/NXDOMAIN;
watch firewall and proxy logs for allowed connections to the C2 after block time.
