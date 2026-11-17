---
id: computing-software.systems-network-administration.dns-dhcp.local-root-zone-rfc8806
name: local-root-zone-rfc8806
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, rfc8806, local-root, mirror-zone, unbound, bind]
level: practitioner
status: verified
description: "Run a local copy of the root zone on resolvers (RFC 8806) with BIND mirror zones or Unbound auth-zone, validation, fallback and monitoring."
sources:
  - https://www.rfc-editor.org/rfc/rfc8806
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-type%20mirror
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html#authority-zone-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local root zone (RFC 8806)

A resolver can hold the whole root zone locally, so root lookups (including junk TLD queries) never
leave the network: lower latency, privacy, and resilience against root server attacks.

## BIND (`type mirror`, documented in the current ARM)
```
zone "." { type mirror; };
```
The mirror zone is transferred like a secondary (RFC 8806 lists `xfr.lax.dns.icann.org` and `xfr.cjr.dns.icann.org`
plus the b, c, d, f, g and k root servers as AXFR sources; none is guaranteed), and the whole zone is DNSSEC-validated
during the transfer and again on load. If a new version fails validation a retransfer is scheduled and the last
validated version is used until it expires; with no usable data BIND falls back to normal recursion.
`rndc zonestatus .` shows serial and status (`zonestatus` is an rndc command).

## Unbound
```
auth-zone:
    name: "."
    primary: 170.247.170.2        # b.root-servers.net (renumbered; 199.9.14.201 is the old address in RFC 8806)
    primary: 192.33.4.12          # c.root
    primary: 192.5.5.241          # f.root
    primary: 2801:1b8:10::b       # b.root IPv6 (old 2001:500:200::b)
    fallback-enabled: yes
    for-downstream: no
    for-upstream: yes
    zonefile: "root.zone"
```
`zonemd-check: yes` (default no) verifies the ZONEMD digest in the zone; when there is a DNSSEC chain of trust the
signatures are checked too. Take the current server addresses from `https://www.internic.net/domain/named.root`.
Checked: a dnspython 2.9 AXFR of the root from `xfr.lax.dns.icann.org` returned 7,359 names (serial 2026102102 at
the time) and `zone.verify_digest()` passed the ZONEMD check.

## Operational notes
- Root zone file is ~2.2 MB (internic root.zone measured at 2,251,862 bytes); the SOA serial is `YYYYMMDDNN` and was
  `2026102101` then `2026102102` within one day, i.e. updated about twice daily.
- Ensure outbound TCP 53 to the transfer servers.
- Monitor serial age: alarm if the local copy is more than 2 days old (`dig @127.0.0.1 . SOA +norecurse`).

## Verify
- [ ] `dig @resolver nonexistent-tld-xyz A` returns NXDOMAIN with no outbound root traffic in a capture.
