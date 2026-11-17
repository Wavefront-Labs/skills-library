---
id: computing-software.software-engineering.clojure.hierarchies-derive-and-isa
name: hierarchies-derive-and-isa
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, derive, isa, hierarchy, make-hierarchy, ancestors, descendants, multimethod-hierarchy, hierarchies-derive-isa]
level: advanced
status: docs-checked
description: "Build keyword hierarchies with derive, test with isa?, use make-hierarchy for isolated hierarchies, and pass :hierarchy to defmulti."
sources: ["https://clojure.org/reference/multimethods"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# derive, isa? and hierarchies

**Goal:** model ad-hoc "is-a" relations among keywords/symbols for multimethod dispatch.

```clojure
(derive ::circle ::shape)
(derive ::square ::shape)
(isa? ::circle ::shape)          ;=> true
(ancestors ::circle)  (descendants ::shape)  (parents ::circle)

(def h (-> (make-hierarchy) (derive :a :b)))
(defmulti f identity :hierarchy #'h)     ; use a var so it can change
(defmethod f :b [_] "b-ish")
(f :a)                                   ;=> "b-ish"
```
- Global `derive` requires namespace-qualified keywords or symbols (to avoid collisions); `make-hierarchy`
  hierarchies accept any.
- `isa?` also works on classes (inheritance) and on vectors elementwise for multi-arg dispatch.
- Global hierarchy is mutable state; prefer a private hierarchy for libraries.
- `underive` removes a relation.

## Failure modes
- Cyclic derivation throws.
- A method for `::shape` and another for `::circle` are fine (most specific wins); two unrelated parents
  cause ambiguity: use `prefer-method`.

## Self-check
After `(derive ::a ::b)`, `(isa? ::a ::b)` is true and `(isa? ::b ::a)` is false.

## Checked
2026-11-02. Confirmed: clojure.org/reference/multimethods: derive/underive/isa?/parents/ancestors/descendants, make-hierarchy with :hierarchy #'var, global derive requires namespace-qualified symbols or keywords, prefer-method for ambiguity, isa? on classes and vectors. No removals.
Method: documentation only; no commands were run.
