---
id: computing-software.qa-testing-engineering.jest-pytest.junit5-parameterized-tests
name: junit5-parameterized-tests
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [parameterizedtest, junit5, valuesource, csvsource, methodsource, data-driven-testing]
level: practitioner
status: docs-checked
description: "Write JUnit 5 parameterized tests: ValueSource, CsvSource with text blocks, MethodSource and ArgumentsProvider, EnumSource, null/empty sources, and readable display names."
sources:
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/writing-tests/parameterized-classes-and-tests.adoc
  - https://github.com/junit-team/junit5/blob/main/documentation/modules/ROOT/pages/appendix.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parameterized tests in JUnit 5

Dependency: `org.junit.jupiter:junit-jupiter-params` (pulled in by the `junit-jupiter` aggregator artifact).

## Sources
```java
@ParameterizedTest
@ValueSource(strings = {"", " ", "\t"})
@NullSource                                 // or @NullAndEmptySource
void rejectsBlankNames(String name) {
  assertThrows(ValidationException.class, () -> new Customer(name));
}

@ParameterizedTest(name = "{index}: {0} {1} -> {2}")
@CsvSource(textBlock = """
    amount, currency, expected
    10,     GBP,      £10.00
    0,      GBP,      £0.00
    1234.5, EUR,      '€1,234.50'
    """, useHeadersInDisplayName = true)
void formatsMoney(BigDecimal amount, String currency, String expected) {
  assertEquals(expected, Money.format(amount, currency));
}

@ParameterizedTest
@CsvFileSource(resources = "/pricing-cases.csv", numLinesToSkip = 1)
void pricingRules(String tier, int qty, BigDecimal expected) { ... }

@ParameterizedTest
@EnumSource(value = OrderStatus.class, names = {"CANCELLED", "REFUNDED"}, mode = EnumSource.Mode.EXCLUDE)
void activeStatusesAreBillable(OrderStatus status) { ... }

@ParameterizedTest
@MethodSource("shippingCases")
void shipping(Address address, BigDecimal expected) { ... }
static Stream<Arguments> shippingCases() {
  return Stream.of(
      Arguments.of(Address.uk("SW1A 1AA"), new BigDecimal("4.99")),
      Arguments.of(Address.de("10115"), new BigDecimal("9.99")));
}
```
Arguments that implement `AutoCloseable` are closed automatically after the test. Reusable providers: implement `ArgumentsProvider` and use `@ArgumentsSource(MyProvider.class)`. External class method: `@MethodSource("com.example.Cases#shipping")`.

## Conversion
Implicit conversion from strings to primitives, enums, `BigDecimal`, `LocalDate`, `Duration`, `File`, etc. Custom: `@ConvertWith(MyConverter.class)`; aggregate many columns into an object with `ArgumentsAccessor` or `@AggregateWith`.

## Gotchas
- Quotes in CsvSource: wrap values containing commas in single quotes; empty quoted `''` = empty string, unquoted empty = null.
- MethodSource methods must be static (unless `@TestInstance(PER_CLASS)`).
- Display names with `{0}` keep reports readable; default shows `[1] 10, GBP, £10.00`.

## Verify
Each case shows as a separate entry in the report with a meaningful name, and adding a row needs no new code.

## Checked

Date: 2026-10-25. Documentation release: JUnit 6.1.3 (GitHub main, release of 2026-08-07).

Confirmed: `@CsvSource` `textBlock` and `useHeadersInDisplayName`; quoting rules (`''` is an empty string, unquoted empty is null; whitespace trimmed unless `ignoreLeadingAndTrailingWhitespace = false`); `@NullAndEmptySource`; `ArgumentsAccessor`/`@AggregateWith` aggregators; `@MethodSource` factory methods needing PER_CLASS if non-static; `junit-jupiter` aggregator contents.

Method: documentation only; no commands were run.
