---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-qos-policy
name: pan-os-qos-policy
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [qos-policy, pan-os, quality-of-service, traffic-classes, qos-profile, egress-guaranteed, bandwidth-management]
level: practitioner
status: draft
description: "Configure PAN-OS QoS profiles, egress interfaces and policy classes to guarantee and limit bandwidth per application."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/quality-of-service"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: protect voice and business apps on constrained links and cap bulk traffic.

```
configure
set network qos profile QP-WAN aggregate-bandwidth egress-max 100
set network qos profile QP-WAN class-bandwidth-type mbps class class1 priority real-time class-bandwidth egress-guaranteed 20 egress-max 40
set network qos profile QP-WAN class-bandwidth-type mbps class class4 priority low class-bandwidth egress-max 30
set network qos interface ethernet1/1 enabled yes regular-traffic default-group qos-profile QP-WAN
set rulebase qos rules voice from trust to untrust source any destination any application [ ms-teams sip ] action class 1
commit
```
QoS applies on egress interface only, classes 1-8, with priority real-time, high, medium, low. Marking DSCP is also possible with `dscp-tos` action in the policy rule.

Gotchas
- The interface must be declared with its real egress bandwidth; a QoS profile larger than the link does nothing useful.
- QoS rules match on pre-NAT addresses and the class is attached to the session; confirm model-specific behaviours.
- Tunnel interfaces need QoS on the physical egress or the tunnel itself depending on the target (confirm).
- Not all models/ports support QoS; check the datasheet.

## Verify
```
show qos interface ethernet1/1 throughput 0
show qos interface ethernet1/1 counter
```
Class counters should increment for the matched traffic.
