---
id: creative-arts.theatre.lighting-design.sacn-and-art-net-lighting-networks
name: sacn-and-art-net-lighting-networks
category: creative-arts
field: theatre
product: lighting-design
tags: [theatre, lighting-design, dmx, sacn, art-net, e1-31, ethernet-lighting, multicast, unicast, nodes, gateways, priority, vlan, lighting-network]
level: practitioner
status: draft
description: "Run DMX over Ethernet with sACN and Art-Net: universes, multicast vs unicast, nodes/gateways, priorities and merging, IP schemes and network hygiene."
sources:
  - "https://tsp.esta.org/tsp/documents/published_docs.php"
  - "https://art-net.org.uk/"
  - "https://en.wikipedia.org/wiki/Streaming_ACN"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# sACN and Art-Net lighting networks

## Protocols
- **sACN** (Streaming ACN, ANSI E1.31): DMX universes over UDP/IP, usually
  **multicast** (one address per universe: 239.255.x.y), universes 1-63,999,
  **priority** per source (0-200, default 100) — highest priority wins,
  allowing backup consoles and overrides. Universe synchronisation optional.
- **Art-Net** (Artistic Licence, v4): DMX over UDP; historically broadcast,
  Art-Net 3/4 supports unicast; addresses by Net/Sub-Net/Universe (port
  addresses up to 32,768); default IP range 2.x.x.x or 10.x.x.x.
Most consoles and nodes support both; choose one per system where possible.

## Building the network
1. **Topology**: console → managed switch → **nodes/gateways** (convert to DMX
   for fixtures) or directly to network-native fixtures.
2. **IP scheme**: static addresses in one subnet (e.g. 10.101.x.x/16 per
   ETC convention, or 2.0.0.x/8 for Art-Net); document in a spreadsheet.
3. **Managed switches** with **IGMP snooping** (and a querier) for sACN multicast,
   so universes go only where subscribed; otherwise multicast floods every port.
4. Separate lighting traffic from other networks (dedicated switches or VLANs);
   no internet/guest devices on the lighting network.
5. Configure each node's ports: universe, protocol, merge mode (HTP/LTP or
   sACN priority).
6. Backup console sends at lower priority (sACN) or tracking backup takes over.

## Troubleshooting
- Tools: sACNView, ETC Concert/Net3 utilities, Art-Net DMX-Workshop, Wireshark.
- Check: link lights, IP conflicts, universe numbers, IGMP, priority clashes
  (two sources at the same priority cause flicker/merging).

## Gotchas
- Broadcast Art-Net on large rigs saturating unmanaged networks.
- Two consoles sending the same universe at the same priority.
- Universe numbering off-by-one between Art-Net (0-based) and sACN (1-based).

## Verify
- [ ] IP and universe plan documented.
- [ ] IGMP snooping/querier configured for sACN.
- [ ] Failover/priority tested with the backup source.
