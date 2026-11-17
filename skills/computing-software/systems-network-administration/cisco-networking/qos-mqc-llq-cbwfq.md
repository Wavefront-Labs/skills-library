---
id: computing-software.systems-network-administration.cisco-networking.qos-mqc-llq-cbwfq
name: qos-mqc-llq-cbwfq
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, qos, quality-of-service, mqc, class-map, policy-map, service-policy, llq, cbwfq, priority-queue, bandwidth-remaining, fair-queue, wred, queuing, show-policy-map-interface]
level: practitioner
status: draft
description: "Build egress queuing with MQC: DSCP class-maps, LLQ priority and its implicit policer, CBWFQ bandwidth percent, fair-queue/WRED in default, reading counters."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/qos_mqc/configuration/xe-16/qos-mqc-xe-16-book.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/qos_conmgt/configuration/xe-16/qos-conmgt-xe-16-book/qos-conmgt-cbwfq.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MQC queuing: LLQ and CBWFQ

Queuing only matters where there is congestion: WAN edges, oversubscribed uplinks. MQC is
three steps: classify (class-map), define actions (policy-map), attach (service-policy).

## Example WAN edge policy (router)
```
class-map match-any VOICE
 match dscp ef
class-map match-any VIDEO
 match dscp af41 af42 cs4
class-map match-any CRITICAL-DATA
 match dscp af21 af22 af31
class-map match-any SCAVENGER
 match dscp cs1
!
policy-map WAN-OUT
 class VOICE
  priority percent 10            ! LLQ: strict priority with an implicit policer at 10%
 class VIDEO
  bandwidth remaining percent 30
 class CRITICAL-DATA
  bandwidth remaining percent 30
  random-detect dscp-based
 class SCAVENGER
  bandwidth remaining percent 1
 class class-default
  bandwidth remaining percent 39
  fair-queue
  random-detect
!
interface GigabitEthernet0/0/0
 service-policy output WAN-OUT
```
- `priority` (LLQ) is serviced first; its implicit policer drops excess **during congestion**
  so voice cannot starve others. Keep total priority at or under ~33% of the link.
- `bandwidth` / `bandwidth percent` guarantees a minimum; `bandwidth remaining percent`
  divides what is left after priority. Do not mix styles within one policy.
- `match-any` vs `match-all` (default): match-all with two DSCP lines never matches.

## Sub-rate circuits
If the physical port is 1 Gb/s but the circuit is 100 Mb/s, queues never fill on the router:
the drops happen in the provider. Nest the queuing policy under a shaper at the CIR (see
qos-policing-and-shaping).

## Read counters
```
show policy-map interface Gi0/0/0 output
! per class: offered rate, drop rate, packets matched, queue depth, total drops, (pkts output/bytes output)
show class-map
```
Drops in class-default during peaks are normal; drops in VOICE mean the priority class is too
small or something non-voice is marked EF.

## Catalyst switches
Catalyst 9000 uses the same MQC syntax but different queuing semantics (`priority level 1`,
`queue-buffers ratio`, `bandwidth remaining ratio`); apply egress policies to switch ports per
the platform QoS guide. Many access deployments use the AutoQoS macros (`auto qos voip
cisco-phone`).

## Verify
- [ ] Policy attached in the right direction (`show policy-map interface` has counters).
- [ ] Under a load test, voice class shows no drops and low latency.
- [ ] Sum of guarantees is 100% or less; router accepted the policy without errors.
