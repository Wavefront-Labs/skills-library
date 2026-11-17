---
id: computing-software.cloud-infrastructure-engineering.netdata.sizing-agent-overview
name: sizing-agent-overview
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, sizing, resource-requirements, capacity-planning]
level: practitioner
status: docs-checked
description: "Baseline CPU, RAM and disk for a standalone Netdata Agent and the feature settings that move them: collectors, frequency, DB mode, tiers, ML, streaming."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/sizing-netdata-agents/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Standalone Agent minimums from the docs:
- CPU: 1%-5% of one core on defaults; 5%-20% in production.
- RAM: 100-200 MB on an empty system; 250-350 MB typical production.
- Disk: about 4 GiB by default (3 GiB metrics plus metadata), configurable per tier.
- Root (Linux) or Administrator (Windows) to install.

What moves the numbers:
- Collected metrics: CPU, RAM, disk I/O and space. Disable unneeded collectors.
- Sample frequency: lowering it, for example 1 s to 2 s, can halve CPU.
- Database mode: on a Child in a Parent-Child setup, `ram` removes disk I/O.
- Database tiers: default is 3; more tiers use more memory.
- Machine learning: CPU and RAM; disable for less critical metrics or adjust training frequency.
- Streaming: CPU, RAM and network; pick a compression algorithm to balance (docs suggest zstd).

Parents scale with Children count and retention. They adapt automatically but may need more RAM for query performance.

For sizing numbers, see the dedicated RAM, CPU, disk and bandwidth pages.

## Checked

2026-11-04. Confirmed against the Netdata Resource utilization page: the CPU, RAM, disk and privilege figures, the five feature rows and their optimisation advice (frequency halving CPU, ram mode on Children, default 3 tiers, ML, zstd), and the Parent scaling note. Removed the closing Verify line, which the page does not state, and reworded the gotcha.

Method: documentation only; no commands were run.
