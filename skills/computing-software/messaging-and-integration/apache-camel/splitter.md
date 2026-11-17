---
id: computing-software.messaging-and-integration.apache-camel.splitter
name: splitter
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, split, streaming, tokenize, parallel-processing]
level: practitioner
status: docs-checked
description: "Camel Split EIP: options and defaults (parallelProcessing, streaming, stopOnException, group, timeout), CamelSplit exchange properties, tokenize and tokenizeXML examples."
sources:
  - https://camel.apache.org/components/next/eips/split-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Splitter

`expression` (required) yields an Iterator, Iterable, Array, Collection, Map, NodeList or delimited String. Defaults by type: Collection/Array/Iterator elements, Map entries, NodeList elements, String split on commas; other types pass through whole.

Options (defaults):
- `delimiter` `,` (`false` disables, `single` keeps one list)
- `parallelProcessing` false (caller still waits)
- `synchronous` false
- `streaming` false (split on demand, less memory)
- `stopOnException` false
- `aggregationStrategy` (default: original message is the output)
- `shareUnitOfWork` false
- `timeout` 0 (ms, parallel)
- `group` N items per List message
- `maxFailedRecords` and `errorThreshold` (0.0-1.0), exclusive with `stopOnException`

Exchange properties: `CamelSplitIndex` (from 0), `CamelSplitSize` (in streaming only the last message has it), `CamelSplitComplete` (last), `CamelSplitResult`, `CamelSplitWatermark`.

Examples: `split(body().tokenize("\n"))`; `split(body()).delimiter("\n")`; `tokenize("\n", 1000)` with streaming gives chunks of 1000 lines; `tokenizeXML("order")` with `inheritNamespaceTagName` for streaming XML. `xpath("//foo/bar")` works but loads the whole document.

Body: inside the steps each part; after the split unchanged unless an aggregation strategy is set.

Verify: a 3-line body split on newline runs the steps 3 times, with `CamelSplitComplete` true on the third.

## Checked

Method: docs-checked 2026-11-09 against https://camel.apache.org/components/next/eips/split-eip.html
