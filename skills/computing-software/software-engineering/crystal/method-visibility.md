---
id: computing-software.software-engineering.crystal.method-visibility
name: method-visibility
category: computing-software
field: software-engineering
product: crystal
tags: [method-visibility, visibility, private, protected, public, access-control, private-def, crystal]
level: practitioner
status: docs-checked
description: "Hide internals in Crystal with private and protected: receiver rules, subclasses, namespaces, and private types."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/visibility.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# private and protected methods

Goal: hide internals.

- Methods are public by default; there is no `public` keyword.
- `private def x` can only be invoked without a receiver; `self.x` is the one allowed receiver. Private methods are visible to subclasses.
- `protected def x` can be invoked on instances of the same type as the current type, or in the same namespace (class, struct, module, ...); calling it from another type is an error. A protected method is callable from the type's scope, its descendants, and types including or inheriting that type.
- `private` also applies to `class`, `module`, `lib`, `enum`, `alias` and constants (`private ONE = 1`).

Verify: calling the private method from outside is a compile error.

## Checked
Checked 2026-11-02 against the crystal-book Visibility page. Removed: setter-with-`self` uncertainty, bare `private` keyword remark, `private def` return value and `memoize` remark, protected-in-module and spec `send` remarks.

Method: documentation only; no commands were run.
