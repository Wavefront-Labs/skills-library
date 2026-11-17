---
id: computing-software.software-engineering.groovy.mocking-stubs
name: mocking-stubs
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, mocking-stubs]
level: advanced
status: docs-checked
description: "Groovy built-in mocking: map and closure coercion, MockFor/StubFor ordering and verify, and the limits that call for Spock."
sources:
  - https://groovy-lang.org/testing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mocks and stubs without a framework
```groovy
// Map coercion: keys are method names, values are closures
def service = [convert: { String key -> 'some text' }] as TranslationService
assert 'some text' == service.convert('key.text')

// MockFor (package groovy.mock.interceptor)
def mock = new MockFor(Person)
mock.demand.getFirst { 'dummy' }
mock.demand.getLast  { 'name' }
mock.use {
    def f = new Family(mother: new Person(first: 'Mary', last: 'Smith'))
    assert f.nameOfMother() == 'dummy name'
}
mock.expect.verify()
```
- `as` also coerces a closure to a single-method type, and implicit SAM coercion applies where the runtime can infer the target type. Groovy creates a proxy, so the object is not a direct instance of the class.
- `MockFor`: expectations are strictly ordered, and use of the mock automatically ends with a `verify`.
- `StubFor`: loosely ordered; its `verify` is sequence independent and optional.
- Both are built with meta-programming, so they cannot test statically compiled classes: Java classes or Groovy `@CompileStatic` classes. Use Spock or a Java mocking library for those.

## Gotchas
- Map coercion with custom `java.util.Map` descendants can misbehave because the mechanism targets certain collection classes.
- Mock and stub expectations apply only inside the `use` closure.

## Self-check
Run the snippet; remove one `demand` and confirm the test fails.

## Checked
Read the Groovy testing guide sections on map coercion, closure coercion, MockFor and StubFor. Removed: the `mock.demand.call` example, the claim that MockFor only intercepts calls from Groovy code, and the "fails at use end" detail beyond the documented automatic verify.

Method: docs-checked 2026-11-09 against the Groovy testing guide (groovy-lang.org/testing.html).
