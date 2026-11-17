---
id: computing-software.software-engineering.prolog.mutex-thread-local
name: mutex-thread-local
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, mutex-thread-local, with-mutex]
level: sme
status: docs-checked
description: "Protect shared state with with_mutex/2 and keep per-thread data with thread_local in SWI-Prolog."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/man/threads.plx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mutexes and thread-local data
```prolog
:- dynamic counter/1.
bump :- with_mutex(m, (retract(counter(N)), N1 is N+1, assertz(counter(N1)))).
:- thread_local seen/1.
```
- `with_mutex(+Mutex, :Goal)` locks Mutex, runs Goal as `once/1` and unlocks on success, failure or exception. A new mutex is created if the name does not exist.
- Prolog mutexes are recursive: the owner thread may lock again; it must unlock as often as it locked.
- `mutex_create(-Id)` creates an anonymous mutex; `mutex_create(+Id)` with an atom creates a named one. `mutex_statistics/0` prints acquisition and collision counts.
- `thread_local Name/Arity` gives each thread its own clause list. A new thread starts with no clauses and its clauses are reclaimed when it ends. A thread-local predicate is dynamic and volatile.
- Clauses of a thread-local predicate in a source file are visible only to the thread that loaded the file.
## Gotchas
- `with_mutex/2` hides choice points in Goal.
- Thread-local facts do not propagate to threads created later; pass data as arguments or messages.
## Self-check
Run N threads that call `bump`; the final `counter/1` must equal N plus the start value.

## Checked

2026-11-03. SWI-Prolog manual threads chapter (threads.plx): with_mutex/2, recursive mutexes, mutex_create/1, mutex_statistics/0, and the thread_local/1 description (per-thread clauses, empty start, reclaim at exit, dynamic and volatile, file clauses seen only by the loading thread). Removed: lock-ordering advice and unlocked-read claims (not covered).

Method: documentation only; no commands were run.
