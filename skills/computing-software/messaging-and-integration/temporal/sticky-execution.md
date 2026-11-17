---
id: computing-software.messaging-and-integration.temporal.sticky-execution
name: sticky-execution
category: computing-software
field: messaging-and-integration
product: temporal
tags: [sticky-execution, sticky-queue, workflow-cache, stickyscheduletostarttimeout, worker-cache]
level: intro
status: docs-checked
description: "Temporal sticky execution: Workers cache workflow state and receive follow-up Workflow Tasks on a worker-specific sticky queue, with a five second fallback."
sources:
  - https://docs.temporal.io/sticky-execution
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Workers cache the state of workflows they run. Sticky Execution, on by default and applied only to Workflow Tasks, steers later Workflow Tasks of an execution to the same Worker so it need not rebuild state from Event History.

Mechanics:
1. The first Workflow Task goes to the Task Queue you named; any polling Worker may take it.
2. The Worker that accepts it keeps polling the original queue and also begins polling a Sticky Queue with an automatically generated name, shared only with it.
3. Follow-up Workflow Tasks for that execution are placed in the Sticky Queue.
4. If the Worker does not start a sticky task shortly after scheduling (five seconds by default), the Service disables stickiness for that execution and puts the task back on the original queue so any Worker can resume it.
5. If a Workflow Task fails, the Worker evicts the execution from its cache (state unknown), which invalidates stickiness, and the task returns to the original queue.

Benefit: lower latency by skipping replay, most visible for latency-sensitive workflows. It does not apply to Activity Tasks, since history belongs to the workflow.

The timeout is tunable: in Go, `StickyScheduleToStartTimeout` in the Worker options.

## Checked

2026-11-08. Read in full: the Sticky Execution page (docs.temporal.io/sticky-execution). Every remaining claim matches those pages. Removed: the closing paragraph on stateless Workers and millions of open executions, which the page does not state.

Method: documentation only; no commands were run.
