---
id: computing-software.systems-network-administration.dns-dhcp.dname-redirection-records
name: dname-redirection-records
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dname, rfc6672, domain-aliasing, cname-synthesis]
level: practitioner
status: verified
description: "Use DNAME to alias an entire subtree, how resolvers synthesise CNAMEs, interaction with DNSSEC and email, and why apex DNAME rarely does what people want."
sources:
  - https://www.rfc-editor.org/rfc/rfc6672
  - https://www.rfc-editor.org/rfc/rfc7535
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNAME

A DNAME at `old.example.` redirects every name BELOW it to the same name under the target:
```
old.example.com.   3600 IN DNAME new.example.net.
```
Query `www.old.example.com A` -> server returns the DNAME plus a synthesised
`www.old.example.com CNAME www.new.example.net.` and follows it if it can.

## What it does not do
- The owner name itself is not redirected: `old.example.com A` is not affected; add records there
  separately (an apex DNAME leaves apex MX/A in place).
- It cannot coexist with other records below the owner (they would be occluded).
- It does not rewrite email addresses or HTTP Host headers; web servers still need a vhost or
  redirect for the old names.

## Uses
- Renaming a branch of the namespace (company rename) while keeping old names resolving.
- Reverse DNS for prefixes shorter than /24: `DNAME` extends classless in-addr.arpa delegation (RFC 6672
  section 6.2).
- AS112 redirection (RFC 7535, "AS112 Redirection Using DNAME") uses DNAME to move sink queries.

## DNSSEC
The DNAME is signed. RFC 6672 says the synthesised CNAME does not have to be signed: a validating
resolver checks the CNAME against the signed DNAME. The synthesised CNAME is given the same TTL as
the DNAME (seen in the test below).

## Test
With `old.example.net. 3600 IN DNAME new.example.org.` in a zone served by CoreDNS 1.15 (queried with
dnspython), `www.old.example.net A` returned this answer section, with the AA flag set:
```
old.example.net.     3600 IN DNAME new.example.org.
www.old.example.net. 3600 IN CNAME www.new.example.org.
```
and `old.example.net A` returned NOERROR with an empty answer (NODATA), so the owner name itself is
not redirected. A resolver then continues with the CNAME target (`dig www.old.example.net A` shows the
same chain plus the final address).

## Verify
- [ ] Several sample names under the owner resolve to their counterparts and the owner itself still answers as intended.
