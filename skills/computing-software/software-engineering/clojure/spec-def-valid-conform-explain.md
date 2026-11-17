---
id: computing-software.software-engineering.clojure.spec-def-valid-conform-explain
name: spec-def-valid-conform-explain
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, clojure.spec, spec, s-def, valid, conform, explain, predicates, s-and, s-or, s-keys, spec-basics-predicates, clojure-spec]
level: practitioner
status: docs-checked
description: "Define specs with s/def, validate with s/valid? and s/conform, read s/explain output, and compose predicates with s/and, s/or, s/coll-of, s/map-of and s/keys."
sources: ["https://clojure.org/guides/spec", "https://clojure.org/about/spec"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# clojure.spec basics

**Goal:** describe and validate data shapes.

Setup: `(require '[clojure.spec.alpha :as s])`. The guide says to declare a dependency on Clojure 1.9.0 or higher.

```clojure
(s/def ::age (s/and int? #(<= 0 % 150)))
(s/valid? ::age 30)                          ;=> true
(s/conform ::age "x")                        ;=> :clojure.spec.alpha/invalid
(s/explain ::age -1)                         ; prints the failing predicate and value
(s/explain-data ::age -1)                    ; data version for programs

(s/def :user/name string?)
(s/def :user/email (s/and string? #(re-matches #".+@.+" %)))
(s/def ::user (s/keys :req [:user/name] :opt [:user/email]))   ; :req-un for unqualified keys
(s/def ::ids (s/coll-of int? :kind vector? :min-count 1))
(s/def ::m (s/map-of keyword? int?))
(s/def ::t (s/or :num number? :str string?))     ; conform returns [:num 1]
(s/def ::status #{:open :closed})                ; sets are predicates
```
- `s/keys` validates every present qualified key that has a registered spec, even ones not listed; that is the
  point of "global" key specs.
- `s/and` conforms left to right, passing conformed values on.
- Keep spec registry names namespaced; use `::` in a dedicated namespace per domain.
- `s/nilable`, `s/merge`, `s/multi-spec`, `s/tuple` cover common needs; regex ops: `s/cat`, `s/*`, `s/+`, `s/?`, `s/alt`.
- `s/coll-of` and `s/map-of` conform every element, so for large collections the guide suggests `s/every` (`s/every-kv` for maps).
- `s/map-of` validates but does not conform keys unless you pass `:conform-keys true`.

## Failure modes
- `s/keys` checks every registered key present in the map, not only the ones listed in `:req`/`:opt`, so a bad value under an unlisted key still fails.
- `s/valid?` returns false for invalid but `s/conform` returns the special `::s/invalid`.

## Self-check
Define a `::user` spec and print `(s/explain-str ::user {})`; confirm it names the missing key.

## Checked
2026-11-03. Confirmed against the clojure.org spec guide: s/def registry, conform and `:clojure.spec.alpha/invalid`, valid?, explain, explain-str, explain-data, s/keys (:req, :opt, :req-un, all registered keys checked), s/and passing conformed values, s/or, s/nilable, s/merge, s/multi-spec, s/coll-of (:kind, :min-count), s/map-of, s/tuple, regex ops, Clojure 1.9.0 requirement. Removed: the `org.clojure/spec.alpha` artifact remark and the `Unable to resolve spec` message (not in the pages read).
Method: documentation only; no commands were run.
