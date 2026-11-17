---
id: computing-software.software-engineering.clojure.profiling-criterium-clj-async-profiler
name: profiling-criterium-clj-async-profiler
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, profiling, benchmark, criterium, clj-async-profiler, visualvm, jfr, flamegraph, time, quick-bench, profiling-benchmarks]
level: advanced
status: docs-checked
description: "Measure Clojure performance with criterium quick-bench/bench and CPU flamegraphs with clj-async-profiler; avoid timing mistakes."
sources: ["https://github.com/hugoduncan/criterium", "https://github.com/clojure-goes-fast/clj-async-profiler"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiling and benchmarking

**Goal:** find real hot spots and compare implementations fairly.

```clojure
(require '[criterium.core :refer [quick-bench bench]])
(quick-bench (my-fn data))             ; quicker, less thorough
(bench (my-fn data))                   ; mean, std-deviation, lower and upper quantile

(require '[clj-async-profiler.core :as prof])
(prof/profile (dotimes [i 10000] (reduce + (range i))))   ; writes a flamegraph HTML
(prof/serve-ui 8080)                                      ; local web UI for the results
```
- Criterium (stable 0.4.6; master is 0.5.x alpha with possible breaking changes) does statistical processing of
  many evaluations, a JIT warm-up period, a gc purge before testing and a forced gc after. `bench` is quiet; wrap in
  `with-progress-reporting` to see progress. It returns results so the JIT cannot treat them as unused.
- Criterium estimates its own measurement overhead once per session; benchmarking very quick functions while the
  machine is busy can report small negative times (`criterium.core/estimated-overhead!` forces a re-estimate).
- It does not aim for ultimate accuracy on very quick expressions: the expression is evaluated inside a function call.
- clj-async-profiler needs Linux or macOS, a JDK (not a JRE) 1.8+ and Clojure 1.10+; it wraps async-profiler.
- On JDK 11 and later start the JVM with `-Djdk.attach.allowAttachSelf` (a `:jvm-opts` entry in a deps.edn alias, or
  `-J-Djdk.attach.allowAttachSelf` on the command line), otherwise you get "Can not attach to current VM".
- On Linux set `kernel.perf_event_paranoid=1` and `kernel.kptr_restrict=0` with `sysctl` for kernel profiling data.
- Flamegraphs are self-contained HTML files saved under `/tmp/clj-async-profiler/results/` by default; change the
  directory with the `clj-async-profiler.output-dir` Java property. Options maps accept `:pid` to sample another
  JVM.
- For more accurate profiles the README recommends `-XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints`.
- Benchmark rules: fix input data, force lazy results (`doall`, `count`), return values so the JIT cannot eliminate
  the work, run with the same JVM flags as production.

## Failure modes
- Benchmarking a single cold call: no warm-up, so JIT effects dominate.
- Optimising code that profiles show is not hot.

## Self-check
Compare `(reduce + (range 1000000))` with a naive lazy version using `quick-bench`; report mean times.

## Checked
2026-11-08. Partial read of both READMEs (the usage, requirements, tuning, output directory and troubleshooting sections of clj-async-profiler; the stable-version, usage and measurement-overhead sections of criterium). Confirmed: everything listed above. Removed: `time` commentary, JDK Flight Recorder command, VisualVM/YourKit and `jcmd` heap dump advice, `clj-memory-meter`, the `-XX:+UseSerialGC` claim, and the reflection/boxed-math checklist, none of which the READMEs state.
Method: documentation only; no commands were run.
