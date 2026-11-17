---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-instance-and-policy-defaults
name: bgp-instance-and-policy-defaults
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, router-bgp, router-id, ebgp-requires-policy, import-check, as-notation]
level: practitioner
status: docs-checked
description: "Start a BGP instance in FRR with router bgp, VRF and view variants, set the router-id, and understand ebgp-requires-policy, network import-check and AS notation."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP instance and policy defaults
- `router bgp ASN` enables BGP; the ASN is a number or two numbers separated by a period. `router bgp ASN vrf VRFNAME` needs a VRF configured in the kernel; each additional AS must use a unique VRF (the same AS may use different VRFs). `router bgp ASN view NAME` creates a view whose selected routes are not installed in the kernel.
- `router bgp ASN as-notation dot|dot+|plain` forces output format.
- `bgp router-id A.B.C.D`: without zebra the router ID defaults to 0.0.0.0, which is invalid and blocks sessions, so set it manually.
- `bgp ebgp-requires-policy` (RFC 8212) needs both incoming and outgoing filters on eBGP sessions: without an incoming filter no routes are accepted, without an outgoing filter none are announced. Enabled by default for the traditional profile, disabled for datacenter. Clear the session after changing it. A missing filter shows "(Policy)" in `show bgp summary`.
- `bgp network import-check` / `no bgp network import-check`: with it a `network` prefix must exist in the RIB. Both profiles require it from 7.4 onward.
- `bgp enforce-first-as` is enabled by default (`neighbor PEER enforce-first-as` per peer); `bgp suppress-duplicates` is enabled by default.
- `bgp no-rib` disables RIB installation at runtime (replaces `-Z`/`--no_zebra`).
- `bgp fast-external-failover` resets eBGP peers on link flap (default on).
- Session events can be traced with `debug bgp neighbor-events [detail]`.

## Checked

2026-11-09. Read the FRR BGP page sections "ASN and Router ID", "Multiple Autonomous Systems", "Views", "Require policy on EBGP", "Enforce first AS", "Suppress duplicate updates", `bgp network import-check`, `bgp fast-external-failover`, "AS-notation support", `bgp no-rib` and the `debug bgp neighbor-events` entry via a local text copy; every command and default above matches. The page also notes that peering to a route server usually needs enforce-first-as disabled.
Method: documentation only; no commands were run.
