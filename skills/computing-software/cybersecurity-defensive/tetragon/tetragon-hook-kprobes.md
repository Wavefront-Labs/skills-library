---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-hook-kprobes
name: tetragon-hook-kprobes
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [hook-kprobe]
level: advanced
status: docs-checked
description: "Hook kernel functions in a Tetragon TracingPolicy with kprobes or fentry/fexit: symbol lookup, syscall prefixes, multiple hooks and fentry limits."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/hooks/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kprobes and fentry hooks

Tetragon hooks the kernel with `kprobes`, `fentry/fexit` and `tracepoints`, and user space with `uprobes`, through sections of `.spec`. Hooking a syscall can cause TOCTOU races when the argument is a pointer to user memory: user space can change the data after the hook but before the kernel uses it. Hooking a later kernel function such as an LSM `security_` hook avoids this.

## Kprobes

A kprobe dynamically hooks any kernel function, so it is tied to your kernel version and might not be portable. List symbols from `/proc/kallsyms`, for example `sudo grep sys_write /proc/kallsyms`.

Syscall symbols carry an architecture prefix (`__arm64_sys_write`, `__x64_sys_write`). For portable policies write `call: "sys_write"` and Tetragon adds the right prefix; the output event still includes it.

```yaml
spec:
  kprobes:
  - call: "fd_install"
    syscall: false
```

`syscall` defaults to `false`; it tells Tetragon whether the function uses the syscall ABI, which differs from regular kernel functions. Several kprobes can share one policy:

```yaml
spec:
  kprobes:
  - call: "sys_read"
    syscall: true
  - call: "sys_write"
    syscall: true
```

## Fentry/fexit

These attach via BTF and ftrace, calling the BPF program directly from a trampoline, which is faster than kprobes. They need a kernel >= 6.1 built with `CONFIG_DEBUG_INFO_BTF=y`:

```shell
grep CONFIG_DEBUG_INFO_BTF /boot/config-$(uname -r)
```

Limitations versus kprobes: enforcement actions such as `Override` and `Signal` are not supported, and each fentry spec attaches to a single kernel function (no multi-attach).

```yaml
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata:
  name: "fentry-example"
spec:
  fentries:
  - call: "tcp_connect"
    syscall: false
    return: true
    args:
    - index: 0
      type: "sock"
    returnArg:
      index: 0
      type: "int"
```

`fentry` attaches at function entry; `return: true` also attaches the `fexit` program, where the return value is available. Syscalls can be traced with `syscall: true`, and the same prefix rules apply. Fentry specs support the same `args`, `returnArg` and `selectors` fields as kprobes, and multiple specs may share a policy.

## Checked

Date: 2026-11-07

Hook points page read in full (about 41 KB). Reworded the fentry limitation to the page's 'such as Override or Signal'.

Method: documentation only; no commands were run.
