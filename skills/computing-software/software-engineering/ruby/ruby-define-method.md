---
id: computing-software.software-engineering.ruby.ruby-define-method
name: ruby-define-method
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-metaprogramming, define-method]
level: advanced
status: gated
description: "Define methods dynamically and call by name safely."
sources: ["https://docs.ruby-lang.org/en/", "https://www.ruby-lang.org/en/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# define_method send and public_send
- `define_method(:"#{n}?") { @s == n }` creates methods from a list; closures keep local variables; `class_eval` with a string is slower and riskier.
- `send` bypasses visibility; `public_send` respects it - use it for user-influenced names, and whitelist names. (gated: unconfirmed, source is paywalled or blocked)
- `instance_variable_get/set`, `Module#instance_methods(false)`.
Verify: test generated methods with `respond_to?`.

## Checked
2026-11-02. Confirmed: Nothing: syntax docs do not cover define_method, send or public_send.
Gated: whole skill; verify in the Module and Object API docs.
Method: documentation only; no commands were run.
