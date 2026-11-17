---
id: computing-software.systems-network-administration.cisco-networking.ospf-external-e1-e2-routes
name: ospf-external-e1-e2-routes
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ospf, ospf-e1-e2, forwarding-address, external-routes, type-5-lsa, redistribution, metric-type, rfc2328, rfc3101]
level: practitioner
status: docs-checked
description: "OSPF external path selection per RFC 2328 16.4: type 1 vs type 2 metrics, ASBR tie-breaks, and how a non-zero forwarding address changes next hop or hides the route."
sources:
  - https://www.rfc-editor.org/rfc/rfc2328
  - https://www.rfc-editor.org/rfc/rfc3101
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPF external routes: type 1, type 2 and the forwarding address

Per RFC 2328: an AS boundary router (ASBR) originates one AS-external-LSA for each external route it learned from
another routing protocol or configuration. The metric is one of two types: type 1 is comparable to the link-state
metric, type 2 is assumed larger than the cost of any intra-AS path. Cisco's route codes are E1 and E2; the RFC speaks
of type 1 and type 2 external paths. Redistribution command syntax is platform-specific and not covered here.

## Path selection (section 16.4, step 6)
1. Intra-area and inter-area paths are always preferred over AS external paths.
2. Type 1 external paths are always preferred over type 2 external paths for the same destination.
3. Among type 2 paths, the smallest advertised type 2 metric wins, regardless of the internal cost
   ("a type 2 external path with type 2 cost of 5 is always preferred over a path with type 2 cost of 10").
4. Remaining ties: with RFC1583Compatibility disabled, section 16.4.1 prefers by the intra-AS paths to the
   ASBR/forwarding address; then least cost. Type 1 compares X+Y (distance to the forwarding address or ASBR plus the
   advertised metric); type 2 with equal metrics compares the distance to the forwarding address or ASBR.
5. For a given ASBR reachable via several routing table entries, the least cost entry is used, and among equals the
   one whose area has the largest area ID (forwarding address 0.0.0.0 case).

Consequence: type 2 makes the exit decision with the external metric alone (good for primary/backup exits set by
metric); type 1 adds the internal distance, so each router tends to choose the nearest ASBR.

## Forwarding address (FA)
- 0.0.0.0 means "send to the advertising ASBR". A non-zero FA lets the ASBR point traffic at a better next hop, for
  example a BGP peer on a shared segment that does not run OSPF, avoiding an extra hop through the ASBR (RFC 2328
  section 2 discussion and 12.4.4.1 example).
- A non-zero FA must resolve in the routing table to an intra-area or inter-area path; otherwise the LSA is ignored.
  This is the silent failure: the LSA is in the database but no route installs. An unreachable ASBR (0.0.0.0 FA case)
  likewise causes the LSA to be skipped.
- The RFC says a non-zero FA "should point to a router belonging to another Autonomous System". When the FA is
  non-zero the installed next hops are those towards the FA, not towards the ASBR.
- LSAs with LSInfinity cost, at MaxAge, or self-originated are skipped.
- Rule of thumb that follows: ensure the FA's subnet is reachable by OSPF-internal routes everywhere the external
  route is needed, and do not summarise or filter it at area borders.

## NSSA (RFC 3101)
- If the next hop of an external route belongs to a network attached to an active NSSA interface of the NSSA ASBR, that
  next hop is copied into the FA of the type 7 LSA. Otherwise the FA may be an address of one of its active interfaces,
  or 0.0.0.0 if the P-bit is clear.
- If the P-bit is set the FA must be non-zero; if an NSSA needs the P-bit and no non-zero FA is available, the type 7 is
  not originated.
- A translated type 5 copies the type 7's non-zero FA; only type 5 LSAs that aggregate type 7s may carry 0.0.0.0.
  So filtering or summarising the FA's address breaks the translated externals.
- Type 5 and type 7 metrics and path types are directly comparable.
- If the interface behind the FA goes down, the router picks a new FA and re-originates, or flushes the LSA.

## Verify
- [ ] On a remote router, the external LSA shows the expected metric type and FA.
- [ ] The FA resolves via an intra- or inter-area route.
- [ ] Failover test: withdrawing the primary ASBR's LSA moves traffic to the backup exit.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read RFC 2328 section 2 (forwarding address discussion), 12.4.4
(and its metric type text), 16.4 and 16.4.1, the Type 2 cost definition in section 11, and RFC 3101 sections 2.3-2.4
(forwarding address rules). The Cisco page 13717-38 returned 404 and was dropped. Removed as unconfirmed: all IOS
`redistribute` lines and the `subnets` keyword remarks, show-command output, the claim that the FA is set whenever the
next hop is on a non-passive broadcast OSPF network (not stated in these pages), and the "make the interface passive"
fix.
