---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-hook-arguments
name: tetragon-hook-arguments
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [hook-arguments, tetragon, tracing-policy]
level: advanced
status: docs-checked
description: "Define hook args in a Tetragon TracingPolicy: index, type, label, returnCopy, sizeFromArgIndex, maxData and resolve with btfType."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/hooks/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon hook arguments and attribute resolution

Goal: tell the BPF code how to read, print and filter each argument. Kprobes, uprobes and tracepoints share the `args` list; each entry needs `index` (zero-based function argument position) and `type`. Optional `label` annotates the output.

```yaml
args:
- index: 0
  type: "int"
  label: "FD"
- index: 1
  type: "file"
```

Arguments you omit are not printed.

## Buffers

For `char_buf` and `char_iovec`:
- `returnCopy`: read the argument when the kretprobe fires, since a buffer (e.g. for `read(2)`) may be empty at entry.
- `sizeFromArgIndex`: index of the argument holding the size (for `write(2)` the 3rd argument `count`; for `writev` the `vlen`).

```yaml
- call: "sys_write"
  syscall: true
  args:
  - index: 1
    type: "char_buf"
    returnCopy: true
    sizeFromArgIndex: 2
  - index: 2
    type: "size_t"
```

`char_buf` stores up to 4096 bytes; more is truncated. `maxData: true` reads up to 327360 bytes (kernels >= 5.4), but does not work with `returnCopy`.

## Attribute resolution (resolve)

Extract a field of a kernel structure with `resolve`. Kprobes: kernel 5.4+. LSM: 5.7+. Not supported for uprobes. Read the kernel struct definition to find field paths (some structures are dynamic).

```yaml
lsmhooks:
- hook: "bprm_check_security"
  args:
  - index: 0 # struct linux_binprm *bprm
    type: "string"
    resolve: "mm.owner.real_parent.comm"
```

Whole structures work too (`type: "file"` with `resolve: "file"`, or `type: "path"` with `resolve: "file.f_path"`). Arrays use brackets: `some.field[12].some.subfield`. Nested pointers work, e.g. `resolve: "user.uid.val"`.

## btfType and btfTypeModule

`btfType` (struct name without `struct`) casts the argument before resolving; `btfPath` supplies BTF for uprobes and USDTs.

```yaml
- index: 1
  type: "uint16"
  btfType: "sockaddr_in"
  resolve: "sin_port"
```

For kprobe arguments with module-defined structs add `btfTypeModule` (module name without `.ko`); Tetragon reads `/sys/kernel/btf/<module>`, and the policy fails to load if unavailable.

## Checked

Date: 2026-11-07

Hook points page read in full (about 41 KB). Limited btfTypeModule to kprobe arguments, as the page states.

Method: documentation only; no commands were run.
