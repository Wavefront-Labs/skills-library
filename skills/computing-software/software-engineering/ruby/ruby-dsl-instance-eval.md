---
id: computing-software.software-engineering.ruby.ruby-dsl-instance-eval
name: ruby-dsl-instance-eval
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-metaprogramming, dsl-instance-eval]
level: advanced
status: docs-checked
description: "Build configuration DSLs with instance_eval/instance_exec and understand self and binding changes."
sources: ["https://docs.ruby-lang.org/en/master/BasicObject.html", "https://docs.ruby-lang.org/en/master/Module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hooks and DSL design instance_eval
- `instance_eval` evaluates a string or block with `self` set to the receiver, giving the code access to its instance variables and private methods; with a block the object is also passed as the block's argument. `instance_exec` does the same and passes the arguments you give it.
- Hook methods documented on `Module`/`Class`: `inherited`, `included`, `extended`, `prepended`, `method_added`; `const_missing` is the callback for an undefined constant lookup.
- Offer a yielding variant (`configure { |c| ... }`) so users do not depend on a changed `self`.
Verify: write a spec for a DSL block that reads an outer local variable.

## Checked
2026-11-02. Confirmed against: instance_eval/instance_exec semantics and hook callbacks (BasicObject, Module pages). Removed or softened (not stated on those pages): closure variable visibility claims.
Method: documentation only; no commands were run.
