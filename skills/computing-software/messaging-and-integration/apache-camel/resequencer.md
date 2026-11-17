---
id: computing-software.messaging-and-integration.apache-camel.resequencer
name: resequencer
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, resequence, batch-mode, stream-mode, ordering]
level: advanced
status: docs-checked
description: "Camel Resequencer EIP: batch mode (size 100, timeout 1000 ms) vs stream mode (capacity 1000), duplicates, reverse, rejectOld and ignoreInvalidExchanges."
sources:
  - https://camel.apache.org/components/next/eips/resequence-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resequencer

Puts out-of-order messages back in order; the Expression is the comparator (header or body part).

**Batch mode (default)**: collect, sort, send. A batch closes at max size or timeout.
- `batchSize` / `size()` 100
- `batchTimeout` / `timeout()` 1000 ms
- `allowDuplicates` keeps duplicates (by default only the first message per value is kept)
- `reverse` flips the default `0..9, A..Z` order

**Stream mode**: emits as soon as the next expected number arrives; needs integers 1,2,3...N (a custom expression can map other values, e.g. names like `YYYYMMDD-DNNN`).
- `capacity` 1000 (pending backlog guard)
- `timeout`: when it expires the current expected number is skipped
- `rejectOld`: throws `MessageRejectedException` for a message older than the last delivered

`ignoreInvalidExchanges` (both modes): without it an invalid exchange (e.g. missing header) throws `CamelExchangeException`; with it they are discarded.

Examples:
```java
resequence().body()
resequence(header("mySeqNo"))
resequence(header("seqnum")).stream()
resequence(header("x")).batch().size(300).timeout(4000L)
```
JMS priority: batch mode with `allowDuplicates()` and `reverse()` on `header("JMSPriority")`, 3 second timeout.

Body is unchanged; the steps receive messages in the new order.

Verify: in batch mode the messages collected in a batch are sorted by the expression (lowest first by default) before they continue to the steps; in stream mode a message is held until its predecessor arrives or the timeout expires.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel Resequence EIP page: batch defaults (100 messages, 1000 ms), stream capacity 1000, duplicate handling, reverse ordering 0..9, A..Z, ignoreInvalidExchanges for both modes with CamelExchangeException, rejectOld and MessageRejectedException, stream timeout skipping the expected number, the custom expression note, JMSPriority example (batch mode, 3000 ms) and unchanged body all match. The old verify line was reworded to documented behaviour. No commands were run.
