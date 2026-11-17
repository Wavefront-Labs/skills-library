---
id: computing-software.cloud-infrastructure-engineering.google-cloud.migrating-classic-vpn-to-ha-vpn
name: migrating-classic-vpn-to-ha-vpn
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, hybrid-connectivity, classic-vpn-migration, policy-based-vpn, ha-vpn, static-routing]
level: advanced
status: docs-checked
description: "Move from Classic VPN (static or policy-based routing) to HA VPN with BGP: inventory, parallel build, route priority cutover, and cleanup, given Classic VPN's dynamic-routing deprecation."
sources: ["https://cloud.google.com/network-connectivity/docs/vpn/how-to/moving-to-ha-vpn", "https://cloud.google.com/network-connectivity/docs/vpn/deprecations/classic-vpn-deprecation", "https://cloud.google.com/network-connectivity/docs/vpn/concepts/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating Classic VPN to HA VPN

Classic VPN: single interface, 99.9% SLA, static (policy-based or route-based) routing. Dynamic (BGP) routing on Classic VPN was deprecated on 1 August 2025: new BGP Classic tunnels cannot be created, and existing ones keep working without an availability SLA.
HA VPN: two interfaces, 99.99% SLA for most topologies, dynamic routing (BGP) only.

## 1. Inventory
```bash
gcloud compute target-vpn-gateways list
gcloud compute vpn-tunnels list --format='table(name,region,targetVpnGateway,peerIp,localTrafficSelector,remoteTrafficSelector,router)'
gcloud compute routes list --filter='nextHopVpnTunnel:*'
```
Note static routes, traffic selectors (policy-based), peer devices and whether they support BGP.
If the peer can't do BGP, HA VPN isn't possible: keep Classic with static routes or replace the device.

## 2. Build HA VPN in parallel
Create HA VPN gateway, Cloud Router, external peer gateway, two tunnels and BGP (see HA VPN setup). The HA VPN gateway gets two new external IP addresses; the Classic gateway's address cannot be kept, and existing Classic tunnels cannot be converted, so you create new tunnels and delete the old ones. The peer device must support BGP.

## 3. Cut over with route preference
- Run the Classic tunnels and the HA VPN tunnels in parallel, verify the HA VPN tunnels and BGP sessions, and check the HA VPN gateway's high-availability configuration.
- Then delete the Classic tunnels; the migration page also tells you to remove any leftover custom static routes.
- Make the peer prefer the new tunnels before removing the old ones.

## 4. Clean up
Delete the tunnels on the Classic gateway, leftover custom static routes, the Classic VPN gateway, and release any static external IP addresses it used.

## Gotchas
- During the parallel phase the peer device runs sessions to both the Classic and the HA VPN gateway IPs; confirm the device supports that many peers and tunnel interfaces.
- Classic VPN BGP configurations that exist today are unsupported for new builds; the deprecation page lists what can still be created (static routing).

## Verify
- [ ] Traffic counters on Classic tunnels go to zero, HA VPN tunnels carry traffic, BGP up on both tunnels; failover test passes.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Confirmed (deprecation page): Classic VPN dynamic routing (BGP) deprecated on August 1 2025, creation no longer supported, existing tunnels continue without an availability SLA; static routing Classic tunnels remain supported.
- Confirmed (moving to HA VPN page): peer must support BGP; HA VPN gets two new external IPs; Classic tunnels cannot be migrated, new tunnels are created and old ones deleted; verify then delete tunnels, leftover custom static routes, the Classic gateway and its static IPs.
- Confirmed (Cloud VPN overview feature table): HA VPN dynamic routing only, 99.99% SLA for most topologies; Classic VPN static routing only, 99.9% SLA.
- Removed: route priority cutover specifics, MED guidance, traffic selector and CHILD_SA claims and the more-specific-static-route claim (not found in the pages read).

Method: documentation only; no commands were run.
