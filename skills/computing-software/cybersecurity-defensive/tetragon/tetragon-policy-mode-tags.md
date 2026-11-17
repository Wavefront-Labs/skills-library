---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-policy-mode-tags
name: tetragon-policy-mode-tags
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [policy-mode-tags, tetragon, enforcement-mode, tags]
level: practitioner
status: docs-checked
description: "Switch a Tetragon policy between monitoring and enforcement mode at three levels, and add tags to categorize generated events."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/mode/"
  - "https://tetragon.io/docs/concepts/tracing-policy/tags/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon policy mode and tags

## Mode

Goal: disable enforcement in a policy without editing its actions. Modes:

- `monitoring`: enforcement operations are elided
- `enforcement`: enforcement operations are performed
- `monitor_only`: the policy has no enforcement actions, so it cannot be set to `enforcement`

Inspect with `tetra tracingpolicy list` (the MODE column, plus NPOST, NENFORCE, NMONITOR counters).

Three ways to set it, lowest to highest priority:

1. In the policy, under `spec.options`, key `policy-mode`:

```yaml
spec:
  options:
    - name: "policy-mode"
      value: "monitor"
```

2. When loading: `tetra tracingpolicy add --mode monitor policy.yaml`
3. At runtime via gRPC: `tetra tp set-mode --namespace pizza enforce-security enforce`

Setting the mode at runtime for a `monitor_only` policy is an error. Loading one always succeeds even with a mode specified, with a warning logged.

## Tags

Goal: categorize events. Tags are an optional field of a TracingPolicy (the page shows them on a kprobe call) and appear in the generated event. Every kprobe call can have at most 16 tags.

```yaml
  kprobes:
  - call: "security_file_permission"
    message: "Sensitive file system write operation"
    syscall: false
    args:
    - index: 0
      type: "file"
    - index: 1
      type: "int"
    selectors:
    - matchArgs:
      - index: 0
        operator: "Prefix"
        values:
        - "/etc"
      - index: 1
        operator: "Equal"
        values:
        - "2" # MAY_WRITE
    tags: [ "observability.filesystem", "observability.process" ]
```

Official tags in the observability namespace:

- `observability.filesystem`: file system operations
- `observability.privilege_escalation`: raising permissions of a user or process
- `observability.process`: a Linux program being executed

You may also define your own tags.

## Checked

2026-11-08. Read the mode and tags pages in full (raw docs markdown). Reworded the tags field description to match the page (an optional policy field shown on a kprobe call); no other changes.

Method: documentation only; no commands were run.
