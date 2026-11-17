---
id: computing-software.rpa-and-low-code.n8n.reference-previous-nodes
name: reference-previous-nodes
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, expressions, json, previous-node, item-matching, binary-data]
level: practitioner
status: docs-checked
description: "Reference data in n8n expressions and the Code node: $json, $('node').item, first/last/all with branch and run index, itemMatching, $input and binary access."
sources:
  - https://docs.n8n.io/build/work-with-data/reference-data/reference-previous-nodes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: read data from the current node's input and from earlier nodes.

## Most used
- `$json`: JSON of the current input item (in the Code node only when running once for each item).
- `$('<node-name>').item.json`: JSON of the linked item in an earlier node.
- `$('<node-name>').item.binary`: binary data of the linked item.
- `$binary` is shorthand for `$input.item.binary` and is not available in the Code node.

## Other nodes' output (JavaScript, works in expressions and Code)
`$("<node-name>").all(branchIndex?, runIndex?)`, `.first(...)`, `.last(...)`; without `branchIndex` it defaults to the output connecting that node to the current one. `.params` gives the node's query settings (operation, limits). `.itemMatching(currentNodeInputIndex)` replaces `.item` in the Code node when tracing back from an input item.

## Current node input
`$input.item`, `$input.all()`, `$input.first()`, `$input.last()`, `$input.params`, and `$input.context.noItemsLeft` (Loop Over Items only). Python exists only in the Code node, with underscore names: `_input.item`, `_input.all()`, `_json` (Run Once for Each Item mode), `_input.context.noItemsLeft`.

## Binary example
Items can hold several binary properties, named by the upstream node (usually `data`); each has `fileName`, `mimeType`, `fileExtension`:
```js
{{ $('HTTP Request').item.binary.data.fileName }}
```

## Checked
Method: docs-checked 2026-11-09 against the n8n "Reference previous nodes" page (docs.n8n.io, read in full).
Nothing removed; the method tables, Code node availability and the binary property description match the page.
