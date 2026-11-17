---
id: computing-software.systems-network-administration.cisco-networking.dhcp-snooping-option-82-insertion-problems
name: dhcp-snooping-option-82-insertion-problems
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, dhcp-snooping, snooping-option-82, option-82, giaddr-zero, dhcp-relay, layer2-security]
level: practitioner
status: draft
description: "Fix DHCP failures caused by DHCP snooping inserting option 82 with giaddr 0: symptoms on IOS and Windows servers, and the three ways to resolve it."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_dhcp.html
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-6500-series-switches/116312-technote-dhcp-00.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DHCP snooping option 82 insertion problems

## What happens
With `ip dhcp snooping` enabled, Catalyst switches **insert option 82** (circuit-id = VLAN/port,
remote-id = switch MAC) into client DHCP requests by default, without setting giaddr (it stays 0.0.0.0).
Then:
- An upstream switch with snooping receives a packet with option 82 on an **untrusted** port and
  drops it (`%DHCP_SNOOPING-5-DHCP_SNOOPING_NONZERO_GIADDR` or "option 82 on untrusted port").
- An IOS relay/server drops it: option 82 present but giaddr 0 is "inconsistent".
- Some servers (older Windows) ignore or mis-handle requests with option 82 and no giaddr.

## Symptoms
Clients get APIPA/no address after snooping is enabled; `show ip dhcp snooping statistics` shows
drops; the server sees nothing or logs inconsistent relay info.

## Fixes (pick one)
1. **Stop inserting** on the access switch if you do not use option 82:
   ```
   no ip dhcp snooping information option
   ```
2. **Allow it on the aggregation switch** that receives it on an untrusted port:
   ```
   ip dhcp snooping information option allow-untrusted
   ```
3. **Trust it on the IOS relay/server**:
   ```
   interface Vlan10
    ip dhcp relay information trusted
   ! or globally
   ip dhcp relay information trust-all
   ```
Also make sure the uplink towards the DHCP server is `ip dhcp snooping trust`.

## Verify
```
show ip dhcp snooping                      ! "Insertion of option 82 is enabled/disabled"
show ip dhcp snooping statistics detail
show ip dhcp snooping binding
debug ip dhcp snooping packet              ! short window
```
- [ ] New clients get leases and bindings appear in the snooping table.
