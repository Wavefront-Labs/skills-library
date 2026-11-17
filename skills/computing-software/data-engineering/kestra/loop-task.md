---
id: computing-software.data-engineering.kestra.loop-task
name: loop-task
category: computing-software
field: data-engineering
product: kestra
tags: [loop, loopuntil, iteration, item-variables, breakwhen, concurrencylimit]
level: advanced
status: docs-checked
description: "Iterate in Kestra with the Loop and LoopUntil flowable tasks: values, item variables, concurrencyLimit, breakWhen, fetchType, and the object-list trap."
sources:
  - https://kestra.io/docs/workflow-components/tasks/flowable-tasks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Loop` runs its children once per item in `values`, each iteration in its own sub-execution. `values` can be a list, JSON array string, map or ION file URI.

```yaml
values: ["value 1", "value 2", "value 3"]
```

Properties: `concurrencyLimit` (`0` default = all in parallel), `transmitFailed` (default `true`), `breakWhen`, `fetchType` (`FETCH`, `STORE`, `AUTO` default), `outputs`.

Item variables: `item.index`, `item.value`, `item.key` (maps only), `item.parent.*`, `item.parents[n].value`.

Traps:

- Duplicate list elements are dropped: `["a", "b", "a"]` runs two iterations.
- A URI value runs one iteration per line.
- For object lists `item.value` is a JSON string; use `fromJson(item.value).field`, not `item.value.field`.
- `breakWhen` only affects unstarted iterations; use `concurrencyLimit: 1` for it to check before each start.
- To stop on failure set `transmitFailed: false` and check `iteration.state`.
- With `fetchType: STORE`, `loopOutputs()` returns `null` for declared IDs. Undeclared outputs are not accessible after the loop.

`LoopUntil` repeats until `condition` is true (evaluated after each iteration), for example `condition: "{{ outputs.ping.code == 200 }}"`. `checkFrequency` takes `interval`, `maxIterations`, `maxDuration`; `failOnMaxReached` defaults to `false`; `iterationCount` is 1-based.

## Checked

2026-11-04. Confirmed against the Kestra flowable tasks page: Loop values types, concurrencyLimit 0 default, transmitFailed default true, breakWhen only affecting unstarted iterations, fetchType FETCH, STORE and AUTO, loopOutputs() null under STORE, duplicate elements dropped, URI iterating per line, fromJson(item.value), LoopUntil condition, checkFrequency, failOnMaxReached default false and 1-based iterationCount. Nothing removed.

Method: documentation only; no commands were run.
