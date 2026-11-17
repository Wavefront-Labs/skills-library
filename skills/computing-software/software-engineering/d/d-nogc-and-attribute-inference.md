---
id: computing-software.software-engineering.d.d-nogc-and-attribute-inference
name: d-nogc-and-attribute-inference
category: computing-software
field: software-engineering
product: d
tags: [d-nogc-and-attribute-inference, function-attributes, gc-free, -vgc, gc-allocation, attribute-inference, static-assert-attributes, nogc, d]
level: practitioner
status: docs-checked
description: "Prevent GC allocations with @nogc, know what the spec forbids (new, ~, AAs, closures), and find allocations with -vgc and -profile=gc."
sources:
  - https://dlang.org/spec/function.html
  - https://dlang.org/dmd-linux.html
  - https://dlang.org/phobos/core_memory.html
  - https://dlang.org/spec/unittest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @nogc, attribute inference and attribute-checking in CI

Goal: write allocation-free code and prove it.

- `@nogc` forbids: constructing an array on the heap, resizing via `.length`, array concatenation and appending (`~`, `~=`), constructing or indexing an associative array, `new` on the heap, and calling non-`@nogc` functions (except inside a `debug` statement). A closure is allowed only if it is `scope`.
- `new` of a class to initialise a `scope` variable is allowed, as it allocates on the stack.
- `dmd -vgc` lists all GC allocations including hidden ones; `-profile=gc` instruments allocations and writes a report to `profilegc.log` when the program ends.
- Inspect attributes with `__traits(getFunctionAttributes, f)`, or attribute a `unittest` (for example `@safe nothrow unittest`) to verify its body.
- `core.memory.GC.disable()`, `GC.enable()` and `GC.collect()` control the collector; `@nogc` alone does not stop another thread's allocation from triggering a collection.

Gotchas:
- `@nogc` is part of the function type: a `@nogc` function is covariant with a non-`@nogc` one, not the reverse.

Verify: `dmd -vgc -c m.d` prints no lines for your hot path.

## Checked
Checked 2026-11-03 against the D spec Functions page (No-GC Functions), the dmd command-line page (`-vgc`, `-profile=gc`), the core.memory page (`GC.enable`, `disable`, `collect`) and the Unit Tests page (attributed unittests). Removed: the `.dup`/`to!string` list, the malloc/allocator escape hatches, the exception-throwing remark and the template-instantiation remark (not stated there).

Method: documentation only; no commands were run.
