---
id: computing-software.software-engineering.nim.defer-and-resource-cleanup
name: defer-and-resource-cleanup
category: computing-software
field: software-engineering
product: nim
tags: [defer-and-resource-cleanup, exceptions, defer, cleanup, raii, finally, resource-management, close, nim]
level: practitioner
status: docs-checked
description: "Use Nim defer and try/finally to release files and handles safely on every exit path."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# defer and resource cleanup

Goal: never leak resources.

- `defer: close(f)` right after opening the file. Any statements following the defer are considered to be in an implicit `try` block in the current block, and the defer body becomes the `finally` part (the manual shows `defer: close(f)` rewritten to `try: ... finally: close(f)`).
- `defer` avoids lexical nesting and offers more flexibility in scoping than `try ... finally`.
- Plain `try: ... finally: close(f)` is the explicit form when you want an explicit scope; `finally` always runs after the exception handlers.
- When `defer` is at the outermost scope of a template or macro, its scope extends to the block where the template or macro is called from.

Gotchas:
- Top-level `defer` statements are not supported, because it is unclear what such a statement should refer to.

Verify: the close message prints after the body and also when the body raises.

## Checked

2026-11-08. Read the Nim manual Defer statement and Try statement sections in full; the bullets above match them.

Removed as unconfirmed on the manual: the reverse-order claim, destructor (`=destroy`) advice, the stdlib shortcut list (`withLock`, `readFile`), and the claims about `return` inside a defer and top-level defer running at program end (the manual says top-level defer is unsupported). Dropped the tutorial and lib index sources (not used).

Method: documentation only; no commands were run.
