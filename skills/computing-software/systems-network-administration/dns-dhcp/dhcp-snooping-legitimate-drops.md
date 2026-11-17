---
id: computing-software.systems-network-administration.dns-dhcp.dhcp-snooping-legitimate-drops
name: dhcp-snooping-legitimate-drops
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, snooping-drops, dhcp-snooping, option-82, cisco, troubleshooting]
level: practitioner
status: draft
description: "Diagnose legitimate DHCP traffic dropped by DHCP snooping: untrusted uplinks, option 82 insertion, rate limits, binding table and DAI/IPSG side effects."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-12/configuration_guide/sec/b_1712_sec_9300_cg/configuring_dhcp.html
  - https://www.rfc-editor.org/rfc/rfc3046
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Legitimate traffic dropped by snooping

DHCP snooping drops server messages (OFFER/ACK) arriving on untrusted ports and enforces option 82
and rate rules. Misconfiguration blocks the real server.

## Check
```
show ip dhcp snooping
show ip dhcp snooping statistics detail
show ip dhcp snooping binding
show logging | include DHCP_SNOOPING
```
Look for counters like "Dropped because untrusted", "Packets dropped due to option 82",
"Packets dropped due to rate limit", and log messages `%DHCP_SNOOPING-5-DHCP_SNOOPING_UNTRUSTED_PORT`
or `DHCP_SNOOPING_MATCH_MAC_FAIL`.

## Common causes and fixes
| Cause | Fix |
|-------|-----|
| Uplink/port-channel toward the server or relay not trusted | `ip dhcp snooping trust` on uplinks (port-channel interface, not just members) |
| Switch inserts option 82 with giaddr 0; upstream relay/server drops it ("giaddr 0 with option 82") | `no ip dhcp snooping information option` on the access switch, or `ip dhcp relay information trust-all` on the relay |
| Rate limit too low on access ports (PXE storms, phones+PCs) | `ip dhcp snooping limit rate 50` (err-disables when exceeded) |
| Snooping enabled for a VLAN without the server reachable through trusted path | trust the right ports or remove the VLAN from `ip dhcp snooping vlan` |
| Client MAC differs from chaddr (some virtual/bridged clients) | `no ip dhcp snooping verify mac-address` |
| Binding table lost after reboot; DAI/IP Source Guard then drop static-renewing clients | `ip dhcp snooping database flash:/dhcp-snoop.db` |

## Side effects
Dynamic ARP Inspection and IP Source Guard rely on the binding table; hosts with static IPs need ARP
ACLs / static bindings (`ip source binding`).

## Verify
- [ ] Snooping statistics show no drops for the affected VLAN and clients complete DORA; bindings appear in `show ip dhcp snooping binding`.
