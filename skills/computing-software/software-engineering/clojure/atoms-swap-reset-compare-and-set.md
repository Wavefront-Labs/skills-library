---
id: computing-software.software-engineering.clojure.atoms-swap-reset-compare-and-set
name: atoms-swap-reset-compare-and-set
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, atoms, swap, reset, compare-and-set, add-watch, validator, deref, shared-state, atoms-swap, clojure-state]
level: practitioner
status: docs-checked
description: "Manage independent synchronous state with atoms: swap! with pure functions, reset!, compare-and-set!, validators, watches and retry semantics."
sources: ["https://clojure.org/reference/atoms"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atoms

**Goal:** share simple, uncoordinated state between threads safely.

```clojure
(def counter (atom 0))
(swap! counter inc)                  ; may retry: the fn must be pure (no side effects)
(swap! counter + 10)
(reset! counter 0)
(compare-and-set! counter 0 1)
(swap-vals! counter inc)             ;=> [old new]
(add-watch counter :log (fn [k ref old new] (println old new)))
(set-validator! counter (fn [n] (>= n 0)))
@counter                             ; deref
```
- `swap!` runs `(f current-value & args)` and retries if another thread changed the atom; side effects in `f`
  can run multiple times.
- Use one atom holding a map for related state instead of several atoms that must stay consistent
  (atoms are not coordinated with each other; use refs for that).
- Atoms support validators (`set-validator!`) and watches (`add-watch`, `remove-watch`); the reference says changes to atoms are always free of race conditions.

## Failure modes
- `swap!` with a function that calls `println` or sends HTTP: duplicate effects on contention.
- Forgetting deref: `counter` is an atom object, `@counter` is the value.

## Self-check
Run `(dotimes [_ 1000] (future (swap! counter inc)))`, wait for the futures, and confirm the count is exact.

## Checked

2026-11-02. Checked against clojure.org/reference/atoms: swap! reads, applies the function and retries with compare-and-set! so the function may run several times and must be side-effect free; compare-and-set!, reset!, swap-vals!, reset-vals!, set-validator!, add-watch / remove-watch; atoms are for state that never needs coordination with other state. Removed: the atom constructor options example, the validator-exception and synchronous-watch remarks, and the compute-outside advice (not stated on the page).

Method: documentation only; no commands were run.
