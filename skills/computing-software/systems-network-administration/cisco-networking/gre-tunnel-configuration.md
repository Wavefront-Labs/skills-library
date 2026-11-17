---
id: computing-software.systems-network-administration.cisco-networking.gre-tunnel-configuration
name: gre-tunnel-configuration
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, vpn, gre, gre-tunnel, tunnel-interface, recursive-routing, tunnel-keepalive, tunnel-source, tunnel-destination, tunnel-state, mgre]
level: practitioner
status: docs-checked
description: "Build a point-to-point GRE tunnel on IOS and read its interface state: tunnel source and destination rules, keepalives, recursion, tunnel protection and mGRE differences."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/generic-routing-encapsulation-gre/118361-technote-gre-00.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GRE tunnel configuration and state

GRE tunnels are stateless: an endpoint keeps no information about the state or availability of the remote endpoint.
By default the local router therefore cannot bring the tunnel's line protocol down just because the far end is
unreachable. Line protocol going down is what removes static routes that point out of the tunnel, which lets a
floating static route or PBR pick an alternate path, so this matters for failover design. GRE is not encryption;
the Cisco page treats IPsec protection as a separate feature (see below).

## Minimal point-to-point tunnel
```
interface Tunnel1
 ip address 10.1.1.1 255.255.255.0
 tunnel source Loopback1
 tunnel destination 10.0.0.1
```
Mirror it on the other router. The tunnel destination must be routable but need not be reachable.

## The four interface states
- up/up: administratively up and protocol up, passes traffic.
- administratively down/down: shut down.
- up/down: administratively up but something keeps line protocol down.
- reset/down: usually transient after a software reset, for example a tunnel misconfigured with an NHS that is its own
  IP address.

A new tunnel with no other configuration is not shut down and sits up/down, because it has no source or destination.
For a point-to-point tunnel to go up/up it needs a valid source (an interface that is itself up/up with an IP
address) and a routable destination. For `tunnel mode gre multipoint` (mGRE) only a valid source is needed.

## Why a point-to-point tunnel is up/down locally
Three local reasons, per the page:
1. No route, including no default route, to the tunnel destination.
2. The interface anchoring the tunnel source is down.
3. The route to the tunnel destination goes through the tunnel itself (recursion).

Fix recursion by making sure the destination is reached through the underlay, not the overlay.

## Keepalives, protection, redundancy
- Keepalives cover the case where tunnelled packets are forwarded but lost before the far end. From IOS 12.2(8)T a
  P2P GRE interface can shut itself down when keepalives fail for a period of time. They apply to P2P tunnels only,
  not mGRE.
- With tunnel protection (IOS 15.4(3)M / 15.4(3)S and later) the GRE line protocol follows the IPsec SA state, so it
  can stay down until the IPsec session is fully established.
- If the tunnel source is a redundancy address such as an HSRP virtual IP, the tunnel tracks the redundancy state and
  stays line-protocol down until the state is ACTIVE.
- mGRE line protocol is down when the source interface is down, or when Interface State Control for DMVPN is enabled
  and no NHS responds.

## Verify
```
show ip interface brief | include Tunnel
show tunnel interface tunnel <n>      ! "Linestate" and "Internal linestate ... evaluated down" lines give the reason
```
- [ ] State is up/up; `show ip route <tunnel-destination>` does not point at the tunnel itself.

## Checked
Date: 2026-11-08. Read in full: Cisco "Determine What Impacts GRE Tunnel Interface States" (document 118361, revision 4.0, Oct 2023).
The second cited page (22327 GRE flap) is a 404 and was dropped.
Confirmed: everything above, from the page's background, four states, P2P and mGRE rules, keepalive, tunnel
protection, redundancy state and troubleshooting sections.
Removed: the 24-byte overhead, `ip mtu 1400` and `ip tcp adjust-mss 1360` figures, 60-80 byte IPsec overhead, the
`%TUN-5-RECURDOWN` message, the OSPF over tunnel config, `tunnel vrf`, static-route pinning, the NAT/PAT and firewall
gotchas, `keepalive 5 3` values and the ping/DF test steps. Protocol number 47 appears on the page only in debug output
and was dropped as a claim.
Method: documentation only; no commands were run.
