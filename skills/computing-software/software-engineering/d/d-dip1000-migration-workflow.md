---
id: computing-software.software-engineering.d.d-dip1000-migration-workflow
name: d-dip1000-migration-workflow
category: computing-software
field: software-engineering
product: d
tags: [d-dip1000-migration-workflow, dip1000-scope, dip1000-migration, preview-flags, safe-migration, dflags, trusted-narrowing, d]
level: advanced
status: draft
description: "Roll out -preview=dip1000 on a project: fix errors by adding scope/return, using @trusted narrowly, and checking with -preview=in and -revert flags in dub."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Adopting DIP1000 in an existing codebase

Goal: turn on stronger @safe without a rewrite.

1. Add `dflags "-preview=dip1000"` to dub.sdl and build `-b unittest`; collect errors.
2. Annotate leaf functions first: add `scope` to non-escaping params, `return scope`/`return ref` where the result borrows.
3. For genuine unsafe internals (manual memory), wrap in a tiny `@trusted` function with a safe signature.
4. Related previews: `-preview=in` (in = const scope, passes large values by ref), `-preview=rvaluerefparam`, `-preview=fieldwise` (confirm availability with `dmd -preview=help`).
5. Lock the behaviour by building CI with the flag, plus `@safe:` at module top for new modules.
6. Check `dmd -transition=help` and `dmd -revert=help` for temporary escape switches while migrating.

Gotchas:
- Third-party dub deps may not compile under the flag; set the flag per configuration or per package (`dflags` in your own package only).
- Warnings from `-preview` flags change between releases.

Verify: CI compile with the flag passes with zero `@trusted` additions outside reviewed files.
