---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-hook-return-lists-macros
name: tetragon-hook-return-lists-macros
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [hook-return-lists, tetragon, tracing-policy]
level: advanced
status: docs-checked
description: "Use data fields, return values, socket tracking, lists and selectorsMacros in a Tetragon TracingPolicy to share hook config."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/hooks/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon data, return values, lists and macros

## Data fields (kprobes)

`data` retrieves a value from the kernel `current_task` for use with `matchData`. Each entry defines a `source` (currently only `current_task`) and a `resolve` path in `struct task_struct`; the example also sets `index` and `type`.

```yaml
data:
- index: 0
  type: "string"
  source: "current_task"
  resolve: "comm"
selectors:
- matchData:
  - index: 0
    operator: "Equal"
    values:
    - "example"
```

## Return values

Set `return: true` and `returnArg` with its `type`.

```yaml
- call: "sk_alloc"
  syscall: false
  return: true
  args:
  - index: 1
    type: int
    label: "family"
  returnArg:
    index: 0
    type: sock
  returnArgAction: TrackSock
```

`returnArgAction` is only for `TrackSock` and `UntrackSock`: Tetragon stores a socket to PID/TGID mapping and uses it when the socket shows up in a `sock` argument elsewhere. Limits: kernel >= 5.3; the mapping is an LRU map (overflow can misattribute events, and can be abused for evasion); shared sockets are attributed to the creating process.

## Lists

Define under `spec.lists` (`name`, `type`, `values`) and reference from `call` as `"list:NAME"`; one kprobe is created per item, all sharing selectors and args.

```yaml
spec:
  lists:
  - name: "dups"
    type: "syscalls"
    values:
    - "sys_dup"
    - "sys_dup2"
    - "sys_dup3"
  kprobes:
  - call: "list:dups"
```

Syscall lists need `type: "syscalls"` and cannot mix with regular functions; a prefix like `i386/sys_dup` picks another ABI. Generated types: `generated_syscalls` (all syscalls) and `generated_ftrace` with a regex `pattern` (e.g. `"^ksys_*"`). With the `InMap` operator on a syscall list, the argument type must be `syscall64`.

## Selector macros

Define under `spec.selectorsMacros`, use with `macros: [name]` in a hook's selector. Useful when argument indices differ (so a list cannot be shared).

```yaml
spec:
  selectorsMacros:
    myappExclusion:
      matchBinaries:
      - operator: "NotPrefix"
        values:
        - "/opt/myapp"
```

Limitation: the same filter field (e.g. `matchArgs`) in a macro and the selector, or in two macros used together, is an error.

## Checked

Date: 2026-11-07

Hook points page read in full (about 41 KB). Reworded the data-field requirements (the page requires source and resolve) and made the macro example values a list; the page's macro example gives a bare string.

Method: documentation only; no commands were run.
