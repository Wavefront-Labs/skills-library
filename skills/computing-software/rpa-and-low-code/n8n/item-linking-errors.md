---
id: computing-software.rpa-and-low-code.n8n.item-linking-errors
name: item-linking-errors
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, item-linking, paired-items, multiple-matching-items, another-branch, item]
level: advanced
status: docs-checked
description: "Fix n8n item linking errors with $(node).item: missing pairing info, multiple matches and other-branch nodes, using first(), last() and all()[index]."
sources:
  - https://docs.n8n.io/build/work-with-data/reference-data/link-data-items/item-linking-errors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: understand why `$('Node').item` fails and fix it.

`.item` works because n8n keeps a thread for every item back through the nodes that produced it. It errors when the thread is broken, when it points to more than one item in the referenced node, or when the referenced node is on a different branch. Either avoid `.item` with `.first()`, `.last()` or `.all()[index]` (you must know the position), or fix the cause.

## `ERROR: Info for expression missing from previous node`
Some node in the chain returns no pairing information. In a **Code node**, return which input items each output item came from (see the page on preserving linking in the Code node). For custom or community nodes, the creator must return that information.

## `ERROR: Multiple matching items for expression`
Nodes like Summarize, Aggregate and Merge combine several items into one, so `.item` is ambiguous. Use `.first()`, `.last()` or `.all()[index]`, or reference a different node holding the same information without multiple matches.

## `ERROR: '<node-name>' is on another branch`
The node is upstream but the current item did not come from it. Example: a Merge node in Append mode outputs Input 1 items then Input 2 items, each linked to only one input. If Input 2 comes from `Get orders`, `{{ $('Get orders').item.json.total }}` resolves for items from Input 2 and fails for Input 1 items. The expression resolves to `null`, the node still succeeds and the execution continues; the error appears in the editor's expression preview. Fix by using `.first()`, `.last()` or `.all()[index]`, or by setting the Merge node to **Combine** mode so each output item holds data from both branches.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/build/work-with-data/reference-data/link-data-items/item-linking-errors

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
