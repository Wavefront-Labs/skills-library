---
id: computing-software.systems-network-administration.dns-dhcp.mismatched-ns-sets
name: mismatched-ns-sets
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, ns-mismatch, delegation, lame-delegation, registrar]
level: practitioner
status: docs-checked
description: "Find and fix mismatched NS sets between the parent delegation and the child apex, and know how resolvers treat each."
sources:
  - https://www.rfc-editor.org/rfc/rfc1034
  - https://datatracker.ietf.org/doc/html/draft-ietf-dnsop-ns-revalidation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mismatched NS sets

A zone's name servers are listed in two places that the DNS protocol does not keep in sync: the delegation NS records in the parent zone, and the NS records at the child zone's apex. They drift after migrations.

## What the standards say
- RFC 1034 section 4.2.2: the administrators of both zones should make sure the NS and glue records that mark both sides of the cut are consistent and stay so. The parent's cut NS records are not part of the parent's authoritative data and should be exactly the same as the NS records at the top node of the subzone.
- Glue (address records for name servers below the cut) is needed only when the server's name is below the cut, and is used only in referral responses.
- The child's apex NS RRset is authoritative and ranks higher in a resolver cache than the parent's delegation NS RRset. Resolver behaviour still varies: per the revalidation draft, some resolvers prefer the parent set, some the child set, and for others it depends on which queries they have processed.
- Resolvers that refresh the TTL of a cached child NS RRset can keep using those servers long after the zone was re-delegated elsewhere, unless they revalidate against the parent when the parent NS TTL expires. The draft is a work in progress, not a deployed standard.
- Parent and child NS TTLs may differ, and some TLDs only support long fixed delegation TTLs, so a short child TTL does not guarantee a quick switch.

## Compare
1. Ask the parent zone's servers for the delegation NS set and glue (a non-recursive NS query to a parent server returns a referral).
2. Ask each listed name server for the zone's apex NS set and SOA, and confirm every server answers authoritatively with the same SOA serial.
3. Any difference between the parent set and the child set is a mismatch to resolve.

## Fix
1. Decide the correct set.
2. Update the child apex NS records on every server or provider.
3. Update the delegation at the parent (through the registrar), including glue if the names are below the cut.
4. Keep old servers answering with correct data until the old parent and child NS TTLs have expired, since resolvers may still hold either set.
5. Remove the zone from old servers only after that.

## Verify
- [ ] Parent and child NS sets are identical, every listed server answers authoritatively, and serials match.

## Checked

Confirmed against RFC 1034 (zone and cut sections 4.2.1 and 4.2.2, read) and the DNS Delegation Revalidation draft (draft-ietf-dnsop-ns-revalidation, version 07 of July 2024, motivation and section 3 read). Removed: the dig and shell-loop commands, the "most modern resolvers prefer child NS" claim (the draft says behaviour varies), the lame-server and old-provider consequence rows (not on the pages), and the instruction to refuse queries on old servers.

Method: docs-checked 2026-11-09 against RFC 1034 (rfc-editor.org text) and draft-ietf-dnsop-ns-revalidation-07 (ietf.org archive text).
