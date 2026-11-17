---
id: computing-software.software-engineering.cpp.cert-cpp-memory-and-container-string-rules
name: cert-cpp-memory-and-container-string-rules
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-cert, cpp-ce-memory, cpp-ce-strings, cert-cpp-memory, cert-cpp-containers-strings, seicert, memory-safety, buffer-overflow]
level: advanced
status: draft
description: "Apply SEI CERT C++ rules for memory (MEM) and containers/strings (CTR, STR): pairing new/delete, bounds, iterator validity, null-terminated strings, with tool support."
sources: ["https://wiki.sei.cmu.edu/confluence/display/cplusplus/2+Rules", "https://wiki.sei.cmu.edu/confluence/display/cplusplus/CTR+Containers", "https://wiki.sei.cmu.edu/confluence/display/cplusplus/STR+Characters+and+Strings"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CERT C++: memory, containers and strings

Rule IDs are from the SEI CERT C++ Coding Standard; check the wiki for the current text since entries are revised.

## Memory (MEM)
- **MEM50-CPP** do not access freed memory; **MEM51** properly deallocate dynamically allocated resources (match `new`/`delete`, `new[]`/`delete[]`, `malloc`/`free`); **MEM52** detect and handle allocation failures (`new` throws `bad_alloc`, `new (std::nothrow)` returns null); **MEM53** explicitly construct and destruct objects when manually managing lifetime; **MEM54** provide placement new with properly aligned storage; **MEM55** honour replacement allocation function requirements; **MEM56** do not store an already-owned pointer in another smart pointer (two `unique_ptr`s on one object); **MEM57** avoid `new` for over-aligned types before C++17.
```cpp
auto p = std::make_unique<T[]>(n);          // owns an array, deletes with delete[]
std::shared_ptr<T> a(raw); std::shared_ptr<T> b(raw);    // MEM56 violation: double delete
```
Fix by RAII everywhere: `unique_ptr`, containers, `make_shared`.

## Containers (CTR)
- **CTR50** guarantee that container indices and iterators are within the valid range; **CTR51** use valid references, pointers and iterators (invalidation by `push_back`, `erase`); **CTR52** guarantee that library functions do not overflow (`std::copy` into a too-small destination); **CTR53** use valid iterator ranges (both from the same container, begin before end); **CTR54** do not subtract iterators that do not refer to the same container; **CTR55** do not use an additive operator on an iterator if the result overflows; **CTR56** pointer arithmetic on polymorphic arrays; **CTR57** provide a valid ordering predicate (strict weak ordering); **CTR58** predicate function objects should not be mutable.

## Strings (STR)
- **STR50** guarantee storage for strings including the terminator; **STR51** do not attempt to create a `std::string` from a null pointer; **STR52** use valid references/iterators for `basic_string`; **STR53** range check element access.

```cpp
std::string s(maybe_null ? maybe_null : "");   // STR51
for (std::size_t i = 0; i < v.size(); ++i) use(v.at(i));  // CTR50 with bounds-checked access in non-hot code
```

## Tool support and enforcement
- clang-tidy `cert-*` checks, `bugprone-use-after-move`, `clang-analyzer-cplusplus.*`; Cppcheck premium CERT add-on; compile with `-D_GLIBCXX_ASSERTIONS` or `_LIBCPP_HARDENING_MODE_FAST` for runtime bounds checks; AddressSanitizer for MEM50/CTR50-51.

## Gotchas
- Mapping to Core Guidelines is partial; follow one primary standard and record deviations.
- Not every CERT rule has a diagnostic; code review checklists still matter.

## Verify
- [ ] Seeded violations (double delete, out-of-range index) are caught by ASan or the hardened library.
- [ ] clang-tidy cert checks run in CI with warnings as errors.
