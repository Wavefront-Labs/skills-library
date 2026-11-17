---
id: computing-software.software-engineering.ruby.ruby-proc-vs-lambda
name: ruby-proc-vs-lambda
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-blocks, proc-vs-lambda]
level: practitioner
status: docs-checked
description: "Understand the arity and return differences between procs and lambdas."
sources: ["https://docs.ruby-lang.org/en/master/Proc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proc vs lambda semantics
- In lambdas, `return` and `break` exit the lambda; in non-lambda procs, `return` exits the enclosing method (LocalJumpError if invoked outside it).
- Lambdas check argument count (ArgumentError on mismatch); `lambda?` tells which kind a Proc is; `arity`, `curry`, and composition with `<<` and `>>` are documented.
Verify: call each kind with the wrong argument count.

## Checked
2026-11-02. Confirmed against: Proc page. Removed or softened (not stated on those pages): &:sym and method(:x).to_proc shorthand.
Method: documentation only; no commands were run.
