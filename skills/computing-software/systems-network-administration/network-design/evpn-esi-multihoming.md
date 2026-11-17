---
id: computing-software.systems-network-administration.network-design.evpn-esi-multihoming
name: evpn-esi-multihoming
category: computing-software
field: systems-network-administration
product: network-design
tags: [evpn, esi, evpn-multihoming, all-active, route-type-1, route-type-4, designated-forwarder, mlag-replacement]
level: practitioner
status: docs-checked
description: "Dual-home servers to two leaves with EVPN ESI multihoming instead of MLAG: ESI and LACP system-id, all-active vs single-active, DF election, and aliasing."
sources:
  - https://www.rfc-editor.org/rfc/rfc7432#section-8
  - https://www.arista.com/en/um-eos/eos-evpn-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EVPN ESI multihoming

MLAG ties two leaves together with a peer link and proprietary sync. EVPN multihoming (RFC 7432)
does the same through BGP: any number of leaves (usually 2) share an Ethernet Segment (ES) toward a
server or switch, identified by an Ethernet Segment Identifier (ESI; RFC 7432 section 5).

## Building blocks
- ESI: same value on every leaf attached to the segment, configured (type 0) or auto-derived
  from LACP (type 1) or a MAC (type 3) per RFC 7432.
- LACP system-id: identical on both leaves so the server sees one LACP partner and bundles the
  links into one port-channel.
- Route type 4 (Ethernet Segment route): leaves discover each other on the ES and elect a
  Designated Forwarder (DF) per VLAN/VNI for BUM traffic (only the DF floods BUM to the server, so
  no duplicates).
- Route type 1 (Ethernet A-D): per-ES and per-EVI; enables aliasing (remote leaves load-balance to
  both leaves even if only one advertised the MAC); RFC 7432 section 8.4 covers aliasing and backup path.
- Split horizon: BUM received from the ES and sent to the peer leaf is not sent back into the ES
  (RFC 7432 uses an ESI label for MPLS; see RFC 8365 for VXLAN).

## Modes
- All-active: both leaves forward unicast (port-channel on the server).
- Single-active: only the DF forwards; used for active/standby attachments or when the device cannot
  bundle.

## Configuration
Syntax is vendor-specific; use the vendor's EVPN multihoming guide. The ESI and the LACP system-id
must match on every leaf of the segment.

## Why choose it over MLAG
No peer link to size or lose, standards-based, scales to more than two leaves, consistent with the
EVPN control plane. Cost: more BGP state and platform support requirements.

## Verify
- [ ] The vendor's EVPN commands show Ethernet segment routes from every leaf on the segment, one
  Designated Forwarder per VLAN and two next hops (aliasing) for server MACs; pulling one server link
  keeps traffic flowing.

## Checked

- Date: 2026-10-28
- Confirmed: RFC 7432 ESI types 0, 1 and 3, Ethernet segment, split horizon with ESI label, aliasing and backup path, Designated Forwarder election; Arista EVPN overview lists Ethernet A-D (type 1) and related route types.
- Removed: the 10-byte figure, the sample ESI values, mass-withdraw timing and the sub-second claim, the Arista configuration block, the Cisco vPC remark, the show commands, the 'default for DC servers' claim.

Method: documentation only; no commands were run.
