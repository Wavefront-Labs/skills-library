---
id: computing-software.software-engineering.erlang.links-and-exit-signals
name: links-and-exit-signals
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-links, links-and-exit-signals]
level: advanced
status: docs-checked
description: "Erlang links: bidirectional exit propagation, normal/kill/killed reasons, process_flag(trap_exit) and EXIT messages."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Links, exit signals and trap_exit
**Goal:** reason correctly about who dies when.

- A link is bidirectional; when one linked process terminates it sends an exit signal carrying its exit reason to the other.
- A non-trapping receiver drops an exit signal with reason `normal` and terminates on any other reason, with the same reason. `exit(Pid, kill)` terminates the receiver unconditionally with reason `killed`. When `kill` arrives over a link, it is trappable and is not converted to `killed`.
- With `process_flag(trap_exit, true)` signals become messages `{'EXIT', FromPid, Reason}` added to the end of the queue.
```erlang
process_flag(trap_exit, true),
Pid = spawn_link(fun() -> exit(boom) end),
receive {'EXIT', Pid, Reason} -> Reason end.      % boom
```
- `link/1`, `unlink/1`, `spawn_link/1`. For `spawn_link` and `spawn_opt` with `link` the link is set up atomically.
- If the linkee does not exist, `link/1` from a non-trapping process on the same node can raise a `noproc` error; otherwise the caller gets an exit signal with reason `noproc`. A lost connection gives `noconnection`.

## Gotchas
- A trapping process that never reads `'EXIT'` messages never notices its parent dying; handle `{'EXIT', Parent, Reason}` and stop.
- `spawn` followed by `link` is not atomic; use `spawn_link`.

## Self-check
Spawn a linked crasher with and without trap_exit and observe the difference.

## Checked
2026-11-02. Reference Manual "Processes" (links, exit signal reasons, receiving exit signals, atomic link in spawn_link/spawn_opt), ERTS `erlang:link/1` docs (noproc behaviour). Removed: the wrong "linking to a dead pid always sends a noproc exit signal" and the claim about which processes should trap exits (supervisor behaviour not read here).
Method: documentation only; no commands were run.
