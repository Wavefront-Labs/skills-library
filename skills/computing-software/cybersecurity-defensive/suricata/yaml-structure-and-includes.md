---
id: computing-software.cybersecurity-defensive.suricata.yaml-structure-and-includes
name: yaml-structure-and-includes
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [suricata-yaml, include, default-log-dir, max-pending-packets]
level: intro
status: docs-checked
description: "Orient yourself in suricata.yaml: include and !include, default-log-dir, max-pending-packets, runmode, default-packet-size and the main sections."
sources: ["https://docs.suricata.io/en/latest/configuration/suricata-yaml.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# suricata.yaml basics

- `include:` and `!include` split config into files, for example `outputs: !include outputs.yaml`. A later include overwrites earlier sections.
- `default-log-dir`: where alerts and events go; `-l` overrides it.
- `max-pending-packets` (example 1024): packets processed simultaneously. Higher uses more RAM; too low leaves cores idle.
- `runmode` (disabled by default, example `autofp`); list options with `--list-runmodes`.
- `default-packet-size` (example 1514): sizes packet memory. Larger packets still work, more slowly.

Main areas: vars, outputs, threading, stream, app-layer, detect, defrag, flow, flow-timeouts, rule files, capture sections (af-packet, dpdk, pf-ring, nfq, ipfw), engine-analysis and profiling.

## Checked

2026-11-04. Confirmed against the suricata.yaml configuration page (max-pending-packets, runmodes, default-packet-size, include and !include, default-log-dir, engine-analysis, profiling).

Removed: a closing verification tip.

Method: documentation only; no commands were run.
