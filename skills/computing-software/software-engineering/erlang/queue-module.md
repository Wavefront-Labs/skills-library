---
id: computing-software.software-engineering.erlang.queue-module
name: queue-module
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-stdlib-collections, queue-module]
level: practitioner
status: docs-checked
description: "Erlang functional data structures: queue (FIFO), sets, gb_trees/ordsets, array and when maps are better."
sources:
  - https://www.erlang.org/doc/apps/stdlib/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# queue, sets, gb_trees and array
**Goal:** pick the right immutable container.

```erlang
Q0 = queue:new(), Q1 = queue:in(a, Q0),
{{value, a}, Q2} = queue:out(Q1),
{empty, _} = queue:out(Q2).
S = sets:from_list([1,2]), sets:is_element(1, S),
S2 = sets:add_element(3, S).
T = gb_trees:insert(k, v, gb_trees:empty()),
{value, v} = gb_trees:lookup(k, T), gb_trees:take_smallest(T).
```
- `queue` operations are amortised O(1) except `all/2`, `any/2`, `delete/2`, `filter/2`, `fold/3`, `join/2`, `len/1`, `member/2`, `split/2` and a few others, which are O(n). `len/1` is O(n); track the length yourself if needed.
- `sets` is map-backed (version 2) by default from OTP 28; `{version, 1}` selects the old representation. A function can return either version if you mix them.
- `ordsets` keep a set as an ordered list, ordered by Erlang term order.
- `gb_trees` is a general balanced tree with ordered keys; its behaviour is logarithmic.
- `array` is a functional, zero-based extendable array with a default value for unset entries.

## Gotchas
- Treat `queue`, `sets` and `gb_trees` as opaque; do not depend on their term structure (the queue docs warn that code assuming the format is "running on thin ice").

## Self-check
Use a queue as a work buffer and drain it with `queue:out/1`.

## Checked
2026-11-02. STDLIB module docs for `queue` (complexity list, out/2 return shapes, opaque warning), `sets` (version 2 default from OTP 28), `ordsets`, `gb_trees` (ordered, lookup, take_smallest), `array` (zero-based, default value). Removed: claims that maps are faster than gb_trees, array O(log n) indexing, ETS-vs-array advice, and the stable-representation gotcha detail (not in the docs).
Method: documentation only; no commands were run.
