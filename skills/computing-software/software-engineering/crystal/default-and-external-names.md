---
id: computing-software.software-engineering.crystal.default-and-external-names
name: default-and-external-names
category: computing-software
field: software-engineering
product: crystal
tags: [default-and-external-names, overloading, default-args, default-values, external-name, keyword-args, parameter-names, optional-args, crystal]
level: practitioner
status: draft
description: "Use default arguments, external names (foo bar : T) and keyword-style calls, and see how they create overloads."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Default values and external parameter names

Goal: design call-friendly APIs.

- `def fetch(url : String, retries = 3, timeout : Time::Span = 5.seconds)`.
- External name: `def move(from start : Int32, to finish : Int32)` is called `move(from: 1, to: 2)` while using `start`/`finish` inside.
- Defaults are evaluated per call and can refer to earlier params.
- Required-after-optional is allowed when later ones are named-only (after `*`).

Gotchas:
- Use `nil` default only when the type includes Nil.
- A reserved word as external name works (`if`, `in`) but may confuse tools.
- Mutable default (`[]`) is fresh on each call, not shared.

Verify: call positionally and by name in specs.
