---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-action-post
name: tetragon-action-post
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [action-post, tetragon, rate-limiting, stack-traces, ima]
level: practitioner
status: docs-checked
description: "Control Tetragon Post and NoPost actions: rate limit events, record kernel and user stack traces, collect IMA file hashes, or suppress events while still enforcing."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/selectors/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon Post and NoPost actions

Goal: decide which events a TracingPolicy hook sends from kernel to the agent, and what extra data they carry.

By default every hook creates an event with the `Post` action, except when a `NoPost` action is in the selector or a rate limit applies.

## Rate limiting

```yaml
matchActions:
- action: Post
  rateLimit: 5m
```

- Value defaults to seconds; suffix `m` or `h` for minutes or hours.
- An event is suppressed if the same action fired for the same thread, within the window, with the same inspected arguments (only the first 40 bytes of each argument are compared). Kernel v5.3 onwards.
- `rateLimitScope` widens it: `"process"` (all threads of a process) or `"global"` (all processes). Default is per thread.

## Stack traces

On kprobes set `kernelStackTrace: true` and/or `userStackTrace: true` under `Post`; uprobes support only `userStackTrace`. Events then carry `kernel_stack_trace` / `user_stack_trace`. Addresses are hidden unless the agent runs with `--expose-stack-addresses`, which the page warns can help break KASLR and ASLR, so restrict who can read such events. View with `tetra getevents -o compact`. User stacks are symbolized from `/proc/<pid>/maps`, so very short-lived processes may lack them; kernels before 5.15 may give incomplete user stacks.

## IMA file hashes

`imaHash: true` (default false) adds `ima_hash` (`sha256:<hash>`) to LSM events. Needs LSM BPF enabled and kernel 5.11+. Supported hooks include `bprm_check_security`, `file_open`, `mmap_file`. Check `CONFIG_INTEGRITY=y` and `CONFIG_IMA=y`; enable with kernel args `lsm=integrity,bpf ima_policy=tcb`. Example:

```yaml
lsmhooks:
- hook: "bprm_check_security"
  args:
    - index: 0
      type: "linux_binprm"
  selectors:
  - matchBinaries:
    - operator: "In"
      values:
      - "/usr/bin/zsh"
      - "/usr/bin/bash"
    matchActions:
      - action: Post
        imaHash: true
```

View with `tetra getevents -e PROCESS_LSM -o compact`.

## NoPost

`NoPost` suppresses the event but all other actions in the selector still run, e.g. `Override` with `argError: -2` on `sys_openat` for `/etc/passwd`, silently.

## Checked

Date: 2026-11-07

Selectors page read in full (about 65 KB); every action claim matched.

Method: documentation only; no commands were run.
