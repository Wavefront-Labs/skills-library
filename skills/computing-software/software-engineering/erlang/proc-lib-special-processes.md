---
id: computing-software.software-engineering.erlang.proc-lib-special-processes
name: proc-lib-special-processes
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-otp-more, proc-lib-special-processes]
level: sme
status: docs-checked
description: "OTP proc_lib: spawn processes with ancestry and crash reports, and synchronous start with init_ack for custom processes."
sources:
  - https://www.erlang.org/doc/system/design_principles.html
  - https://www.erlang.org/doc/apps/stdlib/proc_lib.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# proc_lib and special processes
**Goal:** understand the layer under gen_server for custom processes.

- A process started with `proc_lib` stores the registered names or pids of its parent and its ancestors together with the initial function called. When it terminates abnormally (any exit reason other than `normal`, `shutdown` or `{shutdown, Term}`), a crash report is generated and written by the default logger handler set up by Kernel. The report holds the stored information, the termination reason and information about other processes that terminate as a result.
- `proc_lib:spawn_link/1,2,3,4` spawn linked processes initialised this way.
- `proc_lib:start_link(Module, Function, Args)` (also `/4` with a timeout, default `infinity`, and `/5` with spawn options) blocks until the new process calls `proc_lib:init_ack(Parent, Ret)`; `init_ack(Ret)` is the equivalent form that acknowledges the process that called `start`.
- `proc_lib:set_label/1` sets a label (any term) on the current process to aid debugging; it need not be unique, unlike a registered name.
- If you can use gen_server or gen_statem, do; they are built on this layer.
```erlang
{ok, Pid} = proc_lib:start_link(?MODULE, init, [self()]).
%% in init(Parent): proc_lib:init_ack(Parent, {ok, self()}), then enter the receive loop
```

## Gotchas
- A process started with plain `spawn` gets no ancestry or proc_lib crash report on abnormal exit.
- A special process that must work with the `sys` module (state inspection, suspend, tracing) has to handle system messages in its receive loop; this skill did not verify the `sys` function names, so read the `sys` module reference and the design principles page before implementing it.

## Self-check
Spawn with `proc_lib:spawn/1`, crash it, and compare the log with a plain spawn crash.

## Checked
Read the proc_lib reference (stdlib): initialisation data, crash report conditions and contents, spawn_link, start_link arities and defaults, init_ack/1,2, set_label. Removed: the `sys:handle_system_msg/6` and `sys:get_state/1` specifics (the sys page is not a cited source) and the "init_ack arity unconfirmed" hedge (both arities confirmed).
Method: docs-only read of cited pages, 2026-11-08
