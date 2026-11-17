---
id: computing-software.software-engineering.kotlin.kt-kotlin-test
name: kt-kotlin-test
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-testing, kotlin-test]
level: intro
status: docs-checked
description: "Write unit tests with kotlin.test and Gradle useJUnitPlatform."
sources: ["https://kotlinlang.org/docs/gradle-configure-project.html", "https://kotlinlang.org/docs/jvm-test-using-junit.html", "https://kotlinlang.org/docs/coding-conventions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kotlin.test and JUnit
- Add the `kotlin("test")` dependency to the test source set (it brings the platform-specific kotlin-test dependencies) and enable the JUnit platform with `useJUnitPlatform()` in the Gradle `test` task (`useTestNG()` is the alternative).
- In test code only, method names with spaces in backticks are allowed: `` fun `rejects empty name`() ``.
- Use `assertEquals` and `assertFailsWith<T> { }` from kotlin.test.
Verify: run the Gradle `test` task and open the report.

## Checked
2026-11-03. Confirmed on the Gradle configure-project, JUnit testing and coding conventions pages: kotlin("test"), useJUnitPlatform()/useTestNG(), backticked test names; `assertFailsWith` appears in the kotlinx-coroutines-test README.
Removed: JUnit 5 `@ParameterizedTest`/`@MethodSource` and companion `@JvmStatic` advice (not on the pages).
Method: documentation only; no commands were run.
