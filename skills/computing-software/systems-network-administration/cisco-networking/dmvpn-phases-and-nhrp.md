---
id: computing-software.systems-network-administration.cisco-networking.dmvpn-phases-and-nhrp
name: dmvpn-phases-and-nhrp
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, vpn, dmvpn, nhrp, mgre, ipsec-profile, spoke-to-spoke, phase-2, phase-3, nhrp-redirect, nhrp-shortcut]
level: practitioner
status: docs-checked
description: "DMVPN on IOS XE: hub and spoke mGRE with NHRP and an IPsec profile, and how Phase 2 and Phase 3 differ in routing, NHRP redirect and shortcut, EIGRP and OSPF settings."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_dmvpn/configuration/xe-16/sec-conn-dmvpn-xe-16-book/sec-conn-dmvpn-dmvpn.html
  - https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/111976-dmvpn-troubleshoot-00.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DMVPN phases and NHRP

DMVPN combines GRE tunnels, IPsec encryption and NHRP. One mGRE tunnel interface on the hub handles all spokes with a single IPsec profile and no crypto ACLs, so hub configuration size stays constant as spokes are added.

## Hub tunnel (from the Cisco configuration guide)
```
interface Tunnel0
 ip address 10.0.0.1 255.255.255.0
 ip mtu 1400
 ip nhrp authentication <STRING>
 ip nhrp map multicast dynamic
 ip nhrp network-id 99
 ip tcp adjust-mss 1360
 tunnel source GigabitEthernet0/0/0
 tunnel mode gre multipoint
 tunnel key 100000                      ! optional
 tunnel protection ipsec profile <PROFILE>
```
- The NHRP authentication string must be the same on all hubs and spokes in the same DMVPN network; so must the tunnel key if used.
- NHRP network IDs are locally significant and need not match, though unique IDs across the DMVPN are sensible for maintenance. The range is 1 to 4294967295.
- From IOS XE Denali 16.3, `ip nhrp map multicast dynamic` and `ip nhrp network-id` are enabled by default.
- For the NAT-transparency enhancement the transform set must use IPsec transport mode. All spokes must have a unique address after NAT.

## Spoke tunnel
```
interface Tunnel0
 ip address 10.0.0.11 255.255.255.0
 ip mtu 1400
 ip nhrp authentication <STRING>
 ip nhrp map 10.0.0.1 <HUB_PUBLIC_IP>
 ip nhrp map multicast <HUB_PUBLIC_IP>
 ip nhrp nhs 10.0.0.1
 ip nhrp network-id 99
 ip tcp adjust-mss 1360
 tunnel source GigabitEthernet0/0/0
 tunnel mode gre multipoint             ! or: tunnel destination <HUB_PUBLIC_IP>
 tunnel protection ipsec profile <PROFILE>
```
- Per the guide, `tunnel mode gre multipoint` is for traffic that can use dynamic spoke-to-spoke tunnels; `tunnel destination` is for hub-and-spoke tunnels only.
- The guide's `ip nhrp map` line statically maps the hub tunnel IP to the hub public IP; `ip nhrp nhs` names the hub as next-hop server.

## Phases (from the Cisco DMVPN troubleshooting document)
Routing behaviour depends on the DMVPN phase and the routing protocol; a configuration right for Phase 2 can stop Phase 3 working as intended.

| | Phase 2 | Phase 3 |
|---|---|---|
| Next hop | spokes must learn remote spoke networks with the remote spoke tunnel IP as next hop; the hub must not rewrite it | the hub can remain the next hop |
| Hub summary or default | generally not suitable (keeps the hub in the data path) | supported |
| Spoke-to-spoke trigger | originating spoke, from the routing-table next hop | hub forwards the first packet and sends an NHRP redirect; the spoke sends an NHRP resolution request and builds the direct tunnel |
| Hub config | no redirect | `ip nhrp redirect` on the hub tunnel |
| Spoke config | none beyond NHRP | `ip nhrp shortcut` on each spoke tunnel |

- Phase 2 EIGRP: on the hub tunnel, `no ip next-hop-self eigrp <as-number>` and `no ip split-horizon eigrp <as-number>`. Do not summarise spoke routes at the hub.
- Phase 2 OSPF: the document suggests network type broadcast on hub and spokes (`ip ospf network broadcast`) and `ip ospf priority 0` on spokes so they do not become DR.
- Phase 3 EIGRP/OSPF: the hub can advertise summary or default routes and does not need to preserve the spoke next hop. This skill does not reproduce the per-protocol Phase 3 commands.
- Phase 1 is only touched in the guide as the feature name; the sources do not describe its routing rules, so they are not stated here.

## Verify
Commands named by the configuration guide: `show dmvpn`, `show crypto ipsec sa`, `show ip nhrp traffic`. The troubleshooting document also uses `show ip nhrp` to confirm spokes registered with the hub and `show interface Tunnel<n>`, and notes that ESP (IP protocol 50) must be permitted in the underlay.
- [ ] Tunnel interface up/up, spokes registered at the hub, remote tunnel IP pings.

## Checked
Date: 2026-11-08. Pages: the DMVPN configuration guide (xe-16, 86k characters; searched by command and read around the hub, spoke and NAT-transparency sections, not end to end) and the Cisco DMVPN troubleshooting document (51k; hub tunnel sample and the routing-by-phase sections read in full).
Confirmed: mGRE/IPsec profile hub design, hub and spoke command lists and their explanations, authentication-string and tunnel-key matching, network-ID note and range, 16.3 defaults, transport-mode need for NAT transparency, Phase 2 and Phase 3 routing behaviour, redirect and shortcut commands, EIGRP and OSPF Phase 2 settings, verification commands, ESP note.
Removed: the one-line `ip nhrp nhs ... nbma ... multicast` spoke form, "transport mode recommended" (the guide only requires it for NAT transparency), the Phase 1 row, "Phase 3 is the default choice" and "best scaling", the traceroute behaviour check, and the `ip nhrp redirect` / `ip nhrp shortcut` lines inside the base hub and spoke blocks (shown only in the phase table).
Method: documentation only; no commands were run.
