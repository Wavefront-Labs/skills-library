---
id: computing-software.software-engineering.ruby.ruby-deconstruct-keys
name: ruby-deconstruct-keys
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, deconstruct-keys, pattern-matching]
level: advanced
status: docs-checked
description: "Make your classes match in case/in by defining deconstruct and deconstruct_keys; guards, pin, find pattern and NoMatchingPatternError."
sources: ["https://docs.ruby-lang.org/en/master/syntax/pattern_matching_rdoc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# deconstruct and deconstruct_keys

Pattern matching calls `deconstruct` for array patterns `[a, b]` and `deconstruct_keys(keys)` for hash patterns `{name:, age:}`. Struct and Data define both; plain classes need them:

```ruby
class Point
  attr_reader :x, :y
  def initialize(x, y) = (@x, @y = x, y)
  def deconstruct = [x, y]
  def deconstruct_keys(keys) = { x: x, y: y }   # keys is an Array of requested keys, or nil
end
case Point.new(1, 2)
in [0, 0]            then "origin"
in { x:, y: } if x == y then "diagonal"
in Point(x:, y:)     then "point #{x},#{y}"   # Const(...) also checks ===
end
config = { db: { host: "h" } }
config in { db: { host: String => host } }    # boolean test, binds host
expected = 5
case 5
in ^expected then "pinned"                    # ^ pins an existing value
end
case [1, 42, "x"]
in [*, Integer => n, *post] then n            # find pattern
end
{ status: "ok" } => { status: }               # rightward assignment, raises if no match
```
`deconstruct_keys` receives `nil` when the pattern has `**rest`; otherwise it receives the requested keys, so you can compute only that sub-hash when a full one is expensive. Struct and Data define both `deconstruct` and `deconstruct_keys`; so do MatchData, and Time, Date and DateTime define `deconstruct_keys`.

## Gotchas
- `case/in` with no matching branch and no `else` raises `NoMatchingPatternError`; the `=>` form raises the same way when the structure is unexpected. `NoMatchingPatternKeyError` is the error for a matching key that was not found.
- Hash patterns match subsets (only symbol keys are supported), while array patterns match the whole array unless you add `*`. `in {}` is the exception: it matches only an empty hash.
- Use `in {a: Integer, **nil}` to forbid keys other than those listed.
- `expr in pattern` is the same as a `case` returning true or false.

Verify: match `Point.new(2,2)` and confirm "diagonal", then match a value no branch accepts to see the exception.

## Checked
2026-11-03. Confirmed against ruby/ruby `doc/syntax/pattern_matching.rdoc` (exhaustive `case/in`, `=>` and `in`, whole-array versus subset-hash matching, `{}`, `**nil`, pin `^`, find pattern, `deconstruct`/`deconstruct_keys` with `keys` or `nil`, `Const(...)` checked with `===`, guards, list of classes implementing deconstruction), `struct.c` (Struct and Data define both methods) and `error.c` (NoMatchingPattern errors). Removed: the Ruby 3.0/3.1 stability claim, the old one-line `case ... in` and `result = ... =>` forms (unverified syntax) and the claim about which error a missing key raises.
Method: documentation only; no commands were run.
