---
id: computing-software.software-engineering.crystal.ruby-differences
name: ruby-differences
category: computing-software
field: software-engineering
product: crystal
tags: [ruby-differences, crystal-for-rubyists, rubyist, ruby, static-typing, porting, syntax-differences, crystal]
level: intro
status: draft
description: "List the key differences: static types, compile-time errors, no eval or method_missing at runtime, Char vs String and nil handling."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ruby to Crystal differences

Goal: translate Ruby habits.

- Static types, checked at compile time; `nil` errors become compile errors.
- No runtime `eval`, `send`, `define_method`, `method_missing` (macros do it at compile time), `instance_variable_get`, `require` at runtime.
- `'a'` is a Char, `"a"` a String; Symbols are not strings and are not created at runtime.
- Hash literal `{a: 1}` is a NamedTuple; use `{:a => 1}` or `{"a" => 1}` for Hash.
- `attr_accessor` is `property`, `attr_reader` is `getter`, `attr_writer` is `setter`.
- `puts "#{x}"` same; `x&.foo` is `x.try &.foo`; `block.call` is `block.call` but blocks are `yield` inlined.
- `Integer` overflow raises instead of becoming Bignum; use `BigInt`.
- `rescue => e` is `rescue e`; `raise Class, msg` is `raise Class.new(msg)`; `private` section keyword does not exist.
- `Array.new(3) { }`, `each_with_index`, `inject` is `reduce`; `Struct.new` is `record`.
- `ARGV`, `ENV`, `File`, `Time`, `JSON` exist with similar APIs but different details.

Gotchas:
- Copy-pasting Ruby rarely compiles; port with the type errors as a guide.
- Performance mindset: allocations and unions matter.

Verify: port a 50-line script and fix compiler errors one by one.
