---
id: computing-software.software-engineering.clojure.proxy-gen-class-and-aot-compilation
name: proxy-gen-class-and-aot-compilation
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, proxy, gen-class, aot, compile, genclass, main-class, implementing-interfaces, uberjar, proxy-genclass-aot]
level: advanced
status: draft
description: "Extend Java classes with proxy, generate named classes with gen-class (:main true), and understand AOT compilation, *compile-path* and direct linking."
sources: ["https://clojure.org/reference/compilation", "https://clojure.org/reference/java_interop"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# proxy, gen-class, AOT

**Goal:** produce Java-callable classes and entry points.

```clojure
(proxy [Thread] [] (run [] (println "hi")))              ; subclass a class + interfaces at runtime
(proxy [java.util.TimerTask] [] (run [] ...))

(ns my.app.main (:gen-class))                             ; generates class my.app.main with static main
(defn -main [& args] ...)                                 ; invoked by `java -cp ... my.app.main`
(ns my.Cls
  (:gen-class :name com.example.Cls :methods [[hello [String] String]]))
(defn -hello [this s] (str "hi " s))
```
- `gen-class` only emits a class during AOT compilation (`(compile 'my.app.main)`, `lein uberjar`, tools.build
  `compile-clj`). At the REPL it does nothing useful.
- AOT compiles transitive dependencies too unless restricted, which can ship stale or conflicting class files:
  prefer AOT only for the entry namespace and put `target/classes` first on the classpath.
- `*compile-path*` (default `classes`) must exist and be on the classpath.
- Prefer `reify` for interface implementation and `proxy` only when a superclass must be extended.
- Alternative to gen-class for `-main`: `clojure -M -m my.app.main` (no AOT needed).

## Failure modes
- `ClassNotFoundException: my.app.main` when not compiled or classes dir not on the classpath.
- Stale class files shadow edited source: clean `classes/` before building.

## Self-check
Compile a `:gen-class` namespace and run it with `java -cp classes:<clojure-jars> my.app.main`.
