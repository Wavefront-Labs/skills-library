---
id: computing-software.cloud-infrastructure-engineering.docker.diagnosing-oomkilled-containers
name: diagnosing-oomkilled-containers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, oom, oomkilled, memory-limit, exit-code-137, cgroups, memory-events]
level: advanced
status: docs-checked
description: "Confirm and fix container OOM kills: State.OOMKilled vs exit 137, cgroup memory.events, kernel logs, host vs cgroup OOM, runtime heap sizing, and limits that fit."
sources: ["https://docs.docker.com/engine/containers/resource_constraints/", "https://docs.kernel.org/admin-guide/cgroup-v2.html#memory-interface-files", "https://docs.docker.com/reference/cli/docker/inspect/", "https://docs.docker.com/reference/cli/docker/system/events/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing OOMKilled containers

## Confirm it was an OOM kill
```bash
docker inspect -f 'OOMKilled={{.State.OOMKilled}} Exit={{.State.ExitCode}} Finished={{.State.FinishedAt}}' <c>
docker events --filter event=oom --since 24h
```
- `OOMKilled=true`: the kernel's OOM killer acted on the container. `oom` is a documented
  container event type in `docker events`.
- The `docker run` reference says exit codes other than 125, 126 and 127 are the contained
  command's own exit code, so read the code together with `OOMKilled` and the events.
- If only a child process was killed, check `memory.events` and the application logs.

## Read the cgroup counters (cgroup v2)
```bash
P=<the container's cgroup directory under /sys/fs/cgroup; the path depends on the cgroup driver>
cat $P/memory.max $P/memory.current $P/memory.peak
cat $P/memory.events          # low, high, max, oom (and oom_kill) counters
cat $P/memory.stat
```
Per the kernel's cgroup v2 documentation, `memory.stat` `shmem` covers tmpfs and shared memory,
which count against the cgroup's memory.

## Common causes and fixes
| Cause | Fix |
|---|---|
| Runtime heap sized above the container limit (JVM, Node.js, Go) | Set the runtime's own heap limit below the container limit (check the runtime's documentation for the flag) |
| Worker count multiplied by per-worker memory | Fewer workers, shared memory |
| tmpfs / `/dev/shm` writes | Size tmpfs explicitly; it counts as shared memory |
| Real leak | Track `memory.current` over time, take heap dumps before the limit |

Set limits from observed peak plus headroom: `docker stats --no-stream` or `memory.peak`
over a representative load.

## Host-level OOM
Docker's resource-constraints page: on a host OOM (OOME) the kernel may kill any process,
including Docker. Docker lowers the daemon's OOM priority but not the containers', so a
container is likelier to be killed than the daemon. Do not set `--oom-score-adj` to an extreme
negative value or use `--oom-kill-disable` to get around this; `--oom-kill-disable` is only
safe on containers that also have `-m/--memory` set.

## Gotchas
- `--memory-swap` equal to `--memory` (with `--memory` set) means no swap. If `--memory-swap`
  is unset and the host has swap, the container can use as much swap as `--memory`
  (for example 300m memory gives 600m total).
- Restart policies turn OOMs into restart loops; watch for `oom` in `docker events`.

## Checked
Date: 2026-10-26. Documentation: docker/docs main (last commit 2026-10-23) resource constraints page and run reference; Linux cgroup-v2 documentation (torvalds/linux). Confirmed: `--memory-swap` rules, `--oom-kill-disable` caveat, daemon OOM priority behaviour, `oom` event, exit-code rule, cgroup v2 file names (memory.max/current/peak/events/stat) and the events keys, shmem accounting. Removed as unconfirmed: dmesg grep patterns, the 137 and OOMKilled=false explanations, the systemd-scope cgroup path, JVM, Node and Go flag recommendations, oom_score_adj numbers, "can hang the host".
Method: documentation only; no commands were run.
