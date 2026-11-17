---
id: computing-software.cloud-infrastructure-engineering.vector.reduce-transform
name: reduce-transform
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [reduce, transform, merge-strategies, group-by, transactions, multiline, vector]
level: advanced
status: docs-checked
description: "Collapse multi-event transactions into one log event with reduce, group_by, ends_when and merge strategies."
sources:
  - https://vector.dev/docs/reference/configuration/transforms/reduce/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`reduce` merges multiple log events into one. It is stable and stateful (state is lost on restart) and handles logs only.

```yaml
transforms:
  merge:
    type: reduce
    inputs: [logs]
    group_by: [request_id]
    starts_when: 'starts_with(string!(.message), "BEGIN")'
    ends_when: 'starts_with(string!(.message), "END")'
    expire_after_ms: 30000
    merge_strategies:
      message: concat_newline
      bytes: sum
```

Transaction control:

- `group_by`: ordered fields; each distinct combination is reduced independently.
- `starts_when`: when true, the previous transaction is flushed without this event and a new one starts.
- `ends_when`: when true, the transaction is flushed immediately including this event.
- `end_every_period_ms`: flush a group at that interval.
- `expire_after_ms` (default 30000): flush after this long without events. `flush_period_ms` (default 1000) is how often expiry is checked.
- `max_events`: cap on events grouped together.

Merge strategies per field: `array`, `concat` (space), `concat_newline`, `concat_raw`, `discard` (keep first), `flat_unique`, `longest_array`, `shortest_array`, `max`, `min`, `retain` (keep last non-null), `sum`.

Use it to assemble multi-line stack traces or request lifecycles. With end-to-end acknowledgements, merged events carry all source batches, and all are acknowledged on delivery.

Because it is stateful, route one group's events to one instance.

Verify with a unit test feeding a begin, middle and end event.

## Checked

2026-11-03. Read transforms/reduce. Confirmed: stable, stateful, `group_by`, `starts_when`, `ends_when`, `end_every_period_ms`, `expire_after_ms` default 30000, `flush_period_ms` default 1000, `max_events`, and the full merge strategy list with meanings. Nothing removed.

Method: documentation only; no commands were run.
