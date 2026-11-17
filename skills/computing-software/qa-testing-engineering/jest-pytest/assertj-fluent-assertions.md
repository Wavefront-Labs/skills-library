---
id: computing-software.qa-testing-engineering.jest-pytest.assertj-fluent-assertions
name: assertj-fluent-assertions
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [assertj, fluent-assertions, java-testing, junit5, soft-assertions]
level: practitioner
status: docs-checked
description: "Write readable Java assertions with AssertJ: fluent chains, collection extracting and tuple checks, recursive comparison, exception assertions, and soft assertions."
sources:
  - https://assertj.github.io/doc/
  - https://github.com/assertj/assertj/blob/main/assertj-core/src/main/java/org/assertj/core/api/Assertions.java
  - https://github.com/assertj/assertj/blob/main/assertj-core/src/main/java/org/assertj/core/api/SoftAssertions.java
  - https://github.com/assertj/assertj/blob/main/assertj-core/src/main/java/org/assertj/core/api/junit/jupiter/SoftAssertionsExtension.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluent assertions with AssertJ

`import static org.assertj.core.api.Assertions.*;`

## Basics
```java
assertThat(order.status()).isEqualTo(PAID);
assertThat(order.total()).isEqualByComparingTo("36.00");           // BigDecimal ignoring scale
assertThat(name).isNotBlank().startsWith("Ada").hasSizeLessThan(50);
assertThat(eta).isBetween(LocalDate.of(2026, 10, 17), LocalDate.of(2026, 10, 20));
assertThat(ratio).isCloseTo(0.33, within(0.01));
```
`as("description")` before the assertion labels failures: `assertThat(x).as("VAT for %s", country).isEqualTo(...)`.

## Collections
```java
assertThat(orders).hasSize(3)
    .extracting(Order::sku, Order::qty)
    .containsExactlyInAnyOrder(tuple("SKU-1", 2), tuple("SKU-2", 1), tuple("SKU-3", 5));
assertThat(orders).filteredOn(o -> o.status() == PAID).extracting("id").containsOnly(1L, 3L);
assertThat(orders).allSatisfy(o -> assertThat(o.total()).isPositive());
assertThat(prices).isSortedAccordingTo(Comparator.naturalOrder());
assertThat(map).containsEntry("GBP", 1.0).doesNotContainKey("XXX");
```

## Objects
```java
assertThat(actualOrder)
    .usingRecursiveComparison()
    .ignoringFields("id", "createdAt")
    .withComparatorForType(BigDecimal::compareTo, BigDecimal.class)
    .isEqualTo(expectedOrder);
```
Compares field by field without needing `equals`.

## Exceptions
```java
assertThatThrownBy(() -> basket.apply("EXPIRED"))
    .isInstanceOf(InvalidCodeException.class)
    .hasMessageContaining("expired")
    .hasNoCause();
assertThatExceptionOfType(IllegalArgumentException.class).isThrownBy(() -> new Qty(-1));
assertThatNoException().isThrownBy(() -> basket.apply("SAVE10"));
```

## Soft assertions
```java
SoftAssertions.assertSoftly(s -> {
  s.assertThat(order.status()).isEqualTo(PAID);
  s.assertThat(order.total()).isEqualByComparingTo("36.00");
  s.assertThat(order.items()).hasSize(2);
});
```
JUnit 5: `@ExtendWith(SoftAssertionsExtension.class)` injects a `SoftAssertions` parameter into test methods, or (since AssertJ 3.18.0) into fields annotated `@InjectSoftAssertions`.

## Gotchas
- `assertThat(x)` without a terminal assertion does nothing; use a static analysis rule that flags an ignored `assertThat` result.
- `isEqualTo` on BigDecimal is scale-sensitive (`36.0` != `36.00`); use `isEqualByComparingTo`.

## Verify
Failure messages show expected vs actual with labels, and collection assertions check content, not just size.

## Checked

Date: 2026-10-25. Documentation release: AssertJ core 3.27.x (GitHub main sources, last commit 2026-10-24).

Confirmed: every assertion and factory method used in the examples exists in the sources (`assertThatThrownBy`, `assertThatExceptionOfType().isThrownBy`, `assertThatNoException`, `extracting`, `tuple`, `filteredOn`, `allSatisfy`, `isSortedAccordingTo`, `usingRecursiveComparison().ignoringFields().withComparatorForType()`, `isEqualByComparingTo`, `isCloseTo` with `within`, `assertSoftly`); `SoftAssertionsExtension` and `@InjectSoftAssertions` (since 3.18.0).

Removed as unconfirmed: the Error Prone and SonarLint product names.

Method: documentation only; no commands were run.
