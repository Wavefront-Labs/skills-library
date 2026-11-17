---
id: computing-software.rpa-and-low-code.n8n.looping-over-items
name: looping-over-items
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, loop, loop-over-items, batch-size, execute-once, pagination]
level: practitioner
status: docs-checked
description: "How looping works in n8n: implicit per-item processing, Execute Once, IF-based loops, Loop Over Items batching with Wait, and the nodes that do not iterate."
sources:
  - https://docs.n8n.io/build/flow-logic/loop
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: process many items without building unneeded loops.

n8n nodes take any number of items and by default run once for each item, so a Slack node connected to five customers sends five messages. To process only the first item, turn on **Execute Once** in the node's **Settings** tab.

## When you do need a loop
- Until a condition is met: connect a node's output back to an earlier node and add an **IF** node to decide when to stop.
- Until all items are processed: use **Loop Over Items**. Set **Batch Size** to `1` to handle items individually, or larger to batch (useful for API rate limits). Add a **Wait** node between batches to slow down further. The node stops after all items are batched, so no IF is needed.

## Nodes that do not iterate by themselves
- Code node in **Run Once for All Items** mode, and Execute Workflow in the same mode.
- HTTP Request: pagination is your job; loop to fetch one page at a time.
- Executes once for some operations: CrateDB (`insert`, `update`), Microsoft SQL (`insert`, `update`, `delete`), MongoDB (`insert`, `update`), QuestDB (`insert`), TimescaleDB (`insert`, `update`).
- Redis (one operation runs once regardless of item count) and RSS Read (once per URL).

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/build/flow-logic/loop

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Removed the `$input.context.noItemsLeft` line (not on the page).

Method: documentation only; no commands were run.
