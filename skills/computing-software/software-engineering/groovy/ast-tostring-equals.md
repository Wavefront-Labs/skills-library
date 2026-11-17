---
id: computing-software.software-engineering.groovy.ast-tostring-equals
name: ast-tostring-equals
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, ast-tostring-equals, groovy-ast-annotations]
level: practitioner
status: docs-checked
description: "Boilerplate generation with @ToString, @EqualsAndHashCode, @TupleConstructor, @Canonical and @Sortable."
sources:
  - https://groovy-lang.org/metaprogramming.html
  - https://docs.groovy-lang.org/latest/html/gapi/
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-metaprogramming.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ToString, EqualsAndHashCode, TupleConstructor, Canonical
```groovy
import groovy.transform.*
@ToString(includeNames = true) @EqualsAndHashCode @TupleConstructor
class P { String name; int age }
assert new P('a', 1) == new P('a', 1)
assert new P('a', 1).toString() == 'P(name:a, age:1)'
```
- Options: `excludes`, `includes`, `includeFields`, `callSuper`.
- `@Canonical` is a meta-annotation combining ToString, EqualsAndHashCode and TupleConstructor.
- `@Sortable` generates Comparable and comparators; `@Memoized` caches method results.
- `@MapConstructor` generates a Map-based constructor.

## Gotchas
- `callSuper` defaults to false, so super properties are left out of equals/hashCode unless you set `callSuper = true`.
- Annotated transformations run at compile time: groovyc output differs from the source.

## Checked

2026-11-02. Confirmed against the Metaprogramming chapter (`@ToString`, `@EqualsAndHashCode`, `@TupleConstructor`, `@Canonical`, `@MapConstructor`, `@Sortable`, `@Memoized` option tables). Removed: the unconfirmed deprecation and `@RecordType` claim.

Method: documentation only; no commands were run.

## Self-check
Run the snippet.
