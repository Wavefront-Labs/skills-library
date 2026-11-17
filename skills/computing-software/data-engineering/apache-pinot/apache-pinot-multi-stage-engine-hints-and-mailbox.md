---
id: computing-software.data-engineering.apache-pinot.apache-pinot-multi-stage-engine-hints-and-mailbox
name: apache-pinot-multi-stage-engine-hints-and-mailbox
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, multi-stage-engine, mse, hints, aggoptions, windowoptions, joinoptions, setoptions, is-colocated-by-set-op-keys, mailbox, keep-alive]
level: advanced
status: docs-checked
description: "Multi-stage query engine hints (aggOptions, windowOptions, joinOptions, setOpOptions) and the gRPC mailbox keep-alive properties with defaults and safe tuning order."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/querying-and-sql/multi-stage-query/README.md", "https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/querying-and-sql/multi-stage-query/hints.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-stage engine hints and mailbox settings

## Hints

Multi-stage engine (MSE) behaviour can be customised with hints written as a comment, in the form `/* hintType(hint1='value1',hint2='value2') */`. Hint types: `aggOptions`, `windowOptions`, `joinOptions`, `setOpOptions` (each explained on its operator page).

`setOpOptions` controls the exchange inserted below UNION, UNION ALL, INTERSECT and EXCEPT / MINUS. Its option `is_colocated_by_set_op_keys` is Boolean, default planner chosen:
- `'true'` forces a pre-partitioned direct exchange on every input; `'false'` forces a shuffled hash exchange on every input.
- Honoured only by the V1 planner; the V2 physical optimizer ignores it.
- Force `'true'` only when every input is partitioned compatibly on projected columns, or INTERSECT, EXCEPT and plain UNION can return wrong results. UNION ALL is always safe; for it only `'false'` changes default behaviour.
- Placement: inline on the first branch, or on an outer SELECT wrapping the set operation (the outer-wrap form is preferred for plain UNION and for nested INTERSECT / EXCEPT).
```
SELECT /*+ setOpOptions(is_colocated_by_set_op_keys='true') */ col FROM a
UNION ALL
SELECT col FROM b
```

## Mailbox channel keep-alive

In versions containing Apache Pinot #19383, MSE mailbox data channels use gRPC keep-alive by default, to detect a peer that stopped responding. Keep-alive does not retry failed queries. These are startup settings on brokers and servers:
- `pinot.query.runner.channel.keep.alive.time.ms` default **300000** (client ping interval; non-positive disables; gRPC clamps positive values below 10000 to 10000)
- `pinot.query.runner.channel.keep.alive.timeout.ms` default **30000** (must be positive when enabled)
- `pinot.query.runner.channel.keep.alive.without.calls` default **false**
- `pinot.query.runner.mailbox.server.permit.keep.alive.time.ms` default **300000** (minimum ping interval a mailbox server accepts)
- `pinot.query.runner.mailbox.server.permit.keep.alive.without.calls` default **false**

Tuning order: keep defaults during a mixed-version rollout (older mailbox servers enforce a five-minute minimum and reject pings without calls). First lower the server permit settings everywhere and finish the rolling restart, then lower the client interval (the client interval must be at least the receiver's permitted interval), then optionally enable pings without calls. Prefer lowering the interval before the timeout; very short timeouts can mistake a long GC pause for a dead peer. `too_many_pings` or `GOAWAY(ENHANCE_YOUR_CALM)` means pings were rejected by a peer's permit settings.

## Checked

Confirmed against the Pinot docs pages "Hints" and "Multi-stage query": hint types and syntax, setOpOptions semantics and placement, all five keep-alive properties and defaults, and the tuning sequence. Removed the unsourced claims about enabling MSE with `SET useMultistageEngine=true` or a broker default, and the list of supported operators, which these pages do not state.

Method: docs-only read of cited pages, 2026-11-08
