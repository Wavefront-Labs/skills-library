---
id: computing-software.software-engineering.ruby.ruby-keyword-arguments
name: ruby-keyword-arguments
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-pattern-matching, keyword-arguments]
level: practitioner
status: docs-checked
description: "Use keyword arguments with Ruby 3 separation and forward arguments with ... correctly."
sources: ["https://docs.ruby-lang.org/en/", "https://www.ruby-lang.org/en/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyword arguments and argument forwarding
- `def f(a, b = 1, *rest, k:, o: 2, **kw, &blk)`; required `k:` missing raises ArgumentError; `**nil` forbids keywords.
- Forward everything: `def wrap(...) = target(...)`.
Verify: call each signature with and without the required keyword.

## Checked
2026-11-02. Confirmed: doc/syntax/methods.rdoc: required keyword raises ArgumentError (missing keywords), **nil, ... forwarding.
Removed: Ruby 3.0 separation statement, version numbers and anonymous * and ** forwarding (not in the docs read).
Method: documentation only; no commands were run.
