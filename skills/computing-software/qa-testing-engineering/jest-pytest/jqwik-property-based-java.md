---
id: computing-software.qa-testing-engineering.jest-pytest.jqwik-property-based-java
name: jqwik-property-based-java
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [jqwik, property-based-testing-java, arbitraries-java, junit-platform]
level: practitioner
status: docs-checked
description: "Write property-based tests in Java with jqwik on the JUnit Platform: @Property, built-in and custom @Provide arbitraries, constraints, shrinking, seeds and stateful actions."
sources:
  - https://jqwik.net/docs/current/user-guide.html
  - https://github.com/jqwik-team/jqwik/blob/main/documentation/src/docs/include/rerunning-falsified-properties.md
  - https://github.com/jqwik-team/jqwik/blob/main/documentation/src/docs/include/jqwik-configuration.md
  - https://github.com/jqwik-team/jqwik/blob/main/documentation/src/docs/include/stateful-testing.md
  - https://github.com/jqwik-team/jqwik/blob/main/documentation/src/docs/include/how-to-use.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Property-based testing in Java (jqwik)

jqwik is a JUnit Platform engine (runs alongside Jupiter).
```xml
<dependency><groupId>net.jqwik</groupId><artifactId>jqwik</artifactId><version>${jqwik.version}</version><scope>test</scope></dependency>
```

## Properties
```java
class MoneyProperties {
  @Property(tries = 1000)
  void addingIsCommutative(@ForAll @BigRange(min = "-1e9", max = "1e9") BigDecimal a,
                           @ForAll @BigRange(min = "-1e9", max = "1e9") BigDecimal b) {
    assertThat(Money.of(a).plus(Money.of(b))).isEqualTo(Money.of(b).plus(Money.of(a)));
  }

  @Property
  boolean reverseTwiceIsIdentity(@ForAll List<@IntRange(min = 0, max = 100) Integer> xs) {
    return reverse(reverse(xs)).equals(xs);
  }
}
```
Constraint annotations: `@IntRange`, `@StringLength`, `@AlphaChars`, `@NotEmpty`, `@Size`, `@Positive`, `@UniqueElements`.

## Custom arbitraries
```java
@Provide
Arbitrary<Order> orders() {
  return Combinators.combine(
      Arbitraries.strings().alpha().ofLength(8),
      Arbitraries.integers().between(1, 50),
      Arbitraries.of(Currency.NZD, Currency.USD))
    .as(Order::new);
}
@Property void totalNeverNegative(@ForAll("orders") Order o) { assertThat(o.total()).isNotNegative(); }
```
Filtering: `Assume.that(x != 0)` or `.filter(...)` (keep rejection low).

## Failures
jqwik shrinks automatically and reports the `seed`; reproduce with `@Property(seed = "123456789")`. Failed runs are recorded in a database file (`jqwik.database`, default `.jqwik-database`). What happens on the next run is set by `@Property(afterFailure = AfterFailureMode...)` or `jqwik.failures.after.default`: `SAMPLE_FIRST` (the default: retry the previous falsified sample first), `PREVIOUS_SEED`, `SAMPLE_ONLY` or `RANDOM_SEED`.

## Stateful testing
`ActionChain` (see the stateful testing chapter) applies random sequences of actions to a system under test and checks invariants after each step; `ActionSequence` is the older API.

## Gotchas
- Default `tries` is 1000 (`jqwik.tries.default`); slow properties need fewer tries or cheaper setup (`@BeforeProperty` runs once per property, `@BeforeTry` before every try).
- Edge cases (min, max, 0, empty) are mixed in by default (`jqwik.edgecases.default = MIXIN`); `@Property(edgeCases = EdgeCasesMode.FIRST|MIXIN|NONE)` changes it.
- Maven Surefire and Failsafe have native JUnit Platform support from 2.22.0.

## Verify
Break the invariant: jqwik reports a shrunk sample and seed; rerun with the seed reproduces it.

## Checked

Date: 2026-10-25. Documentation release: jqwik 1.10.2 (GitHub main documentation sources, release of 2026-10-10).

Confirmed: default `afterFailure` mode and the configuration keys (`jqwik.database`, `jqwik.tries.default = 1000`, `jqwik.edgecases.default = MIXIN`); `ActionChain`; constraint annotations (`@IntRange`, `@StringLength`, `@AlphaChars`, `@NotEmpty`, `@Size`, `@Positive`, `@UniqueElements`, `@BigRange(String, String)`); `Assume.that`; `Combinators.combine(...).as(...)`; `@BeforeProperty` / `@BeforeTry`; Surefire 2.22.0 JUnit Platform support; coordinates `net.jqwik:jqwik`.

Removed as unconfirmed: the claim that previously failing samples run first by default through `AFTER_FAILURE = PREVIOUS_SEED` (the documented default is `SAMPLE_FIRST`).

Method: documentation only; no commands were run.
