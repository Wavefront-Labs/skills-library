---
id: computing-software.software-engineering.crystal.closure-capture
name: closure-capture
category: computing-software
field: software-engineering
product: crystal
tags: [closure-capture, closures, closure, capture, variable-capture, by-reference, heap-closure, loop-variable, crystal]
level: practitioner
status: docs-checked
description: "Know what Crystal closures capture: local variables on the heap, mixed types, and C callback limits."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/closures.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/c_bindings/callbacks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Closure capture semantics

Goal: know what a closure captures.

- Captured blocks and proc literals close over local variables and `self`: `x = 0; proc = -> { x += 1; x }` increments the outer `x`.
- A captured local is allocated on the heap by the compiler, and used as the proc's context data, so it outlives the method (`def counter; x = 0; -> { x += 1; x }; end`).
- If a variable is closured by a proc, its type is always the mixed type of all assignments to it, even when the proc is never called: after `x = 1; -> { x = "hello" }; x = 'a'`, `x` is `Int32 | String | Char`. The compiler assumes the proc may run at an unknown time.
- With a plain (non-captured) yielding block, the compiler still tracks the type at each point: after `x = 'a'`, `x` is `Char`.

Gotchas:
- Functions passed to C cannot form closures; the compiler reports `can't send closure to C function`. Pass a non-closure callback plus boxed data instead (see the callbacks section of the C bindings page).

Verify: spec building counters via closures and checking independence.

## Checked
Checked 2026-11-02 against the crystal-book Closures and C bindings callbacks pages. Removed: the loop-variable claim, the hot-loop cost remark, and the `spawn` capture remark.

Method: documentation only; no commands were run.
