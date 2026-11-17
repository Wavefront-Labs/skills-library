---
id: computing-software.systems-network-administration.nix.lang-operators-precedence
name: lang-operators-precedence
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, operators, precedence, set-merge, path-concatenation]
level: practitioner
status: docs-checked
description: "Nix operator precedence and semantics: attribute select, ++, //, + on paths and strings, equality, short-circuiting and the experimental pipe operators."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/language/operators.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
From tightest to loosest binding:
1. `set.path` (with optional `or` fallback)
2. function application (`f x`, left)
3. unary `-`
4. `?` (has attribute path)
5. `++` (list concat, right)
6. `*`, `/`
7. `+`, `-` (`+` also joins strings and paths)
8. `!`
9. `//` (merge sets, right side wins; right-assoc)
10. `<`, `<=`, `>`, `>=`
11. `==`, `!=`
12. `&&`
13. `||`
14. `->` (implication, right)
15. `|>`, `<|` (pipe; experimental)

Semantics:
- Integer-only arithmetic gives an integer; any float operand gives a float. Division by zero and integer overflow are errors.
- `path + string` gives a path. `string + path` copies the file or directory into the store and gives a string.
- `//` evaluates both sides only to weak head normal form, so values stay unevaluated.
- `&&`, `||`, `->` evaluate the right side only when needed: `false && throw "x"` is `false`; `false -> throw "x"` is `true`.
- `A || B && C || D && E` parses as `A || (B && C) || (D && E)`.
- Equality recurses into sets and lists; distinct functions never compare equal.
- Pipe operators need the `pipe-operators` experimental feature.

## Checked

2026-11-04. Confirmed against the Nix manual Operators page: the precedence and associativity table (1 to 15), arithmetic typing and errors, path and string concatenation, `//` strictness, short-circuit behaviour of `&&`, `||` and `->`, the disjunctive normal form example, equality rules and the `pipe-operators` experimental feature. Removed an unsourced command line.

Method: documentation only; no commands were run.
