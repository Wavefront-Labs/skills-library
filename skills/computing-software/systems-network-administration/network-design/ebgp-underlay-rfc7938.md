---
id: computing-software.systems-network-administration.network-design.ebgp-underlay-rfc7938
name: ebgp-underlay-rfc7938
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, dc-fabric, rfc7938, bgp-underlay, spine-leaf, ecmp, asn-design]
level: practitioner
status: docs-checked
description: "Build a data centre underlay with eBGP per RFC 7938: ASN schemes for spines and leaves, unnumbered links, ECMP multipath, BFD, and avoiding path hunting."
sources:
  - https://www.rfc-editor.org/rfc/rfc7938
  - https://www.rfc-editor.org/rfc/rfc5549
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# eBGP underlay (RFC 7938)

RFC 7938 ("Use of BGP for Routing in Large-Scale Data Centers") uses eBGP as the only routing
protocol in a Clos fabric: simple, one protocol, good policy control, scales.

## ASN plan
| Role (RFC 7938 5.2.1) | Scheme |
|---|---|
| Tier 1 (spines) | a single ASN for all Tier 1 devices |
| Tier 2 | a unique ASN per set of Tier 2 devices in the same cluster |
| Tier 3 (ToR/leaf) | a unique ASN per device |
The RFC uses Private Use ASNs from 64512-65534 and notes Four-Octet ASNs as the alternative when
that range runs out. A well-defined ASN scheme plus standard AS_PATH loop detection controls
**path hunting** and ignores complex unwanted paths.

## Link addressing
- EBGP single-hop sessions over each direct point-to-point link (RFC 7938), numbered from a /31
  (FRR accepts /30 or /31), or **BGP unnumbered** (RFC 5549: IPv4 NLRI with an IPv6 link-local next
  hop; FRR `neighbor <interface>`), removing per-link IP planning.
- A loopback per switch for the router ID.

## Key knobs
```
router bgp 4200000011
 bgp router-id 10.0.0.11
 bgp bestpath as-path multipath-relax
 neighbor FABRIC peer-group
 neighbor FABRIC remote-as external
 neighbor FABRIC bfd
 neighbor swp51 interface peer-group FABRIC
 address-family ipv4 unicast
  redistribute connected route-map LOOPBACKS
  maximum-paths 64
```
(FRR syntax.) `multipath-relax` permits ECMP over paths with different AS numbers (needed when
each neighbour tier has a different ASN, RFC 7938 section 6.2). RFC 7938 points to BFD for
sub-second failure detection.

## Policy
Advertise only loopbacks and server subnets; filter everything else; set `allowas-in` only
where a design needs it (RFC 7938 mentions it for shared ASNs).

## Verify
- [ ] Every leaf sees every other leaf loopback with ECMP across all spines; failing a spine removes it within BFD time with no prolonged blackholing.

## Checked
2026-10-28. Confirmed against RFC 7938 (eBGP in Clos fabrics; ASN guidelines in 5.2.1: single-hop sessions, Private Use ASNs 64512-65534, one ASN for Tier 1, unique per Tier 2 cluster and per Tier 3; path hunting control; Four-Octet ASN alternative; multipath relax in 6.2; BFD for sub-second detection; allowas-in), RFC 5549 (IPv4 NLRI with IPv6 next hop) and the FRR BGP manual (`multipath-relax`, `maximum-paths`, `remote-as external`, `neighbor <interface>`). Removed: the 65100 and 4200000000-4294967294 figures, VTEP, the BFD 300 ms and BGP 3/9 s timers, RFC 8950 and the Arista link.
Method: documentation only; no commands were run.
