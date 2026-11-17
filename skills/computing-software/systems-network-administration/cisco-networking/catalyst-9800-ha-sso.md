---
id: computing-software.systems-network-administration.cisco-networking.catalyst-9800-ha-sso
name: catalyst-9800-ha-sso
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst-9800, wlc, wlc-ha-sso, redundancy-port, rmi, n-plus-1, high-availability, wireless]
level: practitioner
status: draft
description: "Pair two Catalyst 9800 WLCs in HA SSO: redundancy port and RMI, priority, stateful client failover, N+1 as an alternative, and failover testing."
sources:
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/technotes/8-8/b_c9800_wireless_controller_ha_sso_dg.html
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/17-9/config-guide/b_wl_17_9_cg.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Catalyst 9800 HA SSO

Two 9800s act as one: the standby holds AP and client state, so a failure is invisible to APs
(no rejoin) and clients stay associated.

## Requirements
- Same model and same IOS XE release (and same install/bundle mode).
- Redundancy port (RP) cabled back to back, or over a L2 link for 9800-CL; latency under 80 ms
  round trip, ideally same site.
- Same management VLAN/subnet on both; one wireless management IP shared.

## Configure (17.x with RMI, recommended)
On both, before pairing:
```
redundancy-management interface Vlan100 primary 10.1.100.11 secondary 10.1.100.12
chassis 1 priority 2            ! primary gets the higher priority
chassis redundancy ha-interface GigabitEthernet3 local-ip 169.254.1.1 /16 remote-ip 169.254.1.2  ! 9800-CL
redundancy
 mode sso
write memory
reload
```
RMI (redundancy management interface) gives each box its own management IP so the standby is
reachable and gateway checks work.

## Verify the pair
```
show chassis
show redundancy
!  Current Software state = ACTIVE / STANDBY HOT
show redundancy states
show chassis rmi
```
Wait for `STANDBY HOT` before testing; bulk sync can take minutes with many APs.

## Gateway reachability check
```
management gateway-failover enable
```
With RMI, the active pings the default gateway; if it loses it while the standby still reaches it,
a switchover happens. Protects against uplink failure, not only box failure.

## N+1 instead of SSO
Separate controllers in the same mobility group; APs have primary/secondary/tertiary controllers
configured (`ap name X controller primary WLC1 10.1.1.10`). On failure APs rejoin the secondary
(tens of seconds, clients reconnect). Use across sites or for different releases.

## Gotchas
- Never configure the standby directly; config syncs from the active.
- Upgrades: ISSU or rolling AP upgrade with N+1; a plain upgrade reloads both.
- Split brain if RP and RMI both fail: the recovery is a reload of the box with the lower priority.
- Licences and Smart reporting follow the active.

## Verify
- [ ] `redundancy force-switchover` in a window: APs stay joined (`show ap summary` uptime), clients
  stay in Run.
