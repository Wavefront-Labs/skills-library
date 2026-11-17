---
id: computing-software.systems-network-administration.dns-dhcp.wildcard-dns-records
name: wildcard-dns-records
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns-records, wildcard-record, rfc4592, empty-non-terminal, nxdomain, subdomain-routing]
level: practitioner
status: verified
description: "Use wildcard DNS records correctly: RFC 4592 matching rules, why existing names and empty non-terminals block wildcards, MX/TXT pitfalls, DNSSEC proofs, and testing."
sources:
  - https://www.rfc-editor.org/rfc/rfc4592
  - https://bind9.readthedocs.io/en/latest/chapter3.html
  - https://www.rfc-editor.org/rfc/rfc9525
  - https://www.rfc-editor.org/rfc/rfc4034
  - https://www.rfc-editor.org/rfc/rfc4035
  - https://man7.org/linux/man-pages/man5/resolv.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wildcard DNS records

```
*.apps.example.net.  300  IN  A  203.0.113.20
```
Any name under `apps.example.net` that does not otherwise exist gets 203.0.113.20: handy for
ingress controllers and per-tenant subdomains.

## Matching rules (RFC 4592)
- The wildcard only matches names that do not exist in the zone at all. If `foo.apps.example.net`
  has any record (even only a TXT), a query for its A record returns NODATA, not the wildcard.
- Empty non-terminals block the wildcard too: if `a.b.apps.example.net` exists, then
  `b.apps.example.net` exists (empty) and does not match `*.apps` (RFC 4592 section 2.2). Servers can
  get this wrong: CoreDNS 1.15's file plugin answered the wildcard for such a name in a test, so
  test your own server.
- `*` only works as the leftmost label, and matches one or more labels:
  `x.y.apps.example.net` matches `*.apps.example.net` (if `y.apps` does not exist; confirmed against
  CoreDNS 1.15, as was NODATA for an existing name that only had a TXT record).
- `*.example.net` does not match `example.net` itself.
- The asterisk in the middle (`foo.*.example.net`) is a literal label, not a wildcard (RFC 4592
  shows `sub.*.example.` as "not a wildcard").

## Pitfalls
- Wildcard at the zone apex level (`*.example.net`) makes every typo resolve: users and monitoring
  never see NXDOMAIN, and mail to misspelt hosts goes somewhere.
- `*.example.net MX` also makes every name accept mail.
- Search-list interaction: a client searching `example.net` turns `www.google.com` into
  `www.google.com.example.net`, which now matches the wildcard. resolv.conf(5) `ndots` (default 1)
  decides which names are tried with the search list first.
- Wildcard CNAMEs to a decommissioned service enable subdomain takeover for every name.
- Wildcard TLS certificates are separate: a wildcard can only be the complete left-most label and
  matches one label (RFC 9525), so `*.apps.example.net` covers one label only.

## DNSSEC
A wildcard RRSIG's Labels field does not count the wildcard label (RFC 4034 section 3.1.3), so it is
smaller than the number of labels in the query name; validators also need NSEC/NSEC3 proof that the
exact name does not exist (RFC 4035 section 3.1.3). Signers handle it; just know larger responses
result.

## Test
```
dig random123.apps.example.net A +short      # wildcard answer
dig existing.apps.example.net A               # NODATA if it only has other types
dig x.y.apps.example.net A +short
```

## Verify
- [ ] Wildcard answers only where intended, and existing names return their own records.
