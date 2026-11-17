---
id: computing-software.rpa-and-low-code.n8n.pin-and-mock-data
name: pin-and-mock-data
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, pin-data, mock-data, testing, customer-datastore, edit-output]
level: practitioner
status: docs-checked
description: "Pin and mock node output in n8n to test without calling external systems: Code or Edit Fields data, Customer Datastore, pin limits, editing and copying data from past executions."
sources:
  - https://docs.n8n.io/build/work-with-data/pin-and-mock-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: develop workflows against stable test data. Pinning and editing are for development only and are not available in production executions.

## Mock data
- **Code** node: return any dataset (complex cases); **Edit Fields (Set)**: **Add fields** for small tests.
- **Customer Datastore** node: a fake dataset for exploring n8n.

## Pin
Pinning saves a node's output and uses it instead of fetching fresh data in later runs. It avoids repeated webhook calls, saves API quota and keeps tests consistent. Only nodes with a single main output can be pinned (error outputs do not count). A banner shows in the output panel when data is pinned; select **Unpin** in it to fetch fresh data.

## Edit pinned data
Run the node, switch the **OUTPUT** view to **JSON**, select **Edit**, change the data, then **Save**; saving also pins it. This lets you test edge cases without staging them in the source system.

## Reuse data from a past execution
Left menu **Executions**, **Open Past Execution**, double-click the node, switch to JSON, then copy by selecting text (ctrl+c) or hover and use **Copy**: **Copy Item Path** and **Copy Parameter Path** give expressions, **Copy Value** copies the JSON. Open your workflow, run the target node if it has no data, **Edit** in JSON view, paste and **Save**.

Best flow: mock, edit into specific scenarios, pin, then keep building on the pinned set.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/build/work-with-data/pin-and-mock-data

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
