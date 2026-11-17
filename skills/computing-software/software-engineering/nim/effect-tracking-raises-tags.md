---
id: computing-software.software-engineering.nim.effect-tracking-raises-tags
name: effect-tracking-raises-tags
category: computing-software
field: software-engineering
product: nim
tags: [effect-tracking-raises-tags, effects-and-pragmas, raises, tags, effects, gcsafe, forbids, noreturn, effect-system, nim]
level: advanced
status: docs-checked
description: "Annotate and check exceptions and effects with raises, tags, forbids and gcsafe, and read inferred effects."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Effect tracking: raises, tags, forbids

Goal: make error and IO behaviour part of signatures.

- `proc p() {.raises: [IOError, OSError].}` makes the compiler verify that nothing else can be raised; `raises: []` means no exception may be raised. A `raises` list can be attached to a proc type, which affects type compatibility.
- Inference for `raises` works on the call graph: an indirect call through a proc type is assumed to raise `system.Exception` unless the type has an explicit `raises` list; a call to a proc with an unknown body (forward declaration) or to a method is assumed to raise `Exception` unless it has a `raises` list; `importc` procs are assumed `raises: []`.
- Exceptions inheriting from `system.Defect` are not tracked: `proc mydiv(a, b): int {.raises: [].}` with `a div b` is valid.
- `effectsOf: callback` on a proc-typed parameter lets a routine pass on the effects of the callback it is given, so a `raises: []` caller passing a raising proc is rejected.
- `{.tags: [IO].}` tags a routine with an effect; a tag is a type name and a `tags` list can be attached to a proc type. `tags: []` forbids all tagged effects in the body. `{.forbids: [IO].}` lists illegal effects: any statement that invokes one fails compilation, and a proc type with a `forbids` list is a subtype-target for equal types without it; the caller does not inherit the forbidden list.
- `noSideEffect` marks a routine whose only side effects go through its parameters; `func` is sugar for a proc with no side effects, and it is a static error if the compiler cannot verify it. `{.cast(noSideEffect).}:` overrides the analysis, and `debugEcho` pretends to be free of side effects.
- GC safe: a proc is GC safe when it does not access global variables that contain GC'ed memory (`string`, `seq`, `ref`, closures), directly or through a GC unsafe call. It is usually inferred; `gcsafe` can mark it, `noSideEffect` implies `gcsafe`, and C-imported routines are assumed `gcsafe`. `{.cast(gcsafe).}:` overrides the analysis.
- The `{.effects.}` statement makes the compiler output a hint listing the effects inferred up to that point.

Gotchas:
- Side effects, GC safety and tags are inferred analogously to exception tracking; imported functions whose effects cannot be inferred can be annotated with `sideEffect`.

Verify: put `raise newException(IOError, "x")` in a proc marked `{.raises: [].}`; compilation fails because the raise is not allowed there.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md from the Nim repository), Effect system chapter in full (Exception tracking, EffectsOf annotation, Tag tracking, Side effects, GC safety effect, Effects pragma). Removed because that chapter does not state them: that gcsafe is needed for procs passed to threads and the lock/threadvar guidance, `func` being "the strongest form", that effects are inferred only for non-exported procs, `{.cast(raises: []).}`, and the `readFile`/IOError verify step. tut1 and lib were not read and were dropped from sources.
Method: documentation only; no commands were run.
