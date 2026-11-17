---
id: computing-software.software-engineering.nim.template-hygiene-inject-gensym
name: template-hygiene-inject-gensym
category: computing-software
field: software-engineering
product: nim
tags: [template-hygiene-inject-gensym, templates, hygiene, gensym, inject, dirty-template, template-scope, nim]
level: advanced
status: docs-checked
description: "Nim template hygiene: gensym and inject pragmas, per-kind defaults, dirty templates, and restrictions on gensym'd symbols."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template hygiene

Goal: control which template names leak to the caller.

- Pragmas `gensym` and `inject` set exposure of a declared symbol. Default: `var`, `let`, `const` and `type` entities are gensym'd (hidden); `proc`, `iterator`, `converter`, `template`, `macro` default to inject (unless a same-name gensym exists in scope).
- A name passed as a template parameter is injected.
- The `dirty` pragma removes hygiene: `inject` and `gensym` have no effect there.
- Limits of gensym'd symbols: they cannot be used in `x.field`, in object construction, or as named parameters; method-call syntax is not available for them.

Gotchas:
- Annotate with `{.inject.}` when the caller must see a declared variable.

Verify: the caller can (or cannot) reference the name as intended.

## Checked

2026-11-03. Confirmed in the manual's template section. Removed: sequtils `it` example, "second template with the same name does not clash" and "injecting before call is a compile error".
Method: documentation only; no commands were run.
