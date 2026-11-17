---
id: computing-software.software-engineering.nim.cycles-cursors-weakrefs
name: cycles-cursors-weakrefs
category: computing-software
field: software-engineering
product: nim
tags: [cycles-cursors-weakrefs, memory-management, cycles, cursor, weak-reference, orc-cycle-collector, leak, owner-pointer, nim]
level: advanced
status: docs-checked
description: "Avoid leaks with ref cycles under ARC and ORC using {.cursor.} fields, ownership design and the cycle collector."
sources:
  - https://nim-lang.org/docs/destructors.html
  - https://nim-lang.org/docs/mm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reference cycles, cursor and weak references

Goal: handle parent/child links without leaks.

- ORC is the default memory management strategy: reference counting plus a cycle collector based on "trial deletion". `--mm:arc` uses the same mechanism without the cycle collector, so reference cycles leak.
- ORC emits more machine code than ARC. The `acyclic` annotation is advised to optimise away collector overhead; if you know your code makes no cycles and code size matters, `--mm:arc` is an option.
- The default `async` implementation produces cycles and leaks memory with `--mm:arc`; use `--mm:orc` or `--mm:yrc` for async.
- Make back-pointers non-owning with the `cursor` pragma:

```nim
type
  Node = ref object
    left: Node             # owning ref
    right {.cursor.}: Node # non-owning ref
```

  A cursor field is not C++'s `weak_ptr`: it takes no part in reference counting and is a raw pointer without runtime checks, so the owner must outlive it.
- `cursor` also removes the construct/destruct overhead when walking linked structures: `var it {.cursor.} = listRoot`.
- The compiler also infers cursors (copy elision) for `let v = tab["key"]` when `tab` is a non-mutated parameter.
- A custom container needs a `=trace` hook for ORC to collect cycles created through it.
- Inspect what the compiler did with `--expandArc:functionName`.

Gotchas:
- A cursor that outlives its target dangles; the pragma is not checked at runtime.

Verify: build a parent/child tree with cursor back-links under --mm:arc and confirm with --expandArc that no reference count operations remain on the cursor field.

## Checked

2026-11-08. Confirmed against Nim's Memory Management document (doc/mm.md, read in full: ORC trial deletion, ARC without the collector, `acyclic`, async leak under ARC, `--expandArc`) and the Nim Destructors and Move Semantics document (doc/destructors.md, read in full: cursor pragma, cursor inference, `=trace`). Removed because neither page states them: the `GC_fullCollect`, `GC_getStatistics`, `getOccupiedMem` and `getTotalMem` helpers, the `-d:nimArcDebug` and `-d:nimArcIds` flags, the "compiler won't warn" remark, the closure-cycle claim and the index-arena advice. The old sources (manual, tut1, lib) were not read for this skill and were dropped.
Method: documentation only; no commands were run.
