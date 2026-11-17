---
id: computing-software.systems-network-administration.dns-dhcp.zone-cuts-and-delegation
name: zone-cuts-and-delegation
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, zone-cut, delegation, glue-records, subdomain-delegation]
level: practitioner
status: verified
description: "Understand zones vs domains and zone cuts: delegating a subdomain with NS and glue, parent/child authority, DS at the cut, and checking a delegation."
sources:
  - https://www.rfc-editor.org/rfc/rfc1034#section-4.2
  - https://www.rfc-editor.org/rfc/rfc9471
  - https://bind9.readthedocs.io/en/latest/chapter3.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zones vs domains and zone cuts

A **domain** is a subtree of the namespace; a **zone** is the part of it served by one set of
authoritative servers. A **zone cut** is where authority passes to a child zone, marked by NS
records in the parent.

## Delegating dev.example.com from example.com
Parent zone `example.com`:
```
dev                 IN NS  ns1.dev.example.com.
dev                 IN NS  ns2.provider.net.
ns1.dev             IN A   192.0.2.53          ; glue: needed because ns1 is inside the child
dev                 IN DS  12345 13 2 <digest>  ; only if the child is signed
```
Child zone `dev.example.com` on ns1/ns2 has its own SOA and the same NS set at its apex.

## Rules at the cut
- The parent is authoritative for the DS (and NSEC) at the cut (RFC 4035); the NS and glue in the parent are
  non-authoritative hints. The child's apex NS set is authoritative and should match.
- No other data may exist in the parent at or below the cut (it would be occluded and never served). Tested with
  CoreDNS 1.15.0 `file` zones: an A record `host.dev` left in the parent zone below the `dev` cut was never returned;
  the query got a referral instead (NOERROR, no AA flag, the NS RRset in AUTHORITY, glue in ADDITIONAL).
- Glue is needed for in-domain name servers (at or below the delegated name); RFC 9471 says a server generating a
  referral MUST include all available in-domain glue or set TC=1 if the message would be too large.
- A name used as an NS target must not be an alias (RFC 2181 section 10.3).

## Check a delegation
```
dig +norecurse @a.gtld-servers.net example.com NS      # parent view
dig +norecurse @<parent-ns> dev.example.com NS         # referral: AUTHORITY section, no AA flag
dig @ns1.dev.example.com dev.example.com SOA +norecurse   # child answers with AA
dig +trace dev.example.com
```

The same test showed the child server answering `dev.example.test SOA` with the AA flag, and a server that is
listed but does not serve the zone answering REFUSED (a lame delegation).

## Common mistakes
- Creating `dev` as a folder of records in the parent AND delegating it: parent records hidden,
  inconsistent answers from different servers.
- Lame delegation: a listed NS does not serve the child zone (REFUSED or no AA).
- Forgetting to update parent NS when moving the child to new servers.

## Verify
- [ ] Parent NS set equals child apex NS set, and every listed server answers authoritatively.
