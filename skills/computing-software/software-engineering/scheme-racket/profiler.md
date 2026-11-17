---
id: computing-software.software-engineering.scheme-racket.profiler
name: profiler
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, profiler, racket-performance]
level: practitioner
status: docs-checked
description: "Find hot spots using (require profile) and profile-thunk, or raco profile, and interpret sampler output."
sources:
  - https://docs.racket-lang.org/profile/index.html
  - https://docs.racket-lang.org/guide/performance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiling with the profile library
**Goal:** measure before optimising.
```racket
(require profile)
(profile-thunk (lambda () (run-workload)) #:delay 0.001)
```
- The profiler is statistical: a background sampler thread takes stack snapshots every `#:delay` seconds (default 0.05), so longer runs are more accurate; `#:repeat n` repeats the thunk to gather more data.
- By default only the current thread is sampled; pass `#:threads? #t` to track threads the computation creates, otherwise their work is missing from the results.
- `raco profile file.rkt` runs the profiler on the file's `main` submodule if it exists, otherwise on the module itself.
- `#:use-errortrace? #t` gives expression-level detail but needs uncompiled sources (remove `.zo` files) and running with `racket -l errortrace -t program.rkt`.
- `#:order` is `'topological` (default), `'self` (time on top of the stack) or `'total` (time anywhere on the stack).
- Profile in plain `racket`: DrRacket's debugging instrumentation can distort timings.
## Self-check
Profile a naive fib 32 and find the function dominating.

## Checked
2026-11-08. Confirmed on the Racket profile library documentation (Toplevel Interface and Collecting Profile Information: `profile-thunk` keywords and defaults, sampler thread, `raco profile`, Errortrace requirements, `#:order` values) and the Guide Performance chapter section 19.1 (DrRacket instrumentation). Removed the `time` form bullet, which this page set does not describe.
Method: documentation only; no commands were run.
