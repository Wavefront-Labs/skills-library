---
id: computing-software.software-engineering.groovy.list-gdk-ops
name: list-gdk-ops
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, list-gdk-ops]
level: practitioner
status: docs-checked
description: "Core GDK collection methods in DefaultGroovyMethods: collect, findAll, inject, groupBy, sort with the mutate flag, collate, withIndex, unique and flatten."
sources:
  - https://github.com/apache/groovy/blob/master/src/main/java/org/codehaus/groovy/runtime/DefaultGroovyMethods.java
  - https://groovy-lang.org/groovy-dev-kit.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# List GDK operations
These methods come from `DefaultGroovyMethods` and work on lists and other collections:
- `collect`, `findAll`, `inject`, `groupBy`, `collate`, `withIndex`, `eachWithIndex` and `unique` are all defined there.
- `flatten` and `inject` appear in the Groovy Development Kit page's collection section.
- `sort` has an overload `sort(Iterable, boolean mutate)`: the boolean says whether the original list is sorted in place. Passing `false` leaves the original untouched and returns a sorted copy.
- `sort(Iterable)` with no flag sorts a `List` in place and returns it; other collections are copied into a new list first.

## Checked

2026-11-03. Confirmed against the `DefaultGroovyMethods` source (signatures of `sort`, `groupBy`, `collate`, `inject`, `withIndex`, `eachWithIndex`, `unique`) and the Groovy Development Kit page. Removed: code snippets with asserted results, the spread-operator null-safety note, and the list of other methods not found as signatures.

Method: documentation only; no commands were run.
