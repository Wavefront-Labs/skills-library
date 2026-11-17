---
id: computing-software.software-engineering.ruby.ruby-struct-data
name: ruby-struct-data
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-modules, struct-data]
level: practitioner
status: docs-checked
description: "Model value objects with Struct and Data.define (Ruby 3.2+), with keyword_init and immutability."
sources: ["https://docs.ruby-lang.org/en/master/Struct.html", "https://docs.ruby-lang.org/en/master/Data.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Struct Data and value objects
- `Struct` classes support `keyword_init`, `to_a`, `deconstruct`, `deconstruct_keys`.
- `Data.define` makes value objects without member writers (immutable, though mutable members are not frozen), with `==`, `to_h`, `deconstruct` and `deconstruct_keys` for pattern matching; a different-class comparison raises ArgumentError.
Verify: assert that Data has no writer methods.

## Checked
2026-11-02. Confirmed against: Struct and Data pages. Removed or softened (not stated on those pages): with(), missing-member rules, version tags.
Method: documentation only; no commands were run.
