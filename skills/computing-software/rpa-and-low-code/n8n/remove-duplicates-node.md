---
id: computing-software.rpa-and-low-code.n8n.remove-duplicates-node
name: remove-duplicates-node
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, remove-duplicates, deduplication, scope, history-size, previous-executions]
level: practitioner
status: docs-checked
description: "Use the n8n Remove Duplicates node (1.64.0 overhaul): dedupe within one input, across executions by new value, higher value or later date, scope and history size."
sources:
  - https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.removeduplicates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: drop repeated items, either inside one run or against what earlier runs processed. The node was overhauled in n8n 1.64.0.

## Operations
1. **Remove Items Repeated Within Current Input**. **Compare**: **All Fields**, **All Fields Except** or **Selected Fields** (comma-separated). For the latter two you may set **Disable Dot Notation** and **Remove Other Fields** (drop fields not used in the comparison).
2. **Remove Items Processed in Previous Executions**. **Keep Items Where**:
   - **Value Is New**: value must be a unique ID field (or combination).
   - **Value Is Higher than Any Previous Value**: value must be incremental.
   - **Value Is a Date Later than Any Previous Date**: value must be an ISO date.
   **Value to Dedupe On** is the field(s). Option **Scope**: `Node` (default; separate history per node, can be cleared alone) or `Workflow` (shared with other nodes using workflow scope). With Value Is New, **History Size** sets how many items are remembered (default 10,000, per the chosen scope).
3. **Clear Deduplication History**: **Mode > Clean Database** wipes the stored items for the chosen **Scope**; the current input is unaffected.


## Checked
Method: docs-checked 2026-11-09 against the n8n "Remove Duplicates" page (docs.n8n.io, read in full).
Removed as not on that page: the closing advice to prefer this node over hand-rolled static data.
