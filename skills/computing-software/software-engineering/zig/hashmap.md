---
id: computing-software.software-engineering.zig.hashmap
name: hashmap
category: computing-software
field: software-engineering
product: zig
tags: [zig, hashmap, zig-std-containers, autohashmap, stringhashmap, getorput, arrayhashmap]
level: practitioner
status: docs-checked
description: "Use Zig HashMap, AutoHashMap, StringHashMap and ArrayHashMap for put/get/getOrPut/iteration with correct key lifetime and context."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/hash_map.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/array_hash_map.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/hash/auto_hash.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HashMap, AutoHashMap and StringHashMap
**Goal:** key-value storage without leaks or dangling keys.

```zig
var m = std.AutoHashMap(u32, []const u8).init(alloc);
defer m.deinit();
try m.put(1, "one");
if (m.get(1)) |v| _ = v;                            // ?V copy
if (m.getPtr(1)) |p| p.* = "uno";                   // in-place
const gop = try m.getOrPut(2);
if (!gop.found_existing) gop.value_ptr.* = "two";
_ = m.remove(1);
var it = m.iterator();
while (it.next()) |e| _ = .{ e.key_ptr.*, e.value_ptr.* };

var names = std.StringHashMap(u32).init(alloc);     // keys are borrowed slices
defer names.deinit();
```
- `StringHashMap` does not copy keys; dupe them (`try alloc.dupe(u8, k)`) and free them yourself on removal/deinit.
- `AutoHashMap` cannot hash slices (compile error from `autoHash`); use `StringHashMap` or a custom context (`std.HashMap(K, V, Ctx, max_load)` with `hash` and `eql`).
- `AutoArrayHashMap`/`StringArrayHashMap` keep insertion order and give contiguous `keys()`/`values()` (fast iteration).
- Unmanaged variants (`AutoHashMapUnmanaged`, `StringHashMapUnmanaged`, `HashMapUnmanaged`) take the allocator per call; in 0.15.1 `std.AutoHashMap` and `std.StringHashMap` are still the managed forms (`init(alloc)`).
- `HashMap` iteration order is not guaranteed and any modification invalidates live iterators (documented).

## Gotchas
- Inserts that may grow the table can invalidate key and value pointers (documented on `getOrPut` and friends).
- `remove(key)` returns `bool`; `removeByPtr(key_ptr)` removes via a key pointer from the map. Collect keys first instead of removing while iterating.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `put`, `get`, `getPtr`, `getOrPut`, `remove`, `removeByPtr`, `iterator`, `keys()`/`values()` and insertion-order wording in hash_map.zig and array_hash_map.zig; the `autoHash` compile error for slices; the managed names in std.zig. Removed: the floats claim and the unmanaged-defaults hedge.

Method: documentation only; no commands were run.

## Self-check
Count word frequencies in a text via `getOrPut`, then verify totals; free duped keys before `deinit`.
