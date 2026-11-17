---
id: computing-software.systems-network-administration.dns-dhcp.nxdomain-vs-nodata
name: nxdomain-vs-nodata
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns-troubleshooting, nxdomain-vs-nodata, negative-caching, soa-minimum, aaaa-missing, empty-non-terminal]
level: practitioner
status: verified
description: "Tell NXDOMAIN from NODATA in dig output, know how each is cached (SOA minimum), and fix common causes: typos, missing AAAA, records in the wrong zone, and empty non-terminals."
sources:
  - https://www.rfc-editor.org/rfc/rfc2308
  - https://www.rfc-editor.org/rfc/rfc8020
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NXDOMAIN vs NODATA

## How they look
```
dig nothere.example.net A
;; status: NXDOMAIN        ANSWER: 0, AUTHORITY: 1 (the zone's SOA)

dig www.example.net AAAA
;; status: NOERROR         ANSWER: 0, AUTHORITY: 1 (SOA)     <- NODATA
```
Both were reproduced against a local authoritative server (CoreDNS 1.15) with dnspython: the missing
name gave `NXDOMAIN` with only the SOA in the authority section, the existing name with no AAAA gave
`NOERROR`, no answer records and the SOA.
- NXDOMAIN: the name does not exist with any type.
- NODATA: the name exists but has no record of the requested type.

## Caching (RFC 2308)
Both are cached for min(SOA TTL, SOA minimum field), e.g. 3600 s (RFC 2308 section 5: the TTL of the
negative answer is the smaller of the SOA's own TTL and its MINIMUM field). After you add a missing record,
resolvers that cached the negative answer keep returning it until that time passes. Lower the SOA
minimum (300-900 s is typical) on zones that change often, and flush specific names on your own
resolvers (`rndc flushname`, `unbound-control flush`).

RFC 8020: an NXDOMAIN means nothing exists below that name either; a resolver that has cached it can
answer NXDOMAIN for any child name. Creating `a.b.example.net` makes `b.example.net` an empty
non-terminal: it exists, so a query for it gets NODATA, not NXDOMAIN (confirmed: with only
`leaf.mid.example.net A` in the zone, `mid.example.net A` returned NOERROR with an empty answer,
while `x.mid.example.net A` returned NXDOMAIN).

## Common causes
| Answer | Likely cause |
|---|---|
| NXDOMAIN for a name you just created | negative cache, record created in the wrong zone (a more specific delegated zone exists), typo, or wrong view |
| NODATA for AAAA | no IPv6 record: normal, clients fall back to A; but some broken clients wait or fail |
| NODATA for A when a CNAME was expected | CNAME exists at another name; check exact spelling |
| NXDOMAIN only from one resolver | split-horizon view or RPZ policy rewriting (`dig +norec @auth` vs resolver) |
| NXDOMAIN from authoritative but record in zone file | zone not reloaded/serial not bumped, or secondary stale |

## Workflow
```
dig name.example.net A @<resolver>
dig name.example.net A @<each authoritative> +norec
dig example.net SOA +short          # minimum field = negative TTL
dig +trace name.example.net         # finds an unexpected delegation
```

## Verify
- [ ] Authoritative servers answer correctly with +norec; resolvers agree after the negative TTL or
  a targeted flush.
