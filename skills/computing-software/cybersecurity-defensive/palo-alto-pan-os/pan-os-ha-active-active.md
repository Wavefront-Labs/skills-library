---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-ha-active-active
name: pan-os-ha-active-active
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [ha-active-active, pan-os, session-owner, session-setup, virtual-address, floating-ip, asymmetric-routing]
level: practitioner
status: draft
description: "Configure PAN-OS active/active HA with device IDs, floating addresses, session owner and setup, and handle asymmetric routing."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/high-availability/set-up-active-active-ha"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: both firewalls forward traffic, typically with asymmetric routing or load sharing upstream.

```
configure
set deviceconfig high-availability group group-id 1 mode active-active device-id 0 peer-ip-address 192.0.2.202
set deviceconfig high-availability group group-id 1 mode active-active network-configuration sync [ virtual-router routing-table ]
set deviceconfig high-availability group group-id 1 mode active-active packet-forwarding yes
set deviceconfig high-availability interface ha3 port ha3-a
commit
```
Peer uses device-id 1. A third link, HA3, carries packet forwarding for sessions where the owner is the other device.

Concepts
- Session owner: processes Content-ID. Session setup device: does the first-packet and NAT. Set owner selection (primary device or first packet) in the Active/Active config.
- Virtual addresses: floating IP (failover) or ARP load sharing (active-active) used by upstream and downstream devices.
- NAT in A/A needs `device-binding` on rules (confirm) so translation is tied to one firewall.

Gotchas
- A/A is more complex than A/P; use it only for asymmetric routing designs. Many Layer 3 designs run better A/P.
- Dynamic routing with A/A requires each peer to have its own router ID; do not sync it.
- Without HA3 the asymmetric flows drop.

## Verify
```
show high-availability state
show high-availability virtual-address
show session id <ID>
```
The session detail shows owner and setup device; test failover by suspending one peer.
