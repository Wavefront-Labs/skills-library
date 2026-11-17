---
id: computing-software.systems-network-administration.cisco-networking.inactive-and-missing-vlan-troubleshooting
name: inactive-and-missing-vlan-troubleshooting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, vlan-troubleshooting, inactive-vlan, show-vlan, switchport, trunk, svi-down]
level: practitioner
status: draft
description: "Fix hosts stuck in a VLAN that does not pass traffic: inactive VLANs, VLAN missing from the database or trunk allowed list, STP blocking, and SVI down conditions."
sources:
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/vlan/10023-3.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/vlan/b_179_vlan_9300_cg.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inactive or missing VLAN troubleshooting

Symptom: a host on an access port gets no DHCP or cannot reach its gateway, or an SVI stays
down/down.

## Work through the path
```
show interfaces Gi1/0/10 switchport | include Mode|Access Mode VLAN|Operational
show vlan brief | include ^20 
show interfaces trunk
show spanning-tree vlan 20
show ip interface brief | include Vlan20
```

## What each finding means
| Finding | Cause and fix |
|---|---|
| `Access Mode VLAN: 20 (Inactive)` | VLAN 20 not in the VLAN database. `vlan 20` / `name USERS`. In VTP client mode it must exist on the server. |
| Port missing from `show vlan brief` | port is a trunk, err-disabled, or a routed port |
| VLAN 20 absent from `Vlans allowed and active in management domain` on the uplink | not in allowed list or not created on this switch: `switchport trunk allowed vlan add 20` |
| VLAN present but in `Vlans in spanning tree forwarding state and not pruned` missing | STP blocking or VTP pruning; check root placement and pruning eligibility |
| `Vlan20 is down, line protocol is down` | no active port (access or forwarding trunk) in VLAN 20 on this switch, or `shutdown` on the SVI |
| VLAN state `act/lshut` or `sus` | VLAN shut down (`shutdown vlan 20`) or suspended in the database |

## Common traps
- `switchport trunk allowed vlan 20` (without `add`) replaces the whole list and cuts every other
  VLAN. Always use `add`/`remove`.
- VTP server with a higher revision number wiping the database when a lab switch is connected.
  Check `show vtp status` revision and mode.
- Native VLAN mismatch: frames for the native VLAN land in a different VLAN on the far side. CDP
  logs `%CDP-4-NATIVE_VLAN_MISMATCH`.
- Voice VLAN configured but phone not getting it because CDP/LLDP is disabled on the port.
- SVI autostate: a VLAN whose only ports are trunks to other switches in STP blocking keeps the
  SVI down. `switchport autostate exclude` on monitoring ports that should not count.

## Verify
- [ ] `show mac address-table vlan 20` learns the host MAC on the access port and the gateway MAC
  on the uplink.
- [ ] Host gets an address and pings the gateway.
