---
id: computing-software.networking-hardware-and-wireless.tailscale.custom-derp-servers
name: custom-derp-servers
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [custom-derp, derp-requirements, peer-relays]
level: advanced
status: docs-checked
description: "Learn the limitations and requirements before running your own DERP server."
sources: ["https://tailscale.com/kb/1118"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom DERP servers

Goal: judge whether a custom DERP server is worthwhile.

The docs say most tailnets do not need one. Tailscale Peer Relays run in your own infrastructure, offer lower latency than DERP, avoid DERP egress data transfer costs in cloud environments, and avoid the overhead of maintaining custom DERP servers. A valid reason to run your own: restrict where encrypted traffic routes for compliance.

**Limitations**

- You must build, deploy and update the DERP server yourself; it is an advanced operation.
- No device sharing or other cross-tailnet features.
- Like normal DERP servers they cannot see the encrypted data, so they do not help network-level debugging.
- They miss some optimizations from the Tailscale control plane.
- They do not work behind a firewall or load balancer.
- Mullvad exit nodes do not work with them.
- Regional routing does not work with them; MagicRoute supports custom DERP servers (see Route selection).

**Requirements**

- Direct internet access; the server must not sit behind NAT devices such as firewalls or load balancers.
- Allow ICMP traffic.
- Open ports for HTTP (80), HTTPS (443) and STUN (3478) to the internet.

**Checklist**

1. Try peer relays first.
2. Provision a directly connected host.
3. Open HTTP, HTTPS, STUN and allow ICMP.

## Checked

2026-11-09. Confirmed against the Tailscale Custom DERP servers page: peer relay comparison, compliance use, every limitation and requirement listed, and the default port numbers. Added the port numbers from the page.

Method: docs-checked 2026-11-09 against tailscale.com/kb/1118 (Custom DERP servers), read in full.
