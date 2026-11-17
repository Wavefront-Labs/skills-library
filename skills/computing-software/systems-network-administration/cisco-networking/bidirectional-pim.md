---
id: computing-software.systems-network-administration.cisco-networking.bidirectional-pim
name: bidirectional-pim
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, multicast, bidir-pim, pim-bidir, rendezvous-point, many-to-many-multicast, df-election]
level: practitioner
status: docs-checked
description: "Understand Bidirectional PIM (RFC 5015) for many-to-many multicast: RPA, RPL, Designated Forwarder election, and how it differs from PIM-SM."
sources:
  - https://datatracker.ietf.org/doc/html/rfc5015
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bidirectional PIM

## When
Applications where many hosts are both senders and receivers. PIM-SM builds a unidirectional shared tree per group
and either encapsulates a source's first packets in Register messages to the RP or builds source-specific state on
the path from source to RP. RFC 5015 says encapsulation costs processing, bandwidth and delay, and source-specific
forwarding adds protocol and memory requirements. BIDIR-PIM dispenses with both: packets are forwarded natively from
a source to the RP using shared-tree state, with no data-driven events.

## Terms (RFC 5015 section 2.1)
- **RPA (Rendezvous Point Address)**: the address that roots the distribution tree for a range of groups. It must be
  routable from all routers in the PIM domain and need not correspond to an interface of a real router (unlike a
  PIM-SM RP). Joins for a BIDIR-PIM group propagate hop by hop toward the RPA.
- **RPL (Rendezvous Point Link)**: the physical link the RPA belongs to. All traffic for groups mapped to that RPA is
  forwarded on the RPL. It is the only link with no DF election.
- **DF (Designated Forwarder)**: one per RPA on every other link (multi-access and point-to-point). It is the router
  on the link with the best route to the RPA, comparing MRIB-provided metrics. It forwards downstream traffic onto
  the link, forwards upstream traffic from the link toward the RPL, processes Joins from downstream routers, and
  ensures delivery to local receivers learned through IGMP or MLD.
- Upstream is toward the RPA; downstream is away from it. Joins are directed only to the DF on the RPF interface.
- The MRIB supplies the routing metrics used for DF election, and the RPF interface is found by looking up the RPA in it.

## Operating notes
- The RPA must be routable from all routers in the PIM domain, so check unicast reachability of it first.
- Confirm platform and release support for BIDIR-PIM in the vendor's release notes.
- Command syntax and `show` output differ by IOS, IOS XE and platform. Take them from the vendor's command reference
  for your release; they are not covered here.

## Checked
Checked 2026-11-08 against RFC 5015 (sections 1 and 2.1): PIM-SM Register and source-state overheads, RPA, RPL, DF,
MRIB, upstream and downstream, Join direction. Removed: Cisco configuration and `show` examples, state-saving
claims, SSM and TCAM remarks, and phantom-RP configuration, none of which the RFC text read states or whose Cisco page
was unreadable (404).
Method: documentation only; no commands were run.
