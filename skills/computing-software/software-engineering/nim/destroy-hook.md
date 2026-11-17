---
id: computing-software.software-engineering.nim.destroy-hook
name: destroy-hook
category: computing-software
field: software-engineering
product: nim
tags: [destroy-hook, destructors-move-semantics, destroy, =destroy, raii, destructor, ownership, lifetime, hooks, nim]
level: advanced
status: docs-checked
description: "Implement =destroy for resource-owning types, write RAII wrappers over pointers and handles, and obey the lifetime rules."
sources:
  - https://nim-lang.org/docs/destructors.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The =destroy hook and ownership

Goal: tie a resource to a value's lifetime.

```nim
type Buf = object
  p: ptr UncheckedArray[byte]
  n: int
proc `=destroy`(b: Buf) =
  if b.p != nil: dealloc(b.p)
```
- `=destroy` frees the object's memory and releases other resources. Variables are destroyed through it when they go out of scope or when the routine that declared them is about to return.
- The hook exists for each concrete or generic `object` type `T` (also a `distinct` type). Its prototype is ``proc `=destroy`(x: T)``; the parameter may be `T` or `var T`.
- Check whether the value was moved away first (`if x.field != nil:`), because a moved-from value is reset by `=wasMoved` and the destructor must then do nothing.
- The compiler is free to cancel a `=wasMoved(x)` followed by `=destroy(x)`.
- Define the hook before the type is used in the module; a hook that comes too late is a compile error ("destructor for 'f' called here before it was seen in this module").
- If you provide `=destroy` and `=copy`, the compiler takes care of `=sink`.

Gotchas:
- `=destroy` is implicitly `.raises: []`: do not raise from a destructor. A destructor that raises produces a warning for backwards compatibility.
- `{.nodestroy.}` is experimental and stops hook injection (the destructor body then has to destroy its own fields).

Verify: a counter incremented in =destroy equals the number of constructed values.

## Checked

2026-11-08. Confirmed against the Nim Destructors and Move Semantics document (doc/destructors.md, read in full): when `=destroy` runs, its prototype and `T`/`var T` parameter, the not-nil guard pattern, implicit `.raises: []` and the warning, `=wasMoved` + `=destroy` cancelling, `=sink` supplied by the compiler from `=destroy` and `=copy`, the hook-before-use error, and the experimental `nodestroy` pragma. Removed because the page does not state them: the claim that hooks are not defined on `ref` types, the 1.x versus 2.x signature history, the "double free" gotcha wording and the automatic destruction of fields. The old sources (manual, tut1, lib) were not read for this skill and were dropped.
Method: documentation only; no commands were run.
