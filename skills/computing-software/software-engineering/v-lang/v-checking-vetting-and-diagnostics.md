---
id: computing-software.software-engineering.v-lang.v-checking-vetting-and-diagnostics
name: v-checking-vetting-and-diagnostics
category: computing-software
field: software-engineering
product: v-lang
tags: [v-checking-vetting-and-diagnostics, errors-debugging-and-diagnostics, v -check, v vet, -w, warnings as errors, -check-syntax, lint, compiler errors, notices, unused variable, v-lang]
level: practitioner
status: draft
description: "Type-check without building, treat warnings as errors, use v vet and understand the common compiler notices and unused errors."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Static checks: v -check, vet, warnings and notices

Goal: catch problems early and cheaply.

- Fast type-check: `v -check .` (confirm flag name for your version; `v -check-syntax file.v` for parse only).
- `v vet .` reports style and risk (missing docs, unused `mut`, long fns; flags vary).
- Warnings: `-W` makes warnings errors in CI (confirm), `-w` silences them, `-N` hides notices.
- Typical compile errors: unused variable/import, immutable assign, missing `mut` at call, non-exhaustive match, unhandled option/result, missing `unsafe`.
- Error format `file.v:line:col: error: message` is editor friendly (`-message-limit N` to see more).
- Use `v fmt -verify .` too; run all in pre-commit.

Gotchas:
- Fix the first error first; V stops at limited messages.
- Version differences make warnings appear after upgrades.

Verify: CI job fails on a deliberately added unused variable.
