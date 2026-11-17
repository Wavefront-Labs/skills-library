---
id: computing-software.rpa-and-low-code.n8n.aggregate-node
name: aggregate-node
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, aggregate, group-items, merge-lists, individual-fields, all-item-data]
level: practitioner
status: docs-checked
description: "Use the n8n Aggregate node to group items into one item, aggregating individual fields or all item data, with Merge Lists, binaries and null handling options."
sources:
  - https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.aggregate
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: turn many items into one item, for example a single list of emails for one Slack message.

## Individual Fields
- **Input Field Name**: the field to collect.
- **Rename Field** toggle with **Output Field Name**. When aggregating several fields you must give each a new output name; you cannot leave several undefined.

## All Item Data
- **Put Output in Field**: name of the output field.
- **Include**: **All fields**, **Specified Fields** (comma-separated **Fields To Include**) or **All Fields Except** (comma-separated **Fields To Exclude**).

## Options
- **Disable Dot Notation** (Individual Fields only): when on, `parent.child` names are not resolved as child fields; default off.
- **Merge Lists** (Individual Fields): if the field is a list, output one flat list instead of a list of lists.
- **Include Binaries** (both types): carry binary data into the output.
- **Keep Missing And Null Values** (Individual Fields): add a null entry for missing or null inputs; off by default, which ignores them.

Related: after Aggregate, referencing earlier nodes with `.item` can hit `Multiple matching items for expression`; use `.first()` or `.all()[index]`.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.aggregate
- https://docs.n8n.io/build/work-with-data/reference-data/link-data-items/item-linking-errors

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
