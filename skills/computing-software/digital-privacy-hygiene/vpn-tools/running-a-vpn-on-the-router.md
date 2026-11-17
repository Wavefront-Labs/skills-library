---
id: computing-software.digital-privacy-hygiene.vpn-tools.running-a-vpn-on-the-router
name: running-a-vpn-on-the-router
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, router-vpn, vpn-configuration, openwrt]
level: practitioner
status: draft
description: "Put a commercial VPN on an OpenWrt or GL.iNet router to cover TVs and consoles, with policy routing, DNS through the tunnel and a kill switch."
sources:
  - "https://openwrt.org/docs/guide-user/services/vpn/wireguard/client"
  - "https://openwrt.org/docs/guide-user/network/routing/pbr"
  - "https://docs.gl-inet.com/router/en/4/interface_guide/wireguard_client/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Running a VPN on the router

**Goal:** devices that can't run VPN apps (smart TVs, consoles, IoT) go through the tunnel, without breaking the
whole household.

## Hardware
OpenWrt-capable router or a GL.iNet travel/home router (OpenWrt-based with a VPN client UI). Router CPU limits
WireGuard throughput; check reviews for real speeds.

## OpenWrt WireGuard client
1. `opkg update && opkg install luci-proto-wireguard`
2. Get a WireGuard config from the provider (private key, address, DNS, peer public key, endpoint).
3. Network > Interfaces > Add new > Protocol WireGuard VPN: paste private key, address; Peers > add peer with
   public key, endpoint, AllowedIPs `0.0.0.0/0, ::/0`, "Route Allowed IPs" on, keepalive 25.
4. Firewall: put the interface in a `vpn` zone with masquerading; forward `lan` > `vpn`; remove `lan` > `wan`
   forwarding for a kill switch.
5. DNS: set the provider's DNS on the WireGuard interface and in DHCP option 6 (or dnsmasq upstream), so clients
   don't use ISP DNS.

## Only some devices (policy-based routing)
Install `pbr` (luci-app-pbr): route a TV's IP via `vpn`, everything else via `wan`. Or put VPN devices on a
separate SSID/VLAN routed through the tunnel.

## Verify
From a TV browser or a laptop on the routed segment: ip check shows provider IP; DNS leak test shows provider DNS.
Unplug WAN, reconnect: no traffic should leave via wan from routed clients.

## Gotchas
- Streaming services block many VPN IPs; route those devices outside the tunnel if needed.
- One exit IP for the whole house links everyone's activity together.
