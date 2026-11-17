---
id: computing-software.software-engineering.c.thread-local-storage-and-once-init
name: thread-local-storage-and-once-init
category: computing-software
field: software-engineering
product: c
tags: [c, thread-local, pthread-once, tss, pthread-key, call-once]
level: advanced
status: docs-checked
description: "Use _Thread_local and pthread_once for per-thread state and one-time initialisation."
sources: ["https://en.cppreference.com/w/c/language/storage_duration", "https://en.cppreference.com/w/c/thread/call_once", "https://man7.org/linux/man-pages/man3/pthread_key_create.3.html", "https://man7.org/linux/man-pages/man3/pthread_once.3p.html", "https://gcc.gnu.org/onlinedocs/gcc/Thread-Local.html", "https://man7.org/linux/man-pages/man3/errno.3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread local storage and once init

Goal: thread-safe globals without ad hoc locking.

- C11 `_Thread_local` (`thread_local` from `<threads.h>`; keyword in C23) gives each thread its own copy: `static _Thread_local int depth;`. GCC/Clang also accept `__thread`.
- Pre-C11 POSIX alternative: `pthread_key_create(&key, destructor)`, `pthread_setspecific`, `pthread_getspecific`; the destructor runs at thread exit for non-NULL values.
- One-time init: `static pthread_once_t once = PTHREAD_ONCE_INIT; pthread_once(&once, init_fn);` or C11 `call_once(&flag, fn)` with `ONCE_FLAG_INIT` (needs `<threads.h>`, which implementations may omit: `__STDC_NO_THREADS__`).
- `errno` is thread-local already.
- Per-thread caches and buffers avoid contention; free thread-owned memory at thread exit (key destructor) to prevent leaks.
- Do not return pointers to thread-local data to other threads.

Verify: spawn threads that each write a distinct value and confirm each reads back its own.

## Checked

- Date: 2026-11-02
- Confirmed: cppreference (`_Thread_local` until C23, `thread_local` since C23; call_once/ONCE_FLAG_INIT; `__STDC_NO_THREADS__` on the C11 page); GCC manual (`__thread` storage class keyword); man7 pthread_key_create (destructor called at thread exit for non-NULL values), pthread_once (`PTHREAD_ONCE_INIT`), errno(3) (errno is thread-local). Removed: the constant-initialiser requirement and the glibc 2.28 version claim.
Method: documentation only; no commands were run.
