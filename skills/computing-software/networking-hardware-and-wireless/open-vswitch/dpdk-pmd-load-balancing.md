---
id: computing-software.networking-hardware-and-wireless.open-vswitch.dpdk-pmd-load-balancing
name: dpdk-pmd-load-balancing
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, dpdk, pmd-auto-lb, pmd-rxq-assign, pmd-sleep-max, pmd-rxq-rebalance, load-balancing, pmd]
level: advanced
status: docs-checked
description: "Balance Open vSwitch DPDK receive queues across PMD threads: pmd-rxq-assign modes, pmd-auto-lb thresholds, pmd-rxq-rebalance, pmd-sleep-max."
sources:
  - https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PMD load balancing
Assignment policy:
`ovs-vsctl set Open_vSwitch . other_config:pmd-rxq-assign=cycles` (also `group`, `roundrobin`).

Automatic rebalance:
```
ovs-vsctl set Open_vSwitch . other_config:pmd-auto-lb=true
ovs-vsctl set Open_vSwitch . other_config:pmd-auto-lb-load-threshold=95
ovs-vsctl set Open_vSwitch . other_config:pmd-auto-lb-improvement-threshold=25
ovs-vsctl set Open_vSwitch . other_config:pmd-auto-lb-rebal-interval=1
```
Defaults: load threshold 95, improvement threshold 25, interval 1 minute. A rebalance happens only when the estimated improvement beats the threshold.

Manual: `ovs-appctl dpif-netdev/pmd-rxq-rebalance`, then check `pmd-rxq-show`.

Power saving: `other_config:pmd-sleep-max=50` sets a maximum sleep in microseconds (per core form such as `50,8:0`); `ovs-appctl dpif-netdev/pmd-sleep-show` displays it.

Verify: `ovs-appctl dpif-netdev/pmd-rxq-show` before and after shows moved queues.

Gotcha: auto load balance needs two or more non-isolated PMDs, cycles or group assignment, and at least one non-isolated PMD polling more than one Rx queue. It does not operate if Rx queues sit on a PMD in a different NUMA node (unless all PMDs are on one NUMA node).

## Checked
2026-11-09. Read in full: docs.openvswitch.org topics/dpdk/pmd (pmd-rxq-assign cycles/group/roundrobin, pmd-auto-lb prerequisites, load threshold default 95%, improvement threshold default 25%, rebal interval in minutes default 1, pmd-rxq-rebalance, pmd-sleep-max with core:value form, pmd-sleep-show). Removed: the unsupported claim about pinned queues; dropped the unused conf.db source.
Method: documentation only; no commands were run.
