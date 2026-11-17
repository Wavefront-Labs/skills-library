---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-action-sock-set-state
name: tetragon-action-sock-set-state
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [action-sock-state, tetragon, tracksock, notify-enforcer, updatestate]
level: advanced
status: docs-checked
description: "Use Tetragon TrackSock/UntrackSock, NotifyEnforcer, Set and UpdateState actions in a TracingPolicy for socket tracking, syscall enforcement and policy state."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/selectors/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon socket, enforcer, Set and state actions

Goal: pick the right advanced `matchActions` entry in a TracingPolicy selector.

## TrackSock / UntrackSock

`TrackSock` maps sockets to processes in a BPF map (kernel 5.3+). Every `TrackSock` needs a matching `UntrackSock`, otherwise the BPF map will be broken. `UntrackSock` deletes the entry for the sock argument at `argSock`:

```yaml
- call: "__sk_free"
  syscall: false
  args:
    - index: 0
      type: sock
  selectors:
    - matchActions:
      - action: UntrackSock
        argSock: 0
```

## NotifyEnforcer

For kernels without `kprobe_multi`. The spec needs `enforcers` (only a single definition allowed) listing syscalls or a `list:` name; the action takes `argError` (passed to `bpf_override_return`) and `argSig` (passed to `bpf_send_signal`). Kill bash on `sys_dup`/`sys_dup2`:

```yaml
spec:
  lists:
  - name: "dups"
    type: "syscalls"
    values: ["sys_dup", "sys_dup2"]
  enforcers:
  - calls: ["list:dups"]
  tracepoints:
  - subsystem: "raw_syscalls"
    event: "sys_enter"
    args:
    - index: 4
      type: "syscall64"
    selectors:
    - matchArgs:
      - index: 0
        operator: "InMap"
        values: ["list:dups"]
      matchBinaries:
      - operator: "In"
        values: ["/usr/bin/bash"]
      matchActions:
      - action: "NotifyEnforcer"
        argSig: 9
```

With `kprobe_multi`, use a kprobe on `list:syscalls` with `Sigkill` instead.

## Set (uprobe and USDT)

Arguments `argIndex` and `argValue`. Uprobe: integer argument, `argIndex` 0-5 on amd64 or 0-7 on arm64. Example sets the first argument of `pizza()` to 42:

```yaml
matchActions:
- action: Set
  argIndex: 0
  argValue: 42
```

USDT: the argument must be a 4-byte `USDT deref` argument (inspect with `readelf -n`).

## UpdateState

Sets or deletes a state declared in `spec.state`, using `state.name` and `state.operator`. `Set` requires a `value` (unsigned 64-bit, e.g. `"1"`); `Delete` accepts none. Updates are atomic, but concurrent probes updating one state have no guaranteed order.

## Checked

Date: 2026-11-07

Selectors page read in full (about 65 KB); every action claim matched.

Method: documentation only; no commands were run.
