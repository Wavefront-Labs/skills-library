---
id: computing-software.software-engineering.ruby.ruby-rbs-type-signatures
name: ruby-rbs-type-signatures
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, rbs-type-signatures, typing]
level: advanced
status: draft
description: "Add type signatures to Ruby with RBS files, rbs collection, Steep or TypeProf, including generics and unions."
sources: ["https://github.com/ruby/rbs", "https://github.com/ruby/typeprof", "https://github.com/soutaro/steep"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RBS type signatures and TypeProf

RBS is Ruby's official signature language, kept in `.rbs` files beside the code (conventionally `sig/`). Ruby itself does not check them at runtime; a checker such as Steep (or Sorbet via its own system) does.

```rbs
# sig/order.rbs
class Order
  attr_reader total: Integer
  def initialize: (items: Array[Item], ?coupon: String?) -> void
  def apply: (Coupon) -> Order | nil
  def each_line: () { (Item) -> void } -> void
             | () -> Enumerator[Item, void]
end
module Priceable[T]
  def price: () -> T
end
```
Workflow:
```sh
gem install rbs steep
rbs collection init && rbs collection install   # signatures for gems, lockfile rbs_collection.lock.yaml
rbs prototype rb lib/order.rb > sig/order.rbs   # first draft, then edit by hand
steep init && steep check
```
TypeProf (`typeprof lib/order.rb`) infers signatures from the code as a starting point.

## Gotchas
- Generated prototypes are mostly `untyped`; treat them as a skeleton and tighten gradually. Do not chase 100 percent.
- Dynamic features (`define_method`, `method_missing`, DSLs) need hand-written signatures or `untyped`.
- Pin the Steep/RBS versions in the Gemfile; signature syntax and the stdlib RBS set shift between releases, so verify against the version you install.
- CI should run `steep check` and `rbs validate`.

Verify: introduce a call with the wrong argument type and confirm `steep check` reports a diagnostic with file and line.
