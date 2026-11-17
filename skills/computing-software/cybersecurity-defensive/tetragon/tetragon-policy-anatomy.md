---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-policy-anatomy
name: tetragon-policy-anatomy
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [policy-anatomy]
level: practitioner
status: docs-checked
description: "Understand a Tetragon TracingPolicy part by part using the fd-install example: hook point, arguments, selectors, Sigkill action, message and tags."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/example/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anatomy of a tracing policy

The page's example policy sends `SIGKILL` to any process that creates a file descriptor to a file named `/tmp/tetragon`. It is for illustration only and should not be used to restrict file access: it can be bypassed, for example with hard links.

```yaml
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata:
  name: "fd-install"
spec:
  kprobes:
  - call: "fd_install"
    syscall: false
    args:
    - index: 0
      type: "int"
    - index: 1
      type: "file"
    selectors:
    - matchArgs:
      - index: 1
        operator: "Equal"
        values:
        - "/tmp/tetragon"
      matchActions:
      - action: Sigkill
```

## Parts

- Required fields: `apiVersion`, `kind` and `metadata.name`, following the Cilium policy / Kubernetes object pattern. The name must comply with Kubernetes naming conventions.
- Hook point (`spec.kprobes`): hooks the kernel function `fd_install`, called when a new file descriptor is created. `syscall: false` marks a regular kernel function, not a syscall. `args` tells Tetragon's BPF code which function arguments to extract and optionally filter on.
- Selectors: filter events to a subset and optionally take an action. Here `matchArgs` applies the `Equal` operator on the `file` struct at argument index 1 and matches on the file path. `matchActions` with `Sigkill` sends SIGKILL to the process that initiated the event.
- `message`: optional short message included in the generated event, set per hook, for example `message: "Installing a file descriptor"`.
- Tags: optional, used to categorize generated events.

## Try it

```shell
echo eBPF! > /tmp/tetragon
sudo ./tetragon --bpf-lib bpf/objs --tracing-policy example.yaml
./tetra getevents -o compact
cat /tmp/tetragon
```

Events: `process /usr/bin/cat /tmp/tetragon`, `open /usr/bin/cat /tmp/tetragon`, then `exit ... SIGKILL`; the shell prints `Killed`. Stop Tetragon with Ctrl+C to disable the policy and remove the BPF programs.

## Checked

Date: 2026-11-07

TracingPolicy example page read in full; every claim matched, no change.

Method: documentation only; no commands were run.
