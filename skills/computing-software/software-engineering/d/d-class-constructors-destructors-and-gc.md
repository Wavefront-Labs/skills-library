---
id: computing-software.software-engineering.d.d-class-constructors-destructors-and-gc
name: d-class-constructors-destructors-and-gc
category: computing-software
field: software-engineering
product: d
tags: [d-class-constructors-destructors-and-gc, classes, constructor, destructor, finalizer, destroy, scoped, refcounted, unique, class-lifetime, d]
level: practitioner
status: docs-checked
description: "Initialise and clean up classes: this(), static this, ~this finalisers run by the GC, destroy(), scoped!T and Unique/RefCounted for deterministic cleanup."
sources:
  - https://dlang.org/spec/class.html
  - https://dlang.org/phobos/std_typecons.html
  - https://dlang.org/phobos/object.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Class constructors, destructors, and scope/RAII with classes

Goal: manage class lifetime deliberately.

- Constructors: `this(int x) { this.x = x; }`; a constructor can delegate to another with a `this(...)` call; the object is statically initialised from the class definition before the constructor body runs.
- `~this()` runs when the GC deletes the object, when a `scope` class instance leaves scope, or when `destroy` is called. The GC is not guaranteed to run it for every unreferenced object and the order is unspecified, so a GC-run destructor must not reference sub-objects.
- Deterministic: `destroy(obj)` runs the destructor now; the runtime marks the object so the destructor is never called twice.
- `scoped!Foo(args)` from `std.typecons` allocates the class object in the current scope; its destructor runs when the result is destroyed. Scoped objects cannot be moved.
- Ownership: `std.typecons.Unique!T` encapsulates unique ownership and calls `destroy` on the resource when it leaves scope unless transferred (`release`); `RefCounted` and `SafeRefCounted` are the reference-counted wrappers.

Gotchas:
- `scoped` is unsafe: it is the caller's job not to escape a reference to the object.

Verify: unittest with a static counter checks `destroy()` increments it once.

## Checked
Checked 2026-11-03 against the D spec Classes page (constructors, destructors), the object module (`destroy`) and std.typecons (`scoped`, `Unique`, `RefCounted`). Removed: finaliser-on-any-thread claim, the throwing-destructor claim, the `emplace` remark and the "resets object state" remark (not confirmed).

Method: documentation only; no commands were run.
