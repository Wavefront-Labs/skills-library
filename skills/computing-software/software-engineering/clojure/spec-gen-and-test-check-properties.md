---
id: computing-software.software-engineering.clojure.spec-gen-and-test-check-properties
name: spec-gen-and-test-check-properties
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, spec, generators, test-check, gen, properties, defspec, for-all, s-gen, with-gen, exercise, shrinking, spec-generators]
level: advanced
status: docs-checked
description: "Generate data from specs with s/gen and s/exercise, override with s/with-gen, and write property tests with clojure.test.check for-all and defspec."
sources: ["https://clojure.org/guides/spec", "https://github.com/clojure/test.check/blob/master/doc/intro.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spec generators and test.check

**Goal:** property-based testing driven by specs.

```clojure
(require '[clojure.spec.gen.alpha :as gen]
         '[clojure.test.check.generators :as tgen]
         '[clojure.test.check.properties :as prop]
         '[clojure.test.check.clojure-test :refer [defspec]])
(gen/sample (s/gen ::user) 3)
(s/exercise ::age 5)                                    ; [[val conformed] ...]
(s/def ::my-kw (s/with-gen (s/and keyword? #(= (namespace %) "my.domain"))
                 #(gen/fmap (fn [s] (keyword "my.domain" s))
                            (gen/such-that not-empty (gen/string-alphanumeric)))))

(defspec sort-idempotent 100
  (prop/for-all [v (tgen/vector tgen/small-integer)]
    (= (sort v) (sort (sort v)))))
```
- In `s/and` the first predicate determines the generator and later ones filter via `such-that`; a filter that is rarely satisfied (e.g. strings containing "hello") fails with "Couldn't satisfy such-that predicate after 100 tries". Supply a generator with `s/with-gen`, which takes a no-arg function returning the generator.
- test.check shrinks failures to a minimal case; the result map shows `:seed`, and the `:shrunk` map holds `:smallest`.
- Fix the root cause shown in `:smallest`, not the original large failing input.
- Spec generators need `org.clojure/test.check` as a dev/test dependency, not a runtime one.
- Use `gen/recursive-gen` (a compound generator plus a scalar generator) for recursive structures, `gen/one-of` to mix generators and `gen/frequency` to weight them, e.g. `(gen/frequency [[9 gen/small-integer] [1 (gen/return nil)]])`.

## Failure modes
- Generators too weak to reach interesting states; add targeted generators.
- Tests that are non-deterministic from side effects.

## Self-check
Write a property that deliberately fails and confirm shrinking prints a tiny counterexample.

## Checked
2026-11-03. Confirmed against the clojure.org spec guide (gen/sample, s/gen, s/exercise returning generated and conformed pairs, s/with-gen with a no-arg fn, gen/fmap, such-that 100-try failure, test.check dev dependency) and the test.check intro, cheatsheet and generator-examples docs (prop/for-all, gen/vector, gen/small-integer, defspec, :seed, :shrunk, :smallest, gen/recursive-gen, gen/one-of, gen/frequency). Removed: the claim that the seed can be replayed with `:seed` (not stated).
Method: documentation only; no commands were run.
