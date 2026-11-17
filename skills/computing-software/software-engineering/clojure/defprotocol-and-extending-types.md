---
id: computing-software.software-engineering.clojure.defprotocol-and-extending-types
name: defprotocol-and-extending-types
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, protocols, defprotocol, extend-type, extend-protocol, extend-via-metadata, polymorphism, satisfies, protocols-extend, clojure-protocols-datatypes]
level: practitioner
status: docs-checked
description: "Define protocols and extend them to existing types with extend-type, extend-protocol or :extend-via-metadata; know dispatch on first argument and reload pitfalls."
sources: ["https://clojure.org/reference/protocols"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# defprotocol and extension

**Goal:** get fast single-dispatch polymorphism on the type of the first argument.

```clojure
(defprotocol Shape
  (area [this] "Area in square units")
  (scale [this k]))

(extend-protocol Shape
  String   (area [s] (count s)) (scale [s k] (apply str (repeat k s)))
  nil      (area [_] 0)         (scale [_ _] nil)
  Object   (area [_] -1)        (scale [x _] x))

(defprotocol Cloneable :extend-via-metadata true (dup [x]))   ; 1.10+: impls may ride on a value's metadata
```
- Methods dispatch on the class of the first argument only; for multiple-argument or value dispatch use
  multimethods.
- `extend-type` extends one type to many protocols; `extend-protocol` one protocol to many types.
- Protocols generate a Java interface; classes created with `deftype`/`defrecord`/`reify` can implement them inline
  (faster, but require the type be defined after the protocol).
- `satisfies?`, `extends?` and `extenders` are the reflective queries on protocols.
- `:extend-via-metadata true` in `defprotocol` (Clojure 1.10+) lets a value's metadata supply implementations.

## Failure modes
- `No implementation of method: :area of protocol: #'ns/Shape found for class: ...`.
- Redefining a protocol creates a new protocol; re-evaluate the types that implement it inline.

## Self-check
Call each method on a String, nil and a keyword and predict which branch answers.

## Checked
2026-11-02. Confirmed: clojure.org/reference/protocols: defprotocol, extend-protocol, extend-type, dispatch on the first argument's type, inline implementation in deftype/defrecord/reify, :extend-via-metadata, satisfies?/extends?/extenders. Removed: the performance claim about satisfies? and the :refer aliasing remark (not in the page).
Method: documentation only; no commands were run.
