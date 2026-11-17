---
id: computing-software.systems-network-administration.cisco-networking.sd-access-fabric-roles
name: sd-access-fabric-roles
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, sda-fabric, sd-access, lisp, vxlan, control-plane-node, border-node, edge-node, scalable-group-tag]
level: practitioner
status: draft
description: "Understand Cisco SD-Access fabric roles: LISP control plane, VXLAN data plane, edge/border/control nodes, virtual networks and SGT policy, and how to verify them."
sources:
  - https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-sda-design-guide.html
  - https://www.rfc-editor.org/rfc/rfc9300
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SD-Access fabric roles

SD-Access is a campus overlay built and managed by Catalyst Center.
- **Underlay:** routed IS-IS (usually via LAN automation) between all fabric switches; loopbacks
  reachable.
- **Control plane:** LISP. Endpoints register (EID -> RLOC) with the control plane node (map server/resolver).
- **Data plane:** VXLAN-GPO carrying VN (VRF) and SGT in the header.
- **Policy plane:** TrustSec SGTs from ISE; SGACLs enforced at egress edge.

## Roles
| Role | Does |
|---|---|
| Edge node | access switch, anycast gateway for endpoints, registers EIDs |
| Control plane node | LISP MS/MR host tracking database |
| Border node | connects fabric to outside: internal border (known routes), external (default) |
| Fabric WLC / AP | wireless integrated; APs in fabric VXLAN to edge |
| Extended node | L2 switch (IE, compact) hanging off an edge |

Anycast gateway: same SVI IP/MAC on every edge for a pool, so hosts roam without changing gateway.
Virtual networks (VNs) = VRFs; inter-VN traffic leaves via the border to a fusion router/firewall.

## Verify (CLI on fabric nodes)
```
show lisp site                                     ! control plane: registered EIDs
show lisp instance-id 4099 ipv4 database            ! edge: local EIDs
show lisp instance-id 4099 ipv4 map-cache           ! edge: resolved remote EIDs
show cts role-based permissions                     ! SGACL policy downloaded
show device-tracking database                       ! endpoint learning on edge
```
- [ ] Endpoint registers on CP node within seconds of connecting; map-cache populated on demand; SGT assigned.
