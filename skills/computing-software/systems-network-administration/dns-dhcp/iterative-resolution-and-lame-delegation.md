---
id: computing-software.systems-network-administration.dns-dhcp.iterative-resolution-and-lame-delegation
name: iterative-resolution-and-lame-delegation
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dns-resolution, recursive-resolution, iterative-query, referral, lame-delegation, delegation, ns-records, parent-child-mismatch, dig-norec, dig-trace, aa-flag, glue-records]
level: practitioner
status: verified
description: "Walk DNS resolution by hand with dig +norec, read referrals and the AA flag, and find lame delegations and parent/child NS mismatches that cause slow or intermittent resolution."
sources:
  - https://datatracker.ietf.org/doc/html/rfc1034
  - https://datatracker.ietf.org/doc/html/rfc8499
  - https://bind9.readthedocs.io/en/latest/manpages.html#dig-dns-lookup-utility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Iterative resolution and lame delegation

## Recursion vs iteration
- Stub resolver (client) asks a **recursive resolver** with RD=1 and expects a final answer.
- The recursive resolver resolves **iteratively**: root -> TLD -> domain's servers, following
  **referrals** (NS records in the authority section, plus glue in additional).
- Authoritative servers answer with AA=1 for their zones and refuse/ignore recursion.

## Do it by hand
```
dig +norec . NS @a.root-servers.net
dig +norec www.example.org A @a.root-servers.net         # referral to org. servers
dig +norec www.example.org A @a0.org.afilias-nst.info    # referral to example.org NS (+glue?)
dig +norec www.example.org A @ns1.example.org            # flags: qr aa -> authoritative answer
dig +trace www.example.org                               # automated: starts from the root and follows referrals
```
Look at `flags:` (aa present?), the AUTHORITY section (who is delegated), ADDITIONAL (glue).
Run with dnspython 2.9 against the live root (RD cleared): `. NS @a.root-servers.net` gave NOERROR with aa and 13
additional glue records; `www.example.org A` there gave NOERROR, no aa, and a referral to `org.` with the NS names
`a2.org.afilias-nst.info.`, `b2.org.afilias-nst.org.`, `d0.org.afilias-nst.org.` and glue; `a0.org.afilias-nst.info` also
resolves and its referral for `example.org` listed Cloudflare name servers (`mitch.ns.cloudflare.com.`,
`katelyn.ns.cloudflare.com.`) with no glue, because they are out of bailiwick. So `ns1.example.org` below is
illustrative: substitute the NS names the referral actually returns.

## Lame delegation
A server listed as NS for a zone that does not answer authoritatively for it: times out,
returns REFUSED/SERVFAIL, or answers without AA (often a referral back up). Resolvers try another
NS after a timeout, so users see **slow or intermittent** resolution rather than total failure.
Check every NS at the parent and the child:
```
dig +short example.org NS @<tld-server>             # parent's view (delegation)
dig +short example.org NS @ns1.example.org          # child's view (zone apex)
for ns in $(dig +short example.org NS); do
  echo "== $ns"; dig +norec +nocmd +noall +comments +answer example.org SOA @$ns | grep -E 'flags|SOA|status'
done
```
Every server should return `status: NOERROR`, `aa` flag and the **same SOA serial**.

## Common causes
- Old provider's servers still listed at the registrar after a migration.
- Typo in an NS name; NS pointing to a CNAME (not allowed).
- Parent and child NS sets differ (child added a server, registrar not updated).
- Missing or stale glue for in-bailiwick NS names (`ns1.example.org` serving `example.org`).
- Secondary not transferring (serial behind): see zone-transfer skills.
Online checks: DNSViz, Zonemaster, `dnsviz probe`.

## Verify
- [ ] All delegated NS answer with aa and identical serials.
- [ ] Parent and child NS sets match; glue correct.
