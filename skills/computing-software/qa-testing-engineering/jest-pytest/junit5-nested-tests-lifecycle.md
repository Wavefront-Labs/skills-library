---
id: computing-software.qa-testing-engineering.jest-pytest.junit5-nested-tests-lifecycle
name: junit5-nested-tests-lifecycle
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [nested-tests, junit5, displayname, test-lifecycle, testinstance]
level: practitioner
status: docs-checked
description: "Organise JUnit 5 tests with @Nested classes, lifecycle hooks (BeforeAll, BeforeEach), TestInstance PER_CLASS, display names and generators for readable reports."
sources:
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/nested-tests.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/test-instance-lifecycle.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/display-names.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/test-execution-order.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested tests, lifecycle and display names (JUnit 5)

## Nested structure
```java
@DisplayName("Basket")
class BasketTest {
  Basket basket;

  @BeforeEach void newBasket() { basket = new Basket(); }

  @Test @DisplayName("is empty when created")
  void emptyOnCreate() { assertTrue(basket.isEmpty()); }

  @Nested @DisplayName("after adding an item")
  class AfterAdding {
    @BeforeEach void addItem() { basket.add(new Item("SKU-1", 2)); }   // runs after outer @BeforeEach

    @Test @DisplayName("is no longer empty")
    void notEmpty() { assertFalse(basket.isEmpty()); }

    @Nested @DisplayName("and applying a 10% code")
    class WithDiscount {
      @BeforeEach void apply() { basket.apply("SAVE10"); }
      @Test void reducesTotal() { assertEquals(new BigDecimal("36.00"), basket.total()); }
    }
  }
}
```
Report reads like a spec: Basket > after adding an item > and applying a 10% code > reducesTotal.

## Lifecycle
- Order: `@BeforeAll` (once) -> per test: outer `@BeforeEach` -> inner `@BeforeEach` -> test -> inner `@AfterEach` -> outer `@AfterEach` -> `@AfterAll`.
- Default: new test instance per test method, so instance fields reset; `@BeforeAll` must be static.
- `@TestInstance(Lifecycle.PER_CLASS)`: one instance per class; non-static `@BeforeAll`, needed for non-static `@MethodSource`; fields are shared, so reset them explicitly. Set globally with `junit.jupiter.testinstance.lifecycle.default=per_class`.
- `@Nested` classes must be non-static inner classes, and they have full lifecycle support including `@BeforeAll` and `@AfterAll` at each level.

## Display names
- `@DisplayName("...")` on class and methods (emoji and spaces allowed).
- Generators: `@DisplayNameGeneration(DisplayNameGenerator.ReplaceUnderscores.class)` turns `adds_item_to_empty_basket` into "adds item to empty basket"; `IndicativeSentences` joins class and method names.

## Ordering
`@TestMethodOrder(MethodOrderer.OrderAnnotation.class)` + `@Order(n)` only for deliberate sequences (e.g. integration workflow); the default method order is deterministic but intentionally non-obvious.

## Gotchas
- Deep nesting (4+ levels) hurts readability; flatten.
- PER_CLASS with mutable fields leaks state between tests.

## Verify
Report shows a readable hierarchy, and each test passes when run alone (`-Dtest=BasketTest$AfterAdding#notEmpty`).

## Checked

Date: 2026-10-25. Documentation release: JUnit 6.1.3 (GitHub main, release of 2026-08-07).

Confirmed: nested class rules and per-level `@BeforeAll`/`@AfterAll`; `junit.jupiter.testinstance.lifecycle.default=per_class`; `ReplaceUnderscores` and `IndicativeSentences` display name generators; `@TestMethodOrder`/`@Order`.

Removed as unconfirmed: the claim that `@BeforeAll` in a `@Nested` class requires PER_CLASS and the 5.10 / Java 16 remark.

Method: documentation only; no commands were run.
