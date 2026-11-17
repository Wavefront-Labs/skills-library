---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-argument-types
name: tetragon-argument-types
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [argument-types, tetragon, tracing-policy]
level: practitioner
status: docs-checked
description: "Pick the right Tetragon args type for a hook argument and know which matchArgs operators each type supports."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/argument_types/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon argument types

Goal: choose the `type` for each `args` entry and filter it with the right `matchArgs` / `matchData` operators.

## Scalars

- 8/16/32/64-bit: `int8`/`sint8`, `uint8`, `int16`, `uint16`, `int`/`sint32`/`int32`, `uint32`, `long`/`sint64`/`int64`, `ulong`/`uint64`/`size_t`.
- All integer types support `Equal`, `NotEqual`, `GT`, `LT`, `Mask`.

## Strings, paths and buffers

- `string`, `filename`, `fd` (resolved to path), `file`, `path`, `dentry`, `linux_binprm`, `data_loc` (tracepoint `__data_loc` strings), `net_device`, `char_buf`: use `Equal`, `NotEqual`, `Prefix`, `Postfix`, plus `SubString` (v6.17+) or `SubStringIgnoreCase` (v6.19+) for most. `char_iovec` and `kiocb` support only `Equal`, `NotEqual`, `Prefix`, `Postfix`.
- `char_buf` needs `sizeFromArgIndex` or `returnCopy`; `char_iovec` uses `sizeFromArgIndex` for vector count; `const_buf` takes a fixed `size`.
- `file` and `path` also support file type filtering.
- `dentry` yields a path within one mountpoint only.
- Full path retrieval needs kernel v5.3+; older kernels cap at 256 path components.

## Network

- `skb`: `SAddr`, `DAddr`, `SPort`, `DPort`, `Protocol`, or the negated `NotSAddr`, `NotDAddr`, `NotSPort`, `NotDPort`; CIDR notation is supported for addresses.
- `sock` and `socket`: `SAddr`, `DAddr`, `SPort`, `DPort`, `Protocol`, `Family`, `State`.
- `sockaddr`: `SAddr`, `SPort`, `Family` (no destination operators).
- `sockaddr_un`: `Equal`, `NotEqual`, `Prefix`, `NotPrefix`, `Family`; abstract names get a leading `@`.

## Kernel objects and misc

`cred`, `bpf_attr`, `perf_event`, `bpf_map`, `bpf_prog`, `user_namespace`, `capability`, `iov_iter`, `load_info`, `module`, `kernel_cap_t`, `cap_inheritable`, `cap_permitted`, `cap_effective`.

- `nop` skips retrieval of that argument.
- `syscall64` outputs a `SyscallId` (number plus ABI such as `x64`, `i386`); used with `raw_syscalls` tracepoints and the `InMap` operator.

## Checked

Date: 2026-11-07

Argument types page read in full. Corrected the skb line: Protocol has no Not variant; the page lists NotSAddr, NotDAddr, NotSPort, NotDPort.

Method: documentation only; no commands were run.
