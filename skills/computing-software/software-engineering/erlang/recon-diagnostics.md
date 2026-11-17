---
id: computing-software.software-engineering.erlang.recon-diagnostics
name: recon-diagnostics
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-debugging, recon-diagnostics]
level: sme
status: draft
description: "Erlang recon library: proc_count, proc_window, bin_leak, recon_trace calls with limits and scheduler usage."
sources:
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# recon for production diagnostics
**Goal:** find memory, CPU and message-queue problems on a running node.

```erlang
recon:proc_count(memory, 5),                 % top 5 processes by memory
recon:proc_count(message_queue_len, 5),
recon:proc_window(reductions, 5, 5000),      % busiest over 5 s
recon:bin_leak(5),                           % GC then rank by freed binary refs
recon:info(Pid),
recon:scheduler_usage(1000),
recon_trace:calls({my_mod, my_fun, '_'}, 100),   % stop after 100 calls
recon_trace:clear().
```
- `recon_trace:calls/3` takes a maximum count, so a trace cannot flood the node.
- `sys:get_state(Pid)` inspects a behaviour's state; `erlang:process_info(Pid, current_stacktrace)` shows where a process is stuck.
- `recon_alloc:memory/1` explains VM memory by allocator.
- Include recon in release builds so it is present when you need it.

## Gotchas
- `sys:get_state` on a busy process blocks behind its mailbox.

## Self-check
Use `proc_count(message_queue_len, 3)` while a test process floods a mailbox.
