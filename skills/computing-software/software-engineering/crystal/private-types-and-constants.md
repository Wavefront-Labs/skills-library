---
id: computing-software.software-engineering.crystal.private-types-and-constants
name: private-types-and-constants
category: computing-software
field: software-engineering
product: crystal
tags: [private-types-and-constants, visibility, private-class, private-constant, file-private, nested-class, internal, crystal]
level: practitioner
status: draft
description: "Make types and constants private to a file or namespace using private class, private constant and nested helpers."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Private types, constants and file-private scope

Goal: keep helpers out of the public API.

- `private class Helper` or `private struct`, `private alias`, `private enum` are visible only within the same file (top-level) or the same namespace body.
- `private CONST = 1` hides a constant from other namespaces.
- Use nested `class Foo::Internal` and document it as internal.
- Top-level `private def` is file-private.

Gotchas:
- File-private applies to the top level only; for namespaced types it restricts to that namespace.
- There is no `internal` keyword.
- The doc generator hides private items unless `--project-name` flags say otherwise (confirm options).

Verify: referencing the type from another file errors with `private constant`.
