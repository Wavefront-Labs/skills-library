---
id: computing-software.systems-network-administration.cisco-networking.cdp-lldp-neighbor-topology-mapping
name: cdp-lldp-neighbor-topology-mapping
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, cdp, lldp, cdp-neighbors, lldp-neighbors, topology-discovery, show-cdp-neighbors-detail, network-documentation, network-diagram, management-address]
level: practitioner
status: draft
description: "Map an unknown network from CDP and LLDP: read neighbor detail for model, port, IP and native VLAN, walk hop by hop, export to a diagram and spot mismatches CDP reports."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sys_mgmt/b_179_sys_mgmt_9300_cg/configuring_cisco_discovery_protocol.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sys_mgmt/b_179_sys_mgmt_9300_cg/configuring_lldp__lldp_med__and_wired_location_service.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mapping topology from CDP and LLDP neighbours

## Read neighbours
```
show cdp neighbors                     ! Device ID, Local Intrfce, Holdtme, Capability, Platform, Port ID
show cdp neighbors detail              ! adds mgmt IP, software version, native VLAN, duplex, VTP domain
show lldp neighbors
show lldp neighbors detail             ! chassis id, port id/description, system name, mgmt address, capabilities
```
Capability codes: R router, S switch, B bridge, H host, I IGMP, P phone, T trans-bridge.
LLDP: B bridge, R router, W WLAN AP, T telephone, S station.

## Walk the network
1. Start at the core. For each neighbour with S or R capability, note local port, remote
   device, remote port and management IP.
2. SSH to each management IP and repeat; keep a visited list.
3. Record edges as `deviceA:portA <-> deviceB:portB`. That is your physical diagram source.

Automate it rather than doing more than ~10 devices by hand:
- Netmiko/Nornir with `show cdp neighbors detail` parsed via TextFSM/Genie (`use_textfsm=True`).
- NetBox device/cable import from the edge list; or tools like Netdisco, LibreNMS (builds maps
  from CDP/LLDP via SNMP: CISCO-CDP-MIB and LLDP-MIB).

## What CDP/LLDP tell you about problems
- `%CDP-4-NATIVE_VLAN_MISMATCH` and `%CDP-4-DUPLEX_MISMATCH` syslogs point at trunk/duplex errors.
- Neighbour shows on two local ports but you expect an EtherChannel: the bundle is not formed.
- Neighbour appears through an unmanaged switch: multiple neighbours on one port.
- No neighbour on an uplink: CDP disabled, a firewall/media converter in between, or a
  non-Cisco device with LLDP only (enable `lldp run`).

## Gotchas
- Holdtime is 180 s (CDP) / 120 s (LLDP); a removed device lingers that long.
- Some devices advertise only an IPv6 or the wrong VLAN's management address.
- Servers with LLDP agents (lldpd, NIC firmware) appear too; useful for finding server ports.

## Verify
- [ ] Every switch-to-switch link appears from both ends with matching ports.
- [ ] Diagram edges agree with `show interfaces description`.
- [ ] No native VLAN or duplex mismatch messages in the logs.
