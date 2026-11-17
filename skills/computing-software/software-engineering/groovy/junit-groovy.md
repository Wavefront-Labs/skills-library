---
id: computing-software.software-engineering.groovy.junit-groovy
name: junit-groovy
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, junit-groovy]
level: practitioner
status: docs-checked
description: "Write Groovy tests with JUnit 5 annotations or GroovyTestCase helpers, shouldFail, and run them in Gradle or Maven."
sources:
  - https://groovy-lang.org/testing.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-testing-guide.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JUnit 4/5 tests in Groovy
```groovy
import org.junit.Test
import static groovy.test.GroovyAssert.shouldFail
class MathTest {
  @Test void adds() { assert 1 + 1 == 2 }
  @Test void fails() { def e = shouldFail(ArithmeticException) { 1 / 0 } ; assert e.message }
}
```
- `groovy.test.GroovyAssert.shouldFail`, `assertScript`, `notYetImplemented`.
- `GroovyTestCase` (JUnit 3 style, derives from `junit.framework.TestCase`) adds methods such as `assertScript`, `shouldFail` and `notYetImplemented`; `GroovyAssert` descends from `org.junit.Assert` for JUnit 4 style tests.
- See the Testing guide for the JUnit 3, 4 and 5 sections and build setup.

## Gotchas
- `GroovyAssert.shouldFail` returns the exception itself, while `GroovyTestCase.shouldFail` returns the exception message.

## Checked

2026-11-02. Confirmed against the Testing guide (JUnit 3 `GroovyTestCase`, JUnit 4 `GroovyAssert`, `shouldFail`, `assertScript`, `notYetImplemented`). Changed the snippet import to JUnit 4 `org.junit.Test`. Removed: Gradle `useJUnitPlatform` and coordinates, the division and visibility gotchas.

Method: documentation only; no commands were run.

## Self-check
Run `gradle test` and confirm both tests are reported.
