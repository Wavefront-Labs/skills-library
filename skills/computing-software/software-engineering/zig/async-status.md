---
id: computing-software.software-engineering.zig.async-status
name: async-status
category: computing-software
field: software-engineering
product: zig
tags: [zig, async-status, zig-async-io, async-await-removed, event-loop, std-io-interface, io-uring]
level: advanced
status: docs-checked
description: "Understand that Zig async/await was removed from the self-hosted compiler, and choose threads, poll-based event loops or the evolving std.Io interface."
sources:
  - https://ziglang.org/documentation/0.15.1/#Async-Functions
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/posix.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Thread/Pool.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async status: async functions in 0.15.1
**Goal:** pick a concurrency model without relying on stale tutorials.

- The 0.15.1 language reference says async functions regressed with the release of 0.11.0, and the current plan is to reintroduce them as a lower-level primitive that powers I/O implementations (tracking issue: stackless coroutines as low-level primitives, ziglang/zig#23446). Treat tutorials that use `async`/`await` as outdated for this release.
- `nosuspend` still exists: it marks a scope where no suspension points are reached, and `suspend` inside it is a compile error.
- Practical options with the standard library:
  1. Threads and blocking IO (`std.Thread`, `std.Thread.Pool`).
  2. A readiness loop you manage with `std.posix.poll`, or `std.os.linux.IoUring` on Linux.
- Keep IO behind your own interface so the model can be swapped when the language feature returns.

## Self-check
Write a poll-based server that handles two sockets in one thread with `std.posix.poll`.

## Checked
2026-11-02. Confirmed in the 0.15.1 language reference (Async Functions, nosuspend), `lib/std/posix.zig` (`poll`), `lib/std/os/linux.zig` (`IoUring`) and `lib/std/Thread/Pool.zig`.
Fixed: the old claim that async keywords were "removed from the language reference" (the reference has an Async Functions section stating the plan to reintroduce them) and the `std.Io` interface claim (in 0.15.1 `std.Io` is the new Reader/Writer namespace). Removed: epoll/kqueue wrappers, libxev/zap/httpz, labeled-switch state machine tip, `-fstage1`, cancellation gotcha.
Method: documentation only; no commands were run.
