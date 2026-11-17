---
id: computing-software.software-engineering.crystal.blocks-yield
name: blocks-yield
category: computing-software
field: software-engineering
product: crystal
tags: [blocks-yield, blocks-and-procs, block, yield, do-end, block-arguments, break, next, return-in-block, inline, crystal]
level: intro
status: docs-checked
description: "Write block-taking methods in Crystal: yield, block parameters, break and next, type restrictions and with yield."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/blocks_and_procs.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/block_forwarding.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blocks and yield

Goal: write block-taking methods.

```crystal
def twice(&)
  yield 1
  yield 2
end
twice { |i| puts i }
```
- The compiler knows a method takes a block from `yield`; a dummy `&` or `&block` parameter makes it explicit.
- Blocks used with `yield` are always inlined: no closures, calls or function pointers, so `3.times { }` is the same as a hand-written `while` loop.
- A block may declare fewer parameters than are yielded; more is an error (`too many block parameters`). `_` is allowed as a parameter name.
- Each block parameter has the union of the types yielded in that position.
- Unpack with parentheses `|(number, word)|`; nesting and splats (`|(x, *y, z)|`) work. Tuples auto-splat (`|number, word, bool|`), so `Hash#each { |key, value| }` works.
- Restrict the block: `def f(start : Int32, &block : Int32 -> Int32)`; a block returning the wrong type is a compile error.
- A method that yields and one that does not are different overloads.
- `with obj yield` (or `with self yield`) makes `obj` the default receiver for calls inside the block.
- `yield` evaluates to the block's last expression.
- `next [value]` exits the block only; `value` becomes the `yield` result. `break [value]` exits the yielding method and becomes its return value (several values become a Tuple, none is `nil`; with a conditional `break` the call type is a union). In nested blocks `break` leaves only the innermost.
- `do ... end` binds to the left-most call; `{ }` binds to the right-most.

Gotchas:
- `break` and `next` are not allowed inside captured blocks (`&block` forwarding).

Verify: spec returning values via `next` and `break`.

## Checked
Checked 2026-11-02 against the crystal-book Blocks and Procs and Block forwarding pages. Removed: `block_given?` remarks, the `return`-in-block claim, the "block cannot be converted to proc" claim, and `& : Int32 -> _` as a restriction form (the page shows `&block : Int32 -> Int32`).

Method: documentation only; no commands were run.
