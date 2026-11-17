---
id: computing-software.networking-hardware-and-wireless.open-vswitch.linux-htb-qos-queues
name: linux-htb-qos-queues
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, linux-htb, qos-queues, qos, queue, min-rate, max-rate, set-queue, enqueue]
level: advanced
status: docs-checked
description: "Configure egress QoS in Open vSwitch with a linux-htb QoS record and Queue records via ovs-vsctl, queue rates, set_queue and cleanup."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vsctl.8.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
  - https://docs.openvswitch.org/en/latest/ref/ovs-actions.7/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# linux htb qos queues
Attach a QoS record and a queue to a port in one transaction:
```
ovs-vsctl -- set port eth0 qos=@newqos -- --id=@newqos create qos type=linux-htb other-config:max-rate=1000000 queues:0=@newqueue -- --id=@newqueue create queue other-config:min-rate=1000000 other-config:max-rate=1000000
```
QoS `type` values: `linux-htb`, `linux-hfsc`, `linux-sfq`, `linux-codel`, `linux-fq_codel`, `linux-netem`, `linux-noop`, `egress-policer`, `trtcm-policer`.

Settings:
- QoS `other_config:max-rate` (htb/hfsc), bit/s; defaults to the link rate for physical interfaces, otherwise 10 Gbps.
- QoS `queues`: map from queue id (0 to 4294967295) to Queue; queue 0 is the default and auto-configured if absent. htb/hfsc ids must be below 61440.
- Queue `other_config`: `min-rate` and `max-rate` (bit/s, at least 1), `burst` (htb, bits), `priority` (htb, default 0, lower gets excess first); `dscp` column 0 to 63.

Steer traffic: `set_queue:N` before output (e.g. `actions=set_queue:1,output:2`); `pop_queue` restores the default. `enqueue(port,queue)` is OpenFlow 1.0 only.

Inspect: `ovs-appctl qos/show-types eth0`, `ovs-appctl qos/show eth0`.

Remove: `ovs-vsctl clear Port eth1 qos`, then destroy the records (unreferenced QoS and Queue records are not auto-deleted): `ovs-vsctl destroy QoS <uuid>`, `ovs-vsctl destroy Queue <uuid>` or `ovs-vsctl -- --all destroy Queue`.

## Checked
2026-11-09. Read the QoS and Queue tables of ovs-vswitchd.conf.db(5) (types, queues key range, queue 0 default, max-rate default, 61440 queue id limit, min-rate, max-rate, burst, priority, dscp), the QoS example in ovs-vsctl(8) (create, clear Port qos, destroy), qos/show and qos/show-types in ovs-vswitchd(8), and the set_queue, pop_queue and enqueue sections of ovs-actions(7). Nothing removed.
Method: documentation only; no commands were run.
