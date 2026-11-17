---
id: computing-software.software-engineering.nim.tables-and-ordered-tables
name: tables-and-ordered-tables
category: computing-software
field: software-engineering
product: nim
tags: [tables-and-ordered-tables, collections-tables-sets-options, table, orderedtable, counttable, hashtable, dictionary, mgetorput, haskeyorput, nim]
level: practitioner
status: docs-checked
description: "Use hash tables for key-value data, ordered iteration, counting, default values and safe lookups."
sources:
  - https://nim-lang.org/docs/tables.html
  - https://nim-lang.org/docs/hashes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table, OrderedTable and CountTable

Goal: store and look up keyed data.

```nim
import std/tables
var t = initTable[string, int]()
t["a"] = 1
t.mgetOrPut("b", 0) += 5
echo t.getOrDefault("c", -1), t.hasKey("a")
```
- Literals: `{"a": 1, "b": 2}.toTable`; `toOrderedTable` preserves insertion order; `CountTable` provides `inc` and `largest`.
- `t["x"]` raises KeyError when absent; use `getOrDefault`, `hasKey`, `withValue`, `t.pop(k, v)`, `t.del(k)`.
- Iteration: `for k, v in t`, `keys`, `values`, `mpairs`.
- `TableRef[K,V]` (`newTable`) has reference semantics.
- Keys need `hash` and `==`; define `hash` for custom types (see std/hashes).

Gotchas:
- `Table` is the usual hash table; only `OrderedTable` is documented to remember insertion order.
- Tables have value semantics: `=` copies the table. Use `TableRef` to share one.

Verify: counting words yields right totals using CountTable.

## Checked

2026-11-03. Confirmed against the tables and hashes pages: toTable, toOrderedTable, getOrDefault, hasKey, withValue, mgetOrPut, pop(key, val), del, mpairs, KeyError on missing key, CountTable inc/largest, value semantics (`=` copies), TableRef/newTable, custom keys need `hash` and `==`. Removed: CountTable `sort` (no entry found on the page) and the unspecified-order and pointer-sharing wording.

Method: documentation only; no commands were run.
