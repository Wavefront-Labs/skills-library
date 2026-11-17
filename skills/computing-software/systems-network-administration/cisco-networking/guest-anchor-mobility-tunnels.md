---
id: computing-software.systems-network-administration.cisco-networking.guest-anchor-mobility-tunnels
name: guest-anchor-mobility-tunnels
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst-9800, guest-anchor, mobility-anchor, mobility-tunnel, guest-wifi, dmz, wlc]
level: practitioner
status: draft
description: "Tunnel guest Wi-Fi to a DMZ anchor WLC: mobility peers, matching WLAN and policy profiles on foreign and anchor, firewall ports, and troubleshooting mobility state."
sources:
  - https://www.cisco.com/c/en/us/support/docs/wireless/catalyst-9800-series-wireless-controllers/214904-configure-mobility-topologies-on-9800-wl.html
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/17-9/config-guide/b_wl_17_9_cg.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Guest anchor and mobility tunnels

Guest traffic from every campus controller (foreign) is carried in a CAPWAP mobility tunnel to an
anchor controller in the DMZ, where it gets a DMZ VLAN and internet-only access. Internal
switches never see guest VLANs.

## Mobility peering (both directions)
On foreign:
```
wireless mobility group name CAMPUS
wireless mobility group member mac-address 00aa.bbcc.0002 ip 192.0.2.10 public-ip 192.0.2.10 group DMZ
```
On anchor: the mirror entry for each foreign. Check:
```
show wireless mobility summary
!  Status: Up   (Control and Data path both up)
```
Firewall between them: UDP 16666 (control, DTLS) and UDP 16667 (data). ICMP helps the keepalive
diagnosis (`mobility ping` uses it).

## WLAN and policy profile
- The WLAN profile (SSID, security, profile name) must be identical on foreign and anchor.
- Foreign policy profile: `mobility anchor 192.0.2.10 priority 1`; VLAN on foreign is irrelevant.
- Anchor policy profile: `mobility anchor` (no IP, marks itself as anchor) plus the DMZ VLAN.
- The anchor does not need APs for this WLAN; it just needs the WLAN enabled and attached to a
  policy tag (any).

## Web auth placement
Web authentication (LWA/CWA) runs on the anchor. For CWA with ISE, the anchor sends RADIUS and
receives CoA, so ISE needs the anchor as a network device and the redirect ACL on the anchor.

## Troubleshooting
```
show wireless client mac-address <mac> detail | include Mobility|Anchor|VLAN
!  Mobility Role: Export Foreign (on foreign)  /  Export Anchor (on anchor)
show wireless mobility peer ip 192.0.2.10
```
Common failures:
- Mobility Control Up / Data Down: UDP 16667 blocked or NAT in path without public-ip set.
- Client stuck in Mobility state: WLAN profile names or security differ between foreign and anchor.
- Client gets an internal IP: anchor not configured on the foreign policy profile.

## Gotchas
- MTU: mobility tunnel adds CAPWAP+DTLS overhead; large guest downloads fragment if the path MTU is
  low. Leave path MTU discovery on.
- Use at least two anchors with different priorities for redundancy.

## Verify
- [ ] Guest client shows Export Foreign/Anchor roles and an address from the DMZ scope.
- [ ] Guest cannot reach internal subnets.
