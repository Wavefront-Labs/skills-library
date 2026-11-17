---
id: computing-software.software-engineering.ruby.ruby-case-in-patterns
name: ruby-case-in-patterns
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-pattern-matching, case-in-patterns]
level: practitioner
status: docs-checked
description: "Destructure arrays, hashes and objects with case/in, guards, find pattern and pin operator."
sources: ["https://docs.ruby-lang.org/en/", "https://www.ruby-lang.org/en/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# case in pattern matching
- `case data in {name: String => n, age: Integer => a} if a > 18 then ... in [first, *rest] ... in {status: "ok" | "done"} ... else ... end`; `^var` pins a value; `in [*, 3, *post]` find pattern.
- No match without `else` raises `NoMatchingPatternError`; `data => {name:}` rightward assignment; `value in pattern` returns boolean.
- Define `deconstruct`/`deconstruct_keys` on your classes.
Verify: test non-matching inputs.

## Checked
2026-11-02. Confirmed: doc/syntax/pattern_matching.rdoc: find pattern, NoMatchingPatternError without else, deconstruct/deconstruct_keys, variable pinning, => and in.
Removed: nothing removed.
Method: documentation only; no commands were run.
