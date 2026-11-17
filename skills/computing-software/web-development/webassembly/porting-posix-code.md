---
id: computing-software.web-development.webassembly.porting-posix-code
name: porting-posix-code
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasi-posix-gaps, no-fork-exec, socket-gaps, wasm]
level: practitioner
status: docs-checked
description: "Compatibility"
sources: ["https://raw.githubusercontent.com/WebAssembly/wasi-libc/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Porting POSIX code

Goal: port existing code.
- `wasi-libc` is a libc for Wasm built on WASI system calls, providing many POSIX-compatible APIs: standard I/O, file I/O, filesystem manipulation, memory management, time, strings, environment variables and program startup. The easiest way to get it is `wasi-sdk`, which includes it in its sysroot.
- Targets include `wasm32-wasip1`, `wasm32-wasip2` and `wasm32-wasip1-threads`.
- Threads: `pthread_*` symbols exist on every target but behave differently. On `wasm32-wasip1` and `wasm32-wasip2` spawning a thread returns an error and blocking on a condition variable traps. `wasm32-wasip1-threads` uses the (largely deprecated) wasi-threads proposal.
- Check each API you use against what the libc provides; anything missing needs a WASI-based replacement or a stub. The README does not list specific unsupported functions, so do not assume `fork`, `exec`, signals or sockets status from this skill.
Verify: the test suite passes under the runtime.

## Checked

2026-11-08. Confirmed in the wasi-libc README (read in full).
Removed as unconfirmed: the list of missing calls (`fork`, `exec`, signals, sockets) and the `--host=wasm32-wasi` configure flag.
Method: documentation only; no commands were run.
