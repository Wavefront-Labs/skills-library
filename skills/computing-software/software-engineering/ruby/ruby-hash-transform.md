---
id: computing-software.software-engineering.ruby.ruby-hash-transform
name: ruby-hash-transform
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, hash-transform, hashes]
level: practitioner
status: docs-checked
description: "Reshape hashes with transform_values, transform_keys, filter_map, group_by, to_h and tally, and know which return a Hash."
sources: ["https://docs.ruby-lang.org/en/master/Hash.html", "https://docs.ruby-lang.org/en/master/Enumerable.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hash transformation methods

```ruby
h = { "a" => 1, "b" => 2, "c" => 3 }
h.transform_values { _1 * 10 }          # {"a"=>10, ...}
h.transform_keys(&:to_sym)              # {a: 1, ...}
h.transform_keys({ "a" => :x })         # remap only listed keys (hash arg)
h.select { |k, v| v > 1 }               # Hash
h.filter_map { |k, v| k if v.odd? }     # Array
h.slice("a", "b"); h.except("c")
h.to_h { |k, v| [k.upcase, v] }         # block must return a pair
h.sum { |_, v| v }
words.group_by(&:size).transform_values(&:count)
words.tally                              # counts by value
h.each_with_object(Hash.new(0)) { |(k, v), acc| acc[v] += 1 }
h.min_by { |_, v| v }                    # returns [k, v]
```
Merge with a block to resolve conflicts: `a.merge(b) { |key, old, new| old + new }`. Core `Hash` has no `deep_merge`.

## Gotchas
- `Hash#map` (Enumerable) returns an Array of whatever the block returns, not a Hash; use `to_h`, `transform_*` or `filter_map` deliberately.
- `transform_keys` with colliding new keys overwrites: `{foo: 0, bar: 1}.transform_keys { "x" }` keeps only the last value. With a hash argument, keys not listed are kept unchanged, and the block (if also given) is called only for unlisted keys.
- Adding a key while iterating a hash raises `RuntimeError` ("can't add a new key into hash during iteration"); build a new hash instead.
- A Hash presents its entries in the order of their creation.

Verify: in irb confirm `{a: 1}.map { |k, v| [k, v] }.class` is Array, `transform_values` returns a Hash, and `{foo: 0, bar: 1, baz: 2}.transform_keys(baz: :foo)` is `{foo: 2, bar: 1}`.

## Checked
2026-11-03. Confirmed against ruby/ruby `hash.c` rdoc and source (`transform_keys` argument and block forms with collision results, `transform_values`, `except`, `to_h` block, merge block for duplicate keys, entry order, "can't add a new key into hash during iteration") and `enum.c` (`filter_map`, `group_by`, `tally`, `each_with_object`, `min_by`, `sum`). Removed: the Ruby 3.0 version tag, the ActiveSupport reference and the advice that bang variants avoid mutation errors.
Method: documentation only; no commands were run.
