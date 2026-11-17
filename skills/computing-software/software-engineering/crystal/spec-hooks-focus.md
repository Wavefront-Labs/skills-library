---
id: computing-software.software-engineering.crystal.spec-hooks-focus
name: spec-hooks-focus
category: computing-software
field: software-engineering
product: crystal
tags: [spec-hooks-focus, spec-framework, before-each, after-each, around-each, before-all, spec-helper, focus, spec-tags, custom-matcher, fixtures, crystal]
level: practitioner
status: draft
description: "Use before_each, after_each, around_each, before_all, after_all, focus, tags, shared helpers and custom expectations."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hooks, focus, tags and spec helpers

Goal: structure larger suites.

- `before_each { db = Db.new }` blocks are closures: declare a nilable local in the describe body (`db = nil`) and assign it in the hook, or use a helper method returning fresh state per example.
- `after_each`, `around_each { |example| setup; example.run; teardown }`, `before_all`/`after_all` (newer versions, confirm).
- Focus: `it "x", focus: true` or `describe ..., focus: true`; then `crystal spec` runs only those.
- Tags: `it "slow", tags: "slow"` then `crystal spec --tag slow` or `--tag ~slow`.
- Helper file `spec/spec_helper.cr` requires `spec` and `../src/myapp`; add helper methods and a custom expectation struct with `match(actual)`, `failure_message`, `negative_failure_message`.

Gotchas:
- Remove `focus: true` before committing; CI may warn.
- Hook order: outer before first, inner after.
- Mock libraries (webmock.cr, spectator) are shards; stdlib has no mocking.

Verify: run with `--order random` several times.
