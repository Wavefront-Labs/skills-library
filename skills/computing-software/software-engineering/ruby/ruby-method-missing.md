---
id: computing-software.software-engineering.ruby.ruby-method-missing
name: ruby-method-missing
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-metaprogramming, method-missing]
level: advanced
status: docs-checked
description: "Implement method_missing with respond_to_missing? and fall back with super."
sources: ["https://docs.ruby-lang.org/en/master/BasicObject.html", "https://docs.ruby-lang.org/en/master/Object.html", "https://docs.ruby-lang.org/en/master/Module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# method_missing and respond_to_missing
- `BasicObject#method_missing` is called when an object receives a message it does not handle; the documented delegation pattern returns `super` for names it does not handle and defines `respond_to_missing?(name, include_private = false)` alongside.
- Dynamic dispatch hides errors; consider `define_method` at definition time.
Verify: `obj.respond_to?(:name)` returns true for the names you handle.

## Checked
2026-11-02. Confirmed against: BasicObject delegation example (method_missing + respond_to_missing?), define_method. Removed or softened (not stated on those pages): argument forwarding syntax, performance claim.
Method: documentation only; no commands were run.
