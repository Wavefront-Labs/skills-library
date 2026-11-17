---
id: computing-software.systems-network-administration.cisco-networking.port-security-sticky-mac-and-violation-modes
name: port-security-sticky-mac-and-violation-modes
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, port-security, sticky-mac, violation-mode, err-disabled, mac-limit, aging, port-security-aging]
level: practitioner
status: docs-checked
description: "Configure switchport port-security with sticky MAC learning, maximum counts for phones, protect/restrict/shutdown violation modes, aging and recovery."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/port_security.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Port security: sticky MAC and violation modes

Defaults (Catalyst 9300, IOS XE 17.9): port security disabled on a port, sticky learning
disabled, maximum one secure MAC address, violation mode shutdown, port security aging disabled.

```
interface GigabitEthernet1/0/10
 switchport mode access                    ! a dynamic (default-mode) port cannot be secure
 switchport access vlan 10
 switchport voice vlan 110
 switchport port-security
 switchport port-security maximum 2        ! PC + phone
 switchport port-security mac-address sticky
 switchport port-security violation restrict
```

## Sticky learning
With sticky learning the interface converts dynamic secure MACs (including ones learned before
sticky was enabled) to sticky secure MACs and adds them to the running configuration, as
`switchport port-security mac-address sticky 0011.2233.4455`. They are not in the startup
configuration until you save; if you do not save them they are lost at restart. Disabling sticky
converts them back to dynamic and removes them from the running configuration. A sticky MAC
can be entered by hand only after sticky learning is enabled.
Moving a user to another port flags a violation if that MAC is a secure address on the other
secure port in the same VLAN, or if the port is already at its maximum.

## Violation modes
| Mode | Drops unknown-source traffic | SNMP trap and syslog | Counter | Port |
|---|---|---|---|---|
| protect | yes | no | no | up |
| restrict | yes | yes | yes | up |
| shutdown (default) | yes | see note | yes | err-disabled |
| shutdown vlan | yes | syslog | yes | only that VLAN err-disabled |

Note: for shutdown the guide's action table says no trap or syslog while its configuration step
says a trap and syslog are sent; verify on your release. Protect is not recommended on trunk
ports because it stops learning when any VLAN hits its maximum.

Recover an err-disabled secure port with `errdisable recovery cause psecure-violation` (global),
`shutdown` then `no shutdown` on the interface, or `clear errdisable interface <id> vlan`.

## Voice VLAN and phones
Cisco's guidance: with a voice VLAN, set the maximum to two. The phone needs one address, learned
on the voice VLAN and not on the access VLAN, and a single PC behind it needs no more. For
more than one PC, allow one per PC plus one for the phone. If the same MAC requests an address on
both the access and voice VLAN, only the access VLAN gets an IP address. Voice VLAN is supported
on access ports only.

## Aging
`switchport port-security aging time <0-1440 minutes>` and
`switchport port-security aging type {absolute | inactivity}`; `aging static` also ages
statically configured addresses. The switch does not support aging of sticky secure addresses.
The default aging type is absolute with time 0 (disabled). When a port disconnects, dynamic
secure MACs are removed immediately, even with inactivity aging.

## Restrictions
- Not supported on EtherChannel interfaces, private VLAN ports, dynamic or dynamic-access ports,
  routed ports, or a SPAN destination port.
- Cisco recommends not enabling port security on an 802.1X authenticator interface.
- Lowering `maximum` below the number of secure addresses already configured is rejected.

## Verify
```
show port-security
show port-security interface Gi1/0/10
show port-security address
show port-security interface Gi1/0/10 vlan
```
- [ ] Plugging an extra device increments the violation count (restrict) without dropping the PC.

## Checked
2026-11-08. Confirmed against the Catalyst 9300 17.9 Security Configuration Guide chapter "Port
Security": defaults, sticky behaviour, violation mode table and text, aging types and range,
voice VLAN guidance, restrictions, recovery commands and show commands. Removed unsupported or
incorrect content: sticky combined with aging (not supported), `maximum 1 vlan voice`,
`clear port-security sticky`, `errdisable recovery interval`, the phone-presents-PC-MAC claim,
the 802.1X multi-auth statement and the "Last Source Address" field. The old
configuring_port_security.html URL 404s.
Method: documentation only; no commands were run.
