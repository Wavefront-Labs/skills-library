---
id: computing-software.systems-network-administration.cisco-networking.wlc-roaming-and-mobility-groups
name: wlc-roaming-and-mobility-groups
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst-9800, wireless, wireless-roaming, mobility-group, l2-roaming, l3-roaming, anchor, mobility-tunnel]
level: practitioner
status: draft
description: "Make clients roam between APs on different 9800 WLCs: mobility groups, mobility tunnels, L2 vs L3 (anchor/foreign) roaming, and checking client mobility state."
sources:
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/17-9/config-guide/b_wl_17_9_cg/m_mobility.html
  - https://www.cisco.com/c/en/us/support/docs/wireless/catalyst-9800-series-wireless-controllers/213912-configure-mobility-topologies-on-9800-wl.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WLC roaming and mobility groups

Roaming within one WLC is local. Between WLCs, the controllers must be in the same
**mobility group** (or domain) and have a mobility tunnel up so client context is handed over.

## Configure (both 9800s)
```
wireless mobility group name CAMPUS
wireless mobility mac-address <own mobility MAC>
wireless mobility group member mac-address <peer MAC> ip 10.99.0.32 public-ip 10.99.0.32 group CAMPUS
```
Requirements: same group name, same virtual IP (e.g. 192.0.2.1), same RF group for good
RRM, UDP 16666 (control) and 16667 (data, CAPWAP) open between controllers, matching
WLAN SSID + security + profile names on both.

## L2 vs L3 roaming
- **L2 roam:** client's VLAN exists on the new WLC; the client entry is moved and the new
  WLC becomes its point of attachment.
- **L3 roam:** VLAN/subnet differs; the original WLC becomes **anchor**, the new one
  **foreign**, traffic tunnelled back so the client keeps its IP.
- Static **guest anchor**: WLAN on the foreign WLC with `mobility anchor <DMZ WLC IP>` sends
  all guest traffic to a DMZ controller.

## Fast roaming
Mobility handles L3 continuity; roam speed comes from 802.11r/OKC/PMK caching (keys
shared via mobility group). See wifi-fast-roaming skills.

## Verify
```
show wireless mobility summary            ! peers, control/data link status UP
show wireless client mac-address <MAC> detail | include Mobility|Anchor|Policy Manager
show wireless mobility ap-list
```
Mobility state of a roamed client shows Local, Anchor or Foreign.
- [ ] Mobility tunnels Up/Up; walk test across controller boundary keeps a continuous ping and the same IP.
