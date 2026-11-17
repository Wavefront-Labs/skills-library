---
id: computing-software.cloud-infrastructure-engineering.openbao.raft-autopilot
name: raft-autopilot
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, autopilot, dead-server-cleanup, server-stabilization-time, min-quorum]
level: advanced
status: docs-checked
description: "Tune OpenBao raft Autopilot: server stabilization, dead server cleanup, min_quorum, and the documented defaults."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/integrated-storage/autopilot.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raft Autopilot

Autopilot is enabled by default; dead server cleanup is not.

## Features

- **Server stabilization**: new voters join as non-voters and are promoted after staying healthy for `server_stabilization_time`.
- **Dead server cleanup**: unhealthy nodes are removed automatically.
- **State API**: details on all Raft nodes in one call, for monitoring.

## Settings and defaults

- `cleanup_dead_servers`: `false`; requires `min_quorum` too
- `dead_server_last_contact_threshold`: `24h` (only when cleanup is on)
- `min_quorum`: no default; set to the expected voter count when cleanup is enabled, since Autopilot will not prune below it
- `max_trailing_logs`: `1000` (how far a log may lag before unhealthy)
- `last_contact_threshold`: `10s`
- `server_stabilization_time`: `10s`

Configure through the Autopilot configuration API (see the raftautopilot API page).

## Gotcha

OpenBao's Autopilot resembles Consul's, but defaults and thresholds differ, and the underlying implementations differ. Do not copy Consul values across.

## Checked

2026-11-04. Read the OpenBao Autopilot concepts page in full. Confirmed: the three features, follower health factors, every default listed (`cleanup_dead_servers`, `dead_server_last_contact_threshold`, `min_quorum`, `max_trailing_logs`, `last_contact_threshold`, `server_stabilization_time`), the configuration API and the Consul difference note. Removed: nothing.
Method: documentation only; no commands were run.
