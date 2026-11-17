---
id: computing-software.firmware-embedded-development.iot-protocols.thread-6lowpan-addressing
name: thread-6lowpan-addressing
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [thread-6lowpan-addressing, thread-ipv6, thread, mesh-local, rloc, aloc, iot-protocols]
level: practitioner
status: docs-checked
description: "Thread IPv6 addressing: link-local, ML-EID, RLOC, ALOC and global addresses, plus the multicast groups Thread nodes use."
sources:
  - https://openthread.io/guides/thread-primer/ipv6-addressing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread IPv6 addressing

**Goal:** Know the address types on a Thread node and which one applications should use.

## Steps
1. Scopes: link-local (one radio hop), mesh-local (fd00::/8, within the Thread network), global (2000::/3).
2. Link-Local Address (fe80::): IID from the 802.15.4 Extended Address; used for neighbour discovery, link configuration and routing exchange; not routable.
3. Mesh-Local EID (ML-EID): fd00::/8 (a ULA), random IID chosen after commissioning, does not change with topology. Applications should use it.
4. RLOC: Mesh-Local prefix plus IID 0000:00ff:fe00:RLOC16. Generated on attach, used to route within the network, changes with topology, generally not used by applications.
5. ALOC: IID 0000:00ff:fe00:fcXX, used to find the RLOC when it is unknown (0xfc00 Leader, 0xfc01-0xfc0f DHCPv6 Agent, 0xfc10-0xfc2f Service, 0xfc30-0xfc37 Commissioner, 0xfc40-0xfc4e Neighbor Discovery Agent).
6. Global Unicast Address: 2000::/3, IID by SLAAC, DHCPv6 or set manually by the application layer.
7. Multicast: ff02::1 (link-local, all FTDs and MEDs), ff02::2 (link-local, all FTDs), ff03::1 (mesh-local, all FTDs and MEDs), ff03::2 (mesh-local, all FTDs). Sleepy end devices are reached with unicast-prefix-based multicast (RFC 3306).

## Gotcha
Do not store RLOCs as identity: they change when the topology changes. Use the ML-EID.

## Verify
- [ ] The device's address list shows link-local, ML-EID and RLOC entries
- [ ] ML-EID stays the same after a router change
- [ ] A global address appears when a prefix is available

## Checked

2026-11-08. Confirmed on the OpenThread IPv6 addressing page: scopes and prefixes, every address type, ALOC ranges, multicast table. Corrected: the old skill said ff03::fc is all routers and listed ff03::1 and ff02::1 loosely; the page lists ff02::2 and ff03::2 for FTDs. Link-local prefix is given as fe80::/16 on the page (fe80::/64 removed). Removed: 6LoWPAN compression, 127-byte frame fragmentation and 1280-byte ping, which the page does not cover (it does not mention 6LoWPAN).
Method: documentation only; no commands were run.
