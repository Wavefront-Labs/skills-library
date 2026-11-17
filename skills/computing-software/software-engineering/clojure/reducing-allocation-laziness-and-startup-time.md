---
id: computing-software.software-engineering.clojure.reducing-allocation-laziness-and-startup-time
name: reducing-allocation-laziness-and-startup-time
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, performance, startup-time, direct-linking, laziness, transducers, allocation, gc, aot, cds, performance-laziness-startup]
level: advanced
status: draft
description: "Cut allocation and startup cost: transducers instead of lazy chains, into/reduce, direct linking, AOT, AppCDS, avoiding eager requires, and GC choices."
sources: ["https://clojure.org/reference/compilation", "https://clojure.org/reference/transducers"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Laziness, allocation and startup time

**Goal:** faster pipelines and quicker process start.

- Replace chains like `(->> xs (map f) (filter g) (take n))` that allocate intermediate seqs with a transducer:
  `(into [] (comp (map f) (filter g) (take n)) xs)`.
- `reduce` and `reduce-kv` on maps are faster than seq-based iteration; `mapv`/`filterv` return vectors eagerly.
- Direct linking: `-Dclojure.compiler.direct-linking=true` when compiling (AOT) removes var indirection for
  Clojure and your own fns, at the cost of REPL redefinition of already-linked callers. Use for production only.
- Startup: Clojure loads and compiles namespaces at start; AOT compilation, fewer namespaces, and lazy `requiring-resolve`
  for rarely used code reduce it. Typical `clojure.core` load is ~0.5-1s on the JVM (varies).
- JVM flags: `-XX:+UseSerialGC` for small containers, `-XX:TieredStopAtLevel=1` for short-lived tools,
  `-Xshare:auto` / AppCDS archives to speed class loading (JDK version dependent).
- GC choice: G1 (default), ZGC/Shenandoah for low-latency heaps; benchmark with your workload.
- Allocation hotspots: `apply str`, repeated `concat`, `assoc` in tight loops (use transients), boxing, `format`.
- Do not `memoize` unbounded caches; use bounded caches (core.cache or caffeine via interop).
- For CLIs prefer Babashka or GraalVM native images over JVM Clojure scripts.

## Failure modes
- Direct linking breaks `with-redefs` in tests.
- Over-eager parallelism with `pmap` for tiny tasks.

## Self-check
Run `time java -jar app.jar --help` before/after AOT and direct linking; record both.
