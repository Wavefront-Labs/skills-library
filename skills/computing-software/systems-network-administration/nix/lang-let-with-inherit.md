---
id: computing-software.systems-network-administration.nix.lang-let-with-inherit
name: lang-let-with-inherit
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, let-in, with-expression, inherit, shadowing]
level: practitioner
status: docs-checked
description: "Use let-in, with and inherit in Nix correctly, including shadowing rules, rec versus non-rec attribute sets and the infinite recursion pitfall."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/language/syntax.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Let: `let x = 1; y = 2; in x + y` defines local variables. The old `let { ...; body = ...; }` form exists but should not be used in new code.

Inherit:
- `inherit x;` copies `x` from the surrounding scope into a set or let.
- `inherit (src) a b;` copies specific attributes from another set.

With: `with e1; e2` brings the attributes of set `e1` into scope for `e2`.
- Bindings from `let` and function arguments shadow `with` bindings.
- Nested `with` expressions shadow outer ones; the innermost wins.

Recursive sets: `rec { a = 1; b = a + 1; }`. Without `rec`, a name refers to the enclosing scope, not siblings. Mutual references that never terminate give an infinite recursion error.

Attribute sets in general:
- Attribute paths `a.b.c = 1;` create nested sets.
- Access with `.`, with fallback by `or`: `set.missing or "default"`.
- Names must be unique within a set; they can be quoted or interpolated (`${name}`), and a dynamic name that evaluates to `null` is omitted.

Comments: `#` to end of line; `/* ... */` blocks cannot nest, so a second `/*` inside ends the comment early and causes a syntax error.

## Checked

2026-11-04. Confirmed against the Nix manual Language Constructs page: `let`-`in` and the old `let { body = ... }` form, `inherit` and `inherit (src)`, `with` scoping and the manual's shadowing examples, `rec` and the infinite recursion error, attribute paths, `or`, quoted and interpolated names, the `null` name rule, and comment rules. Removed an unsourced command-output line.

Method: documentation only; no commands were run.
