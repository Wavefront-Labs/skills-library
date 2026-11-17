---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-spine-leaf-underlay-bgp-ecmp
name: sw-spine-leaf-underlay-bgp-ecmp
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [spine-leaf-design, ecmp-hashing, fabric-underlay-bgp, sw-l3-fabric]
level: advanced
status: draft
description: "Design a routed spine-leaf underlay: link sizing, oversubscription, ECMP hashing and eBGP-per-node versus IGP choices."
sources:
  - https://www.juniper.net/documentation/
  - https://www.rfc-editor.org/rfc/rfc4271
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spine-leaf underlay

- Every leaf connects to every spine; the fabric is routed (L3) so all uplinks carry traffic using ECMP. Add capacity by adding spines.
- Underlay routing: eBGP with one ASN per leaf (or per rack) and a shared spine ASN is common; OSPF/IS-IS are also used. Choose by team skills and scale.
- ECMP hashes on 5-tuple; elephant flows can collide on a path. Tune hash fields; consider flowlet or adaptive load balancing where supported.
- Use point-to-point /31 links, BFD for fast failure detection, and consistent MTU (jumbo 9216) across the fabric.
- Plan oversubscription at the leaf (server ports vs uplinks).

## Verify
- [ ] Each leaf shows the expected number of ECMP next hops for remote prefixes.
