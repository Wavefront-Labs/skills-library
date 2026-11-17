---
id: computing-software.systems-network-administration.network-design.dns-cache-poisoning
name: dns-cache-poisoning
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-attacks, dns-poisoning, dnssec, kaminsky-attack, source-port-randomization]
level: practitioner
status: docs-checked
description: "Understand and mitigate DNS cache poisoning: Kaminsky-style spoofing, source port and ID randomisation, DNSSEC validation, 0x20, and locking down resolvers."
sources:
  - https://www.rfc-editor.org/rfc/rfc5452
  - https://www.rfc-editor.org/rfc/rfc4033
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DNS cache poisoning

## Attack
An attacker races the real authoritative server, sending forged responses to a recursive resolver. A forged reply is
accepted only if it matches the outstanding query: the DNS ID (a 16-bit field), the question, the source and
destination addresses and the UDP port. If it arrives first, the resolver caches the attacker's data and serves it
until the TTL expires. RFC 5452 explains that the 16-bit ID alone is too little protection, and that the query's source
port acts as an additional ID field of up to 16 bits when it is randomised; a fixed source port removes that protection.

## Mitigations
| Control | Effect |
|---|---|
| Source port randomisation (RFC 5452) | extends the effective transaction ID; check that NAT or firewalls in front of resolvers do not de-randomise ports |
| DNSSEC validation on resolvers (RFC 4033) | forged answers for signed zones fail validation; validating resolvers can set the AD bit |
| Restrict recursion to internal clients | outsiders cannot trigger queries |
| Patch resolver software | resolver vendors publish fixes for newly found attacks |

## Check your resolvers
- Query a deliberately broken signed domain through the resolver and confirm it fails when validation is on.
- Check responses for the AD flag on signed names.
- Check your resolver software's documentation for the validation setting name (BIND, Unbound and Windows DNS
  differ), and for port-randomisation behaviour.

## Verify
- [ ] All internal resolvers validate DNSSEC, randomise source ports (not de-randomised by NAT), and refuse recursion
  from outside.

## Checked
2026-10-28. Confirmed in RFC 5452 (16-bit DNS ID, source port as additional ID field, randomisation) and RFC 4033 (AD
bit, validation). Removed as unconfirmed: Kaminsky and SAD DNS descriptions, 0x20 encoding, DNS cookies (RFC 7873),
EDNS buffer size, DoT/DoH advice, the `porttest` and `dnssec-failed.org` commands, Unbound and BIND directive names (the
ISC page is a product overview).
Method: documentation only; no commands were run.
