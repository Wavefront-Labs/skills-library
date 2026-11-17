---
id: computing-software.software-engineering.crystal.block-forwarding
name: block-forwarding
category: computing-software
field: software-engineering
product: crystal
tags: [block-forwarding, blocks-and-procs, shorthand-block, symbol-to-proc, map, with-index, ampersand, crystal]
level: practitioner
status: docs-checked
description: "Forward blocks in Crystal: yield versus &block, proc forwarding with &proc, and the short &.method syntax."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/block_forwarding.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/blocks_and_procs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Block forwarding

Goal: delegate blocks cleanly.

- Non-captured blocks are forwarded with `yield`: `foo { |x| yield x }` inside a method declared `def wrap_foo(&)`. This is inlined and is the preferred form.
- `&block` forwarding (`def wrap_foo(&block : Int32 -> _)` then `foo(&block)`) requires at least the input types, generates closures and is slower. Avoid it when `yield` is enough.
- `break` and `next` are not allowed inside captured blocks, so they fail under `&block` forwarding.
- Pass an existing proc as a block with `&`: `invoke(&proc)`; `invoke(proc)` is an arity error. `twice &-> { puts "Hello" }` and `twice &->say_hello` also work.
- Short one-parameter syntax: `method &.some_method` or `method(&.some_method)` is sugar for `{ |x| x.some_method }` with no performance penalty. With other required arguments it goes in the argument list: `["a", "b"].join(",", &.upcase)`. Operators work too: `method &.+(2)`.

Verify: `crystal eval 'p [1,2].map(&.to_s)'`.

## Checked
Checked 2026-11-02 against the crystal-book Block forwarding and Blocks and Procs pages. Removed: the `forall U` return-type claim, the list of Enumerable methods, "single call chain only" for `&.`, and the Proc-allocation remark beyond the documented "closures and slower".

Method: documentation only; no commands were run.
