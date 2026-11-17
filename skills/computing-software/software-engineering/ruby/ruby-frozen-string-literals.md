---
id: computing-software.software-engineering.ruby.ruby-frozen-string-literals
name: ruby-frozen-string-literals
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-objects, frozen-string-literals]
level: practitioner
status: gated
description: "Use symbols for identifiers, frozen_string_literal magic comments and dup rules for strings."
sources: ["https://docs.ruby-lang.org/en/", "https://www.ruby-lang.org/en/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Symbols strings and frozen string literals
- `# frozen_string_literal: true` at file top makes literals immutable (`FrozenError` on `<<`); use `+""` or `String.new` for a mutable buffer, `str.dup` for copies. Ruby 3.4 warns on mutating un-annotated literals only with `-W:deprecated` (chilled strings; check NEWS).
- Symbols are unique immutable identifiers; do not call `to_sym` on untrusted input in old Rubies (symbol GC arrived in 2.2, so modern risk is low but keep it bounded).
- `String#<<` mutates; `+` creates new strings. (gated: unconfirmed, source is paywalled or blocked)
Verify: run with `RUBYOPT=-W:deprecated`.

## Checked
2026-11-02. Confirmed: Nothing: doc/syntax/literals.rdoc does not mention the frozen_string_literal comment.
Gated: whole skill; verify in the String and NEWS docs.
Method: documentation only; no commands were run.
