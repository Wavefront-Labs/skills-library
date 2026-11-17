---
id: computing-software.systems-network-administration.cisco-networking.ap-modes-and-flexconnect
name: ap-modes-and-flexconnect
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, wlc, catalyst-9800, lightweight-ap, ap-modes, flexconnect, local-mode, monitor-mode, sniffer-mode, local-switching, central-switching, site-tag, flex-profile, wireless-lan-controller]
level: practitioner
status: draft
description: "Pick AP modes on a Catalyst 9800: local vs FlexConnect switching, monitor and sniffer modes, flex profiles and site tags, and behaviour when the WLC is unreachable."
sources:
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/17-9/config-guide/b_wl_17_9_cg/m_flexconnect.html
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/technical-reference/c9800-config-model.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AP modes and FlexConnect (Catalyst 9800)

## Modes (CCNA 2.6)
| Mode | Use |
|---|---|
| Local (default) | campus APs; all client data tunnelled to WLC in CAPWAP (central switching) |
| FlexConnect | branch APs across a WAN; data switched locally onto a VLAN, control to WLC |
| Monitor | dedicated wIPS/rogue detection/location; no clients |
| Sniffer | captures 802.11 on one channel and streams to a Wireshark host (UDP 5555, peekremote) |
| Bridge / Flex+Bridge | mesh backhaul |
| SE-Connect | spectrum analysis (CleanAir) |
| Sensor / Fabric | Catalyst Center assurance / SD-Access |
Changing mode reboots the AP.

## 9800 config model
APs get behaviour from three tags: **policy tag** (WLAN-to-policy profile), **site tag**
(AP join profile + flex profile; "Enable Local Site" unchecked = FlexConnect), **RF tag**.
```
wireless profile flex BRANCH-FLEX
 native-vlan-id 10
 vlan-name USERS
  vlan-id 20
wireless tag site BRANCH-SITE
 flex-profile BRANCH-FLEX
 no local-site                      ! makes APs with this tag FlexConnect
wireless profile policy BRANCH-POLICY
 no central-switching
 no central-dhcp
 vlan USERS
 no shutdown
ap 00a1.b2c3.d4e5
 site-tag BRANCH-SITE
 policy-tag BRANCH-POLICY
```
The AP switch port is a **trunk** with native VLAN = AP management VLAN and the client VLANs allowed.

## FlexConnect behaviour when the WLC is unreachable (standalone)
- Clients on WLANs with local switching and local/PSK auth stay connected.
- Central-auth 802.1X clients can continue if "local auth"/RADIUS from AP is configured; new
  ones fail otherwise. Centrally switched WLANs stop.
- Use a **flex group** (`site tag` per branch) for fast roaming key caching (OKC/CCKM) between
  APs of the branch.

## Gotchas
- Local mode across a WAN tunnels every client packet to the data centre: hairpin latency and
  WAN load.
- Max APs per site tag affects image predownload and key distribution; keep one site tag per branch.
- Sniffer mode needs Wireshark decode as `peekremote` on UDP 5555.

## Verify
- [ ] `show ap name <AP> config general | i Mode|Site Tag|Flex` shows the intended mode.
- [ ] Clients at the branch get addresses from the local VLAN (`show wireless client summary detail`).
- [ ] Pull the WAN in a test: existing clients on locally switched WLANs keep working.
