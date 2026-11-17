---
id: computing-software.software-engineering.groovy.spock-spec-structure
name: spock-spec-structure
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, spock-spec-structure, groovy-spock]
level: practitioner
status: docs-checked
description: "Spock specs: feature methods, given/when/then/expect/cleanup blocks, implicit conditions, fixture methods and @Shared fields."
sources:
  - https://raw.githubusercontent.com/spockframework/spock/master/docs/spock_primer.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spock specification structure
```groovy
import spock.lang.Specification
class StackSpec extends Specification {
  def "pop returns last pushed"() {
    given: def s = new Stack<Integer>()
    when:  s.push(1); s.push(2)
    then:  s.pop() == 2
           s.size() == 1
  }
  def "empty pop throws"() {
    when: new Stack<Integer>().pop()
    then: thrown(EmptyStackException)
  }
}
```
- Blocks: `given` (alias `setup`, which was the original name; `given:` is optional and statements before the first explicit block form an implicit `given` block), `when`, `then`, `expect`, `cleanup`, `where`.
- Top-level expressions in `then` and `expect` are implicit conditions (no `assert`), except calls to `void` methods and interactions.
- Fixture methods: `setup()`, `cleanup()`, `setupSpec()`, `cleanupSpec()`; share state across features with `@Shared` fields.
- `thrown(Type)` in `then:` checks the exception from `when:`.

## Gotchas
- Conditions inside helper methods need an explicit `assert`, or wrap them in `with(...)` / `verifyAll`.

## Self-check
Run the spec with your build tool and confirm both features pass.

## Checked
Method: docs-checked 2026-11-09 against the Spock docs source spock_primer.adoc (raw GitHub). Dropped the Spock/Groovy artifact-naming claim and the Gradle command as unconfirmed.
