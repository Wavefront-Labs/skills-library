---
id: computing-software.software-engineering.kotlin.kt-ktlint-detekt
name: kt-ktlint-detekt
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-tooling, ktlint-detekt]
level: practitioner
status: docs-checked
description: "Enforce Kotlin style with ktlint formatting and detekt static analysis with a baseline in CI."
sources: ["https://github.com/pinterest/ktlint", "https://detekt.dev/docs/gettingstarted/gradle/", "https://detekt.dev/docs/introduction/baseline/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linting with ktlint and detekt
- ktlint formats with `ktlint -F` and reads its code style from `.editorconfig` through the `ktlint_code_style` property (values include `intellij_idea`, `android_studio` and `ktlint_official`).
- detekt's Gradle plugin provides the `detekt` task and `detektBaseline`, which creates a baseline of existing findings so a project can adopt rules gradually.
- Run both in CI; let formatting be automatic and review detekt findings.
Verify: introduce a deliberate violation and confirm CI fails.

## Checked
2026-11-03. Confirmed on the ktlint docs (CLI install and code-styles pages, from the project repo) and the detekt Gradle and baseline pages: `ktlint -F`, `ktlint_code_style`, detektBaseline.
Removed: detekt rule-set names (complexity, style, coroutines) and the Kotlin Coding Conventions/Android style mapping (not confirmed).
Method: documentation only; no commands were run.
