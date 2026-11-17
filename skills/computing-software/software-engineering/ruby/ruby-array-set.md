---
id: computing-software.software-engineering.ruby.ruby-array-set
name: ruby-array-set
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-collections, array-set]
level: intro
status: docs-checked
description: "Use Array slicing, destructuring, Set and efficient membership tests."
sources: ["https://docs.ruby-lang.org/en/master/Array.html", "https://docs.ruby-lang.org/en/master/Set.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Array operations and Set
- Documented Array methods: `slice` (same as `[]`), `first(count)`, `dig`, `compact`, `flatten`, `uniq`, `rotate`, `sample`, `product`, `combination`.
- `Set` decides equality with `Object#eql?` and `Object#hash` and assumes stored elements do not change; if they do, the set becomes unreliable. Operators: `|` (union), `&` (intersection), `-` (difference), `^`; predicates `subset?`, `superset?`.
- Use a `Set` for membership checks instead of repeated `include?` on a large array, and measure hot paths.
Verify: put a mutable object in a Set, change it, and observe lookups failing.

## Checked
2026-11-02. Confirmed against: Array and Set method names, Set equality via eql?/hash and operator list. Removed or softened (not stated on those pages): slice syntax shortcuts, destructuring, autoload version, O(1) wording, dup depth, Benchmark.ips.
Method: documentation only; no commands were run.
