---
id: computing-software.software-engineering.crystal.porting-ruby-gems-idioms
name: porting-ruby-gems-idioms
category: computing-software
field: software-engineering
product: crystal
tags: [porting-ruby-gems-idioms, crystal-for-rubyists, porting-ruby, metaprogramming-macros, duck-typing, ruby-gem, translate, ruby-to-crystal, dynamic-to-static, crystal]
level: practitioner
status: draft
description: "Port Ruby scripts and gems to Crystal: replace metaprogramming with macros, duck typing with modules, hashes with NamedTuple or structs."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Porting Ruby code and idioms

Goal: migrate with a plan.

- Start with data: replace Hash-of-anything with structs/records or `JSON::Serializable` classes; heterogeneous values become unions or a JSON::Any boundary.
- Replace `define_method` loops with `{% for %}` macros; `respond_to?` branching with overloads or `is_a?`; `Module#prepend` with `include` plus `super`.
- Replace `method_missing` DSLs with explicit methods or `macro method_missing`.
- Replace `Comparable`/`Enumerable` includes one-to-one; they exist with the same names.
- Use `crystal build --no-codegen` as the fast feedback loop; annotate method signatures at module boundaries.
- Libraries: check shardbox for equivalents instead of porting (ORM, HTTP, templating: ECR is the built-in template engine, `ECR.embed`).

Gotchas:
- Optional arguments of varying types turn into unions that spread everywhere; normalise early.
- Blocks that return different types per call site compile separately.
- Ruby `Hash#each` ordering is insertion; same in Crystal.

Verify: the ported script passes the same fixtures as the Ruby one.
