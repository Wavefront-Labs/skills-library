---
id: computing-software.software-engineering.erlang.monitors
name: monitors
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-links, monitors]
level: practitioner
status: docs-checked
description: "Erlang monitors: unidirectional process monitoring, DOWN message shape, demonitor with flush and node monitoring."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitors and DOWN messages
**Goal:** watch a process without sharing its fate.

```erlang
Ref = erlang:monitor(process, Pid),
receive
    {'DOWN', Ref, process, Pid, Reason} -> {down, Reason}
after 5000 -> erlang:demonitor(Ref, [flush]), timeout
end.
```
- A process or port monitor fires once, when the target terminates, does not exist at creation time, or the connection to it is lost; then it is removed.
- Monitoring a nonexistent process delivers a `'DOWN'` message with reason `noproc`.
- Monitor a registered name on another node with `erlang:monitor(process, {Name, Node})`; a registered name is resolved to a pid only once, when the monitor is created.
- `erlang:monitor_node(Node, true)` delivers `{nodedown, Node}`; for monitoring many nodes use `net_kernel:monitor_nodes/1`.
- `demonitor(Ref, [flush])` removes the monitor and any `'DOWN'` message for it already in the mailbox.

## Gotchas
- Call `demonitor(Ref, [flush])` when you stop caring, or a late DOWN can land in the mailbox.

## Self-check
Monitor a short-lived process and print the DOWN tuple.

## Checked
2026-11-02. ERTS `erlang` module docs (monitor/2, demonitor/2 flush, monitor_node/2, registered-name resolution), `ref_man_processes` Processes chapter (monitors). Removed: `{nodeup, Node}` message detail for `monitor_nodes` and the claim that `gen_server:call` uses a monitor internally (not confirmed in the pages read).
Method: documentation only; no commands were run.
