---
id: computing-software.software-engineering.groovy.multimethods-dispatch
name: multimethods-dispatch
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, multimethods-dispatch]
level: advanced
status: docs-checked
description: "Groovy selects overloads by runtime argument types, not declared types, and how @CompileStatic changes it."
sources:
  - https://groovy-lang.org/objectorientation.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-object-orientation.adoc
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-semantics.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple dispatch
```groovy
void p(Object o) { println 'object' }
void p(String s) { println 'string' }
Object o = 'x'
p(o)     // dynamic Groovy prints 'string' (Java would print 'object')
```
- Dynamic Groovy picks the method from the run-time types of the arguments: first name and argument count (varargs allowed), then the type of each argument.
- Under `@TypeChecked`, flow typing selects methods from inferred argument types (not declared types), which stays close to but is not guaranteed equal to the runtime choice.
- Two variants at exactly the same distance are ambiguous and throw at runtime; a cast selects the method you want.

## Gotchas
- For a primitive argument, a declared parameter type of the same or slightly larger size is preferred.

## Checked

2026-11-02. Confirmed against the Object orientation chapter (Method selection algorithm, ambiguity, casting), the Differences with Java chapter (Multi-methods) and the Semantics chapter (flow typing). Fixed: the original said `@TypeChecked`/`@CompileStatic` use compile-time declared types; the docs say flow typing uses inferred types. Removed: null-argument and closure dispatch claims.

Method: documentation only; no commands were run.

## Self-check
Run the snippet and confirm it prints `string`.
