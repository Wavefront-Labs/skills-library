---
id: computing-software.systems-network-administration.cisco-networking.discovery-protocol-hardening
name: discovery-protocol-hardening
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, cdp, lldp, disable-cdp, discovery-protocol-hardening, no-cdp-enable, no-lldp-transmit, information-disclosure, cdp-flood, device-hardening, internet-edge]
level: practitioner
status: draft
description: "Decide where CDP and LLDP should run: disable on internet, untrusted and user-facing ports, keep on infrastructure links and phones, and the attacks each choice prevents."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sys_mgmt/b_179_sys_mgmt_9300_cg/configuring_cisco_discovery_protocol.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hardening CDP and LLDP

CDP and LLDP send hostname, model, software version, management IP, native VLAN and port
names in cleartext every 30-60 s. Anyone on the port can read them with Wireshark
(`cdp || lldp`) and use the version to pick exploits. Malformed CDP frames have also been the
vector for real remote-code-execution bugs (CDPwn, 2020).

## Policy
| Port type | CDP | LLDP |
|---|---|---|
| Switch/router infrastructure links | on | on (multivendor) |
| IP phones, APs (need voice VLAN/PoE negotiation) | on | on (LLDP-MED for non-Cisco) |
| User access ports without phones | off | off, or receive only |
| Internet/ISP-facing, DMZ, partner links | off | off |
| Server ports | per need (hypervisor mapping is useful) | per need |

## Configure
```
interface GigabitEthernet0/0/0         ! ISP-facing
 no cdp enable
 no lldp transmit
 no lldp receive
!
interface range Gi1/0/1 - 24           ! user ports, phones present
 ! keep CDP for Cisco phones; restrict information
!
no cdp run                             ! global off on edge routers with no internal need
no lldp tlv-select system-description  ! hide software version where LLDP must run
```
On IOS XE `cdp run` is global; `no cdp enable` is per interface. Turning CDP off globally on
access switches also breaks Cisco phone voice VLAN discovery unless LLDP-MED is on.

## Related protections
- Keep IOS patched for CDP/LLDP parser advisories (check the Cisco PSIRT for your release).
- CDP table exhaustion floods (Yersinia) are mitigated by disabling CDP on user ports and port
  security limiting MACs.
- Control-plane policing can rate-limit CDP/LLDP punts.

## Verify
- [ ] `show cdp interface` lists only infrastructure and phone ports.
- [ ] `show lldp interface` shows Tx/Rx disabled on internet and untrusted ports.
- [ ] A packet capture on a user port shows no CDP/LLDP frames from the switch.
- [ ] Phones still get the voice VLAN after the change.
