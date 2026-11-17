---
id: computing-software.systems-network-administration.dns-dhcp.dns-propagation-per-authoritative-server
name: dns-propagation-per-authoritative-server
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dns-propagation, authoritative-servers, ttl, caching]
level: practitioner
status: docs-checked
description: "Check DNS changes properly: query every authoritative server directly, compare serials, then reason about resolver caches and TTLs instead of propagation myths."
sources:
  - https://www.rfc-editor.org/rfc/rfc1034
  - https://www.rfc-editor.org/rfc/rfc2308
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checking propagation per authoritative server

DNS does not "propagate". Authoritative servers get the change (via transfer or provider API), and
caches expire their old copy after the TTL they received.

## Step 1: every authoritative server
```
for ns in $(dig +short NS example.com); do
  echo "$ns"; dig +short +norecurse @$ns example.com SOA; dig +short +norecurse @$ns www.example.com A
done
dig +nssearch example.com                # queries each listed name server for the SOA
```
All should show the same serial and the new answer. If one differs, the problem is transfer/
provider sync, not caching.

## Step 2: the parent delegation (for NS changes)
```
dig +norecurse @<a-parent-zone-nameserver> example.com NS
```
NS/glue changes at the registrar depend on the TLD operator's publishing schedule and on the old NS TTL in the parent.

## Step 3: caches
- Ask a few public resolvers and an internal resolver with `dig @<resolver>`. The TTL in
  their answer counts down to when they will refetch.
- Old answer remaining past the old TTL: the resolver had it cached before you lowered the TTL, or
  it caps or raises TTLs, or clients cache (browsers, applications, OS stub caches).
- Negative answers (NXDOMAIN for a name you just created) are cached for the minimum of the SOA MINIMUM field and the SOA record TTL (RFC 2308 section 5).
- Flush where you control the resolver: `rndc flushname www.example.com` (BIND), `unbound-control flush www.example.com` (Unbound).

## Planning changes
Lower the TTL at least one old-TTL period before the change, make the change, raise TTL later.

## Verify
- [ ] All authoritative servers serve the new data and major resolvers return it after the old TTL has elapsed.

## Checked

Date: 2026-10-26. Documentation: BIND dig man page (+nssearch, +norecurse, +short) and rndc man page (flushname), Unbound unbound-control (flush), read 2026-10-26. Confirmed those commands and options. Removed unconfirmed claims about .com parent TTL, Java caching property, public resolver addresses, Windows flush commands and public cache purge pages. RFC 2308 section 5 confirmed: negative-answer TTL is the minimum of SOA MINIMUM and the SOA TTL.

Method: documentation only; no commands were run.
