---
id: computing-software.systems-network-administration.cisco-networking.radius-dynamic-vlan-assignment
name: radius-dynamic-vlan-assignment
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, dynamic-vlan-assignment, radius, dot1x, tunnel-private-group-id, ise, freeradius, aaa-authorization]
level: practitioner
status: draft
description: "Assign VLANs per user or device from RADIUS after 802.1X/MAB: the three tunnel attributes, switch authorization config, VLAN names vs IDs, and verification."
sources:
  - https://www.rfc-editor.org/rfc/rfc3580
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_ieee_802_1x_port_based_authentication.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RADIUS dynamic VLAN assignment

One port configuration for every desk; the RADIUS server decides the VLAN from who or what
authenticated.

## RADIUS attributes (RFC 3580), all three required
```
Tunnel-Type = VLAN (13)
Tunnel-Medium-Type = IEEE-802 (6)
Tunnel-Private-Group-ID = "20"        ! VLAN ID or VLAN name
```
FreeRADIUS `users` example:
```
alice  Cleartext-Password := "x"
       Tunnel-Type = VLAN, Tunnel-Medium-Type = IEEE-802, Tunnel-Private-Group-Id = "20"
```
In ISE: Authorization Profile, Common Tasks, VLAN, tag ID 1, value `20` or `USERS`.

## Switch side
```
aaa new-model
aaa authentication dot1x default group ISE
aaa authorization network default group ISE        ! without this the VLAN is ignored
aaa accounting dot1x default start-stop group ISE
dot1x system-auth-control

interface Gi1/0/10
 switchport mode access
 switchport access vlan 999                         ! fallback/default before auth
 authentication port-control auto
 mab
 dot1x pae authenticator
```
The assigned VLAN must exist in the switch VLAN database. Using names (`vlan 20` / `name USERS`)
lets one RADIUS policy work across sites with different VLAN numbers.

## Verify
```
show access-session interface Gi1/0/10 details
!   Vlan Group:  Vlan: 20
!   Server Policies: Vlan Group: Vlan: 20
show interfaces Gi1/0/10 switchport | include Operational Mode|Access Mode
```

## Gotchas
- Client must re-DHCP after the VLAN change. Windows does when 802.1X completes; devices
  authenticated by MAB after a delay may hold the old lease. Order dot1x and MAB carefully or use
  short pre-auth leases.
- Missing `aaa authorization network` is the most common reason the VLAN does not apply.
- Voice devices use `cisco-av-pair = device-traffic-class=voice` instead of a VLAN.
- If the VLAN does not exist, authorisation fails (`%DOT1X-5-FAIL`, `VLAN not found`); the port
  stays unauthorised.
- With multi-auth host mode all sessions must land in the same data VLAN.

## Verify
- [ ] `show access-session` shows the expected VLAN per user group.
- [ ] Host gets an address from the assigned VLAN's scope.
