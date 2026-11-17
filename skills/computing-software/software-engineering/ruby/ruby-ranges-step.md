---
id: computing-software.software-engineering.ruby.ruby-ranges-step
name: ruby-ranges-step
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ranges-step, ranges]
level: intro
status: docs-checked
description: "Use Ruby ranges for iteration, case matching, endless and beginless ranges, step, size, and cover? versus include?."
sources: ["https://docs.ruby-lang.org/en/master/Range.html", "https://docs.ruby-lang.org/en/master/Numeric.html#method-i-step"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ranges and step iteration

```ruby
(1..5).to_a          # inclusive: [1,2,3,4,5]
(1...5).to_a         # exclusive end
(1..).first(3)       # endless range: [1, 2, 3]
(..10).include?(3)   # beginless range: true
(1..5) % 2           # Range#% is step: ((1..5).%(2))
('a'..'e').step(2) { |c| p c }   # a, c, e (String#succ)
(1..5).step(2).to_a  # [1, 3, 5]
1.step(10, 3).to_a   # [1,4,7,10]
case age when 0...13 then :child when 13..19 then :teen else :adult end
(1..3).cover?(1.5)   # true; include? on numeric ranges behaves like cover?
('a'..'d').cover?("cc")    # true
('a'..'d').include?("cc")  # false (string ranges test elements)
5.clamp(1..10)
```

## Gotchas
- `(1..).to_a` raises `RangeError` ("cannot convert endless range to an array"), but iterating an endless range with `each`, `map` or `each_slice` and no break never ends; call `.lazy` or `first(n)` / `take`.
- A Float begin cannot iterate: `(1.0..2.0).each` raises `TypeError` ("can't iterate from Float") and so does `(0.5..2.5).size`, while `cover?` works. `(1.0..).step(1.5)` is allowed and gives an arithmetic sequence.
- `(5..1).to_a` is empty; use `5.downto(1)` or `(1..5).reverse_each`. A negative step needs begin above end: `(6..0).step(-2)` yields 6, 4, 2, 0, while `(0..6).step(-2)` yields nothing.
- Ranges of other objects (Time, custom classes) need `<=>` to compare; `each` needs `succ`. `step` on a non-numeric range requires an explicit step (else `ArgumentError`) and uses `+`.
- `Range#size` returns the count for numeric ranges, `Infinity` for `(1..)` and `nil` for `('a'..'z')`.

Verify: print `(1.0..2.0).cover?(1.5)` (true) and rescue the TypeError from `(1.0..2.0).each {}` and the RangeError from `(1..).to_a` to confirm each rule.

## Checked
2026-11-03. Confirmed against ruby/ruby `range.c` rdoc and source (`step` and `%` examples, String step with an integer, negative step, `to_a` RangeError, `can't iterate from`, `size` table, `include?` versus `cover?`, `===` in case), `compar.c` (`clamp(range)`) and `array.c` (`a[..2]`, `a[..-1]`). Fixed: the old gotcha said `(1..).to_a` loops forever; it raises RangeError. Removed: the Ruby version tags, the float-accumulation "may miss 1.0" claim, and the `Range#sum` claim.
Method: documentation only; no commands were run.
