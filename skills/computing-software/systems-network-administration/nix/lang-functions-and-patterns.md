---
id: computing-software.systems-network-administration.nix.lang-functions-and-patterns
name: lang-functions-and-patterns
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-language, function-patterns, default-arguments, at-pattern]
level: practitioner
status: docs-checked
description: "Write Nix functions: single-argument, curried, set patterns with defaults and ellipsis, and @ bindings, plus the default-value gotcha with @."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/language/syntax.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Functions are written `pattern: body`. They have no names and are curried, so partial application works.

Pattern forms:
- A single identifier: `x: x + 1`.
- A set pattern naming exact attributes: `{ a, b }: a + b`.
- A set pattern with `...` to allow extra attributes: `{ a, ... }: a`.
- Defaults in a set pattern: `{ a, y ? "foo" }: a + y`.
- An `@` pattern binding the whole argument: `args@{ a, ... }: args`.

All pattern bindings are in scope throughout the function, including inside default expressions.

Gotcha: an `@` binding does not include defaults, so `args.a` may be missing even though the pattern supplied a default for `a`. Use the named binding, not `args.a`, for defaulted values.

Related forms:
- `if e1 then e2 else e3`: `e1` must be a boolean.
- `assert cond; body` returns `body` if `cond` is true, otherwise evaluation aborts with a backtrace. Implication (`->`) is handy for dependency checks.

A set with a callable `__functor` attribute can be applied like a function, receiving the set as its first argument.

## Checked

2026-11-04. Confirmed against the Nix manual Language Constructs page: `pattern: body`, single identifier, set patterns, ellipsis, defaults with `?`, `@` patterns and the warning that `args@` omits defaults, bindings in scope across default values, no function names, currying, `if`, `assert` and `->`, and `__functor`. Removed an unsourced command-output claim.

Method: documentation only; no commands were run.
