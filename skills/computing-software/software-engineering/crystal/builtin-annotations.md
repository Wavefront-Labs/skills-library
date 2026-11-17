---
id: computing-software.software-engineering.crystal.builtin-annotations
name: builtin-annotations
category: computing-software
field: software-engineering
product: crystal
tags: [builtin-annotations, annotations, alwaysinline, noinline, packed, extern, threadlocal, deprecated, raises, callconvention, crystal]
level: practitioner
status: docs-checked
description: "Know Crystal's compiler annotations: Link, Extern, Packed, AlwaysInline, NoInline, Flags, Deprecated, CallConvention and more."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/annotations/built_in_annotations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Built-in annotations

Goal: know the standard annotations.

- `@[AlwaysInline]` hints the compiler to always inline a method. `@[NoInline]` never inlines a call; it has no effect if the method yields, since yielding methods are always inlined.
- `@[Flags]` marks an enum as a flags enum, changing methods like `to_s`.
- `@[Link(...)]` tells the compiler how to link a C library (see the `lib` section).
- `@[Extern]` lets a Crystal struct be used in `lib` declarations; `@[Extern(union: true)]` makes it behave like a C union (unsafe).
- `@[Packed]` marks a C struct as packed (no padding between fields); only needed when the C library uses packed structs.
- `@[ThreadLocal]` on class variables and C external variables makes them thread local. The standard library uses it for the runtime; it should not be needed outside it.
- `@[Raises]` marks a method or lib `fun` as possibly raising; `@[ReturnsTwice]` marks one that returns twice (like C `setjmp`).
- `@[Deprecated("...")]` marks a method, type or parameter deprecated; it shows in API docs and the compiler warns at use.
- `@[CallConvention("X86_StdCall")]` sets a lib `fun`'s calling convention. Valid: C (default), Fast, Cold, WebKit_JS, AnyReg, X86_StdCall, X86_FastCall.
- `@[TargetFeature("+avx2")]` enables CPU features or a CPU model for one `def` or `fun`.
- The standard library defines more annotations.

Verify: apply one and compile.

## Checked
Checked 2026-11-02 against the crystal-book Built-in annotations page. Removed: `@[Experimental]`, the `--warnings all --error-on-warnings` remark, "Windows C APIs" and profiling remarks.

Method: documentation only; no commands were run.
