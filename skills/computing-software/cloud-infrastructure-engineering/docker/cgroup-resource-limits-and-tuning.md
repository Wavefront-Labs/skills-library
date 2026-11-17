---
id: computing-software.cloud-infrastructure-engineering.docker.cgroup-resource-limits-and-tuning
name: cgroup-resource-limits-and-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, cgroups, cgroup-v2, cgroup-v1, memory-limit, oom-killer, oom-score-adj, cpu-shares, cpu-quota, cpuset, memory-swappiness, memory.max, pids-limit, docker-stats, throttling, cfs-scheduler, unified-hierarchy, systemd-cgroup-driver]
level: advanced
status: docs-checked
description: "What --memory and --cpus actually set in cgroups, why a container gets OOM-killed under its limit, CPU throttling vs shares, and reading the real numbers from /sys/fs/cgroup."
sources: ["https://docs.docker.com/engine/containers/resource_constraints/", "https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.docker.com/engine/deprecated/", "https://docs.kernel.org/admin-guide/cgroup-v2.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cgroup resource limits and tuning for containers

**Goal:** know what `--memory`/`--cpus` actually configure in the kernel, why a container
dies at a memory number that "should" have been enough, and how to read the ground truth
instead of trusting `docker stats` alone.

## Memory
`--memory=512m` sets `memory.max` (cgroup v2; `memory.limit_in_bytes` on v1) — a hard cap.
Exceeding it does not get a graceful warning: the kernel OOM-killer fires **inside that
cgroup**, killing processes in that container, often your main process — `docker inspect <id> --format '{{.State.OOMKilled}}'`
confirms this after the fact; exit code `137` (SIGKILL) is the symptom you see first.
- `--memory-swap` sets the combined memory+swap ceiling; `--memory-swap` equal to `--memory`
  disables swap for the container entirely. Leaving `--memory-swap` unset while setting
  `--memory` lets the container use as much swap as the `--memory` value (for example 300m memory gives 600m total memory plus swap), if the host has swap configured. `--memory-swap=-1` allows unlimited swap and `0` is ignored.
- `--memory-reservation` is a soft limit (it must be lower than `--memory`) used only when Docker detects contention or low memory on the host — not a
  guarantee, don't treat it as a request/limit pair the way Kubernetes uses those terms.
- Runtimes with managed heaps (JVM, Node) use memory beyond the heap, so leave headroom between the runtime's own heap setting and the container's `--memory` cap; consult the runtime's documentation for its heap-sizing flags.

## CPU
Two different, easily confused knobs:
- `--cpus=1.5` — a **hard ceiling**: the container cannot use more than 1.5 cores even if
  the host is otherwise idle. Implemented via CFS quota/period (`cpu.max` on v2:
  `150000 100000` = 1.5 cores per 100ms period). Good for predictable
  performance in a noisy-neighbor environment; bad if you actually wanted a *minimum*, not
  a cap — the container will throttle (visibly as added latency, not an error) even with
  idle cores sitting right there.
- `--cpu-shares=512` — a **relative weight** (default 1024), only enforced when CPU cycles are constrained. This is the "fair scheduling priority" knob, not a cap.
- `--cpuset-cpus=0,1` pins a container to specific cores — useful for cache-locality-
  sensitive workloads or isolating noisy containers to cores you've already reserved via
  `isolcpus`, not needed for ordinary workloads.
- Throttling is invisible in `docker stats` CPU% (which can read well under 100% while
  still being throttled in short bursts); check `cpu.stat`'s `nr_throttled`/
  `throttled_usec` under `/sys/fs/cgroup/.../<container>/` for the real signal when
  latency looks bursty but CPU% looks fine.

## cgroup v1 vs v2
Docker deprecated cgroup v1 support in Engine 29.0, though it keeps supporting it until May 2029. Docker auto-detects the version and maps `--memory`/`--cpus` to the right v1 or v2 files, so
the CLI flags don't change — but the filesystem paths you'd inspect by hand do
(`memory.limit_in_bytes` under the v1 memory controller vs `memory.max` on v2; the exact directory depends on the cgroup driver). `docker info` shows `Cgroup Version` (or `docker info -f '{{.CgroupVersion}}'`), so check which you are on before hunting for a file that moved.

## pids-limit
`--pids-limit=200` caps the number of processes/threads a container can fork — the fix for
a fork-bomb (accidental or malicious) taking down the whole host by exhausting the kernel's
global PID table, which otherwise isn't contained by memory/CPU limits at all.

## Verify
The `memory.max` file inside the container's cgroup matches the
`--memory` value you set; deliberately run a container that allocates past its limit and
confirm `docker inspect --format '{{.State.OOMKilled}}'` reports `true` and the exit code is
`137`, not a silent hang or a different failure.

## Checked

Checked against docker/docs `engine/containers/resource_constraints.md`, the `docker container run` option reference (`data/cli/engine/docker_container_run.yaml`) and `engine/deprecated` (docker/docs latest commit 2026-10-23, Engine 29).

- `--memory-swap` semantics (equal to `--memory` disables swap; unset gives total twice `--memory`; `-1` unlimited; `0` ignored), `--memory-reservation` must be lower than `--memory`, `--cpu-shares` default 1024 and only enforced under constraint, `--cpuset-cpus`, `--oom-kill-disable`/`--oom-score-adj` guidance.
- `--pids-limit` is an int64 option (`-1` for unlimited, default 0).
- Cgroup v1 deprecated in Engine 29.0 and supported until May 2029; `docker info` reports `Cgroup Version`.
- Removed as unconfirmed: oom_score_adj victim selection, JVM flag guidance, distro default list and the host-specific cgroup file paths. `cpu.max` (format `$MAX $PERIOD`), `cpu.stat` fields `nr_throttled` and `throttled_usec`, and `memory.max` were confirmed in the Linux kernel cgroup-v2 admin guide (`Documentation/admin-guide/cgroup-v2.rst`, current mainline).

Method: documentation only; no commands were run.
