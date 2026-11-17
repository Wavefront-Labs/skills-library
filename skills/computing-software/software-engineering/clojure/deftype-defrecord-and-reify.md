---
id: computing-software.software-engineering.clojure.deftype-defrecord-and-reify
name: deftype-defrecord-and-reify
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, defrecord, deftype, reify, records, positional-constructor, map-constructor, interfaces, proxy, deftype-defrecord-reify]
level: practitioner
status: docs-checked
description: "Choose among defrecord, deftype, reify and proxy; use ->Rec and map->Rec constructors, inline protocol and interface implementation, and know record map semantics."
sources: ["https://clojure.org/reference/datatypes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# defrecord, deftype, reify

**Goal:** model domain entities and implement interfaces with the right construct.

```clojure
(defrecord Point [x y]
  Shape
  (area [_] 0))

(->Point 1 2)                    ; positional constructor
(map->Point {:x 1 :y 2 :z 3})    ; map constructor; extra keys kept in the ext map
(:x (assoc (->Point 1 2) :y 5))  ; records behave like maps
(deftype Counter [^:unsynchronized-mutable n]
  clojure.lang.IDeref (deref [_] n))
(reify Object (toString [_] "anon"))   ; anonymous, closes over locals
```
- Use plain maps first; records pay off for protocol dispatch speed, fixed field type hints and named constructors.
- Records: map interface, equality by type and fields, `dissoc` of a field returns a plain map.
- `deftype`: no map behaviour; supports mutable fields (`^:unsynchronized-mutable`, `^:volatile-mutable`) that are
  private to the type's methods.
- `reify` creates one-off implementations of protocols and interfaces (not abstract classes); `proxy` can extend
  classes but is slower.
- Fields hint primitives: `(defrecord P [^long x ^long y])`.

## Failure modes
- Records are compared by type: `(= (->Point 1 2) {:x 1 :y 2})` is false.
- `->Point` wrong arg count throws ArityException; `map->Point` ignores missing fields (nil).

## Self-check
`(= (->Point 1 2) (map->Point {:x 1 :y 2}))` is true, and `(dissoc (->Point 1 2) :x)` is not a Point.

## Checked
2026-11-02. Confirmed: clojure.org/reference/datatypes: defrecord (map interface, extensible fields, value equality, positional and map constructors), deftype (mutable fields only on deftype), reify, primitive field hints. Removed: the class-reload remark.
Method: documentation only; no commands were run.
