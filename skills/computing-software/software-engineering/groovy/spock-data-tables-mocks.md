---
id: computing-software.software-engineering.groovy.spock-data-tables-mocks
name: spock-data-tables-mocks
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, spock-data-tables-mocks]
level: advanced
status: docs-checked
description: "Spock where: blocks for data-driven tests and Mock/Stub/Spy interactions with cardinality."
sources:
  - https://raw.githubusercontent.com/spockframework/spock/master/docs/data_driven_testing.adoc
  - https://raw.githubusercontent.com/spockframework/spock/master/docs/interaction_based_testing.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data tables, interactions and mocking
```groovy
def "max of #a and #b is #c"() {
  expect: Math.max(a, b) == c
  where:
  a | b || c
  1 | 3 || 3
  7 | 4 || 7
}
def "notifies once"() {
  given: def sub = Mock(Subscriber)
  when:  new Pub(sub).fire('e')
  then:  1 * sub.receive('e')
}
```
- `where:` accepts tables (a double pipe `||` visually separates inputs from expected outputs) and data pipes (`a << [1, 2]`). `#name` tokens in the feature name are replaced per iteration; `#featureName` and `#iterationIndex` are also supported.
- Iterations are unrolled by default (Spock 2); `@Rollup` or `unroll { unrollByDefault false }` in the config restores rolled-up reporting.
- Stubs return canned values and ignore call counts: `sub.receive(_) >> "ok"`; `>>>` gives a sequence, `>> { args -> ... }` computes a response. `Spy(...)` wraps a real object (`Spy(constructorArgs: [...])`; use `callRealMethod()` in a closure to delegate).
- Interaction forms: `0 * _`, `(1.._) * sub.method(_)`, `1 * sub.m(!null)`.
- Mock a method and stub it in the same interaction: `1 * sub.receive("m") >> "ok"`. Splitting mocking and stubbing into two statements does not work.

## Gotchas
- Mocking classes needs a class-mocking library (the docs name ByteBuddy and cglib); some spies also need Objenesis.
- Interactions declared in a `then:` block are matched before any others and apply to the preceding `when:`.

## Self-check
Run the spec and check the report lists one iteration per table row.

## Checked
Method: docs-checked 2026-11-09 against the Spock docs sources data_driven_testing.adoc and interaction_based_testing.adoc (raw GitHub). Dropped the claim that `Stub()` specifically needs property syntax (`stub.name >> 'x'`) as unconfirmed.
