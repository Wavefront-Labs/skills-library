---
id: computing-software.networking-hardware-and-wireless.unbound.munin-and-cacti-graphs
name: munin-and-cacti-graphs
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, munin, cacti, graphing, unbound-munin, monitoring]
level: intro
status: draft
description: "Graph Unbound statistics with the Munin plugin or the Cacti contrib package: setup steps, plugin environment settings and available graph names."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/core/monitoring.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# munin and cacti graphs
Munin:
1. Install `munin` and `munin-node`.
2. Copy the `unbound_munin_` plugin script from the Unbound source `contrib` directory somewhere on the system.
3. Symlink it into the munin plugins directory under a graph name, e.g. `ln -s /etc/unbound/unbound_munin_ /etc/munin/plugins/unbound_munin_hits`.
4. In the `[unbound*]` section of `plugin-conf.d/plugins.conf` set `user root`, `env.statefile`, `env.unbound_conf`, `env.unbound_control`, and optionally `env.spoof_warn` (default 1000) and `env.spoof_crit` (default 100000).
5. Restart `munin-node`.

Graph names: `unbound_munin_hits`, `_queue`, `_memory`, `_by_type`, `_by_class`, `_by_opcode`, `_by_rcode`, `_by_flags`, `_histogram`. Several need `extended-statistics: yes`.

Set `statistics-cumulative: yes` if the tool expects ever-increasing counters.

Cacti: follow the README in `contrib/unbound_cacti.tar.gz` in the Unbound source, contributed by Dmitriy Demidov.

Both depend on a working `unbound-control`.
