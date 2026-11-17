---
id: computing-software.cybersecurity-defensive.threat-intelligence.infrastructure-pivoting
name: infrastructure-pivoting
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [adversary-profiling, infrastructure-pivoting, passive-dns, certificate-pivoting, jarm, whois-history, censys, threat-actor-infrastructure]
level: advanced
status: draft
description: "Expand one adversary indicator into their wider infrastructure: passive DNS, certificate and TLS fingerprint pivots, WHOIS and hosting patterns, scanning data, and confidence."
sources: ["https://www.first.org/global/sigs/cti/curriculum/", "https://search.censys.io/", "https://github.com/salesforce/jarm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Infrastructure pivoting

Start from a C2 IP or phishing domain; find related infrastructure the adversary controls to block it
proactively and track the actor.

## Pivot types
| From | Pivot via | Sources |
|---|---|---|
| Domain | Passive DNS (IPs it resolved to over time), sibling domains on same IP | DomainTools, SecurityTrails, RiskIQ/Defender TI, Farsight DNSDB, VirusTotal |
| Domain | WHOIS history: registrant email, registrar, name servers, registration timing patterns | WHOIS history services |
| IP | Reverse DNS / other domains, open ports and banners, hosting ASN | Censys, Shodan, BinaryEdge |
| TLS certificate | SHA1/SHA256 fingerprint, subject/issuer quirks, serial reuse | crt.sh, Censys certificates |
| TLS server | JARM / JA4S fingerprints, default C2 certificates (Cobalt Strike, Sliver defaults) | Censys/Shodan queries |
| HTTP | Favicon hash (mmh3), page title, response headers, unique body strings | Shodan `http.favicon.hash:`, Censys |
| Malware | C2 config extractions, shared code, mutexes | Sandbox reports, VirusTotal relationships |

Example Censys query style: `services.tls.certificates.leaf_data.subject.common_name: "Major Cobalt Strike"`
or `services.jarm.fingerprint: <jarm>`.

## Method
1. Record the seed with source and confidence.
2. Pivot one hop at a time; for each new node, note the linking attribute.
3. Score link strength: unique certificate hash or unique favicon = strong; shared hosting IP or popular
   registrar = weak (thousands of unrelated sites).
4. Time-bound: passive DNS overlap in the same weeks is stronger than years apart.
5. Validate before acting: is the new domain actually malicious (content, sandbox, reputation)?

## Outputs
- Blocklist candidates with confidence and expiry.
- Actor infrastructure profile (preferred registrars, hosting providers, naming patterns, TLS habits)
  for future detection rules (e.g. new domains matching a regex registered at the same registrar).
- STIX relationships in the TIP linking indicators to the actor/campaign.

## OPSEC
- Querying attacker infrastructure directly (visiting sites, scanning) can tip them off; prefer passive
  sources, use isolated browsing infrastructure if needed.
- Some commercial sources share queries; know your providers' terms.

## Gotchas
- Shared CDN/hosting (Cloudflare, shared hosting) produce huge, meaningless pivot sets.
- Sinkholed domains point to researcher infrastructure; check before attributing.

## Verify
Peer review of the pivot graph: each edge has a recorded attribute and strength, and blocks are only
proposed for nodes validated as malicious.
