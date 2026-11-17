---
id: computing-software.cloud-infrastructure-engineering.kubernetes.node-level-logging-with-fluent-bit-and-fluentd
name: node-level-logging-with-fluent-bit-and-fluentd
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, fluent-bit, fluentd, daemonset, logging, log-rotation, multiline-parsing, backpressure, containerd-logs, cri-log-format, kubernetes-filter, tail-input]
level: advanced
status: docs-checked
description: "Running Fluent Bit/Fluentd as a node-level DaemonSet log pipeline: tail-position tracking, multiline parsing, backpressure, and log-rotation loss."
sources: ["https://docs.fluentbit.io/manual/pipeline/inputs/tail", "https://docs.fluentbit.io/manual/pipeline/filters/kubernetes", "https://docs.fluentbit.io/manual/administration/backpressure", "https://kubernetes.io/docs/concepts/cluster-administration/logging/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node-level logging with Fluent Bit / Fluentd: the DaemonSet pattern and its gotchas

**Goal:** understand why node-level log collection is a DaemonSet tailing files, not a
central service pulling logs, and the handful of failure modes (rotation loss, multiline
splitting, backpressure) that cause silent gaps rather than errors.

## 1. The architecture
Kubernetes gives you no built-in log shipping. The standard pattern is a **DaemonSet** (one
Fluent Bit/Fluentd pod per node) that:
1. Tails container log files on the host — containerd writes them to
   `/var/log/containers/<pod>_<namespace>_<container>-<id>.log` (symlinks into
   `/var/log/pods/.../*.log`, which itself symlinks into the real log file under the
   container's log directory). The DaemonSet mounts these host paths read-only.
2. Parses the **CRI log format** (the kubelet's standard container log format). Fluent Bit's built-in
   `cri` multiline parser handles CRI logs and concatenates split entries; without that step long lines
   are fragmented.
3. Attaches Kubernetes metadata (pod, namespace, labels, annotations) via the
   `kubernetes` filter (Fluent Bit) / `kubernetes_metadata` plugin (Fluentd), which calls the
   Kubernetes API (or kubelet) and caches the result in memory (`kube_meta_cache_ttl` is 0 by default, meaning no TTL).
4. Buffers and ships to a backend (Loki, Elasticsearch, a cloud log sink) — see
   `computing-software.cloud-infrastructure-engineering.kubernetes.loki-log-aggregation-in-kubernetes`
   for that half.

Fluent Bit and Fluentd are often combined (Fluent Bit on nodes, Fluentd as an aggregator); don't assume only
one component when debugging a gap. The Fluent Bit `forward` and `loki` outputs both exist.

## 2. Log rotation is the silent-loss failure mode
The kubelet rotates container logs (`containerLogMaxSize` default 10Mi, `containerLogMaxFiles` default 5).
If the collector falls behind a fast rotation cycle, lines can be lost. Fluent Bit's `tail` input has
`rotate_wait` (default 5 seconds of extra monitoring after rotation) and a `db` file that stores
monitored files and offsets. With a database, the last offset is restored on restart; without one,
files discovered at start are read from the end unless `read_from_head` is true (default false), so
lines written while the pod was down can be missed. Put the `db` file on a hostPath volume so it
survives pod restarts.

## 3. Multiline parsing
Stack traces, JSON pretty-printed across lines, and any app not emitting one-event-per-line
need multiline rules or they ship as N separate broken events. Two layers to configure
correctly:
- CRI-level joining of split entries: the built-in `cri` (and `docker`) multiline parsers; `docker_mode`
  is an older alternative that cannot be combined with multiline.
- **Application-level multiline** (a Java stack trace): the tail input's `multiline.parser` property takes
  one or more multiline parser definitions (built-ins include `java` and `python`, or define your own),
  configured per log format.

## 4. Backpressure and resource limits
- Under a log burst, Fluent Bit's `mem_buf_limit` makes the input pause (a `paused (mem buf overlimit)` warning)
  until buffered chunks flush. The docs say some inputs can lose data in memory-only buffering and
  recommend filesystem buffering (`storage.type filesystem`) when loss must be avoided. A paused tail input
  falls behind and risks rotation loss.
- One DaemonSet pod serves the whole node, so one very chatty pod can delay shipping for the others.
- Size requests and limits for the log DaemonSet; if it is OOM-killed the node's logs stop.

## Gotchas
- `kubectl logs` reads the same node log files the collector tails; if `kubectl logs` works but nothing
  reaches the backend, look at the collector. `kubectl logs` returns at most the current log file
  content (for example 10MiB of a 40MiB burst when rotation is at 10MiB).
- The `fluentbit.io/exclude` pod annotation only takes effect when the Kubernetes filter has
  `K8S-Logging.Exclude` enabled (likewise `fluentbit.io/parser` needs `K8S-Logging.Parser`).
- stdout/stderr only: anything an app writes to a file inside the container instead of stdout
  needs a sidecar or an explicit file tail, standard DaemonSet collection never sees it.

## Verify
- [ ] A deliberately long (multi-KB) single log line and a multi-line stack trace both arrive in the backend as one event each, not fragmented.
- [ ] The Fluent Bit `db` offset file is on a hostPath volume that survives pod restarts.
- [ ] Collector resource usage and buffer pause warnings are monitored.

## Checked

2026-10-26, against Fluent Bit docs (fluent/fluent-bit-docs, latest commit 2026-10-24: tail input, Kubernetes filter, multiline parsing, buffering, backpressure) and the Kubernetes logging architecture page. Confirmed: kubelet rotation defaults (10Mi, 5 files), tail `db`, `rotate_wait` (5), `read_from_head`, `docker_mode`, `multiline.parser`, built-in cri/docker/java/python multiline parsers, `mem_buf_limit` pause behaviour and filesystem buffering advice, Kubernetes filter exclude and parser annotations, metadata caching defaults. Wrong: `Mem_Buf_Limit` was described as dropping events (the input pauses), and restarts without a database were described as re-reading from the start (default is to start at the end). Removed unconfirmed binary-size, CRI line layout and Fluentd-specific (`overflow_action`) claims; Fluentd configuration was not checked.

Method: documentation only; no commands were run.
