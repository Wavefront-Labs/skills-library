---
id: computing-software.software-engineering.clojure.calling-java-methods-fields-and-constructors
name: calling-java-methods-fields-and-constructors
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, java-interop, new, dot-form, static-methods, fields, doto, import, bean, memfn, interop-calls-members, clojure-java-interop]
level: practitioner
status: docs-checked
description: "Call Java from Clojure with (Class. args), (.method obj), (Class/staticMethod), (.-field obj), doto and ..; convert collections and use import."
sources: ["https://clojure.org/reference/java_interop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calling Java from Clojure

**Goal:** use any JVM library idiomatically.

```clojure
(import '(java.util ArrayList HashMap) '(java.time Instant))
(def l (ArrayList.))                  ; (new ArrayList)
(.add l "x")                          ; instance method; (. l add "x") is the base form
(Math/abs -3)                         ; static method
Math/PI  Integer/MAX_VALUE            ; static fields
(.-x (java.awt.Point. 1 2))            ; public instance field access (.-field)
(doto (ArrayList.) (.add 1) (.add 2)) ; returns the object after calls
(.. System (getProperties) (get "user.dir"))   ; chain; or use ->: (-> System .getProperties (.get "x"))
(Instant/now)
(map #(.getName ^java.io.File %) files)        ; method names cannot be used as fns directly
(memfn getName)                                 ; or use #(.getName %)
```
- Clojure collections implement java.util interfaces: `(java.util.ArrayList. [1 2 3])` works; use
  `(vec jlist)`, `(into {} jmap)`, `(seq jarray)` to go the other way.
- Arrays: `(make-array Long/TYPE 3)`, `(long-array 3)`, `aget`, `aset`, `aclone`, `into-array`.
- Overloaded methods resolve at compile time with type hints, else at runtime by reflection (slow).
- Varargs Java methods take an array: `(String/format "%s %s" (to-array [a b]))` or use `format`.
- Inner classes use `$`: `java.util.Map$Entry`.

## Failure modes
- A "No matching method" error: the argument count or types do not match any overload (nil without a type hint is a common cause).
- `NullPointerException` calling a method on nil.
- Overload resolution picks different methods for boxed and primitive arguments; hint or coerce arguments (see the Java interop page on type hints).

## Self-check
`(.toUpperCase "abc")` and `(String/valueOf 1)` both work; remove the hint in a hot loop and see reflection warnings.

## Checked
2026-11-02. Confirmed: clojure.org/reference/java_interop: (Class. args), (. obj method), (.-field obj), Class/staticMethod and static fields, doto, .., memfn, make-array/into-array/to-array/aget/aset/aclone/long-array, nested class `Outer$Inner` naming, type hints versus reflection. Removed: the boxing example and exact error text, neither of which the page states.
Method: documentation only; no commands were run.
