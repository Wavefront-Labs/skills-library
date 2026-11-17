---
id: computing-software.software-engineering.kotlin.kt-safe-call
name: kt-safe-call
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-null-safety, safe-call]
level: intro
status: docs-checked
description: "Handle nullable values with ?., ?:, !! and let, and know when each hides a bug."
sources: ["https://kotlinlang.org/docs/null-safety.html", "https://kotlinlang.org/docs/typecasts.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe calls, elvis and not-null assertion
- `a?.b` yields null if `a` is null; `a ?: default` supplies a fallback; `a!!` throws NullPointerException. The documented causes of an NPE in Kotlin are an explicit `throw NullPointerException()`, `!!`, and data inconsistency during initialization (plus Java interop).
- `x?.let { use(it) }` runs a block only when non-null.
- `!!` is acceptable only after a check the compiler cannot see; each use is a documented assumption.
- `as?` returns null on failed cast, `as` throws ClassCastException.
Verify: compile with a nullable input and confirm no `!!` remains in production paths (`grep -n '!!'`).

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (null-safety.html, typecasts.html): ?., ?:, !!, let, as?, as and the listed NPE causes. Removed as not stated there: the `?: return` example and the advice against chaining `?.let` for if/else (not on the page).

Method: documentation only; no commands were run.
