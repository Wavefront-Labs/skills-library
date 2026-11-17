---
id: computing-software.systems-network-administration.cisco-networking.catalyst-9000-egress-queuing
name: catalyst-9000-egress-queuing
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, egress-queuing, catalyst-qos, priority-queue, qos-queue-softmax-multiplier, buffers, output-drops]
level: practitioner
status: draft
description: "Configure and verify Catalyst 9000 egress queuing: queuing policy with priority level, bandwidth remaining, buffer softmax tuning, and reading per-queue drop counters."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/qos/b_179_qos_9300_cg.html
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9000/216193-understand-queue-buffer-allocation-on-c.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Catalyst 9000 egress queuing

Catalyst 9000 ports have up to 8 egress queues (2 can be priority). By default all traffic shares
queue 0 with modest buffers, so bursts toward a slower port (10G to 1G, many-to-one) drop.

## Queuing policy (egress only)
```
class-map match-any VOICE
 match dscp ef
class-map match-any VIDEO
 match dscp af41 cs4
class-map match-any CONTROL
 match dscp cs6 cs3
class-map match-any SCAVENGER
 match dscp cs1

policy-map EGRESS-Q
 class VOICE
  priority level 1
  police rate percent 10          ! cap the priority queue
 class VIDEO
  priority level 2
  police rate percent 20
 class CONTROL
  bandwidth remaining percent 10
 class SCAVENGER
  bandwidth remaining percent 1
 class class-default
  bandwidth remaining percent 60
  queue-buffers ratio 50

interface range Gi1/0/1-48
 service-policy output EGRESS-Q
```
Marking is done on ingress (trust DSCP or classify and set); egress queuing only acts on existing
markings.

## Buffers
Shared buffer per ASIC; each queue gets a hard minimum and can borrow up to a soft maximum.
Raising the softmax multiplier lets queues absorb bigger bursts:
```
qos queue-softmax-multiplier 1200     ! global, range 100-4800
```
This is often the fix for output drops on uplink-to-access congestion without changing classes.

## Read the counters
```
show interfaces Gi1/0/10 | include output drops
show platform hardware fed switch active qos queue stats interface Gi1/0/10
!  Q0 enqueue/drop counters per threshold (Th0/Th1/Th2)
show platform hardware fed switch active qos queue config interface Gi1/0/10
show policy-map interface Gi1/0/10 output
```
Drops in the default queue with none in priority queues = bursty bulk traffic: buffers/softmax.
Drops in the priority queue = priority traffic exceeding its police rate.

## Gotchas
- Without a police on `priority level`, priority traffic can starve everything else.
- Only one queuing policy per port; combining marking and queuing in one egress policy is
  restricted on some releases.
- Wired AutoQoS generates an equivalent policy; inspect before editing by hand.

## Verify
- [ ] Per-queue stats show voice in the priority queue with zero drops during a load test.
- [ ] Output drops on congested ports fall after buffer tuning.
