---
id: computing-software.software-engineering.debugging.oom-kills-and-container-memory-limits
name: oom-kills-and-container-memory-limits
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, memory-debugging, oom-killer, oomkilled, cgroups, container-memory-limits, exit-code-137, kubernetes]
level: practitioner
status: docs-checked
description: "Diagnose OOM kills (exit 137, OOMKilled): Kubernetes and cgroup v2 evidence, what counts against a memory limit, and fix patterns."
sources: ["https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/", "https://docs.kernel.org/admin-guide/cgroup-v2.html", "https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html", "https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OOM kills and container memory limits

**Goal:** when a process dies with exit code 137 / `OOMKilled`, prove it was memory,
find what consumed it, and size limits and runtimes so it stops.

## Evidence
```bash
kubectl describe pod <pod>       # Last State: Terminated, Reason: OOMKilled, Exit Code: 137
kubectl get pod <pod> --output yaml    # lastState.terminated: exitCode 137, reason OOMKilled
```
The Events section of `kubectl describe` can show a `Warning OOMKilling` line with the text
"Memory cgroup out of memory: Kill process ...".
Kubernetes shows `Reason: OOMKilled` with `Exit Code: 137` when a container exceeds its
memory limit, and the restart count rises as the container is restarted.
In cgroup v2, `memory.events` has an `oom_kill` counter: the number of processes of that
cgroup killed by any kind of OOM killer. `memory.events.local` is the non-hierarchical version.

## How limits are enforced
- Kubernetes: memory limits are enforced reactively by the kernel with OOM kills. A container
  that over-allocates is not necessarily killed immediately; the kernel acts when it detects
  memory pressure.
- cgroup v2 `memory.max` is the hard limit: if usage reaches it and cannot be reduced, the
  OOM killer is invoked inside that cgroup, and it never kills tasks outside the cgroup.
- `memory.high` throttles the cgroup with reclaim and never invokes the OOM killer, so a
  too-low high boundary shows as slowdown, not kills.
- `memory.oom.group` makes the OOM killer treat the cgroup as one workload (all tasks killed
  together or none). Tasks with `oom_score_adj` -1000 are never killed.
- A container with no limit can use all node memory, and in a node OOM it has a greater chance
  of being killed.
- Node-level victim choice uses `/proc/<pid>/oom_score`: a higher score means more likely to be
  selected, and it reflects `oom_score_adj`.

## What counts against the limit
- The cgroup memory page cache includes tmpfs and shared memory (cgroup v2 `memory.stat`).
- The Kubernetes limit also applies to pages in memory-backed volumes such as `emptyDir` with
  `medium: Memory`; the kubelet tracks tmpfs `emptyDir` as container memory use. With a pod memory
  limit set, the maximum size of such an `emptyDir` is the pod's memory limit.
- Runtime heap settings (JVM, Node, Go, .NET) are not covered by these sources: look up your
  runtime's container-sizing docs and leave headroom below the limit for non-heap memory.

## Fix patterns
- Real leak: see the managed and native memory-leak skills.
- Legitimate peak (batch job, large upload): stream instead of buffering, bound concurrency,
  or raise the limit.

## Verify
- [ ] Root cause tied to a memory metric trend or profile, not guessed.
- [ ] The runtime's heap cap leaves measured headroom below the container limit under peak load.

## Checked
2026-11-09. Confirmed against the Kubernetes "Resource Management for Pods and Containers" and
"Assign Memory Resources" pages (OOMKilled, exit code 137, reactive enforcement, tmpfs emptyDir
counted as memory), the cgroup v2 admin guide (memory.max, memory.high, memory.events oom_kill,
memory.oom.group) and proc_pid_oom_score(5). Removed: dmesg/journalctl/docker inspect commands,
the working-set metric claim, the eviction note, the 128+9 explanation, and all per-runtime flags
(MaxRAMPercentage, NativeMemoryTracking, max-old-space-size, GOMEMLIMIT, DOTNET_* settings) and
the 85-90% alert threshold, none stated by the cited pages.
Method: documentation only; no commands were run.
