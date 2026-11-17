---
id: computing-software.software-engineering.cpp.operator-new-replacement-and-leak-detection
name: operator-new-replacement-and-leak-detection
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-allocation, cpp-al-newdelete, cpp-al-leaks, operator-new, leak-detection, leaksanitizer, valgrind]
level: practitioner
status: docs-checked
description: "Replace global operator new/delete for counting or arenas, and find C++ leaks with LeakSanitizer and Valgrind memcheck, reading the leak categories."
sources: ["https://en.cppreference.com/w/cpp/memory/new/operator_new", "https://github.com/google/sanitizers/wiki/AddressSanitizerLeakSanitizer", "https://valgrind.org/docs/manual/mc-manual.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replacing operator new and finding leaks

## Replace global allocation (instrumentation, tests)
The global `operator new`/`delete` overloads (plain, array, `std::align_val_t` and `std::nothrow_t` forms) are replaceable. The default `operator new(count)` allocates (whether via `std::malloc` or `std::aligned_alloc` is unspecified); on failure it calls the installed new-handler, or throws `std::bad_alloc` if there is none. The non-allocating placement forms cannot be replaced.

The reference's replacement example (trimmed):
```cpp
#include <cstdlib>
#include <new>
// no inline, required by [replacement.functions]/3
void* operator new(std::size_t sz)
{
    if (sz == 0)
        ++sz;                       // avoid std::malloc(0) which may return nullptr on success
    if (void* ptr = std::malloc(sz))
        return ptr;
    throw std::bad_alloc{};         // required by [new.delete.single]/3
}
void operator delete(void* ptr) noexcept { std::free(ptr); }
void operator delete(void* ptr, std::size_t) noexcept { std::free(ptr); }
// also replace operator new[] / delete[] (and sized forms)
```
- Do not mark the replacements `inline`.
- Replace the array forms too; `new int[10]` is guaranteed to call the replacement in C++11 and later.
- Add a counter to the replacement to assert "no allocations in this section" in tests.
- Per-class allocation: a class can declare its own `T::operator new`; a class-specific placement `new` with matching signature is the only way to customise placement `new` when `::new` is not used.

## Find leaks
LeakSanitizer (LSan) is integrated into AddressSanitizer, supported on x86_64 Linux and OS X, and enabled by default in ASan builds on x86_64 Linux. It stays dormant until the end of the process, then runs a leak detection phase.
```
clang++ -g -fsanitize=address main.cpp && ./a.out
ASAN_OPTIONS=detect_leaks=1 ./a.out         # needed to enable on OS X
ASAN_OPTIONS=detect_leaks=0 ./a.out         # run ASan without leak detection
clang++ -fsanitize=leak main.cpp            # leak detection only, no ASan instrumentation slowdown
valgrind --leak-check=full --show-leak-kinds=definite,possible ./a.out
```
- Tune LSan with `LSAN_OPTIONS`. If built with `-fsanitize=leak`, put stack-trace flags such as `fast_unwind_on_malloc`, `malloc_context_size` and `strip_path_prefix` in `LSAN_OPTIONS` instead of `ASAN_OPTIONS`.
- Suppress known leaks with a file of `leak:<pattern>` lines (one per line, substring-matched against the symbolised stack trace: function, source file or binary name) and `LSAN_OPTIONS=suppressions=suppr.txt`. Defaults can be compiled in via `__lsan_default_options` and `__lsan_default_suppressions`.
- Memcheck summary categories: definitely lost, indirectly lost (reachable only through a lost block), possibly lost, still reachable. With `--leak-check=full` it details each definitely or possibly lost block. `--show-leak-kinds=all` also shows reachable and indirectly lost blocks. Fixing a definitely lost block also fixes its indirectly lost children.
- Memcheck also reports mismatched use of allocation and deallocation functions, and uninitialised-value origins with `--track-origins=yes`.

## Verify
- A deliberately leaking test (`new int;`) is detected, confirming the tool is wired.
- The CI test binary runs under ASan with LSan and exits 0.

## Checked
Read the cppreference operator new page, the LeakSanitizer wiki page and the Valgrind Memcheck manual (leak sections). Removed as unconfirmed: the thread-safe atomic counter code, heaptrack usage, MSVC/Windows and macOS alternatives, the ptrace container failure and fix, and the singleton intentional-leak remark.
Method: docs-checked 2026-11-09 against the cppreference operator new page, the LeakSanitizer wiki and the Valgrind Memcheck manual.
