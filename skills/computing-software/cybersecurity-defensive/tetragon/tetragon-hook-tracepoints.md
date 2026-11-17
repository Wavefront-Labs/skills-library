---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-hook-tracepoints
name: tetragon-hook-tracepoints
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [hook-tracepoint, tetragon, tracing-policy]
level: practitioner
status: docs-checked
description: "Hook kernel tracepoints and raw tracepoints in a Tetragon TracingPolicy, including args by index, the raw flag and resolve."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/hooks/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon tracepoint hooks

Goal: observe a statically defined kernel tracepoint from a `TracingPolicy`. Tracepoints are stable across kernel versions, so they are more portable than kprobes.

## Find the tracepoint

- List subsystems: `sudo ls /sys/kernel/tracing/events`
- Read an event's format: `sudo cat /sys/kernel/tracing/events/net/netif_receive_skb/format`
- Tracepoints can also hook system calls; see the `raw_syscalls` and `syscalls` subsystems.

## Standard tracepoint

Observe all syscalls and read the syscall ID from the argument at index 4:

```yaml
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata:
  name: "raw-syscalls"
spec:
  tracepoints:
  - subsystem: "raw_syscalls"
    event: "sys_enter"
    args:
    - index: 4
      type: "int64"
```

## Raw tracepoints

Set `raw: true`. Raw tracepoints give access to the raw tracepoint arguments (standard ones expose arguments through the tracepoint format). They attach without the perf layer, so should be a bit faster.

The kernel defines arguments with `TRACE_EVENT(...)`, e.g. `sched_process_exec` has `TP_PROTO(struct task_struct *p, pid_t old_pid, struct linux_binprm *bprm)`. Store the 3rd argument:

```yaml
spec:
  tracepoints:
    - subsystem: "sched"
      event: "sched_process_exec"
      raw: true
      args:
        - index: 2
          type: "linux_binprm"
```

The event reports `linux_binprm_arg` with `path` (e.g. `/usr/bin/ls`) and `permission` (e.g. `rwxr-xr-x`).

Use `resolve` to pull a field from an argument, for example the `pid` of the first `task_struct` argument:

```yaml
      args:
        - index: 0
          type: "int"
          resolve: "pid"
        - index: 2
          type: "linux_binprm"
```

That yields an `int_arg` with the pid plus the `linux_binprm_arg`.

## Checked

Date: 2026-11-07

Hook points page read in full (about 41 KB); every claim matched, no change.

Method: documentation only; no commands were run.
