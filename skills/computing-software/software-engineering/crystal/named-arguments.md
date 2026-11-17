---
id: computing-software.software-engineering.crystal.named-arguments
name: named-arguments
category: computing-software
field: software-engineering
product: crystal
tags: [named-arguments, splats-named-args, named-args, call-by-name, argument-order, labels, crystal]
level: intro
status: docs-checked
description: "Call Crystal methods by name: any order, required parameters, defaults, and the splat restriction."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/default_and_named_arguments.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Named arguments at call sites

Goal: call by name.

- Every argument can be passed by name as well as by position: `john.become_older by: 5`.
- The order of the names does not matter as long as all required parameters are covered: `some_method y: 10, x: 20`; a missing required one is `missing argument: x`.
- Defaults are for the last parameters (`def become_older(by = 1)`).
- Positional arguments can be mixed with names after them: `some_method 10, z: 10`.
- When a method has a splat parameter, named arguments cannot be used for positional parameters.

Verify: `Foo.new(age: 1, name: "z")` compiles.

## Checked
Checked 2026-11-02 against the crystal-book Default parameter values and named arguments page. Removed: duplicate-argument error, hash-literal remark, API-breakage and external-names remarks, signature-listing error.

Method: documentation only; no commands were run.
