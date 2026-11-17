---
id: computing-software.software-engineering.groovy.delegate-owner-this
name: delegate-owner-this
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, delegate-owner-this, groovy-delegate]
level: advanced
status: docs-checked
description: "Meaning of this, owner and delegate in a closure and the default resolve order."
sources:
  - https://groovy-lang.org/closures.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-closures.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# this, owner and delegate
- `this`: enclosing class (instance or static). `owner`: enclosing object, closure or class. `delegate`: defaults to owner, can be reassigned.
- Method/property lookup order: OWNER_FIRST by default (owner, then delegate).
- Nested closures: owner is the outer closure; `delegate` of inner defaults to that outer closure.
- Set `closure.delegate = obj` before calling.

## Gotchas
- Inside a class, `this` in a closure is the class instance, not the closure.

## Self-check
Print `this`, `owner`, `delegate` inside nested closures to see the chain.

## Checked

2026-11-02. Confirmed against the Closures chapter (this, owner, delegate, delegation strategy; OWNER_FIRST is the default strategy). Removed: the claim about Java APIs that copy or curry closures and `cl.clone()`.

Method: documentation only; no commands were run.
