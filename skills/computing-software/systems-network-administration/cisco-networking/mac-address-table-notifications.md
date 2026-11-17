---
id: computing-software.systems-network-administration.cisco-networking.mac-address-table-notifications
name: mac-address-table-notifications
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, mac-move-notification, mac-address-notification, mac-address-table, snmp-trap, mac-threshold, l2-monitoring]
level: practitioner
status: docs-checked
description: "Enable MAC move, change and threshold notification traps on Catalyst switches, set their intervals and thresholds, and verify them."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sys_mgmt/b_179_sys_mgmt_9300_cg/administering_the_device.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MAC address-table notifications

On Catalyst 9300 (IOS XE 17.9) these are SNMP notifications sent to an NMS host; each needs the
`snmp-server host ... mac-notification` target, the global trap enable and the feature enable.

## Three notification types
| Type | Fires when | Feature command | Trap enable |
|---|---|---|---|
| MAC move | a MAC moves from one port to another within the same VLAN | `mac address-table notification mac-move` | `snmp-server enable traps mac-notification move` |
| Change (add/remove) | a MAC is added to or removed from an enabled interface | `mac address-table notification change` | `snmp-server enable traps mac-notification change` |
| Threshold | MAC table use reaches or exceeds the limit | `mac address-table notification threshold` | `snmp-server enable traps mac-notification threshold` |

```
conf t
 snmp-server host 172.20.10.10 traps private mac-notification
 snmp-server enable traps mac-notification move
 mac address-table notification mac-move
 snmp-server enable traps mac-notification change
 mac address-table notification change
 mac address-table notification change interval 60
 mac address-table notification change history-size 100
 snmp-server enable traps mac-notification threshold
 mac address-table notification threshold
 mac address-table notification threshold limit 85
 mac address-table notification threshold interval 300
interface Gi1/0/1
 snmp trap mac-notification change added
 snmp trap mac-notification change removed
```
Ranges and defaults from the guide:
- Change: `interval` 0 to 2147483647 s, default 1; `history-size` 0 to 500, default 1. The
  per-interface `snmp trap mac-notification change {added | removed}` selects which events send
  a trap on that Layer 2 interface.
- Threshold: `limit` 1 to 100 percent, default 50; `interval` at least 120 s, default 120.
- Disable with the `no` form of the trap enable and of the feature command.

## Show
```
show mac address-table notification mac-move
show mac address-table notification change            ! parameters and history table
show mac address-table notification threshold
show mac address-table count
```

## Using them
- A MAC that keeps moving between ports in a VLAN is the signal to investigate (for loops see
  the STP topology change and loop skill).
- Enable change notifications per interface only where the events matter, since every add or
  removal is an event.

## Verify
- [ ] `show mac address-table notification mac-move` reports the feature enabled.
- [ ] Move a laptop between two ports; a move notification reaches the NMS.

## Checked
2026-11-08. Confirmed against the Catalyst 9300 17.9 System Management guide ("Administering the
Device"): the three notification procedures, command syntax, ranges, defaults, per-interface
trap command, disable commands and the show commands. Removed unsupported content: the
%SW_MATM-4-MACFLAP_NOTIF syslog line, the combined `snmp-server enable traps` form, the
flapping-pattern interpretations, roaming and vMotion remarks, and the rate-limiting claim.
The original Layer 2 guide and command reference links were dropped (404 and not used).
Method: documentation only; no commands were run.
