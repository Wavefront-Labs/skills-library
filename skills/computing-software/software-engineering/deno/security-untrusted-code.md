---
id: computing-software.software-engineering.deno.security-untrusted-code
name: security-untrusted-code
category: computing-software
field: software-engineering
product: deno
tags: [security, untrusted-code, defense-in-depth, frozen-lockfile, cached-only, web-worker, microvm]
level: sme
status: docs-checked
description: "Layered defences for running untrusted code under Deno: limited permissions, frozen lockfile, cached-only, reduced-permission workers, OS sandboxes and VMs."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/security.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Running completely untrusted code needs more than one layer of defence. The docs recommend using all of these together:

- Run `deno` with limited permissions and decide up front what code actually needs to run. Prevent more code being loaded using a `--frozen` lockfile and `--cached-only`.
- Isolate the untrusted part in a Web Worker with a reduced permission set so it cannot inherit everything the main program was granted.
- Use OS sandboxing such as `chroot`, `cgroups`, `seccomp`.
- Use a VM or MicroVM (gVisor, Firecracker, etc).

Permissions that bypass the sandbox, treated as equivalent to `--allow-all`:

- `--allow-run`: subprocesses run with their own permissions; `--allow-run=deno` is especially dangerous since the child can use `--allow-all`. Prefer specific trusted executables (`--allow-run=git`).
- `--allow-ffi`: native code can issue system calls directly, regardless of `--allow-*` flags.

Do not combine `--allow-write` with `--allow-run` where the writable directory contains an allowed executable: the binary could be overwritten.

Also scan dependencies with `deno audit` as a CI gate.

## Checked

2026-11-04. Confirmed against docs runtime/fundamentals/security.md: layered defences, bypass permissions, write+run warning, deno audit.

Method: documentation only; no commands were run.
