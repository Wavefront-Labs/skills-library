---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-action-override
name: tetragon-action-override
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [action-override, tetragon, tracing-policy]
level: sme
status: docs-checked
description: "Use the Tetragon Override action to change a kprobe, LSM or uprobe return value, redirect symbols or set registers, with its restrictions."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/selectors/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon Override action

Goal: run in place of the probed function and return a chosen value (unlike `Sigkill`, which kills the process). The code path or user process receiving the value decides whether to stop.

| Hook | Arguments |
| --- | --- |
| kprobe | `argError` |
| uprobe | `argError,argRegs,argNewSymbol,argNewAddr,argNewOffset` |
| lsmhooks | `argError` |

## kprobe and LSM

Make `sys_symlinkat` return -1 when the first argument is `/etc/passwd`:

```yaml
kprobes:
- call: "sys_symlinkat"
  syscall: true
  args:
  - index: 0
    type: "string"
  - index: 1
    type: "int"
  - index: 2
    type: "string"
  selectors:
  - matchArgs:
    - index: 0
      operator: "Equal"
      values:
      - "/etc/passwd\0"
    matchActions:
    - action: Override
      argError: -1
```

Needs a kernel built with `CONFIG_BPF_KPROBE_OVERRIDE` (error injection framework). Other functions annotated `ALLOW_ERROR_INJECTION()` are listed in `/sys/kernel/debug/error_injection/list`. Overriding `security_` hooks works from kernel 5.7.

## uprobe (can crash the traced app)

```yaml
uprobes:
- path: "test"
  symbols:
  - "func"
  selectors:
  - matchActions:
    - action: Override
      argError: 123
```

Conditions: uprobe at the start of the function, called via `call`, function returns `int`, and kernel 6.18+ for raw register manipulation.

Redirect to another symbol with `argNewSymbol: "malloc_patched"`, or `argNewOffset: "0x0000115c"` / `argNewAddr: "0x00001137"`. Restrictions: only a single symbol can be redirected; the new symbol must exist in the binary and have the same signature (not verified; mismatches can crash the app). `sopath` loads a shared object with the override symbol (experimental; needs dynamic libc.so.6 with `dlopen`, i.e. >= 2.34; no Intel CET/AMD Shadow Stack; no floating point arguments).

## argRegs

```yaml
    - action: Override
      argRegs:
      - "rax=11"
      - "rbp=(%rsp)"
      - "rip=8(%rsp)"
      - "rsp=8%rsp"
      - "rdi=cel(data0 + 1)"
```

Forms: constant, register, register plus offset, dereference, dereference plus offset, `cel(...)` (must return a 64-bit integer; data via `source: "pt_regs"`). Interface likely to change; `cel()` and `matchCEL` share a pool of eight compiled expressions per policy.

## Checked

Date: 2026-11-07

Selectors page read in full (about 65 KB); every action claim matched.

Method: documentation only; no commands were run.
