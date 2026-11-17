---
id: computing-software.web-development.biome.linter-run-rules-naming-and-group-model
name: linter-run-rules-naming-and-group-model
category: computing-software
field: web-development
product: biome
tags: [biome, biome-lint, linter, rules, rule-groups, naming-convention, language-agnostic-rules, nursery, recommended-rules]
level: intro
status: docs-checked
description: "Run biome lint, understand rule naming (use vs no), groups, recommended defaults, nursery rules, and why globs are discouraged on the CLI."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/linter/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Biome's linter statically analyzes code to find and fix common errors and help write better, modern code. It supports multiple languages.

**Run it.** `biome lint` runs on the project root; pass files or directories such as `biome lint ./src ./public`. Warning from the docs: if you pass a glob your shell expands it, **Biome doesn't support globs**, and the result varies by shell (some do not support `**` or `{}` alternation in `biome lint ./src/**/*.test.{js,ts}`). Shell expansion also costs performance and limits the file count. Globs on the CLI are discouraged; use the `includes` configuration.

**Rules.** A rule enforces or denies a style or construct that may cause bugs. Naming convention: `use*` rules enforce or suggest something, `no*` rules deny something. A violation emits a diagnostic, e.g. `noDebugger` denies `debugger` statements. Each rule has a default severity (see the rule docs). Recommended rules vary by language and are enabled with default or no configuration when you run `lint` or `check`. Some rules are language-agnostic, such as `noUselessEscapeInString`, which reports useless escapes in both JavaScript and CSS. Biome ships no formatting rules: the formatter handles those.

**Groups.** Accessibility (a11y), Complexity, Correctness (code guaranteed incorrect or useless), Nursery, Performance, Security, Style (warnings by default, not errors) and Suspicious (likely incorrect or useless). `noDebugger` belongs to `suspicious`.

**Nursery.** New rules still in development. On stable versions they need explicit opt-in because of possible bugs or performance problems even when marked recommended; on nightly builds they are enabled by default. They are promoted to other groups when stable or removed, and are not subject to semantic versioning.

Rules should explain the error, why it triggered (a note) and what to do (a code action or note).

## Checked

2026-11-08. Read the linter index page in full. Unchanged: running lint, the glob warning, use and no naming, groups, nursery behaviour, language-agnostic rules and rule pillars. Removed: the invented Verify step.

Method: documentation only; no commands were run.
