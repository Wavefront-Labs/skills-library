---
id: computing-software.software-engineering.java.fluent-assertions-with-assertj
name: fluent-assertions-with-assertj
category: computing-software
field: software-engineering
product: java
tags: [java, java-testing, assertj, assertions, soft-assertions, recursive-comparison, junit5]
level: practitioner
status: docs-checked
description: "Write readable, diagnosable Java assertions with AssertJ: collections, exceptions, recursive comparison, soft assertions, custom assertions and common misuse."
sources:
  - https://assertj.github.io/doc/
  - https://github.com/assertj/assertj/blob/main/assertj-core/src/main/java/org/assertj/core/api/Assertions.java
  - https://github.com/assertj/assertj/blob/main/assertj-core/src/main/java/org/assertj/core/api/RecursiveComparisonAssert.java
  - https://github.com/assertj/assertj/blob/main/assertj-core/src/main/java/org/assertj/core/api/SoftAssertions.java
  - https://github.com/assertj/assertj/blob/main/assertj-core/src/main/java/org/assertj/core/api/junit/jupiter/InjectSoftAssertions.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluent assertions with AssertJ

**Goal:** assertions that read like specifications and fail with messages that explain the difference.

## 1. Basics
```java
import static org.assertj.core.api.Assertions.*;
assertThat(order.status()).isEqualTo(PAID);
assertThat(total).isEqualByComparingTo("10.00");          // BigDecimal: ignores scale (10.0 vs 10.00)
assertThat(name).isNotBlank().startsWith("Ord").hasSizeLessThan(40);
assertThat(created).isCloseTo(Instant.now(), within(5, ChronoUnit.SECONDS));
assertThat(optional).hasValueSatisfying(o -> assertThat(o.id()).isPositive());
```
Add `.as("order %d status", id)` before the assertion for context in the failure message.

## 2. Collections
```java
assertThat(orders)
    .hasSize(3)
    .extracting(Order::id, Order::status)
    .containsExactlyInAnyOrder(tuple(1L, PAID), tuple(2L, NEW), tuple(3L, PAID));
assertThat(emails).containsOnly("a@x.co", "b@x.co").doesNotHaveDuplicates();
assertThat(lines).filteredOn(l -> l.qty() > 1).hasSize(2);
assertThat(map).containsEntry("currency", "EUR").doesNotContainKey("secret");
assertThat(list).allSatisfy(o -> assertThat(o.total()).isPositive());
```

## 3. Exceptions
```java
assertThatThrownBy(() -> service.pay(order))
    .isInstanceOf(PaymentDeclined.class)
    .hasMessageContaining("insufficient")
    .hasCauseInstanceOf(GatewayException.class);
assertThatNoException().isThrownBy(() -> service.validate(order));
assertThatExceptionOfType(IllegalArgumentException.class).isThrownBy(() -> new Money(-1));
```

## 4. Recursive comparison (DTOs, entities)
```java
assertThat(actual)
    .usingRecursiveComparison()
    .ignoringFields("id", "createdAt")
    .withComparatorForType(BigDecimal::compareTo, BigDecimal.class)
    .isEqualTo(expected);
```
Compares field by field without needing `equals`; the failure lists every differing path.

## 5. Soft assertions
```java
SoftAssertions.assertSoftly(s -> {
    s.assertThat(dto.name()).isEqualTo("Ana");
    s.assertThat(dto.email()).isEqualTo("ana@x.co");
});
```
Reports all failures at once; with JUnit 5 use `@ExtendWith(SoftAssertionsExtension.class)` and a field annotated `@InjectSoftAssertions` (since 3.18.0) or an injected `SoftAssertions` parameter.

## Gotchas
- `assertThat(x)` without a terminal assertion asserts nothing; use a static analysis rule that flags an ignored `assertThat` result.
- `isEqualTo` on BigDecimal compares scale; use `isEqualByComparingTo`.
- `containsExactly` is order-sensitive; `containsExactlyInAnyOrder` is not.
- Mixing JUnit `assertEquals(expected, actual)` with AssertJ style in one codebase confuses readers; pick one.

## Verify
- Make a test fail intentionally and check the message names the field/element that differs, not just "expected true but was false".

## Checked

Date: 2026-10-25. Documentation release: AssertJ core 3.27.x (GitHub main sources, last commit 2026-10-24).

Confirmed: methods used in the examples exist in the sources (`hasValueSatisfying`, `doesNotHaveDuplicates`, `hasCauseInstanceOf`, `containsExactlyInAnyOrder`, `hasSizeLessThan`, `isNotBlank`, recursive comparison configuration, `assertSoftly`); `@InjectSoftAssertions` since 3.18.0.

Removed as unconfirmed: the Error Prone and SpotBugs rule names.

Method: documentation only; no commands were run.
