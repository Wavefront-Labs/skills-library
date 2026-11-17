---
id: computing-software.systems-network-administration.cisco-networking.urpf-unicast-reverse-path-forwarding
name: urpf-unicast-reverse-path-forwarding
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, urpf, unicast-rpf, anti-spoofing, bcp84, rfc3704, strict-mode, loose-mode, feasible-rpf, ingress-filtering]
level: practitioner
status: docs-checked
description: "Choose a uRPF flavour per RFC 3704 (BCP 84): strict, feasible-path, loose, loose ignoring default; where asymmetric or multihomed routing breaks each."
sources:
  - https://www.rfc-editor.org/rfc/rfc3704
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unicast RPF (RFC 3704 / BCP 84)

uRPF is a way to implement ingress filtering against spoofed source addresses: the source address of each packet is
checked against the forwarding table. RFC 3704 lists five implementation techniques; the vendor knobs map onto these.
Interface commands are not given here (the Cisco uRPF page was a 404 when checked): consult your platform's guide for
how it names strict and loose checks and any default-route option.

| Technique | Check | Where RFC 3704 says it fits |
|---|---|---|
| Ingress access list | source matched against a list of acceptable prefixes | deterministic but manually maintained; stale lists drop legitimate traffic |
| Strict RPF | FIB lookup of the source; packet passes only if it arrived on the interface that would be used to reach that source | "very reasonable" in front of an edge network; far better than ACLs when the edge advertises many BGP prefixes |
| Feasible-path RPF | as strict, but alternative (feasible) paths are also valid, e.g. all or N feasible BGP paths | asymmetric or multihomed edges, if all paths carry consistent route advertisements |
| Loose RPF | only that a route exists (a default route counts) | drops "Martian" or unrouted sources; little value as edge ingress filtering |
| Loose RPF ignoring default routes | a route must exist, default routes excluded | where defaults only catch bogus sources and explicit routes cover legitimate ones |

## Failure modes the RFC names
- Strict needs symmetric routing. Common at an edge facing its ISP, not common between ISPs (hot-potato routing).
- If legitimate prefixes are not advertised to or accepted by the filtering router, strict drops that traffic, the same
  as an incomplete ACL. "If an advertisement is filtered, the packets will be filtered as well" applies to feasible RPF
  too.
- Operational fix for strict with asymmetric BGP: give directly received routes a better local preference that is not
  propagated (vendor weight or protocol distance), possibly automated with communities. This breaks if there is strict
  filtering between the primary and secondary edge routers, especially with different ISPs.
- Loose RPF loses directionality, so it cannot confine an edge network to its own source addresses.
- A default route can nullify loose RPF completely. Some implementations check where the default points: if it points
  at the interface with loose RPF, anything passes; if it points elsewhere, bogus sources are still dropped.
- Good fit for loose: an ISP filtering its upstream links to drop Martian or unrouted sources, or as "contract
  verification" that the neighbour does its own ingress filtering (it only catches unrouted sources, not another
  network's address space).

## Design guidance
1. Filter at every level (customer edge, ISP edge, LAN uplinks): defence in depth, and it protects your own
   infrastructure addresses from being spoofed at your borders.
2. Between peers, strict works as long as routing stays reasonably symmetric.
3. Multihomed: prefer feasible RPF or operational strict tuning; fall back to loose on the interfaces where
   asymmetry is unavoidable (section 4.1), and make sure each ISP's filter is complete (section 4.2) or that you only
   send traffic with a provider's prefix to that provider (section 4.3).

## Verify
- [ ] State which technique each interface uses and why (symmetric, multihomed, upstream).
- [ ] Test: a packet with a source unrouted on that interface is dropped; a legitimate source arriving by the backup
      path is not.
- [ ] Check whether a default route is present and what the platform does with it before relying on loose mode.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read RFC 3704 sections 2.1-2.5 (five techniques), 3.1-3.3 and 4 to
4.1. RFC 3704 is the cited source; later revisions were not read. Removed as unconfirmed: all IOS command lines and
`allow-default`, ACL exemption for DHCP, RTBH remark, show commands and counters, `hping3` test, and the IPv6 command.
