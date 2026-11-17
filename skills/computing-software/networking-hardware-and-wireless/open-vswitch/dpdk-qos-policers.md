---
id: computing-software.networking-hardware-and-wireless.open-vswitch.dpdk-qos-policers
name: dpdk-qos-policers
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, egress-policer, trtcm, dpdk, qos, cir, cbs, eir, ebs, policer]
level: advanced
status: docs-checked
description: "Rate-limit DPDK ports in Open vSwitch with egress-policer and trtcm-policer (RFC 4115): cir/cbs/eir/ebs keys, inspection and removal."
sources:
  - https://docs.openvswitch.org/en/latest/topics/dpdk/qos/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dpdk qos policers
Keys under `other-config`: `cir` (committed information rate), `cbs` (committed burst), `eir` and `ebs` (excess rate and burst, trTCM only); port QoS maps queues via `queues:<id>`.

Egress policer on one port:
```
ovs-vsctl set port vhost-user0 qos=@newqos -- --id=@newqos create qos type=egress-policer other-config:cir=46000000 other-config:cbs=2048
```
Examine: `ovs-appctl -t ovs-vswitchd qos/show vhost-user0`
Clear: `ovs-vsctl destroy QoS vhost-user0 -- clear Port vhost-user0 qos`

trTCM multi-queue (RFC 4115): queue level is color-blind, port level color-aware; Green and Yellow forward, Red drops.
```
ovs-vsctl --timeout=5 set port dpdk1 qos=@myqos -- --id=@myqos create qos type=trtcm-policer other-config:cir=50000 other-config:cbs=2048 other-config:eir=50000 other-config:ebs=2048 queues:10=@dpdk1Q10 queues:20=@dpdk1Q20 -- --id=@dpdk1Q10 create queue other-config:cir=100000 other-config:cbs=2048 other-config:eir=0 other-config:ebs=0 -- --id=@dpdk1Q20 create queue other-config:cir=0 other-config:cbs=0 other-config:eir=50000 other-config:ebs=2048
```
Queue 10 (high priority) is marked Green, queue 20 Yellow. Rates are bytes without the Ethernet header, so 1000 pps of 64-byte packets is 50,000.

Ingress policing also works on DPDK ports: `ovs-vsctl set interface vhost-user0 ingress_policing_rate=368000 ingress_policing_burst=1000`; clear with rate 0.

## Checked
2026-11-09. Read in full: docs.openvswitch.org topics/dpdk/qos (egress-policer, trtcm-policer example, queue 10 Green and queue 20 Yellow, rates in bytes without the Ethernet header, qos/show, destroy QoS command, ingress policing set and clear). Nothing removed.
Method: documentation only; no commands were run.
