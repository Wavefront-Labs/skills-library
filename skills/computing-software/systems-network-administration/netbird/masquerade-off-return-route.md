---
id: computing-software.systems-network-administration.netbird.masquerade-off-return-route
name: masquerade-off-return-route
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, masquerade, return-route, source-ip-visibility, netplan]
level: advanced
status: docs-checked
description: "Disable masquerade on a Linux NetBird routing peer to preserve overlay source IPs: adding and persisting the return route, testing, HA limits and security."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/networks/masquerade.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Masquerade (SNAT to the routing peer's LAN IP) is on by default. Turn it off only when destinations must see real overlay IPs, for auditing or overlay-IP firewall rules. Linux routing peers only.

Steps:
1. Disable under Network Routing in the dashboard, or PUT to the networks/routers API with `"masquerade": false`.
2. Add a return route on the destination host (or its default gateway) for the NetBird range via the routing peer's LAN IP.
3. Prefer your account's /16 over the default `100.64.0.0/10`; find it with `netbird status` on an enrolled peer.
4. Test first with a temporary `ip route add`, confirm from a NetBird peer, then remove.
5. Persist: check `/etc/netplan/`. If YAML files exist, add the route under the interface's `routes:` and run `netplan apply`; if empty, use a systemd-networkd drop-in and `networkctl reload`. Do not mix methods.
6. Verify with `ip route show` after reboot and tcpdump on the destination.

HA is harder: the route cannot follow failover by itself. Use different metrics and VRRP or a health-checked router to move the next hop; health checks should test through the tunnel. Never point the route at two peers at once. Established TCP may survive failover but stall; new connections fail until both sides converge.

Security: the route exposes the destination subnet to NetBird, so restrict with policies and host firewalls.

## Checked

2026-11-04. Confirmed against the NetBird masquerade page: default on, Linux only, dashboard and API toggle, return route and per-account /16, test route, netplan and systemd-networkd persistence, verification, HA guidance and warning, security note. Nothing removed.
Method: documentation only; no commands were run.
