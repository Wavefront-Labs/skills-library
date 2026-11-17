---
id: computing-software.software-engineering.ruby.ruby-memoization-patterns
name: ruby-memoization-patterns
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, memoization-patterns, caching]
level: practitioner
status: docs-checked
description: "Memoize Ruby methods with ||= and know when nil or false defeats it; local-variable and assignment-method traps."
sources: ["https://docs.ruby-lang.org/en/master/syntax/assignment_rdoc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memoization with ||= and assignment rules

```ruby
def settings = @settings ||= load_settings   # computes once unless the value is nil or false
```
- `a ||= x` assigns when `a` is `nil` or `false`; `a &&= x` assigns when `a` is neither. They behave like `a || a = x`, not `a = a || x`.
- So `||=` recomputes whenever the cached value is `nil` or `false`. A cache that must remember those values needs a different check (the assignment page does not cover `defined?`; test it yourself before relying on it).
- An uninitialized instance variable is `nil`, so `@x ||= ...` works without initialising `@x` first. Instance variables belong to one object; objects of the same class do not share them.
- Class variables (`@@x`) are shared between a class, its subclasses and its instances, and reading an uninitialized one raises NameError. Classes are objects with their own instance variables, so do not confuse the two when caching at class level.
- Global variables (`$x`) are visible everywhere and `nil` when uninitialized.

## Gotchas
- Assignment methods need a receiver: inside a method, `value = 42` creates a local variable, so write `self.value = 42` to call `value=`.
- A local variable is created when the parser sees the assignment, not when it runs: `a = 0 if false` leaves `a` as `nil`.
- `big_calculation = big_calculation()` makes later bare references the local variable (the cached value); call the method with `self.big_calculation` or empty parentheses.
- `p a if a = 0.zero?` raises NameError, because the bare `a` is parsed first as a method call.
- A block creates a new scope: variables first assigned inside do not leak out, while outer variables are visible inside.

## Checked

Date: 2026-11-08. Read in full: the Ruby syntax documentation for assignment (the raw rdoc source on GitHub). Removed: the per-argument Hash cache, `Hash#fetch` with a block and `Hash.new` block examples, thread safety and Mutex advice, `ObjectSpace::WeakMap`, LRU gems, FrozenError on frozen objects and Marshal and inspect notes, because the Hash class page is a stub at docs.ruby-lang.org and the assignment page does not cover them. The Hash class page was dropped from the sources.

Method: documentation only; no commands were run.
