---
id: computing-software.networking-hardware-and-wireless.open-vswitch.actions-resubmit-and-tables
name: actions-resubmit-and-tables
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, resubmit, goto-table, write-actions, clear-actions, clone, multi-table, pipeline, registers]
level: practitioner
status: docs-checked
description: "Build multi-table Open vSwitch pipelines with resubmit, goto_table, write_actions, clear_actions, clone and register moves, and avoid going back to earlier tables."
sources:
  - https://docs.openvswitch.org/en/latest/ref/ovs-actions.7/
  - https://docs.openvswitch.org/en/latest/tutorials/ovs-advanced/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# actions: resubmit and tables
Pipeline control actions:
- `resubmit([port],[table][,ct])` searches a flow table and runs the actions found, then continues with the next action; `resubmit(,table)` is the common form. `resubmit:port` is the short form. A given `port` replaces the input port for the lookup only; with no table, the current flow's table is used. `ct` was added in OVS 2.7.
- `goto_table:table` (instruction) must be the last instruction in a flow and must move forward: it is an error if the table is less than or equal to the flow's own table. `resubmit` is more flexible.
- `write_actions(action...)` adds actions to the action set, carried between tables and executed at the end of the pipeline; `clear_actions` clears the action set.
- `clone(action...)` runs the nested actions, saving and then restoring packet and pipeline state (OVS 2.7).
- `push:src` / `pop:dst` use a general-purpose stack; `exit` stops execution of further actions.

Typical pattern: table 0 admits traffic and does `resubmit(,1)`, later tables do VLAN, learning and output, passing state in registers (`load:...->NXM_NX_REG0[0..15]`). The advanced tutorial uses five tables this way: 0 admission, 1 VLAN input, 2 learn source MAC, 3 look up destination port, 4 output (see ovs-advanced-pipeline-tutorial).

Example, from the tutorial:
`ovs-ofctl add-flow br0 "table=0, priority=0, actions=resubmit(,1)"`

Limits: OVS caps a packet at 4,096 resubmits in total (goto_table and output to the table port count as resubmits); a resubmit to a strictly later table does not count against the recursion depth limit (OVS 2.6 and later). Exceeding either limit is an error that stops packet processing; OVS 2.10 and later logs a trace of the execution.

`ofproto/trace` prints each table visited as a numbered block under `bridge("br0")`, followed by the actions and `Datapath actions:`.

## Checked
2026-11-04. Confirmed against ovs-actions(7) (resubmit, clone, push/pop, exit, write_actions, clear_actions, goto_table, Errors sections) and the advanced tutorial (five tables, `resubmit(,1)` flow, trace output). Removed the invented "Resubmitted flow" trace text.
Method: documentation only; no commands were run.
