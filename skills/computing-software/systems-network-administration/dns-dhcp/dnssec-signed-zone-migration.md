---
id: computing-software.systems-network-administration.dns-dhcp.dnssec-signed-zone-migration
name: dnssec-signed-zone-migration
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dnssec, dns-migration, dnssec-migration, ds-record, multi-signer, go-insecure, provider-change, algorithm-rollover, registrar, dnskey]
level: advanced
status: docs-checked
description: "Move a DNSSEC-signed zone between providers without validation outages: go-insecure-and-resign vs multi-signer (RFC 8901) approaches, DS timing, and verification at each step."
sources:
  - https://datatracker.ietf.org/doc/html/rfc8901
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating a DNSSEC-signed zone

The danger: during NS changeover, some resolvers fetch DNSKEYs from the old provider and data
from the new (or vice versa). If the DS at the parent does not match keys that sign what resolvers
receive, validating users get SERVFAIL.

## Method 1: go insecure, move, re-sign (simple, brief loss of DNSSEC protection)
1. Remove the DS at the registrar.
2. Wait for the parent DS TTL plus the maximum TTL of cached DNSKEY/RRSIG records.
3. Confirm no DS at the parent (`dig DS example.org @<tld-ns>` empty). Zone is now insecure but valid.
4. Move the zone and switch NS (see dns-provider-migration). Wait the parent NS TTL.
5. Enable signing at the new provider, publish the new DS, verify with DNSViz.
Also the safe way to do an algorithm change if your signer cannot do an algorithm rollover.

## Method 2: multi-signer (no insecure window, RFC 8901 model 2)
RFC 8901 Model 2 is "Unique KSK Set and ZSK Set per Provider": each provider signs the DNSKEY RRset with its own KSK, and the zone owner's DS RRset has one DS per provider. Providers need a common signing algorithm. BIND's `dnssec-policy` has a `tag-range` option intended for multi-signer scenarios.
1. Enable signing at the new provider; exchange the public DNSKEYs between providers as RFC 8901 describes, so both serve a consistent DNSKEY RRset (provider support varies; check each provider's documentation).
2. Add the new provider's DS at the registrar alongside the old one; wait the DS TTL.
3. Switch NS to the new provider; wait the parent NS TTL plus DNSKEY TTL.
4. Remove the old provider's DS, then its DNSKEYs from the new provider; decommission.
Both providers must use the **same algorithm** (RFC 8901).

## Checks at each step
```
dig +short DS example.org @<parent-nameserver>
dig +dnssec +multi DNSKEY example.org @ns1.old.net
dig +dnssec +multi DNSKEY example.org @ns1.new.net
delv example.org SOA +vtrace
```
DNSViz on the zone between steps; it shows which DS matches which DNSKEY per server.

## Gotchas
- A registrar that only accepts DNSKEY (and computes the DS) or one DS at a time constrains method 2.
- NSEC vs NSEC3 differences between providers are fine; algorithm differences are not.

## Verify
- [ ] DNSViz clean at every step; no SERVFAIL reports from validating resolvers (test through at least two validating resolvers).

## Checked

Date: 2026-10-26. Documentation: RFC 8901 (multi-signer models and common-algorithm requirement), BIND ARM dnssec-policy tag-range note, 2026-10-26. Confirmed: Model 2 definition (unique KSK and ZSK sets, one DS per provider) and the same-algorithm requirement. Removed the unconfirmed provider support list and the unconfirmed TTL durations; the Cloudflare page was not read, so it is no longer cited.

Method: documentation only; no commands were run.
