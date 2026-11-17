---
id: computing-software.qa-testing-engineering.test-automation.dead-and-unreachable-code-detection
name: dead-and-unreachable-code-detection
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [dead-code-detection, unreachable-code, static-analysis, vulture, knip]
level: practitioner
status: verified
description: "Find dead and unreachable code with vulture, knip, staticcheck/deadcode and compiler warnings, confirm with coverage and usage data, and remove it safely."
sources:
  - https://github.com/jendrikseipp/vulture
  - https://knip.dev/
  - https://go.dev/blog/deadcode
  - https://eslint.org/docs/latest/rules/no-unreachable
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dead and unreachable code detection

**Goal:** less code to test and maintain; unreachable code also hides logic defects (a condition that can never be true).

## Tools by language
| Language | Tool | Command |
|---|---|---|
| Python | vulture | `vulture src/` (exit code 3 when it finds something); whitelist file for framework-called code (`vulture --make-whitelist > whitelist.py`). Unused functions, classes and variables are reported at 60% confidence, so `--min-confidence 80` hides them and shows only unused imports and arguments (run) |
| Python | ruff | `F401` unused imports, `F841` unused variables (both fired) |
| JS/TS | knip | `npx knip` finds unused files, exports, dependencies (run: reported an orphan file, an unused export and an unused dependency) |
| JS/TS | ESLint | `no-unreachable`, `no-unused-vars`, `@typescript-eslint/no-unnecessary-condition` (the last needs typed linting via typescript-eslint `projectService`; all three fired on a test file) |
| Go | deadcode, staticcheck | `deadcode ./...` (unreachable funcs from main, includes exported ones); `staticcheck` U1000 (flags unused unexported identifiers only; both run, install with `go install golang.org/x/tools/cmd/deadcode@latest` and `honnef.co/go/tools/cmd/staticcheck@latest`) |
| Java/Kotlin | PMD `UnusedPrivateMethod` (rule exists in the PMD docs, not run here) | |
| C/C++ | compiler `-Wunused` (GCC and Clang); `-Wunreachable-code` is a Clang option and is absent from the GCC warning docs; clang-tidy | |

## Confirming it is dead
1. Static finding says unused.
2. Coverage from the full test suite *and* production coverage/usage (e.g. logs, feature flag evaluation counts, endpoint metrics over 30-90 days) shows zero execution.
3. Search for dynamic use: reflection, `getattr`, string-based routing, DI containers, serializers, public API consumed by other repos.

## Removal
- Delete in a dedicated PR; run full regression.
- For public endpoints or library APIs: deprecate, log usage, remove after the deprecation window.
- Remove the tests that only exercised dead code.

## Unreachable conditions as defects
A branch the type checker or analyzer proves impossible (`if x is None` after a non-optional assignment) often means the author expected a case that cannot happen, or the real check is missing elsewhere. Investigate before deleting.

## Gotchas
- Framework entry points (Django views, pytest fixtures, Spring beans) look unused to static tools; whitelist them.
- Low-confidence vulture results have many false positives, but the confidence filter also removes real unused functions (60%); review the 60% list once, whitelist the framework entry points, then gate on the cleaned list.

## Verify
The dead-code tool runs in CI with an allowlist, and new unused exports/files fail the build.
