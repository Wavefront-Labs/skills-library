---
id: computing-software.software-engineering.v-lang.v-or-blocks-and-propagation
name: v-or-blocks-and-propagation
category: computing-software
field: software-engineering
product: v-lang
tags: [v-or-blocks-and-propagation, option-and-result-types, or block, propagation, early return, error handling, defaults, v-lang]
level: advanced
status: docs-checked
description: "Choose between or defaults, early return, ! and ? propagation, panic and mixing option and result chains in one function."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# or blocks, propagation and combining option/result

Goal: pick the right failure strategy per call site.

There are four ways to handle an option/result:
- Propagate: `resp := http.get(url)!` for results; after a call producing an option use `?`, and the enclosing function must return an option as well. In `main()` propagation panics.
- Break from execution early: `user := find(7) or { return }`. Call `panic()` or `exit()` to stop the whole program, or use `return`, `break`, `continue` (the last two only inside a `for` loop).
- Default value at the end of the block: `x := f() or { 'default' }`; it must have the same type as the content being handled.
- `if` unwrapping: `if resp := http.get(url) { ... } else { println(err) }`.

Details:
- `or { return err }` is the long form of `!` for results; `or { return none }` propagates absence from an option.
- V has no way to forcibly unwrap; use `or { panic(err) }`.
- A Result's `or` block binds `err` to its `IError`; an Option's `or` block does not bind `err`. A local `err` declared in a nested block shadows it.
- Converting absence into a Result failure: construct an explicit error in the `or` block (`or { return error('absent') }`).
- A `match` expression can propagate results with `!` in its branches.

Verify: write one function exercising the styles and assert behaviour with tests.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Handling options/results", "Option/Result types and error handling"). Removed as not stated there: the `os.read_file(p)!.split_into_lines()` chaining example, "`!` on an option / `?` on a result cannot be mixed" wording, advice on panic for expected failures, `x := f() or { 0 }` as a specific example (the default-value rule is kept).

Method: documentation only; no commands were run.
