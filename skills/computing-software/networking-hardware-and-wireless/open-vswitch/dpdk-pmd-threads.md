---
id: computing-software.networking-hardware-and-wireless.open-vswitch.dpdk-pmd-threads
name: dpdk-pmd-threads
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, dpdk, pmd, pmd-cpu-mask, pmd-rxq-affinity, n-rxq, emc, smc, pmd-perf-show, pmd-rxq-show]
level: advanced
status: docs-checked
description: "Pin and inspect DPDK PMD threads in Open vSwitch: pmd-cpu-mask, n_rxq, pmd-rxq-affinity, pmd-rxq-show, pmd-perf-show, EMC and SMC settings."
sources:
  - https://docs.openvswitch.org/en/latest/topics/dpdk/pmd/
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PMD threads
- Cores: `ovs-vsctl set Open_vSwitch . other_config:pmd-cpu-mask=0xc` (cores 2 and 3).
- Queues per port: `ovs-vsctl set Interface dpdk-p0 options:n_rxq=2`.
- Pin queues: `ovs-vsctl set Interface dpdk-p0 other_config:pmd-rxq-affinity="0:4,1:5"` (queue:core pairs).

Inspect:
- `ovs-appctl dpif-netdev/pmd-rxq-show` shows queue to PMD assignment and load.
- `ovs-appctl dpif-netdev/pmd-stats-clear` resets the cumulative PMD stats before a measurement.
- `ovs-appctl dpif-netdev/pmd-perf-show` needs `other_config:pmd-perf-metrics=true`.

Caches:
- `other_config:emc-insert-inv-prob` default 100 (insert about 1 in 100 flows); 0 disables the EMC.
- Per interface: `other_config:emc-enable`.
- `other_config:smc-enable` is false by default.

Verify: `pmd-rxq-show` lists each rxq under the core you pinned.

Gotcha: PMD threads on cores with pinned Rx queues become isolated by default and poll only those queues; with no non-isolated PMD left, unpinned queues are not polled.

## Checked
2026-11-09. Read in full: docs.openvswitch.org topics/dpdk/pmd (n_rxq, pmd-rxq-affinity example and isolation warning, pmd-rxq-show, pmd-perf-show, pmd-perf-metrics, pmd-stats-clear). Partial read of ovs-vswitchd.conf.db.5 and ovs-vswitchd.8 man pages: pmd-cpu-mask, emc-insert-inv-prob (default 100, 0 disables EMC), emc-enable (per interface), smc-enable (default false), pmd-perf-metrics, pmd-stats-clear. Removed: pmd-stats-show (not in the man page) and the 100% CPU/isolated core advice (not stated).
Method: documentation only; no commands were run.
