---
id: computing-software.software-engineering.ruby.ruby-truthiness
name: ruby-truthiness
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-objects, truthiness]
level: intro
status: docs-checked
description: "Know that only nil and false are falsy and use &. and || safely."
sources: ["https://raw.githubusercontent.com/ruby/ruby/master/doc/syntax/calling_methods.rdoc", "https://docs.ruby-lang.org/en/master/Hash.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Truthiness nil and safe navigation
- The safe navigation operator `&.` skips the call when the receiver is `nil` and returns `nil`.
- `Hash#fetch` and `Hash#dig` are documented ways to read keys; a default value or default_proc changes what a missing key returns.
Verify: test with `false` and `nil` values separately.

## Checked
2026-11-02. Confirmed against: calling_methods doc (&.) and Hash page. Removed or softened (not stated on those pages): falsy-values statement and ||= semantics (not located in the fetched syntax pages).
Method: documentation only; no commands were run.
