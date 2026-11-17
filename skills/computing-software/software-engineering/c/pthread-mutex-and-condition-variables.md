---
id: computing-software.software-engineering.c.pthread-mutex-and-condition-variables
name: pthread-mutex-and-condition-variables
category: computing-software
field: software-engineering
product: c
tags: [c, c-threads-atomics, pthread-mutex, condition-variable, pthread-create, deadlock, spurious-wakeup]
level: practitioner
status: docs-checked
description: "Use pthread mutexes and condition variables correctly: predicate loops, lock ordering, join or detach."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://pubs.opengroup.org/onlinepubs/9799919799/", "https://man7.org/linux/man-pages/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pthread mutex and condition variables

Goal: correct blocking synchronisation between threads.

- Create/join: `pthread_create(&t, NULL, fn, arg)`; `pthread_join(t, &ret)` (or detach, never both). Pass heap or long-lived data as `arg`, not a pointer to a loop variable. Link with `-pthread` (compile and link).
- `pthread_mutex_lock/unlock` around every access to shared state; initialise with `PTHREAD_MUTEX_INITIALIZER` or `pthread_mutex_init`. Check return codes in debug builds; `PTHREAD_MUTEX_ERRORCHECK` helps find misuse.
- Condition variables: always wait in a loop on a predicate: `while (!ready) pthread_cond_wait(&cv, &m);` (spurious wakeups). Change the predicate while holding the mutex, then `pthread_cond_signal`/`broadcast`.
- Prevent deadlock with a global lock order and avoid calling unknown callbacks while holding a lock.
- Timed waits use `pthread_cond_timedwait` with an absolute `CLOCK_REALTIME` time (or set the cond clock to `CLOCK_MONOTONIC` via an attribute).
- `fork` in a multithreaded process only copies the calling thread.

Verify: build with `-fsanitize=thread` and run a stress loop; also `helgrind` via Valgrind.

## Checked

2026-11-02. Confirmed in pthread_create(3), pthread_join(3), pthread_cond_timedwait (POSIX and man pages), pthread_mutexattr_settype(3p), fork(2), GCC Link Options (`-pthread`), Clang ThreadSanitizer, Valgrind Helgrind: spurious wakeups, default `CLOCK_REALTIME` for timed waits, `PTHREAD_MUTEX_ERRORCHECK`, child has a single thread after `fork`. Removed: the TSan/ASan combination remark.

Method: documentation only; no commands were run.
