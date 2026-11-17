---
id: computing-software.software-engineering.crystal.modules-mixins
name: modules-mixins
category: computing-software
field: software-engineering
product: crystal
tags: [modules-mixins, modules, module, mixin, include, extend, comparable, enumerable, iterable, crystal]
level: practitioner
status: draft
description: "Share behaviour with include (instance methods) and extend (class methods), and use stdlib modules like Comparable and Enumerable."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Modules as mixins: include and extend

Goal: reuse code without inheritance.

- `include Comparable(Foo)` plus `def <=>(other : Foo)` gives `<`, `>`, `between?`, `clamp`.
- `include Enumerable(T)` plus `def each(&)` gives map, select, sort_by, min_by, sum and about 60 more.
- `include Iterator(T)` plus `def next` gives lazy chains.
- `extend self` in a module turns its methods into module functions.
- `module M; def self.helper; end; end` for utilities.

Gotchas:
- Included module methods sit after the class in lookup, so the class overrides them; `super` calls the module's.
- `extend` adds class-level methods; the `included`/`extended` macro hooks run at include time.
- Instance variables declared in a module appear in includers.

Verify: spec that sorting uses `<=>` and `to_a` works via Enumerable.
