---
id: computing-software.software-engineering.erlang.container-cpu-memory
name: container-cpu-memory
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-containers-ci, container-cpu-memory]
level: sme
status: draft
description: "BEAM in containers: scheduler count versus CPU quota, memory limits, dirty schedulers and crash dump volume."
sources:
  - https://github.com/erlef/setup-beam
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running the BEAM under CPU and memory limits
**Goal:** avoid throttling and OOM kills in Kubernetes or Docker.

- Set CPU requests/limits and align the scheduler count: `+S N:N` or `ERL_FLAGS="+S 2:2"` to match the CPU limit; more schedulers than the quota cause CFS throttling.
- Newer OTP versions read cgroup CPU limits to size schedulers (support depends on version; unconfirmed which), so verify with `erlang:system_info(schedulers_online)` inside the container.
- Memory: the VM can exceed expectations because of fragmentation and binary buffers; set the container memory limit with headroom and watch `erlang:memory(total)` plus OS RSS.
- Limit per-process memory with `max_heap_size` and message queue checks.
- Mount a volume for `erl_crash.dump` and send logs to stdout.
- Use readiness probes against a health endpoint, and a preStop wait for graceful shutdown.

## Gotchas
- Kubernetes distribution clustering needs stable DNS names or a peer discovery library; static `-name` per pod otherwise.

## Self-check
Run with a CPU limit of 1 and compare latency with `+S 1:1` versus default.
