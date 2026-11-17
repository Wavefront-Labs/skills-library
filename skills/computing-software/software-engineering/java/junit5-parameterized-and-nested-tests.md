---
id: computing-software.software-engineering.java.junit5-parameterized-and-nested-tests
name: junit5-parameterized-and-nested-tests
category: computing-software
field: software-engineering
product: java
tags: [java, java-testing, junit5, parameterized-tests, nested-tests, junit-jupiter, extensions]
level: practitioner
status: docs-checked
description: "Write expressive JUnit 5 tests: parameterized sources, @Nested structure, display names, lifecycle, extensions, tags and parallel execution."
sources:
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/parameterized-classes-and-tests.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/nested-tests.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/parallel-execution.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/migrating-from-junit4.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JUnit 5 parameterized and nested tests

**Goal:** compact, readable test suites that cover input variations without copy-paste.

## 1. Parameterized tests
```java
@ParameterizedTest(name = "{0} -> {1}")
@CsvSource({
    "'',          false",
    "a@b.co,      true",
    "no-at-sign,  false",
})
void validatesEmail(String input, boolean expected) {
    assertEquals(expected, EmailValidator.isValid(input));
}

@ParameterizedTest
@MethodSource("orders")
void totals(Order order, BigDecimal expected) { assertEquals(expected, order.total()); }
static Stream<Arguments> orders() {
    return Stream.of(arguments(order(line(2, "5.00")), new BigDecimal("10.00")));
}

@ParameterizedTest
@EnumSource(value = Status.class, names = {"CANCELLED", "REFUNDED"})
void terminalStates(Status s) { assertTrue(s.isTerminal()); }

@ParameterizedTest @NullAndEmptySource @ValueSource(strings = {" ", "\t"})
void rejectsBlank(String s) { ... }
```
Requires `junit-jupiter-params` (included in the `junit-jupiter` aggregate).

## 2. Nested structure
```java
@DisplayName("Shopping cart")
class CartTest {
    Cart cart = new Cart();
    @Nested class WhenEmpty {
        @Test void totalIsZero() { assertEquals(ZERO, cart.total()); }
    }
    @Nested class WithOneItem {
        @BeforeEach void add() { cart.add(item("book", "12.00")); }
        @Test void totalIsItemPrice() { ... }
        @Nested class AfterDiscount { ... }
    }
}
```
Outer `@BeforeEach` runs before inner ones. Only non-static inner classes can be `@Nested`.

## 3. Lifecycle and extensions
- A new instance per test method by default; `@TestInstance(PER_CLASS)` allows non-static `@BeforeAll`.
- Extensions replace JUnit 4 runners/rules: `@ExtendWith(MockitoExtension.class)`, `@TempDir Path dir`, `@Timeout(2)`, Spring's `@SpringBootTest` (includes the extension).
- `assertAll(...)` reports every failed assertion in a group; `assertThrows` returns the exception for further checks.

## 4. Tags and selection
```java
@Tag("slow") @Test void bigImport() { }
```
Maven surefire `<groups>`/`<excludedGroups>`, Gradle `useJUnitPlatform { excludeTags("slow") }`.

## 5. Parallel execution
```properties
# src/test/resources/junit-platform.properties
junit.jupiter.execution.parallel.enabled=true
junit.jupiter.execution.parallel.mode.default=concurrent
junit.jupiter.execution.parallel.mode.classes.default=concurrent
```
Guard shared resources with `@ResourceLock("db")` or `@Isolated`.

## Gotchas
- JUnit 4 tests (`org.junit.Test`) only run on the JUnit Platform when `junit-vintage-engine` is on the test runtime path; the Vintage engine is deprecated, so migrate the tests.
- `@CsvSource` trims leading and trailing whitespace outside quotes and treats unquoted empty values as null; write `''` for an empty string.
- Test method order is deterministic but not obvious; tests must not depend on it (`@TestMethodOrder` only for genuine scenarios).

## Verify
- The test report lists each parameter combination by display name, and `mvn -Dgroups=slow test` runs only tagged tests.

## Checked

Date: 2026-10-25. Documentation release: JUnit 6.1.3 (GitHub main, release of 2026-08-07) and Surefire 3.6.0.

Confirmed: CSV quoting and trimming rules; `@NullAndEmptySource`, `@EnumSource`, `@MethodSource`; nested class rules; `assertAll` and `assertThrows` (returns the exception) in `Assertions` source; Vintage engine requirement and deprecation; parallel properties; `-Dgroups` with Surefire.

Method: documentation only; no commands were run.
