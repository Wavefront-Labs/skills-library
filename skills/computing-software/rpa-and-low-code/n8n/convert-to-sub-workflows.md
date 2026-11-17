---
id: computing-software.rpa-and-low-code.n8n.convert-to-sub-workflows
name: convert-to-sub-workflows
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, sub-workflow, refactor, execute-workflow-trigger, expressions, conversion]
level: practitioner
status: docs-checked
description: "Convert selected nodes to a sub-workflow in n8n 1.97.0 or later, meeting the single-in single-out selection rules and handling type, AI node and accessor caveats."
sources:
  - https://docs.n8n.io/build/flow-logic/convert-to-sub-workflows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: refactor part of a workflow into a reusable sub-workflow. Available from n8n 1.97.0. Right-click the canvas background with nodes selected and choose **Convert to sub-workflow**. Expressions referencing other nodes are updated automatically and added as parameters on the Execute Workflow Trigger node.

## Selection must be valid
- No trigger nodes.
- Exactly one node in the selection receives connections from outside, and it has a single input branch (so not a Merge node) and no incoming connections from other selected nodes.
- Exactly one node sends connections outside, with a single output branch (so not an IF node), and no outgoing connections to other selected nodes.
- All nodes between the input and output nodes are included.

## Caveats
- Input and output types default to allow-all; set constraints manually in the Execute Sub-workflow Trigger node and the Edit Fields node labeled **Return** (only present if the sub-workflow has outputs).
- AI sub-nodes: select all of them, and duplicate nodes shared with other AI Agents before converting.
- The new workflow uses `v1` execution ordering regardless of the parent; change it in settings if needed.
- `first()`, `last()` and `all()` expressions are rewritten and get variable suffixes such as `_firstItem`, `_lastItem`, `_allItems`; verify they still behave.
- `itemMatching` needs a fixed number as index, not an expression.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/build/flow-logic/convert-to-sub-workflows

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
