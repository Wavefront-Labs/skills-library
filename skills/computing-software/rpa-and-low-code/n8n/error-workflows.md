---
id: computing-software.rpa-and-low-code.n8n.error-workflows
name: error-workflows
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, error-workflow, error-trigger, stop-and-error, workflow-settings, failure]
level: practitioner
status: docs-checked
description: "Set an error workflow in n8n workflow settings, start it with the Error Trigger and force failures with the Stop and Error node."
sources:
  - https://docs.n8n.io/build/flow-logic/handle-errors-gracefully
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get alerted or react when an execution fails.

## Set it up
1. Build a workflow whose first node is the **Error Trigger**. Add what should happen (for example email or Slack alerts).
2. In each workflow that should report failures open **Workflow Settings** and select that workflow as the error workflow. One error workflow can serve many workflows.
3. The error workflow runs when an execution fails, typically from node setting errors or the workflow running out of memory.

## Fail on purpose
Add the **Stop And Error** node to force a failure under conditions you choose; the failure triggers the error workflow. Use it after an IF branch that detects bad data.

## Investigating failures
Use the Executions list (for one workflow or all workflows you can access), load data from a previous execution into the current workflow, and enable log streaming.

Gotcha: the error workflow must start with the Error Trigger node; this is the stated requirement.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/build/flow-logic/handle-errors-gracefully

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Removed the Enterprise label on log streaming (not stated on the page).

Method: documentation only; no commands were run.
