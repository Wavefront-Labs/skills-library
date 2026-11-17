---
id: computing-software.systems-network-administration.netbird.site-to-site-routes
name: site-to-site-routes
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, site-to-site, static-routes, cloud-forwarding, routing-peer-groups]
level: advanced
status: docs-checked
description: "Connect two sites with NetBird routes: setup keys per site, routes with masquerade, bidirectional policies, static routes on clientless devices and cloud forwarding."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/network-routes/use-cases/site-to-site.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Routes are deprecated; the page recommends Networks Site-to-Site for new setups. Routes remain the option when no policy should gate traffic. Subnets must not overlap.

Example: Site A `10.0.0.0/24` (group `site-a-routers`), Site B `10.1.0.0/24` (`site-b-routers`).

1. Setup Keys: one per site auto-assigning that site's group.
2. On each routing peer: `curl -fsSL https://pkgs.netbird.io/install.sh | sh` then `sudo netbird up --setup-key YOUR_SETUP_KEY`.
3. Routes: for Site A use `10.0.0.0/24`, routing peer `site-a-routers`, distribution group `site-b-routers`, Masquerade on; mirror for Site B.
4. Policies: `site-a-routers` to `site-b-routers` and the reverse, All protocols (tighten by port later).
5. Clientless devices need a static route to the other subnet via the local routing peer, preferably on the site router (e.g. destination `10.1.0.0/24`, gateway `10.0.0.50`). Linux test: `sudo ip route add 10.1.0.0/24 via 10.0.0.50`; make permanent with netplan (`sudo netplan apply`) or a systemd-networkd drop-in, not both. Windows: `route -p add 10.1.0.0 mask 255.255.255.0 10.0.0.50`.
6. Verify with ping and then a real service (`curl`), from both sites.

Cloud peers: AWS disable source/destination check and add a route table entry; GCP enable IP forwarding and a custom route; Azure enable NIC IP forwarding, a route table entry and permissive NSGs.

If the routing peer reaches the far site but its LAN devices cannot, check its forward policy.

## Checked

2026-11-04. Confirmed against the NetBird Routes site-to-site page: deprecation note, example subnets and groups, setup keys, install and up commands, route fields, bidirectional policies, static route examples for Windows and Linux, netplan or networkd choice, verification, AWS GCP Azure forwarding notes. Nothing removed.
Method: documentation only; no commands were run.
