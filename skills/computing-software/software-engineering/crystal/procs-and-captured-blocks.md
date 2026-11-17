---
id: computing-software.software-engineering.crystal.procs-and-captured-blocks
name: procs-and-captured-blocks
category: computing-software
field: software-engineering
product: crystal
tags: [procs-and-captured-blocks, blocks-and-procs, proc, capture-block, proc-literal, call, method-to-proc, callback, crystal]
level: practitioner
status: draft
description: "Create Proc values with -> literals, capture a block with &block, call procs and convert methods to procs."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Procs and capturing a block

Goal: store and pass code.

- Literal: `add = ->(a : Int32, b : Int32) { a + b }; add.call(1, 2)` (parameter types required).
- Capture a block: `def on(&block : String -> Nil); @cb = block; end`, then `@cb.call("x")`.
- From a method: `->obj.method(Int32)` or `->Foo.bar(String)`.
- Pass proc as a block: `arr.each(&my_proc)`.
- `Proc#partial`, `#arity`, `#curry` is not provided; wrap in a closure.

Gotchas:
- A proc holds captured variables on the heap; a block does not.
- `return` inside a proc literal returns from the proc; `break` is not allowed.
- The captured type of `&block` must be annotated to be stored in an ivar.

Verify: spec that a stored callback fires once with the expected argument.
