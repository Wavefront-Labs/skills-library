---
id: computing-software.systems-network-administration.cisco-networking.vrrp-address-owner-and-interop
name: vrrp-address-owner-and-interop
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, fhrp, vrrp, vrrp-owner, vrrpv3, priority-255, multivendor-gateway, vrrp-preempt, rfc5798]
level: practitioner
status: docs-checked
description: "VRRP per RFC 5798: address owner at priority 255, preemption default, timer arithmetic, Accept_Mode, v2/v3 mixing and what authentication was dropped, for multivendor gateways."
sources:
  - https://datatracker.ietf.org/doc/html/rfc5798
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VRRP address owner and multivendor interop (RFC 5798)

Protocol-level behaviour of VRRPv3 as RFC 5798 states it. Vendor CLI syntax is deliberately not given: look up your
platform's FHRP configuration guide for the commands that set these parameters.

## Address owner
- The router that owns the virtual router's IPv4 or IPv6 address (the VIP equals a real interface address) MUST use
  priority 255. Routers backing up use 1-254, default 100.
- At startup an owner sends an ADVERTISEMENT and a gratuitous ARP (IPv4) or unsolicited Neighbor Advertisement (IPv6)
  carrying the virtual MAC, so it takes over at once.
- The owner "always preempts, independent of the setting" of Preempt_Mode.
- Section 8.3.2: configure at most one priority-255 router per VRID on a link. Without any 255 router and with
  preemption off, no preemption happens.
- Priority 0 in an ADVERTISEMENT means the Master has stopped participating, so Backups take over without waiting for
  the Master-down timeout.
- Backup priorities should be spread out (RFC example: add a second Backup at 50 rather than 99 or 100) for faster
  convergence.
- IPv6 caveat for a restarting owner: DAD may fail because a Backup answers that it owns the address; the RFC suggests
  not running DAD in that case.

## Parameters and defaults (section 6.1)
| Parameter | RFC value |
|---|---|
| Priority | 100 default for non-owners |
| Advertisement_Interval | 100 centiseconds (1 second) default; the Max Adver Int wire field is 12 bits |
| Skew_Time | ((256 - priority) * Master_Adver_Interval) / 256 |
| Master_Down_Interval | (3 * Master_Adver_Interval) + Skew_Time |
| Preempt_Mode | True by default |
| Accept_Mode | False by default |

- A Backup adopts the Master's advertised interval, so mismatched timers do not break the election, but the RFC warns
  that a higher-priority Master advertising more slowly than its Backups is unstable (section 5.2.7).
- With Preempt_Mode false, or an advertisement priority greater than or equal to the local one, the Backup resets its
  Master_Down_Timer; otherwise it discards the advertisement.
- Accept_Mode False: the Master does not accept packets addressed to the owner's IP if it is not the owner (so a ping
  to the VIP can fail on a non-owner Master). Deployments that ping the VIP may set Accept_Mode True. IPv6 Neighbor
  Solicitations and Advertisements must not be dropped either way.

## Addressing on the wire
- IPv4 advertisements go to 224.0.0.18, IP protocol 112, TTL 255; a receiver MUST discard packets whose TTL is not 255.
- Virtual MAC: 00-00-5E-00-01-{VRID} for IPv4 and 00-00-5E-00-02-{VRID} for IPv6.
- Advertisements are sent with the virtual MAC as source so learning bridges find the segment.
- A non-owner Master SHOULD NOT forward packets addressed to the VIP (a reject host route is one mechanism).

## Interop and security
- v2 and v3 mixing is optional in implementations and intended only for migration, not as a permanent design. A dual-mode
  Backup times out on the Master's advertised rate.
- Do not give a VRRPv2-only router a higher priority than a dual-mode router running sub-second intervals.
- When upgrading, run v3 Masters at 100 centiseconds until the v2 routers are upgraded, then move to faster rates.
- VRRPv3 has no authentication. Earlier VRRP versions had several types; experience showed misconfigured secrets caused
  multiple Masters and authentication would not stop a hostile Master anyway. The TTL 255 check limits attacks to the
  local LAN. Switch features that filter ARP/ND per port can be extended to VRRP on untrusted ports.
- Backups must send the same Router Advertisement options as the address owner (section 8.2.3).

## Verify
- [ ] One Master per VRID; Backups agree on VIP and version.
- [ ] Exactly one priority-255 router per VRID, or none.
- [ ] Failover: the Master-down time you observe matches 3 x advertisement interval plus skew.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read RFC 5798 sections 5.1.1 (destination, TTL, protocol), 5.2.4-5.2.7
(priority, Max Adver Int), 6.1 (parameters, Preempt_Mode, Accept_Mode), 6.4.1 (startup), 7.3 (virtual MAC), 8.2.2, 8.3,
8.4 (v2/v3 interoperation) and 9 (security). Removed as unconfirmed: all IOS XE syntax (the Cisco FHRP page is a 404),
`preempt delay`, tracking, the HSRP comparison table, and the claim that IOS XE answers pings to the VIP.
