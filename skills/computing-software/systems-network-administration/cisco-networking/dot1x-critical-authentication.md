---
id: computing-software.systems-network-administration.cisco-networking.dot1x-critical-authentication
name: dot1x-critical-authentication
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, 802-1x, dot1x, critical-auth, critical-vlan, inaccessible-auth-bypass, radius-down, catalyst-9300]
level: practitioner
status: docs-checked
description: "Keep users working when RADIUS is unreachable with 802.1X inaccessible authentication bypass: dead criteria, critical VLAN, critical voice VLAN, recovery on Catalyst 9300."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_ieee_802_1x_port_based_authentication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Critical authentication when RADIUS is down

Inaccessible authentication bypass, also called critical authentication or the AAA fail policy, is for when the switch
cannot reach the configured RADIUS servers and new hosts cannot be authenticated. The switch checks RADIUS server
status when it tries to authenticate a host on a critical port. If all servers are unavailable it grants the host
network access and puts the port in the critical-authentication state, in the RADIUS-configured or user-specified
access VLAN (the critical VLAN), giving limited access.

Source: Catalyst 9300 17.9 802.1X guide (classic `authentication` / `dot1x critical` syntax). It does not cover the
IBNS 2.0 policy-map/service-template syntax; read your platform's identity-control-policy guide for that.

## Behaviour by port state
- Unauthorised port: goes to critical-authentication in the RADIUS or user-specified access VLAN.
- Already authorised port that reauthenticates: goes to critical-authentication in the current VLAN (possibly the one
  RADIUS assigned earlier).
- Server fails mid-exchange: the exchange times out and the port goes critical on the next attempt.
- A guest-VLAN client stays in the guest VLAN; a port in a restricted VLAN stays in it, in critical state.
- The guide lists IAB support on single-host and multihost ports; for multi-auth it uses
  `authentication event server dead action reinitialize vlan <vlan-id>`, which reinitialises all connected hosts into
  the critical VLAN.
- Do not use an RSPAN VLAN as the critical VLAN; on a private VLAN host port it must be a secondary private VLAN.
- The critical VLAN must be active on the switch: if it is inactive or down, the session keeps trying to enable it,
  fails repeatedly and can hold a large amount of memory.

## Configuration (steps from the guide)
```
aaa new-model
radius-server dead-criteria time 20 tries 10   ! time 1-120 s, tries 1-100; defaults are chosen dynamically
radius-server deadtime 60                      ! minutes 0-1440, default 0
dot1x critical eapol                           ! optional: send EAPOL-Success when a critical port authenticates
dot1x critical recovery delay 2000             ! ms, 1-10000, default 1000
interface gigabitethernet 1/0/1
 authentication event server dead action authorize vlan 20
 switchport voice vlan 30
 authentication event server dead action authorize voice
```
- `authorize`: move any new host trying to authenticate to the critical VLAN. `reinitialize`: move all authorised
  hosts on the port to the critical VLAN.
- Critical voice VLAN: the voice VLAN cannot be the same as the critical data VLAN, and the feature only takes effect
  in multidomain or multi-auth host mode. Phones learn the voice VLAN via CDP, LLDP or DHCP. Dynamic critical voice
  VLAN assignment is not supported with nested service templates (it makes the device loop between VLANs).
- Recovery: configured critical ports are automatically reauthenticated when RADIUS returns, paced by the recovery
  delay. The guide's example also uses `dot1x critical recovery action reinitialize` on the interface.
- Limit: 2000 is the maximum number of dot1x sessions with critical-auth VLAN enabled and server reinitialised.
- Remove with the `no` forms of `authentication event server dead action`, `radius-server dead-criteria`,
  `radius-server deadtime`.
- On a switch stack the active switch sends RADIUS keepalives and shares server status with members; when status
  changes from dead to alive it reauthenticates all critical-state ports.

## Verify
```
show authentication interface gigabitethernet 1/0/1
show authentication sessions interface gigabitethernet 1/0/1
```
Lab test: block RADIUS and confirm a new client lands in the critical VLAN and reauthenticates on recovery.

## Checked
Checked 2026-11-08 against the Cisco Catalyst 9300 17.9 "Configuring IEEE 802.1x Port-Based Authentication" chapter:
IAB behaviour, guidelines, critical voice VLAN, command ranges and defaults, session limit, example, stack behaviour.
Removed: the IBNS 2.0 policy-map block, `event aaa-available`, `authentication event server alive action`,
`show access-session` commands, the critical-ACL gotcha, and the IBNS 2.0 article, which returned 404.
Method: documentation only; no commands were run.
