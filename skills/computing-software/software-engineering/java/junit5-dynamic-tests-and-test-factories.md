---
id: computing-software.software-engineering.java.junit5-dynamic-tests-and-test-factories
name: junit5-dynamic-tests-and-test-factories
category: computing-software
field: software-engineering
product: java
tags: [java, junit5, dynamic-tests, testfactory, dynamictest, data-driven-tests, junit-jupiter]
level: practitioner
status: docs-checked
description: "Generate tests at run time with JUnit 5 @TestFactory and DynamicTest from files or tables; know the lifecycle limits."
sources: ["https://junit.org/junit5/docs/current/user-guide/#writing-tests-dynamic-tests"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JUnit 5 dynamic tests and @TestFactory

## When
Use `@TestFactory` when test cases are discovered at run time (files in a directory, rows of a spec, contract tests per implementation) or need individual names and structure. For a fixed table of arguments, `@ParameterizedTest` is simpler (see `junit5-parameterized-and-nested-tests`).

## Basic
```java
@TestFactory
Stream<DynamicTest> parsesAllFixtures() throws IOException {
    return Files.list(Path.of("src/test/resources/fixtures")).sorted()
        .map(p -> DynamicTest.dynamicTest("parse " + p.getFileName(),
                  () -> assertDoesNotThrow(() -> Parser.parse(Files.readString(p)))));
}
```
A `@TestFactory` method is a factory for test cases, not a test itself. It must return a single `DynamicNode` or a "stream" of them: `Stream`, `Collection`, `Iterator`, `Iterable`, or an array. `DynamicContainer` (a display name plus child nodes) lets you build nested hierarchies; `DynamicTest` is a display name plus an `Executable`, which can be a lambda or method reference. Dynamic tests execute lazily, enabling non-deterministic generation. Any `Stream` returned is closed by JUnit via `stream.close()`, so resources such as `Files.lines()` or `Files.list()` are safe to return directly. Like `@Test`, a `@TestFactory` method must not be `private` or `static` and may declare parameters resolved by `ParameterResolver`s.

## Lifecycle - the key difference
There are no lifecycle callbacks for individual dynamic tests. `@BeforeEach` and `@AfterEach` methods (and their extension callbacks) run for the `@TestFactory` method as a whole, not for each dynamic test, so fields on the test instance are not reset between dynamic tests from the same factory. Put per-case setup inside each lambda.

## Rules
- Make each display name unique and descriptive: it identifies a failing case.
- Do not generate thousands of cases from unseeded random data; log the seed.

## Verify
Add a new fixture file and confirm a new test entry appears in the report without code changes; break the fixture and see only that case fail.

## Checked

Method: docs-checked 2026-11-09 against the JUnit 5 user guide Dynamic Tests page (factory return types, DynamicNode and DynamicContainer, lazy execution, stream closing, lifecycle warning). The DynamicTest API page was not read; dropped the testSourceUri overload, IDE filtering, XML reporting and Assumptions claims.
