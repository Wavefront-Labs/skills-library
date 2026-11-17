---
id: computing-software.software-engineering.ruby.ruby-mixins-include-prepend
name: ruby-mixins-include-prepend
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-modules, mixins-include-prepend]
level: practitioner
status: docs-checked
description: "Choose include, prepend and extend and understand the ancestors chain."
sources: ["https://docs.ruby-lang.org/en/master/Module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mixins include prepend extend
- `Module#ancestors` lists the modules a module/class includes or prepends, including itself, in lookup order; `prepend` places a module ahead of the class.
- Callbacks: `included(othermod)`, `extended(othermod)`, `prepended(othermod)`; `extend` adds a module's methods to one object.
- Inspect the chain with `Klass.ancestors`.
Verify: assert `ancestors` order in a test.

## Checked
2026-11-02. Confirmed against: Module page ancestors/prepend and callbacks. Removed or softened (not stated on those pages): ClassMethods idiom, super-chain wording.
Method: documentation only; no commands were run.
