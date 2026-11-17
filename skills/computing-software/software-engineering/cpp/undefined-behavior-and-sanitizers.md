---
id: computing-software.software-engineering.cpp.undefined-behavior-and-sanitizers
name: undefined-behavior-and-sanitizers
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, undefined-behavior, ubsan, asan, valgrind, strict-aliasing, use-after-free, buffer-overflow, signed-overflow, sanitizers, memory-safety, data-race]
level: advanced
status: docs-checked
description: "Catch C++ undefined behavior before it ships: AddressSanitizer, UBSan, strict aliasing violations, signed overflow, and why -O2 can change behavior."
sources: ["https://clang.llvm.org/docs/AddressSanitizer.html", "https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html", "https://clang.llvm.org/docs/ThreadSanitizer.html", "https://clang.llvm.org/docs/MemorySanitizer.html", "https://github.com/cplusplus/draft"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C++ undefined behavior and sanitizers — catch it before the compiler exploits it

**Goal:** find UB (use-after-free, out-of-bounds access, signed overflow, strict
aliasing violations) with instrumented builds, because UB is not "probably fine" —
the compiler is licensed to assume it never happens and optimize accordingly.

## 1. Run the sanitizers in CI, not just when something looks wrong
```
clang++ -fsanitize=address,undefined -g -O1 file.cpp
```
- **AddressSanitizer (ASan)**: catches heap/stack buffer overflows, use-after-free,
  use-after-return, double-free. Typical slowdown is 2x, acceptable for test/CI builds; Clang's
  docs say the runtime is for testing, not production.
- **UndefinedBehaviorSanitizer (UBSan)**: catches signed integer overflow, null
  pointer use, misaligned access, invalid shifts, out-of-bounds indexing of arrays with a
  known bound (`-fsanitize=bounds`), and more. It does **not** detect strict-aliasing violations.
- **ThreadSanitizer (TSan)**: data races (typical slowdown 5x-15x; run it as a separate build).
- **MemorySanitizer (MSan)**: use of uninitialized memory — needs all program code
  (including libraries) instrumented to avoid false reports; use selectively.
Running these only when a bug is already suspected misses the much larger set of UB
that hasn't crashed yet but is silently corrupting state or will break on the next
compiler upgrade.

## 2. Why "it works" under -O0 and breaks under -O2
The compiler assumes UB never happens and optimizes on that assumption. Classic
example: a null check *after* a dereference of the same pointer gets deleted by the
optimizer, because if the dereference didn't crash, the pointer "must" be non-null
by the language's rules — even though in practice the dereference just happened not
to fault (reading from unmapped memory doesn't always trap immediately). This is why
"it ran fine in debug" is not evidence of correctness — UB's whole danger is that
undefined does not mean "will visibly fail."

## 3. Signed integer overflow is UB, unlike unsigned
```cpp
int x = INT_MAX;
x + 1;              // UB — not guaranteed to wrap, may be optimized away entirely
unsigned u = UINT_MAX;
u + 1;               // well-defined: wraps to 0
```
A loop condition like `for (int i = 0; i < n && arr[i+1] != 0; i++)` where `i+1`
could overflow is a candidate for the compiler to assume the condition is always
true (since overflow "can't happen") and remove bounds entirely. UBSan's
`-fsanitize=signed-integer-overflow` catches signed overflow directly; prefer unsigned types for
values that are genuinely never negative, or check bounds before the arithmetic.

## 4. Strict aliasing violations
```cpp
float f = 1.0f;
int i = *reinterpret_cast<int*>(&f);   // UB: accessing a float's bytes as an int
                                        // through an incompatible pointer type
```
The language rules let the compiler assume objects of unrelated types do not overlap, so
violating them (common in manual type-punning) can make the optimizer reorder or
eliminate accesses. UBSan does not report this. Use `std::bit_cast` (C++20) or `memcpy`
into an object of the other type instead of a `reinterpret_cast` punning trick.

## 5. Use-after-free and use-after-return
A dangling reference/pointer to a destroyed stack frame or freed heap object is UB
whether or not the memory has been reused yet — ASan's use-after-return (enabled at
runtime by default on Linux) and use-after-free checks report the access with a precise
stack trace, rather than silently reading
garbage-that-happens-to-look-valid, which is what makes these bugs so hard to
reproduce without the sanitizer.

## Gotchas
- For most checks UBSan prints a report and continues; `-fno-sanitize-recover=...` makes it print and
  exit instead, so add `-fno-sanitize-recover=all` in CI to stop at the first UB found.
- A release build that disables assertions (`NDEBUG`) and sanitizers entirely means
  production has zero safety net for a bug that only manifests under production's
  specific inputs — consider shipping a canary/staging build with sanitizers enabled
  under real traffic for critical services, accepting the performance cost there.

## Verify
- [ ] CI runs at least one ASan+UBSan build of the test suite, with
      `-fno-sanitize-recover=all`, not only the plain build.
- [ ] Any manual type-punning uses `std::bit_cast`/`memcpy`, not `reinterpret_cast`
      between unrelated pointer types.
- [ ] Integer types used in bounds/index arithmetic are unsigned where negative is
      never meaningful, or explicitly checked for overflow before use.
- [ ] A bug that "disappeared" after an optimization-level or compiler-version change
      was investigated for UB before being declared fixed.

Related: computing-software.software-engineering.cpp.raii-and-smart-pointers,
computing-software.software-engineering.debugging.native-debugging-with-gdb-lldb

## Checked

Date: 2026-10-25. Documentation: Clang AddressSanitizer, UndefinedBehaviorSanitizer, MemorySanitizer and ThreadSanitizer pages (llvm/llvm-project clang/docs, head 2026-10-25) and the C++ working draft (cplusplus/draft, head 2026-10-24).

Confirmed: ASan typical slowdown 2x, use-after-return default `runtime`; UBSan checks signed-integer-overflow, null, alignment, shift and bounds, and its default recover behaviour with `-fno-sanitize-recover`; the UBSan page lists no strict-aliasing check; TSan typical slowdown 5x-15x; MSan needs all code instrumented; the draft states that an expression result not in the range of representable values has undefined behaviour.
Removed as unconfirmed: the claim that UBSan detects strict-aliasing violations (it does not), the ASan/TSan combination rule, the claim that bit_cast and memcpy are "exempted" from the aliasing rule (reworded), and Valgrind speed comparisons. The remaining optimiser examples are illustrative language-level reasoning, not tool claims.

Method: documentation only; no commands were run.
