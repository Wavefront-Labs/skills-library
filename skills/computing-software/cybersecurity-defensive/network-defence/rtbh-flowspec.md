---
id: computing-software.cybersecurity-defensive.network-defence.rtbh-flowspec
name: rtbh-flowspec
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [rtbh, remotely-triggered-black-hole, bgp-flowspec, ddos-mitigation, bgp-communities, rfc-7999, isp-blackholing]
level: advanced
status: docs-checked
description: "Use RTBH and BGP FlowSpec for DDoS mitigation: destination and source-based blackholing, BLACKHOLE community with your ISP, FlowSpec rules, safeguards and withdrawal."
sources: ["https://datatracker.ietf.org/doc/html/rfc7999", "https://datatracker.ietf.org/doc/html/rfc5635", "https://datatracker.ietf.org/doc/html/rfc8955"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RTBH and FlowSpec

## Destination-based RTBH
When a single IP is flooded beyond your link capacity, announce that /32 (or /128) to your upstream with
the BLACKHOLE community (RFC 7999 well-known community 0xFFFF029A, written `65535:666`, or the ISP's own
community). The ISP drops traffic to that IP at their edge - the target goes offline, but everything else on
the link survives. RFC 7999 says the blackhole prefix should be as long as possible (typically /32 IPv4 or
/128 IPv6) to limit collateral damage, and that honouring the community is each operator's choice: in a
bilateral relationship it must be agreed beforehand, and the receiver should only honour announcements for
prefixes the neighbour is authorised to advertise.

On your own trigger router (vendor syntax varies, check your platform): a static discard route for the
victim /32 is redistributed into BGP with the BLACKHOLE community plus `no-export`, so it does not propagate
beyond the neighbour you intended.

## Source-based RTBH (RFC 5635)
Drop traffic *from* attacking sources: uRPF on edge interfaces combined with routes for the attacking source
prefixes pointing at a discard next-hop. RFC 5635 warns that strict-mode uRPF drops legitimate traffic under
asymmetric routing and that loose mode can also discard legitimate traffic, so understand the effect before
enabling uRPF. It works only inside your network or with ISP support.

## FlowSpec (RFC 8955)
Distribute filters by BGP. Match components include destination prefix, source prefix, IP protocol, port,
destination port, source port, ICMP type and code, TCP flags, packet length, DSCP and fragment. Actions are
carried as extended communities: traffic-rate (a rate of 0 discards all matching traffic), and rt-redirect to
a VRF identified by route-target (for example a scrubbing VRF). Far more surgical than RTBH (e.g. drop UDP
source port 123 to the target, keep TCP 443). RFC 7999 states the BLACKHOLE community is not intended to be
used with FlowSpec NLRI; they are separate mechanisms.

## Safeguards
- ISP agreements: which communities, max prefix length accepted, and that the prefix is covered by space you
  are authorised to advertise.
- Prefix filters so only your own space can be blackholed; do not leak blackhole routes beyond the intended
  neighbour (RFC 7999 recommends adding `NO_EXPORT` or `NO_ADVERTISE` on receipt). Make sure origin validation
  does not block legitimate blackhole announcements.
- Runbook with authorisation, logging, and a timer to withdraw. RFC 7999 encourages storing BGP updates that
  carry the BLACKHOLE community for later audit.
- FlowSpec validation: a rule is accepted when its originator matches the originator of the best-match unicast
  route for the destination prefix, and it is revalidated whenever unicast routes change. Do not relax this.

## Verify
- [ ] Tabletop/test with a test IP: ISP looking glass shows blackhole route; withdrawal restores traffic.

## Checked
Checked 2026-11-09 against RFC 7999 (community value 0xFFFF029A, section 3 operational recommendations,
prefix length, NO_EXPORT, not for FlowSpec), RFC 5635 (uRPF strict and loose caveats) and RFC 8955 (match
types, traffic-rate 0, rt-redirect, validation procedure). Removed: the Cisco IOS-XE configuration block
(not covered by the sources), the MANRS source (not used), the TCAM claim and the "customer cone validation"
wording.
Method: docs-checked 2026-11-09 against RFC 7999, RFC 5635 and RFC 8955, pages read in full or by section.
