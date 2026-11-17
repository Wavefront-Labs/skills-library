---
id: computing-software.cybersecurity-defensive.suricata.threading-and-cpu-affinity
name: threading-and-cpu-affinity
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [threading, cpu-affinity, worker-cpu-set, autopin]
level: advanced
status: docs-checked
description: "Pin Suricata threads: set-cpu-affinity, management, receive and worker cpu sets, balanced versus exclusive mode, priorities, autopin and per-interface sets."
sources: ["https://docs.suricata.io/en/latest/configuration/suricata-yaml.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Threading and CPU affinity

`threading` section:
- `set-cpu-affinity: no` by default; the sample config has `autopin: no`.
- `detect-thread-ratio: 1.5` is the default multiplier of CPU cores.
- `stack-size: 8MB` suggested if the build default is too small.
- Sets: `management-cpu-set`, `receive-cpu-set`, `worker-cpu-set`, `verdict-cpu-set`. Each has `cpu` (`all`, ranges or lists), `mode` (`balanced` or `exclusive`) and `prio` (`low`, `medium`, `high`, `default`).
- `interface-specific-cpu-set` (8.0) overrides worker and receive sets per interface.
- `autopin` pins workers to the NUMA node of the capture interface; needs `hwloc` and `--enable-hwloc`.

DPDK takes worker cores from `threading.cpu-affinity["worker-cpu-set"]`.

## Checked

2026-11-04. Confirmed against the suricata.yaml configuration page: Threading, CPU affinity sets (cpu, mode, prio), interface-specific CPU affinity, NUMA-aware autopin with hwloc, DPDK section.

Changed: `autopin: no` is stated only as the sample value, not as a documented default.

Method: documentation only; no commands were run.
