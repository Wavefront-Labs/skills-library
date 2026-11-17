---
id: computing-software.software-engineering.nim.choosing-mm-orc-arc-refc
name: choosing-mm-orc-arc-refc
category: computing-software
field: software-engineering
product: nim
tags: [choosing-mm-orc-arc-refc, memory-management, orc, arc, refc, mm, gc, memory-manager, reference-counting, mark-and-sweep, nim]
level: practitioner
status: docs-checked
description: "Select --mm:orc, arc, refc, markAndSweep or none, understand the trade-offs, defaults and cycle handling."
sources:
  - https://nim-lang.org/docs/mm.html
  - https://nim-lang.org/docs/nims.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a memory manager: ORC, ARC, refc

Goal: pick the right memory model.

- `--mm:orc` is the default and the recommended switch for new code: reference counting plus a cycle collector ("trial deletion"); no stop-the-world, shared heap.
- `--mm:arc` is the same mechanism without the cycle collector, so reference cycles leak; ORC produces more machine code, so ARC can suit code-size-sensitive targets when you know there are no cycles. The default `async` implementation produces cycles, so use ORC (or YRC) there.
- `--mm:atomicArc` and `--mm:yrc` are thread-safe variants of ARC and ORC using atomic instructions.
- `--mm:refc` is deferred reference counting with a mark-and-sweep backup for cycles; heaps are thread-local.
- `--mm:markAndSweep`, `--mm:boehm`, `--mm:go` also exist; `--mm:none` never frees memory and the docs say to use `--mm:arc` instead.
- Set it in a config file with `switch("mm", "orc")` (the nims guide: `--FOO:VAL` is `switch("FOO", "VAL")`).

Gotchas:
- Break ownership cycles with the `{.cursor.}` pragma (a non-owning ref), or the `acyclic` annotation to skip cycle collection overhead.
- ARC/ORC are not thread-safe for `ref` values accessed across threads; move isolated subgraphs between threads with `isolate`.

Verify: `nim c --mm:arc -d:useMalloc` build runs a leak-free test under valgrind (the mm.md table marks ARC as Valgrind compatible).

## Checked

2026-11-02. Confirmed against mm.md (modes, comparison table, `--expandArc`, async note, `isolate`), destructors.md (`cursor`) and nims.md (`switch`). Removed: the Nim 1.x default claim, the `--gc:orc` alias, `{.unowned.}`, and the claim that ARC/ORC need `=destroy`-aware code.
Method: documentation only; no commands were run.
