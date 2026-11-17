---
id: computing-software.software-engineering.d.d-struct-copy-constructor-postblit-destructor
name: d-struct-copy-constructor-postblit-destructor
category: computing-software
field: software-engineering
product: d
tags: [d-struct-copy-constructor-postblit-destructor, structs-and-unions, copy-constructor, postblit, destructor, move, ~this, lifecycle, raii, d]
level: advanced
status: docs-checked
description: "Control struct lifecycle: this(ref return scope S) copy ctor, deprecated this(this) postblit, ~this destructor, std.algorithm.move and emplace semantics."
sources:
  - https://dlang.org/spec/struct.html
  - https://dlang.org/phobos/std_algorithm_mutation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Copy constructors, postblit, destructors and move

Goal: write resource-owning structs.

- Copy constructor: `this(ref return scope const S rhs) { ... }` Overloads for `const`, `immutable`, mutable sources are allowed.
- Postblit `this(this)` is the older form; the plan is for copy constructors to replace it. A struct defining both uses the postblit for implicit copying, unless the postblit is disabled, in which case the copy constructor is used.
- Destructor `~this()` runs when the object goes out of scope or before an assignment; field destructors run at the end of the parent's. `destroy` calls it early, and it still runs again at scope exit.
- Move: `std.algorithm.mutation.move(source, target)` or `move(source)` (returns the value); if the struct has a destructor or postblit the source is reset to its `.init`. `swap(a, b)` exchanges two values.
- Non-copyable owner: `@disable this(this);` plus `ref`/`move` transfer.
- Reference-counted wrapper: store the pointer and counter, increment in copy ctor, decrement in `~this`.

Gotchas:
- A moved-from value is reset to `.init` (for structs with a destructor or postblit), so the destructor must tolerate it.

Verify: count constructor/destructor calls in a unittest with a static counter.

## Checked
Checked 2026-11-03 against the D spec Structs and Unions page (copy constructors, postblits, destructors) and the std.algorithm.mutation page (`move`, `swap`). Removed: the "D 2.094+" version gate, the "postblit cannot take parameters" remark and the GC-collected-struct remark (not on those pages).

Method: documentation only; no commands were run.
