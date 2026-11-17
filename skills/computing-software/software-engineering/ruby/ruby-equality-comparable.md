---
id: computing-software.software-engineering.ruby.ruby-equality-comparable
name: ruby-equality-comparable
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-objects, equality-comparable]
level: advanced
status: docs-checked
description: "Implement ==, eql?, hash and <=> correctly so objects work as hash keys and sort."
sources: ["https://docs.ruby-lang.org/en/master/Object.html", "https://docs.ruby-lang.org/en/master/Comparable.html", "https://docs.ruby-lang.org/en/master/Hash.html", "https://docs.ruby-lang.org/en/master/Set.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Equality eql hash and Comparable
- `==` is value equality, `equal?` is identity, `eql?` is hash equality, `===` is case equality (effectively `==` by default).
- Hash keys and Set elements are the same when their `hash` values match and the objects are `eql?`: override `eql?` and `hash` together to use your objects as keys or in a Set.
- `include Comparable` and define `<=>` to get `<`, `<=`, `==`, `>`, `>=`, `between?` and `clamp`; `<=>` should return `nil` for incomparable objects.
Verify: put two equal objects in a Hash and assert there is one key.

## Checked
2026-11-02. Confirmed against: Object equality methods, Hash key rule, Comparable operators and nil from <=>. Removed or softened (not stated on those pages): 1.eql?(1.0) example, uniq claim.
Method: documentation only; no commands were run.
