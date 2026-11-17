---
id: computing-software.systems-network-administration.cisco-networking.copp-policy-design
name: copp-policy-design
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, copp-policy, control-plane-policing, control-plane, policer, management-plane, ddos]
level: practitioner
status: docs-checked
description: "Design and verify Control Plane Policing on IOS-XE: build MQC classes from ACLs, police per class, attach with control-plane, and read the per-class conformed/exceeded counters."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/qos_plcshp/configuration/xe-16/qos-plcshp-xe-16-book/qos-plcshp-ctrl-pln-plc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CoPP policy design

Control Plane Policing (CoPP) is a QoS filter on traffic to and from the control plane, protecting IOS-XE routers and
switches against reconnaissance and DoS attacks so forwarding and protocol state survive an attack or heavy load.
The control plane is treated as its own interface (the punt/inject interface): packets are punted to the RP on input
and injected on output. The rules apply only once a packet is known to be destined to the control plane, or is
leaving it.

## Rules of the feature
- It uses MQC (class-map, policy-map, `control-plane`). Only two policy-map commands are supported: `police` and
  `set`.
- Match criteria: standard and extended IP ACLs, plus `match dscp`, `match ip dscp`, `match ip precedence`,
  `match precedence`, `match protocol arp`, `match protocol ipv6`, `match protocol pppoe`,
  `match protocol pppoe-discovery`, `match qos-group`. `match input-interface` is not supported, and NBAR-based
  features may not work well at the control plane.
- Build the class map and policy map first, then attach: `control-plane`, then `service-policy {input | output}
  <policy-map>`. Platform-specific restrictions are checked when the policy is applied.
- Output policing runs in silent mode (discarded packets generate no message) and gives no performance benefit; it
  only controls what leaves the device.
- On the ASR 1000 the management interface connects directly to the RP, so traffic through it is not subject to the
  forwarding plane's CoPP.

## Example shape
In a CoPP ACL, `permit` entries are the traffic the class matches and polices; `deny` entries exempt trusted hosts
from that class (as in the page's Telnet example).
```
access-list 140 deny tcp host 10.1.1.1 any eq telnet
access-list 140 permit tcp any any eq telnet
class-map telnet-class
 match access-group 140
policy-map control-plane-in
 class telnet-class
  police 80000 conform transmit exceed drop
control-plane
 service-policy input control-plane-in
```
Named ACLs work with `match access-group name <ACL>`. The pps form is `police rate <n> pps` followed by
`conform-action <action>` (page example: `police rate 10 pps`, `conform-action transmit`).

## Design practice (judgement, not from the page)
- Classify routing, management and undesirable traffic separately and keep a `class-default`.
- Start with a non-dropping exceed action, read the counters over a representative period, then set real limits.
- Avoid dropping routing-protocol traffic outright.
- Platform-specific built-in policies (for example on Catalyst switches) differ; read your platform's CoPP guide.

## Verify
```
show policy-map control-plane [all] [input [class <class>] | output [class <class>]]
show control-plane {aggregate | cef-exception | counters | features | host | transit}
```
The first command shows, per class, packets and bytes, the match, and `conformed`/`exceeded`/`violated` counts with
their actions. Check that adjacencies stay up and exceed counters rise only in classes you intend to limit.

## Checked
Checked 2026-11-08 against the Cisco IOS XE "Control Plane Policing" chapter (xe-16 QoS policing and shaping guide):
supported commands and match criteria, attach steps, silent output mode, ACL permit/deny semantics, police syntax,
show commands and output fields. Removed: `system-cpp-policy`, `cpp system-default`, the QFP show command, and the
specific rate figures and one-week rollout period, which that page does not state. The security-centre CoPP best
practices page redirects to a 404 and was not used.
Method: documentation only; no commands were run.
