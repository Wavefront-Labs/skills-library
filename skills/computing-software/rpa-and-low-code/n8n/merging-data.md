---
id: computing-software.rpa-and-low-code.n8n.merging-data
name: merging-data
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, merge, compare-datasets, code-node, node-executions, split]
level: practitioner
status: docs-checked
description: "Choose the right way to merge in n8n: Merge node for split branches or two nodes, Code node for multiple runs of one node, Compare Datasets for four-way output."
sources:
  - https://docs.n8n.io/build/flow-logic/merge-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: combine data streams correctly.

- **Branches after a split**: bring them back together with the **Merge** node. Its operations include appending data sets, keeping only new items and keeping only existing items.
- **Two previous nodes, even without a split**: also the Merge node, to build one dataset from the outputs of several nodes.
- **Multiple executions of one node** (a node running several times inside one workflow execution, for example in a loop with Loop Over Items and Wait): use the **Code** node. This is node executions, not workflow executions.
- **Compare then merge**: the **Compare Datasets** node compares two streams before merging and outputs up to four different streams.

Rule of thumb: if the streams exist side by side at the same time use Merge; if they arrive across loop iterations use Code; if you need to know what differs, use Compare Datasets.

## Checked
Method: docs-checked 2026-11-09 against the n8n "Merging data" page (docs.n8n.io, read in full).
Nothing removed; the closing rule of thumb is a summary of the page's three methods, not a separate claim.
