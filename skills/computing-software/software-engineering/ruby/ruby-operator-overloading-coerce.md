---
id: computing-software.software-engineering.ruby.ruby-operator-overloading-coerce
name: ruby-operator-overloading-coerce
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, operator-overloading-coerce, operators]
level: practitioner
status: docs-checked
description: "Overload operators in Ruby (+, ==, <=>, [], unary, to_s) and implement coerce so 2 * your_object works."
sources: ["https://docs.ruby-lang.org/en/master/syntax/methods_rdoc.html", "https://docs.ruby-lang.org/en/master/Numeric.html#method-i-coerce"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator overloading and coerce

Operators are ordinary methods; define them on your class:
```ruby
Vec = Struct.new(:x, :y) do
  def +(o) = Vec.new(x + o.x, y + o.y)
  def -@ = Vec.new(-x, -y)             # unary minus
  def *(k) = k.is_a?(Numeric) ? Vec.new(x * k, y * k) : raise(TypeError, "#{k.class} can't be coerced")
  def [](i) = to_a.fetch(i)
  def ==(o) = o.is_a?(Vec) && to_a == o.to_a
  alias eql? ==
  def hash = to_a.hash
  def coerce(num) = [self, num]               # makes 2 * vec work (retried as vec * 2)
  def to_s = "(#{x}, #{y})"
end
```
`2 * vec` calls `Integer#*`, which does not know Vec, so Ruby calls `vec.coerce(2)` and retries the operation with the returned 2-element array `[a, b]` as `a * b`; a `coerce` that does not return a 2-element array raises `TypeError` ("coerce must return [x, y]"), and a missing `coerce` raises `TypeError` ("... can't be coerced into ..."). Include `Comparable` and define `<=>` to get `<`, `>`, `between?` and `clamp`.

The documented operator methods are `+ - * ** / % & | ^ >> << == != === =~ !~ <=> < <= > >=`, each taking one argument; you cannot alter their precedence. Define unary minus and plus as `-@` and `+@`; `~` and `!` unary methods may be written with or without `@`. Element reference and assignment are `[]` and `[]=`.

## Gotchas
- Hash uses both `#hash` and `#eql?` to decide whether two objects are the same key, so define them together if instances are Hash keys.
- Creating an alternate meaning for an operator can confuse users who expect plus to add and minus to subtract.
- Unary methods accept zero arguments.

Verify: confirm `2 * Vec.new(1,2)` returns a Vec, `Vec.new(1,2) == Vec.new(1,2)` is true, and `{Vec.new(1,2) => 1}[Vec.new(1,2)]` is 1.

## Checked
2026-11-03. Confirmed against ruby/ruby `doc/syntax/methods.rdoc` (operator method list, unary `@` forms, `[]`/`[]=`, precedence), `numeric.c` (`Numeric#coerce`, coerce TypeError messages), `compar.c` (between?, clamp) and `hash.c` (Hash uses `#hash` and `#eql?`). Removed: the non-overloadable operator list, the `<=>` nil/sort advice, the `<<` chaining and TypeError-versus-NoMethodError advice, and the undefined `Scalar` class in the example.
Method: documentation only; no commands were run.
