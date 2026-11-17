---
id: computing-software.software-engineering.perl.threads-ithreads
name: threads-ithreads
category: computing-software
field: software-engineering
product: perl
tags: [perl, ithreads, threads-shared, thread-queue, perlthrtut, useithreads, threads-ithreads, perl-concurrency]
level: advanced
status: docs-checked
description: "Use Perl threads when perl is built with ithreads: join or detach every thread, relay signals, and avoid non-thread-safe modules."
sources: ["https://perldoc.perl.org/threads"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interpreter threads

**Goal:** know when and how to use ithreads.

```bash
perl -V:useithreads        # useithreads='define' means threads are available
```
```perl
use threads;
my @workers = map { threads->create(sub { return 42 }) } 1..4;
print $_->join, "\n" for @workers;
```

## Rules
- Join or detach every thread. If the program exits without all threads joined or detached, a warning is issued ("Perl exited with active threads").
- `->detach` makes the thread unjoinable and discards its return value; detached threads still running when the program exits are silently terminated. In that case Perl's global destruction phase is not executed, so if you need it for clean-up (for example removing temp files), join all threads instead of detaching.
- Calling `->join()` or `->detach()` on an already joined or detached thread throws an error.
- Some Perl modules are not thread-safe: they may crash the interpreter during execution or dump core on termination. Check a module before using it in threads.
- To handle alarms (SIGALRM) in threads, set up the signal handler in the main thread and relay the signal to the thread with the thread signalling method (`->kill`). With unsafe signals in effect, signal handling is not thread-safe and `->kill()` cannot be used.
- Tuning the thread stack size can significantly reduce memory use and raise the number of simultaneously running threads.
- Before Perl 5.28, locales could not be used with threads; from 5.28 they can, with caveats, on systems with thread-safe locale functions.

## Self-check
- [ ] `perl -Mthreads -e 'print threads->create(sub{42})->join'` prints `42` on a perl built with ithreads.

## Checked
Read the threads page only. Removed, because it is not stated there or the page was not read: threads::shared and Thread::Queue guidance (including the example using them), data-copy and creation-cost claims, `CLONE_SKIP`, DBI handles, OS-packager and Strawberry Perl claims, the "signals go to the main thread only" claim, and the fork/event-loop recommendation. The Thread::Queue and perlthrtut sources were dropped from the source list.
Method: docs-only read of cited pages, 2026-11-08
