---
id: computing-software.software-engineering.cpp.cert-cpp-exceptions-and-concurrency-rules
name: cert-cpp-exceptions-and-concurrency-rules
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-cert, cpp-ce-concurrency, cert-cpp-exceptions-concurrency, seicert, err-rules, con-rules, destructors-noexcept]
level: advanced
status: draft
description: "Apply SEI CERT C++ exception (ERR) and concurrency (CON) rules: never throw from destructors, catch by reference, lock discipline, condition variables and thread lifetime."
sources: ["https://wiki.sei.cmu.edu/confluence/display/cplusplus/ERR+Exceptions+and+Error+Handling", "https://wiki.sei.cmu.edu/confluence/display/cplusplus/CON+Concurrency"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CERT C++: exceptions and concurrency

Rule numbers belong to the SEI CERT C++ standard; check the wiki for current wording.

## Exceptions (ERR)
- **ERR50** do not abruptly terminate the program (`abort`, `exit` skipping destructors; `std::terminate` from uncaught exception); **ERR51** handle all exceptions (a top-level `catch` in `main` and in thread entry functions); **ERR52** do not use `setjmp`/`longjmp` (skips destructors); **ERR53** do not reference base-class members in a constructor/destructor catch handler of a function-try-block; **ERR54** catch handlers should order by most derived to base; **ERR55** honour exception specifications; **ERR56** guarantee exception safety; **ERR57** do not leak resources when handling exceptions; **ERR58** handle exceptions during static initialisation; **ERR59** do not throw an exception across execution boundaries (C APIs, threads, DLLs); **ERR60** exception objects must be nothrow copy constructible (`catch` by value copies; throw only exception types with non-throwing copy); **ERR61** catch by lvalue reference; **ERR62** detect errors when converting a string to a number (`std::from_chars`, `stoi` throwing handling).
```cpp
struct Guard { ~Guard() noexcept { try { flush(); } catch (...) { /* log, never rethrow: destructors are noexcept */ } } };   // DCL57
try { run(); } catch (const std::exception& e) { log(e.what()); return 1; } catch (...) { return 2; }   // ERR51 + ERR61
```

## Concurrency (CON)
- **CON50** do not destroy a locked mutex; **CON51** ensure actively held locks are released on exceptional conditions (use RAII locks); **CON52** prevent data races when accessing bit-fields from multiple threads; **CON53** avoid deadlock by locking in a predefined order (`std::scoped_lock`); **CON54** wrap functions that can spuriously wake up in a loop (use the predicate overload of `wait`); **CON55** preserve thread safety and liveness when using condition variables (notify under correct conditions, avoid lost wake-ups); **CON56** do not speculatively lock a non-recursive mutex already owned by the calling thread.
Also mind thread lifetime: a joinable `std::thread` destroyed calls `std::terminate` (use `std::jthread`); catch exceptions inside thread functions.

## Tooling
clang-tidy `cert-err33-c`, `cert-err58-cpp` (static init throwing), `cert-err60-cpp`, `bugprone-exception-escape`; Clang `-Wthread-safety`; ThreadSanitizer; `-Wterminate`.

## Gotchas
- `noexcept` destructors are the default; throwing from one calls `std::terminate`.
- Catching `...` swallows `forced_unwind` on some glibc cancellation paths: rethrow it.
- Rule coverage in tools is partial; add tests that inject exceptions at each step (fault injection).

## Verify
- [ ] Test throws from every allocation/callback point and asserts invariants and no leaks under ASan.
- [ ] TSan stress test with concurrent producers/consumers passes.
