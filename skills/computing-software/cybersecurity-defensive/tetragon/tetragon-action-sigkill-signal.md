---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-action-sigkill-signal
name: tetragon-action-sigkill-signal
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [action-sigkill, tetragon, tracing-policy]
level: practitioner
status: docs-checked
description: "Use Tetragon matchActions Sigkill and Signal to terminate or signal the process making a matching call, with the shape of a write-block policy."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/selectors/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon Sigkill and Signal actions

Goal: act in the kernel on a matching call. Actions go under `matchActions` in a selector; if the selector matches, the action runs. `Sigkill`, `Override`, `Post`, `TrackSock`, `UntrackSock` and `UpdateState` run directly in kernel BPF code; `GetUrl` and `DnsLookup` run in user space after the event arrives.

## Sigkill

Terminates synchronously, from the kernel, the process that made the matching call. This policy kills any `sys_write` to a path prefixed `/etc/passwd` from a process that is not PID 0 or 1 in its namespace. Because `kubectl exec` spawns a process in the container PID namespace that is not a child of PID 1, it is caught:

```yaml
- call: "sys_write"
  syscall: true
  args:
  - index: 0
    type: "fd"
  - index: 1
    type: "char_buf"
    sizeFromArgIndex: 2
  - index: 2
    type: "size_t"
  selectors:
  - matchPIDs:
    - operator: NotIn
      followForks: true
      isNamespacePID: true
      values:
      - 0
      - 1
    matchArgs:
    - index: 0
      operator: "Prefix"
      values:
      - "/etc/passwd"
    matchActions:
    - action: Sigkill
```

## Signal

Sends a given signal to the current process; the number is `argSig`. Same policy, using `SIGKILL(9)`:

```yaml
    matchActions:
    - action: Signal
      argSig: 9
```

The rest of the call (hook, `args`, `selectors`) is the same as the Sigkill example.

## Enforcement

The page cautions to consult the Enforcement section of the Tetragon docs before using either action for enforcement.

## Checked

Date: 2026-11-07

Selectors page read in full (about 65 KB); every action claim matched.

Method: documentation only; no commands were run.
